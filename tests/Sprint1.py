from src.pheme import *


def test_creation_personnage():
    """Test de la création d'un personnage"""
    print("=" * 50)
    print("TEST 1: Création de personnages")
    print("=" * 50)

    # Création de plusieurs personnages avec différentes émotions
    hero = Character("Alice", Personality(agreeableness=0.8, extraversion=0.5), Emotions(happiness=0.8, fear=0.2))
    print(hero)

    villain = Character("Bob", Personality(neuroticism=0.7, openness=-0.3), Emotions(anger=0.9, disgust=0.6))
    print(villain)

    sage = Character("Merlin", Personality(conscientiousness=0.9, openness=-0.9), Emotions(happiness=0.5, surprise=0.1))
    print(sage)

    print()


def test_changement_emotions():
    """Test du changement d'émotions"""
    print("=" * 50)
    print("TEST 2: Changement d'émotions")
    print("=" * 50)

    personnage = Character("Charlie", Personality(neuroticism=0.6, extraversion=-0.4), Emotions(fear=0.8, sadness=0.6))
    print(personnage)

    print("\n--- Changement d'émotions ---")
    personnage.changeEmotions(Emotions(happiness=0.7, surprise=0.5))
    print(personnage)

    print()


def test_changement_personnalite():
    """Test du changement de personnalité"""
    print("=" * 50)
    print("TEST 3: Changement de personnalité")
    print("=" * 50)

    personnage = Character("Diana", Personality(openness=0.7, agreeableness=0.9), Emotions(happiness=0.9, surprise=0.3))
    print(personnage)

    print("\n--- Changement de personnalité ---")
    personnage.changePersonality(Personality(openness=-0.5, agreeableness=0.2))
    print(personnage)

    print()


def test_changements_multiples():
    """Test de changements multiples"""
    print("=" * 50)
    print("TEST 4: Changements multiples")
    print("=" * 50)

    personnage = Character("Evan", Personality(conscientiousness=-0.6, extraversion=0.4), Emotions(anger=0.7, surprise=0.4))
    print(personnage)

    print("\n--- Évolution du personnage ---")
    personnage.changeEmotions(Emotions(happiness=0.6, surprise=0.2))
    personnage.changePersonality(Personality(conscientiousness=0.5, extraversion=0.1))
    print(personnage)

    print()


def test_diverses_emotions():
    """Test avec diverses émotions"""
    print("=" * 50)
    print("TEST 5: Diverses émotions")
    print("=" * 50)

    # Test avec différentes combinaisons d'émotions
    emotions_tests = [
        ("Joyeux", Emotions(happiness=0.9)),
        ("Triste", Emotions(sadness=0.8)),
        ("En colère", Emotions(anger=0.9)),
        ("Apeuré", Emotions(fear=0.8)),
        ("Surpris", Emotions(surprise=0.9)),
        ("Dégoûté", Emotions(disgust=0.8)),
        ("Neutre", Emotions()),
    ]

    for nom, emotion in emotions_tests:
        perso = Character(nom, Personality(), emotion)
        print(f"  - {perso}")

    print()


def test_relations():
    """Test des relations entre personnages"""
    print("=" * 50)
    print("TEST 6: Relations entre personnages")
    print("=" * 50)

    # Création de personnages avec émotions
    garcon = Character("Garçon", Personality(agreeableness=-0.5, neuroticism=0.6), Emotions(anger=0.8, disgust=0.5))
    frere = Character("Frère", Personality(agreeableness=0.7, neuroticism=0.4), Emotions(fear=0.6, sadness=0.4))
    roi = Character("Roi", Personality(conscientiousness=0.8, extraversion=0.3), Emotions(happiness=0.5))
    general = Character("Général", Personality(conscientiousness=0.9, extraversion=0.5), Emotions(happiness=0.6, surprise=0.2))
    personne_a = Character("Personne A", Personality(agreeableness=0.9, extraversion=0.7), Emotions(happiness=0.9))
    personne_b = Character("Personne B", Personality(agreeableness=0.8, extraversion=0.6), Emotions(happiness=0.9, surprise=0.3))

    # Un garçon déteste son frère
    relationship_1 = Relationship(
        source=garcon,
        target=frere,
        typeRelationship=TypeRelationship(privacy=-0.7, commitment=-0.5, passion=-0.8)
    )

    # Roi envers son général (relation professionnelle)
    relationship_2 = Relationship(
        source=roi,
        target=general,
        typeRelationship=newRelatioship_Professionally(privacy=0.2, commitment=0.8, passion=0.0)
    )

    # Relation amoureuse
    relationship_3 = Relationship(
        source=personne_a,
        target=personne_b,
        typeRelationship=newRelatioship_Lovely()
    )

    print("=== Fratrie conflictuelle ===")
    print(relationship_1)

    print("\n=== Relation professionnelle ===")
    print(relationship_2)

    print("\n=== Relation amoureuse ===")
    print(relationship_3)

    # Test de mise à jour
    print("\n=== Après amélioration de la relation fraternelle ===")
    relationship_1.updateRelationship(newPrivacy=0.3, newCommitment=0.4, newPassion=0.1)
    print(relationship_1)

    print()


def test_types_relations():
    """Test des différents types de relations prédéfinis"""
    print("=" * 50)
    print("TEST 7: Types de relations prédéfinis")
    print("=" * 50)

    alice = Character("Alice", Personality(), Emotions(happiness=0.7))
    bob = Character("Bob", Personality(), Emotions(happiness=0.6))

    # Test de tous les types de relations
    types = [
        ("Lovely", newRelatioship_Lovely()),
        ("Friendly", newRelatioship_Friendly()),
        ("Family", newRelatioship_Family()),
        ("Professionally", newRelatioship_Professionally()),
        ("Unfriendly", newRelatioship_Unfriendly()),
    ]

    for name, type_rel in types:
        rel = Relationship(alice, bob, type_rel)
        print(f"\n=== Relation {name} ===")
        print(rel)

    print()


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Tests de Pheme - Sprint 1")
    print("=" * 50 + "\n")

    try:
        # Tests des personnages
        test_creation_personnage()
        test_changement_emotions()
        test_changement_personnalite()
        test_changements_multiples()
        test_diverses_emotions()

        # Tests des relations
        test_relations()
        test_types_relations()

        print("=" * 50)
        print("Tous les tests sont terminés avec succès !")
        print("=" * 50)

    except Exception as e:
        print(f"\nERREUR: {e}")
        import traceback
        traceback.print_exc()
