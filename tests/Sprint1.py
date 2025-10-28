from src.pheme import *


def test_creation_personnage():
    """Test de la création d'un personnage"""
    print("=" * 50)
    print("TEST 1: Création de personnages")
    print("=" * 50)

    # Création de plusieurs personnages avec différents enums
    hero = Character("Alice", Caractere.COURAGEUX, Personality(agreeableness=0.8, extraversion=0.5))
    hero.decrire()

    villain = Character("Bob", Caractere.AGRESSIF, Personality(neuroticism=0.7, openness=-0.3))
    villain.decrire()

    sage = Character("Merlin", Caractere.CALME, Personality(conscientiousness=0.9, openness=-0.9))
    sage.decrire()

    print()


def test_changement_caractere():
    """Test du changement de caractère"""
    print("=" * 50)
    print("TEST 2: Changement de caractère")
    print("=" * 50)

    personnage = Character("Charlie", Caractere.TIMIDE, Personality(neuroticism=0.6, extraversion=-0.4))
    personnage.decrire()

    print("\n--- Changement de caractère ---")
    personnage.changer_caractere(Caractere.COURAGEUX)
    personnage.decrire()

    print()


def test_changement_personnalite():
    """Test du changement de personnalité"""
    print("=" * 50)
    print("TEST 3: Changement de personnalité")
    print("=" * 50)

    personnage = Character("Diana", Caractere.JOYEUX, Personality(openness=0.7, agreeableness=0.9))
    personnage.decrire()

    print("\n--- Changement de personnalité ---")
    personnage.changer_personnalite(Personality(openness=-0.5, agreeableness=0.2))
    personnage.decrire()

    print()


def test_changements_multiples():
    """Test de changements multiples"""
    print("=" * 50)
    print("TEST 4: Changements multiples")
    print("=" * 50)

    personnage = Character("Evan", Caractere.IMPULSIF, Personality(conscientiousness=-0.6, extraversion=0.4))
    personnage.decrire()

    print("\n--- Évolution du personnage ---")
    personnage.changer_caractere(Caractere.PATIENT)
    personnage.changer_personnalite(Personality(conscientiousness=0.5, extraversion=0.1))
    personnage.decrire()

    print()


def test_tous_les_caracteres():
    """Test avec tous les caractères disponibles"""
    print("=" * 50)
    print("TEST 5: Tous les types de caractère")
    print("=" * 50)

    for caractere in Caractere:
        perso = Character(f"Test_{caractere.name}", caractere, Personality())
        print(f"  - {perso}")

    print()


def test_relations():
    """Test des relations entre personnages"""
    print("=" * 50)
    print("TEST 6: Relations entre personnages")
    print("=" * 50)

    # Création de personnages
    garcon = Character("Garçon", Caractere.AGRESSIF, Personality(agreeableness=-0.5, neuroticism=0.6))
    frere = Character("Frère", Caractere.TIMIDE, Personality(agreeableness=0.7, neuroticism=0.4))
    roi = Character("Roi", Caractere.CALME, Personality(conscientiousness=0.8, extraversion=0.3))
    general = Character("Général", Caractere.COURAGEUX, Personality(conscientiousness=0.9, extraversion=0.5))
    personne_a = Character("Personne A", Caractere.JOYEUX, Personality(agreeableness=0.9, extraversion=0.7))
    personne_b = Character("Personne B", Caractere.JOYEUX, Personality(agreeableness=0.8, extraversion=0.6))

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

    alice = Character("Alice", Caractere.JOYEUX, Personality())
    bob = Character("Bob", Caractere.CALME, Personality())

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
        test_changement_caractere()
        test_changement_personnalite()
        test_changements_multiples()
        test_tous_les_caracteres()

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
