import numpy as np


class EngineConfiguration:
    """
    Configuration du système de relations sociales.
    Contient toutes les matrices et paramètres configurables.

    todo: pour l'instant tout a été rempli par un IA, faudrait les choisir mieux
    """

    # === Émotions ===

    # Matrice de transformation directe : Interaction (5D) -> Emotions (6D)
    # [agency, communion, intensity, physical_contact, valence] -> [happiness, sadness, anger, fear, surprise, disgust]
    interaction_to_emotion_direct = np.array([
        [0.3, 0.5, 0.2, 0.1, 0.8],  # happiness: fortement influencé par valence et communion
        [0.1, -0.4, 0.1, 0.0, -0.7],  # sadness: inversement proportionnel à valence et communion
        [0.4, -0.5, 0.3, 0.2, -0.5],  # anger: influencé par agency négatif et valence négative
        [0.3, -0.3, 0.2, 0.1, -0.4],  # fear: lié à l'agency des autres et valence négative
        [0.2, 0.3, 0.5, 0.3, 0.0],  # surprise: fortement lié à l'intensité
        [-0.1, -0.5, 0.1, 0.0, -0.6],  # disgust: lié à communion et valence négatives
    ])

    # Matrice de modulation par la personnalité: Personality (5D) -> Emotion weights (6D)
    # [openness, conscientiousness, extraversion, agreeableness, neuroticism]
    personality_modulation = np.array([
        [0.2, -0.1, 0.4, 0.3, -0.5],  # happiness modulé par extraversion et stabilité
        [0.0, 0.1, -0.3, -0.2, 0.6],  # sadness modulé par neuroticism
        [-0.1, -0.2, 0.1, -0.5, 0.5],  # anger modulé par faible agreeableness et neuroticism
        [0.0, 0.2, -0.2, -0.1, 0.7],  # fear modulé par neuroticism
        [0.4, 0.0, 0.2, 0.0, 0.2],  # surprise modulé par openness
        [-0.2, 0.1, -0.1, -0.4, 0.3],  # disgust modulé par faible agreeableness
    ])

    # === Relations ===

    # Matrice de transformation directe : Interaction (5D) -> Relationship change (3D)
    # [agency, communion, intensity, physical_contact, valence] -> [privacy, commitment, passion]
    interaction_to_relationship_direct = np.array([
        [0.1, 0.4, 0.2, 0.3, 0.5],  # privacy: influencé par communion, contact physique et valence
        [0.2, 0.5, 0.1, 0.1, 0.6],  # commitment: fortement influencé par communion et valence
        [0.3, 0.3, 0.5, 0.4, 0.4],  # passion: influencé par intensity et physical_contact
    ])

    # Matrice de compatibilité des personnalités : Personality (5D) -> Relationship modifier (3D)
    personality_to_relationship = np.array([
        [0.3, 0.1, 0.2, 0.4, -0.2],  # privacy: ouverture et agreeableness
        [0.0, 0.5, 0.1, 0.3, -0.3],  # commitment: conscientiousness et agreeableness
        [0.2, -0.1, 0.4, 0.1, 0.0],  # passion: extraversion et openness
    ])

    # === Atténuations et modulation ===

    # Facteur d'atténuation pour les effets indirects sur les émotions
    indirect_emotion_attenuation = 0.3

    # Facteur d'atténuation pour les effets indirects sur les relations
    indirect_relationship_attenuation = 0.2

    # Force de la modulation de la personnalité sur les émotions (direct)
    personality_emotion_modulation_direct = 0.5

    # Force de la modulation de la personnalité sur les émotions (indirect)
    personality_emotion_modulation_indirect = 0.3

    # Force de la modulation de la personnalité sur les relations (direct)
    personality_relationship_modulation_direct = 0.3

    # Force de la modulation de la personnalité sur les relations (indirect)
    personality_relationship_modulation_indirect = 0.2

    # Atténuation de la valence pour l'acteur d'une interaction
    actor_valence_attenuation = 0.5

    # Poids de la moyenne des personnalités pour les relations directes
    personality_compatibility_weight = 0.5

    # === Clamping ===

    relationship_min = -1.0
    relationship_max = 1.0
