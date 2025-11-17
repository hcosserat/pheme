from Character import Character
from Enum import Caractere
from Personality import Personality


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


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Test de la classe Character")
    print("=" * 50 + "\n")

    try:
        test_creation_personnage()
        test_changement_caractere()
        test_changement_personnalite()
        test_changements_multiples()
        test_tous_les_caracteres()

        print("=" * 50)
        print("Test terminé")
        print("=" * 50)

    except Exception as e:
        print(f"\nERREUR: {e}")
        import traceback

        traceback.print_exc()
