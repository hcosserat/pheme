import numpy as np


class EngineConfiguration:
    """Config du système de relations sociales avec matrices et paramètres."""
    alpha = 0.3

    # === Émotions ===

    # Matrice transformation directe : Interaction (5D) -> Emotions (6D)
    # [agency, communion, intensity, physical_contact, valence] -> [happiness, sadness, anger, fear, surprise, disgust]
    interaction_to_emotion_direct = np.array([
        [0.3, 0.5, 0.2, 0.1, 0.8],  # happiness: valence et communion
        [0.1, -0.4, 0.1, 0.0, -0.7],  # sadness: inverse valence et communion
        [0.4, -0.5, 0.3, 0.2, -0.5],  # anger: agency négatif et valence négative
        [0.3, -0.3, 0.2, 0.1, -0.4],  # fear: agency des autres et valence négative
        [0.2, 0.3, 0.5, 0.3, 0.0],  # surprise: lié à l'intensité
        [-0.1, -0.5, 0.1, 0.0, -0.6],  # disgust: communion et valence négatives
    ]) * alpha  # évolution plus lente

    # Matrice modulation par personality: Personality (5D) -> Emotion weights (6D)
    personality_modulation = np.array([
        [0.2, -0.1, 0.4, 0.3, -0.5],  # happiness: extraversion et stabilité
        [0.0, 0.1, -0.3, -0.2, 0.6],  # sadness: neuroticism
        [-0.1, -0.2, 0.1, -0.5, 0.5],  # anger: faible agreeableness et neuroticism
        [0.0, 0.2, -0.2, -0.1, 0.7],  # fear: neuroticism
        [0.4, 0.0, 0.2, 0.0, 0.2],  # surprise: openness
        [-0.2, 0.1, -0.1, -0.4, 0.3],  # disgust: faible agreeableness
    ]) * alpha

    # === Relations ===

    # Matrice transformation directe : Interaction (5D) -> Relationship change (3D)
    interaction_to_relationship_direct = np.array([
        [0.1, 0.4, 0.2, 0.3, 0.5],  # privacy: communion, contact physique et valence
        [0.2, 0.5, 0.1, 0.1, 0.6],  # commitment: communion et valence
        [0.3, 0.3, 0.5, 0.4, 0.4],  # passion: intensity et physical_contact
    ]) * alpha

    # Matrice compatibilité personalities : Personality (5D) -> Relationship modifier (3D)
    personality_to_relationship = np.array([
        [0.3, 0.1, 0.2, 0.4, -0.2],  # privacy: ouverture et agreeableness
        [0.0, 0.5, 0.1, 0.3, -0.3],  # commitment: conscientiousness et agreeableness
        [0.2, -0.1, 0.4, 0.1, 0.0],  # passion: extraversion et openness
    ]) * alpha

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
