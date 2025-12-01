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
    """
    Gère les mises à jour des émotions et relations basées sur les interactions.
    """

    def __init__(self, graph: Graph):
        """
        Args:
            graph: Le graphe contenant les personnages et leurs relations
        """
        self.graph = graph
        self.config = EngineConfiguration()
        # Liste des propagations en attente : (tick_arrivée, cible, interaction)
        self.pending_propagations: List[Tuple[int, Character, Interaction]] = []

    def tick(self, current_tick: int):
        """
        Met à jour la diffusion des informations.
        À appeler à chaque tick de la simulation.
        Traite les informations dont le temps de trajet est écoulé.
        """
        # On filtre les événements qui sont arrivés (tick_arrivée <= current_tick)
        remaining_propagations = []

        for arrival_tick, target, interaction in self.pending_propagations:
            if arrival_tick <= current_tick:
                # L'information arrive au personnage cible
                # On vérifie s'il ne la connait pas déjà (pour éviter les doublons)
                if interaction not in target.knownInteractions:
                    target.learnAboutInteraction(interaction)
                    # Le personnage réagit à cette nouvelle information
                    self.processInteractionForCharacter(target, interaction)

                    # Optionnel : Ici, on pourrait déclencher une re-diffusion (bouche-à-oreille)
                    # self.diffuseInteraction(target, interaction, current_tick)
            else:
                # L'information est toujours en transit
                remaining_propagations.append((arrival_tick, target, interaction))

        self.pending_propagations = remaining_propagations

    def diffuseInteraction(self, source: Character, interaction: Interaction, current_tick: int,
                           already_informed: Set[Character] = None):
        """
        Un Character diffuse une information sur une Interaction à ses voisins.
        La diffusion prend du temps selon la distance informationnelle des relations.

        Args:
            source: Le personnage qui diffuse l'information
            interaction: L'interaction à diffuser
            current_tick: Le tick actuel de la simulation
            already_informed: (Obsolète avec le système de tick, gardé pour compatibilité)
        """
        # Le propagateur apprend l'info immédiatement s'il ne la connait pas
        if interaction not in source.knownInteractions:
            source.learnAboutInteraction(interaction)

        neighbors = self.graph.getNeighbors(source)

        for neighbor in neighbors:
            # Récupérer la relation pour connaître la distance
            relationship = self.graph.getEdge(source.name, neighbor.name)

            if relationship is not None:
                # Calcul du moment d'arrivée de l'information
                distance = relationship.informational_distance
                arrival_tick = current_tick + distance

                # On planifie l'arrivée de l'information
                self.pending_propagations.append((arrival_tick, neighbor, interaction))

    def processInteractionForCharacter(self, character: Character, interaction: Interaction):
        """
        Un Character traite une Interaction.

        - Si le Character fait partie de l'Interaction, changements directs
        - Si le Character a une relation avec un des participants, changements indirects

        Args:
            character: Le personnage qui traite l'interaction
            interaction: L'interaction à traiter
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
        Traite une interaction directe (le personnage est impliqué).
        Met à jour ses émotions et sa relation avec l'autre participant.
        Met également à jour indirectement les relations avec les proches de l'autre participant.

        Args:
            character: Le personnage qui traite l'interaction
            interaction: L'interaction
            is_actor: True si le personnage est l'acteur, False s'il est la cible
        """
        # Déterminer l'autre personnage
        other_character = interaction.target if is_actor else interaction.actor

        # Vecteurs pour les calculs matriciels
        interaction_vector = interaction.asArray()
        personality_vector = character.personality.asArray()
        current_emotions = character.emotions.asArray()

        # Inverser la valence si c'est l'acteur (l'acteur voit l'interaction différemment)
        if is_actor:
            interaction_vector = interaction_vector.copy()
            interaction_vector[4] *= self.config.actor_valence_attenuation

        # === 1. Mise à jour des émotions ===
        new_emotions_array = self._apply_emotion_change_direct(
            current_emotions, interaction_vector, personality_vector
        )
        self._update_character_emotions(character, new_emotions_array)

        # === 2. Mise à jour de la relation directe ===
        relationship = self.graph.getEdge(character.name, other_character.name)

        # Si la relation n'existe pas, on la crée (Relation Neutre par défaut)
        if relationship is None:
            new_type = TypeRelationship(0.0, 0.0, 0.0)
            self.graph.addEdge(character.name, other_character.name, new_type)
            relationship = self.graph.getEdge(character.name, other_character.name)

        self._update_relationship_direct(character, other_character, relationship, interaction_vector)

        # === 3. Propagation : Mise à jour des relations associées ===
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
        Traite une interaction indirecte (le personnage connaît un participant).
        Les changements sont atténués.

        Args:
            character: Le personnage observateur
            interaction: L'interaction observée
            has_relation_with_actor: True si le personnage connaît l'acteur
            has_relation_with_target: True si le personnage connaît la cible
        """
        if not (has_relation_with_actor or has_relation_with_target):
            return

        # Vecteurs pour les calculs
        interaction_vector = interaction.asArray()
        personality_vector = character.personality.asArray()
        current_emotions = character.emotions.asArray()

        # Mise à jour des émotions (impact indirect)
        new_emotions_array = self._apply_emotion_change_indirect(
            current_emotions, interaction_vector, personality_vector
        )
        self._update_character_emotions(character, new_emotions_array)

        # Mise à jour des relations avec les participants connus
        if has_relation_with_actor:
            relationship = self.graph.getEdge(character.name, interaction.actor.name)
            if relationship is not None:
                self._update_relationship_indirect(character, relationship, interaction_vector)

        if has_relation_with_target:
            relationship = self.graph.getEdge(character.name, interaction.target.name)
            if relationship is not None:
                self._update_relationship_indirect(character, relationship, interaction_vector)

    def _update_character_emotions(self, character: Character, new_emotions_array: np.ndarray):
        """
        Met à jour les émotions d'un personnage à partir d'un vecteur numpy.

        Args:
            character: Le personnage à mettre à jour
            new_emotions_array: Vecteur numpy (6,) des nouvelles émotions
        """
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
        """
        Met à jour une relation de manière directe.

        Args:
            source: Personnage source de la relation
            target: Personnage cible de la relation
            relationship: L'objet Relationship à mettre à jour
            interaction_vector: Vecteur de l'interaction
        """
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
        """
        Met à jour une relation de manière indirecte.

        Args:
            observer: Personnage observateur
            relationship: L'objet Relationship à mettre à jour
            interaction_vector: Vecteur de l'interaction
        """
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
        """
        Vérifie si deux personnages ont une relation.

        Args:
            character1: Premier personnage
            character2: Deuxième personnage

        Returns:
            True s'il existe une relation de character1 vers character2
        """
        return self.graph.getEdge(character1.name, character2.name) is not None

    def processInteractionForGroup(self, group: list[Character], interaction: Interaction):
        """
        Traite une interaction par tout un ensemble de personnages.
        Par exemple, si plusieurs personnages ont vu une interactions avoir lieu.

        Args:
            group: liste des Character qui traiteront l'interaction
            interaction: interaction à traiter
        """
        for character in group:
            self.processInteractionForCharacter(character, interaction)

    def processInteractionForAll(self, interaction: Interaction):
        """
        Traite une interaction pour tous les personnages du graphe.

        Args:
            interaction: L'interaction à traiter
        """
        self.processInteractionForGroup(self.graph.listNode, interaction)

    # === À partir d'ici c'est le calcul matricielle pour la mise à jour des vecteurs ===

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
