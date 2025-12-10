from typing import Set, List, Tuple

import numpy as np

from .EngineConfiguration import EngineConfiguration
from ..Characters.Character import Character
from ..Characters.Emotions import Emotions
from ..Interactions.Interaction import Interaction
from ..Relationships.Relationship import Relationship
from ..Relationships.TypeRelationship import TypeRelationship
from ..Universe.Graph import Graph


class InteractionsEngine:
    """Gère les updates des émotions et relations basées sur les interactions."""

    def __init__(self, graph: Graph):
        """
        Args:
            graph: Le graph contenant les characters et leurs relations
        """
        self.graph = graph
        self.config = EngineConfiguration()
        # Liste des propagations en attente : (tick_arrivée, cible, interaction)
        self.pending_propagations: List[Tuple[int, Character, Interaction]] = []

    def tick(self, current_tick: int):
        """
        Update la diffusion des infos à chaque tick.
        Traite les infos dont le temps de trajet est écoulé.
        """
        # Filtrer les événements arrivés (tick_arrivée <= current_tick)
        remaining_propagations = []

        for arrival_tick, target, interaction in self.pending_propagations:
            if arrival_tick <= current_tick:
                # L'info arrive au character cible
                # Éviter les doublons
                if interaction not in target.knownInteractions:
                    target.learnAboutInteraction(interaction)
                    # Le character réagit à cette nouvelle info
                    self.processInteractionForCharacter(target, interaction)

                    # Optionnel : bouche-à-oreille
                    # self.diffuseInteraction(target, interaction, current_tick)
            else:
                # L'info est toujours en transit
                remaining_propagations.append((arrival_tick, target, interaction))

        self.pending_propagations = remaining_propagations

    def diffuseInteraction(self, source: Character, interaction: Interaction, current_tick: int,
                           already_informed: Set[Character] = None):
        """
        Un Character diffuse une info sur une Interaction à ses voisins.
        La diffusion prend du temps selon la distance informationnelle.
        """
        # Le propagateur apprend l'info immédiatement
        if interaction not in source.knownInteractions:
            source.learnAboutInteraction(interaction)

        neighbors = self.graph.getNeighbors(source)

        for neighbor in neighbors:
            # Récupérer la relation pour connaître la distance
            relationship = self.graph.getEdge(source.name, neighbor.name)

            if relationship is not None:
                # Calcul du moment d'arrivée de l'info
                distance = relationship.informational_distance
                arrival_tick = current_tick + distance

                # Planifier l'arrivée de l'info
                self.pending_propagations.append((arrival_tick, neighbor, interaction))

    def processInteractionForCharacter(self, character: Character, interaction: Interaction):
        """
        Un Character traite une Interaction.
        - Si impliqué directement : changements directs
        - Si relation avec participant : changements indirects
        """
        # Vérifier si le personnage est directement impliqué
        is_actor = (character == interaction.actor)
        is_target = (character == interaction.target)
        is_directly_involved = is_actor or is_target

        if is_directly_involved:
            self._process_direct_interaction(character, interaction, is_actor)
        else:
            self._process_indirect_interaction(
                character,
                interaction,
                self._has_relationship(character, interaction.actor),
                self._has_relationship(character, interaction.target)
            )

    def _process_direct_interaction(self, character: Character, interaction: Interaction, is_actor: bool):
        """
        Traite une interaction directe (character impliqué).
        Update émotions et relation avec l'autre participant + relations indirectes.
        """
        # Déterminer l'autre character
        other_character = interaction.target if is_actor else interaction.actor

        # Vecteurs pour les calculs matriciels
        interaction_vector = interaction.asArray()
        personality_vector = character.personality.asArray()
        current_emotions = character.emotions.asArray()

        # Inverser la valence si c'est l'acteur
        if is_actor:
            interaction_vector = interaction_vector.copy()
            interaction_vector[4] *= self.config.actor_valence_attenuation

        # === 1. Update des émotions ===
        new_emotions_array = self._apply_emotion_change_direct(
            current_emotions, interaction_vector, personality_vector
        )
        self._update_character_emotions(character, new_emotions_array)

        # === 2. Update de la relation directe ===
        relationship = self.graph.getEdge(character.name, other_character.name)

        # Créer relation neutre si n'existe pas
        if relationship is None:
            new_type = TypeRelationship(0.0, 0.0, 0.0)
            self.graph.addEdge(character.name, other_character.name, new_type)
            relationship = self.graph.getEdge(character.name, other_character.name)

        self._update_relationship_direct(character, other_character, relationship, interaction_vector)

        # === 3. Propagation : Update des relations associées ===
        neighbors = self.graph.getNeighbors(other_character)
        for neighbor in neighbors:
            if neighbor.name == character.name:
                continue

            rel_with_neighbor = self.graph.getEdge(character.name, neighbor.name)

            if rel_with_neighbor is not None:
                self._update_relationship_indirect(character, rel_with_neighbor, interaction_vector)

    def _process_indirect_interaction(self, character: Character, interaction: Interaction,
                                      has_relation_with_actor: bool, has_relation_with_target: bool):
        """
        Traite une interaction indirecte (character connaît un participant).
        Changements atténués.
        """
        if not (has_relation_with_actor or has_relation_with_target):
            return

        # Vecteurs pour les calculs
        interaction_vector = interaction.asArray()
        personality_vector = character.personality.asArray()
        current_emotions = character.emotions.asArray()

        # Update des émotions (impact indirect)
        new_emotions_array = self._apply_emotion_change_indirect(
            current_emotions, interaction_vector, personality_vector
        )
        self._update_character_emotions(character, new_emotions_array)

        # Update des relations avec les participants connus
        if has_relation_with_actor:
            relationship = self.graph.getEdge(character.name, interaction.actor.name)
            if relationship is not None:
                self._update_relationship_indirect(character, relationship, interaction_vector)

        if has_relation_with_target:
            relationship = self.graph.getEdge(character.name, interaction.target.name)
            if relationship is not None:
                self._update_relationship_indirect(character, relationship, interaction_vector)

    def _update_character_emotions(self, character: Character, new_emotions_array: np.ndarray):
        """Update les émotions d'un character depuis un vecteur numpy."""
        new_emotions = Emotions(
            happiness=float(new_emotions_array[0]),
            sadness=float(new_emotions_array[1]),
            anger=float(new_emotions_array[2]),
            fear=float(new_emotions_array[3]),
            surprise=float(new_emotions_array[4]),
            disgust=float(new_emotions_array[5])
        )
        character.changeEmotions(new_emotions)

    def _update_relationship_direct(self, source: Character, target: Character,
                                    relationship: Relationship, interaction_vector: np.ndarray):
        """Update une relation de manière directe."""
        current_relationship_array = relationship.asArray()
        personality_source = source.personality.asArray()
        personality_target = target.personality.asArray()

        new_relationship_array = self._apply_relationship_change_direct(
            current_relationship_array, interaction_vector,
            personality_source, personality_target
        )

        relationship.typeRelationship.privacy = float(new_relationship_array[0])
        relationship.typeRelationship.commitment = float(new_relationship_array[1])
        relationship.typeRelationship.passion = float(new_relationship_array[2])
        relationship.typeRelationship.nom = relationship.typeRelationship.identifyName()

    def _update_relationship_indirect(self, observer: Character, relationship: Relationship,
                                      interaction_vector: np.ndarray):
        """Update une relation de manière indirecte."""
        current_relationship_array = relationship.asArray()
        personality_observer = observer.personality.asArray()

        new_relationship_array = self._apply_relationship_change_indirect(
            current_relationship_array, interaction_vector, personality_observer
        )

        relationship.typeRelationship.privacy = float(new_relationship_array[0])
        relationship.typeRelationship.commitment = float(new_relationship_array[1])
        relationship.typeRelationship.passion = float(new_relationship_array[2])
        relationship.typeRelationship.nom = relationship.typeRelationship.identifyName()

    def _has_relationship(self, character1: Character, character2: Character) -> bool:
        """Vérifie si deux characters ont une relation."""
        return self.graph.getEdge(character1.name, character2.name) is not None

    def processInteractionForGroup(self, group: list[Character], interaction: Interaction):
        """Traite une interaction par tout un ensemble de characters."""
        for character in group:
            self.processInteractionForCharacter(character, interaction)

    def processInteractionForAll(self, interaction: Interaction):
        """Traite une interaction pour tous les characters du graph."""
        self.processInteractionForGroup(self.graph.listNode, interaction)

    # === Calculs matriciels pour l'update des vecteurs ===

    def _apply_emotion_change_direct(self, current_emotions: np.ndarray,
                                     interaction_vector: np.ndarray,
                                     personality_vector: np.ndarray) -> np.ndarray:
        """
        Applique un changement d'émotion direct pour un personnage impliqué dans une interaction.

        Formule mathématique:
            Δe = M_interaction @ i     (@ c'est le produit matriciel)
            m_p = M_personality @ p
            e_new = e_current + Δe × (1 + m_p × α)
            e_final = clamp(e_new, e_min, e_max)

        Où:
            - e ∈ ℝ⁶ : vecteur d'émotions [happiness, sadness, anger, fear, surprise, disgust]
            - i ∈ ℝ⁵ : vecteur d'interaction [agency, communion, intensity, physical_contact, valence]
            - p ∈ ℝ⁵ : vecteur de personnalité [openness, conscientiousness, extraversion, agreeableness, neuroticism]
            - M_interaction ∈ ℝ⁶ˣ⁵ : matrice de transformation interaction vers émotions
            - M_personality ∈ ℝ⁶ˣ⁵ : matrice de modulation par la personnalité
            - α : coefficient de modulation (personality_emotion_modulation_direct)

        Args:
            current_emotions: vecteur numpy (6,) des émotions actuelles
            interaction_vector: vecteur numpy (5,) représentant l'interaction
            personality_vector: vecteur numpy (5,) de la personnalité

        Returns:
            vecteur numpy (6,) des nouvelles émotions clampées dans [e_min, e_max]
        """
        # Calcul du changement d'émotion basé sur l'interaction
        emotion_delta = self.config.interaction_to_emotion_direct @ interaction_vector

        # Modulation par la personnalité
        personality_mod = self.config.personality_modulation @ personality_vector

        # Application du changement modulé
        new_emotions = current_emotions + emotion_delta * (
                1.0 + personality_mod * self.config.personality_emotion_modulation_direct
        )

        return new_emotions

    def _apply_relationship_change_direct(self, current_relationship: np.ndarray,
                                          interaction_vector: np.ndarray,
                                          personality_source: np.ndarray,
                                          personality_target: np.ndarray) -> np.ndarray:
        """
        Applique un changement de relation direct.

        Formule mathématique:
            Δr = M_relationship @ i     (@ c'est le produit matriciel)
            m_p₁ = M_personality_rel @ p_source
            m_p₂ = M_personality_rel @ p_target
            m_p = (m_p₁ + m_p₂) × ω
            r_new = r_current + Δr × (1 + m_p × α)
            r_final = clamp(r_new, r_min, r_max)

        Où:
            - r ∈ ℝ³ : vecteur de relation [privacy, commitment, passion] (théorie de Sternberg)
            - i ∈ ℝ⁵ : vecteur d'interaction [agency, communion, intensity, physical_contact, valence]
            - p_source, p_target ∈ ℝ⁵ : vecteurs de personnalité (Big Five)
            - M_relationship ∈ ℝ³ˣ⁵ : matrice de transformation interaction → relation
            - M_personality_rel ∈ ℝ³ˣ⁵ : matrice de compatibilité des personnalités
            - ω : poids de la compatibilité (personality_compatibility_weight)
            - α : coefficient de modulation (personality_relationship_modulation_direct)

        Args:
            current_relationship: vecteur numpy (3,) [privacy, commitment, passion]
            interaction_vector: vecteur numpy (5,) représentant l'interaction
            personality_source: vecteur numpy (5,) personnalité de la source
            personality_target: vecteur numpy (5,) personnalité de la cible

        Returns:
            vecteur numpy (3,) de la nouvelle relation clampée dans [r_min, r_max]
        """
        # Changement basé sur l'interaction
        relationship_delta = self.config.interaction_to_relationship_direct @ interaction_vector

        # Compatibilité des personnalités (moyenne des deux influences)
        personality_mod_source = self.config.personality_to_relationship @ personality_source
        personality_mod_target = self.config.personality_to_relationship @ personality_target
        personality_mod = (
                                  personality_mod_source + personality_mod_target) * self.config.personality_compatibility_weight

        # Application du changement modulé
        new_relationship = current_relationship + relationship_delta * (
                1.0 + personality_mod * self.config.personality_relationship_modulation_direct
        )

        return np.clip(new_relationship, self.config.relationship_min, self.config.relationship_max)

    def _apply_emotion_change_indirect(self, current_emotions: np.ndarray,
                                       interaction_vector: np.ndarray,
                                       personality_vector: np.ndarray) -> np.ndarray:
        """
        Applique un changement d'émotion indirect (le personnage a une relation avec un personnage impliqué).

        Formule mathématique:
            Δe = (M_interaction × β) @ i     (@ c'est le produit matriciel)
            m_p = M_personality @ p
            e_new = e_current + Δe × (1 + m_p × γ)
            e_final = clamp(e_new, e_min, e_max)

        Où:
            - e ∈ ℝ⁶ : vecteur d'émotions [happiness, sadness, anger, fear, surprise, disgust]
            - i ∈ ℝ⁵ : vecteur d'interaction [agency, communion, intensity, physical_contact, valence]
            - p ∈ ℝ⁵ : vecteur de personnalité [openness, conscientiousness, extraversion, agreeableness, neuroticism]
            - M_interaction ∈ ℝ⁶ˣ⁵ : matrice de transformation interaction → émotions
            - M_personality ∈ ℝ⁶ˣ⁵ : matrice de modulation par la personnalité
            - β : facteur d'atténuation indirect (indirect_emotion_attenuation)
            - γ : coefficient de modulation indirect (personality_emotion_modulation_indirect)

        Args:
            current_emotions: vecteur numpy (6,) des émotions actuelles
            interaction_vector: vecteur numpy (5,) représentant l'interaction
            personality_vector: vecteur numpy (5,) de la personnalité

        Returns:
            vecteur numpy (6,) des nouvelles émotions clampées dans [e_min, e_max]
        """
        # Changement atténué
        emotion_delta = (self.config.interaction_to_emotion_direct *
                         self.config.indirect_emotion_attenuation) @ interaction_vector

        # Modulation par la personnalité (encore plus atténuée)
        personality_mod = self.config.personality_modulation @ personality_vector

        # Application du changement modulé
        new_emotions = current_emotions + emotion_delta * (
                1.0 + personality_mod * self.config.personality_emotion_modulation_indirect
        )

        return new_emotions

    def _apply_relationship_change_indirect(self, current_relationship: np.ndarray,
                                            interaction_vector: np.ndarray,
                                            personality_observer: np.ndarray) -> np.ndarray:
        """
        Applique un changement de relation indirect (observer une interaction entre autres).

        Formule mathématique:
            Δr = (M_relationship × β) @ i     (@ c'est le produit matriciel)
            m_p = M_personality_rel @ p_observer
            r_new = r_current + Δr × (1 + m_p × γ)
            r_final = clamp(r_new, r_min, r_max)

        Où:
            - r ∈ ℝ³ : vecteur de relation [privacy, commitment, passion] (théorie de Sternberg)
            - i ∈ ℝ⁵ : vecteur d'interaction [agency, communion, intensity, physical_contact, valence]
            - p_observer ∈ ℝ⁵ : vecteur de personnalité de l'observateur (Big Five)
            - M_relationship ∈ ℝ³ˣ⁵ : matrice de transformation interaction → relation
            - M_personality_rel ∈ ℝ³ˣ⁵ : matrice de compatibilité des personnalités
            - β : facteur d'atténuation indirect (indirect_relationship_attenuation)
            - γ : coefficient de modulation indirect (personality_relationship_modulation_indirect)

        Args:
            current_relationship: vecteur numpy (3,) [privacy, commitment, passion]
            interaction_vector: vecteur numpy (5,) représentant l'interaction
            personality_observer: vecteur numpy (5,) personnalité de l'observateur

        Returns:
            vecteur numpy (3,) de la nouvelle relation clampée dans [r_min, r_max]
        """
        # Changement atténué
        relationship_delta = (self.config.interaction_to_relationship_direct *
                              self.config.indirect_relationship_attenuation) @ interaction_vector

        # Modulation par la personnalité de l'observateur
        personality_mod = self.config.personality_to_relationship @ personality_observer

        # Application du changement modulé
        new_relationship = current_relationship + relationship_delta * (
                1.0 + personality_mod * self.config.personality_relationship_modulation_indirect
        )

        return np.clip(new_relationship, self.config.relationship_min, self.config.relationship_max)
