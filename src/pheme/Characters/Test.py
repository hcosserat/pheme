from Character import Character
from Enum import Caractere, Personnalite


def test_creation_personnage():
    """Test de la création d'un personnage"""
    print("=" * 50)
    print("TEST 1: Création de personnages")
    print("=" * 50)
    
    # Création de plusieurs personnages avec différents enums
    hero = Character("Alice", Caractere.COURAGEUX, Personnalite.OPTIMISTE)
    hero.decrire()
    
    villain = Character("Bob", Caractere.AGRESSIF, Personnalite.PESSIMISTE)
    villain.decrire()
    
    sage = Character("Merlin", Caractere.CALME, Personnalite.ANALYTIQUE)
    sage.decrire()
    
    print()


def test_changement_caractere():
    """Test du changement de caractère"""
    print("=" * 50)
    print("TEST 2: Changement de caractère")
    print("=" * 50)
    
    personnage = Character("Charlie", Caractere.TIMIDE, Personnalite.INTROVERTI)
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
    
    personnage = Character("Diana", Caractere.JOYEUX, Personnalite.PESSIMISTE)
    personnage.decrire()
    
    print("\n--- Changement de personnalité ---")
    personnage.changer_personnalite(Personnalite.OPTIMISTE)
    personnage.decrire()
    
    print()


def test_changements_multiples():
    """Test de changements multiples"""
    print("=" * 50)
    print("TEST 4: Changements multiples")
    print("=" * 50)
    
    personnage = Character("Evan", Caractere.IMPULSIF, Personnalite.CREATIF)
    personnage.decrire()
    
    print("\n--- Évolution du personnage ---")
    personnage.changer_caractere(Caractere.PATIENT)
    personnage.changer_personnalite(Personnalite.PRAGMATIQUE)
    personnage.decrire()
    
    print()


def test_tous_les_caracteres():
    """Test avec tous les caractères disponibles"""
    print("=" * 50)
    print("TEST 5: Tous les types de caractère")
    print("=" * 50)
    
    for caractere in Caractere:
        perso = Character(f"Test_{caractere.name}", caractere, Personnalite.OPTIMISTE)
        print(f"  - {perso}")
    
    print()


def test_toutes_les_personnalites():
    """Test avec toutes les personnalités disponibles"""
    print("=" * 50)
    print("TEST 6: Tous les types de personnalité")
    print("=" * 50)
    
    for personnalite in Personnalite:
        perso = Character(f"Test_{personnalite.name}", Caractere.CALME, personnalite)
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
        test_toutes_les_personnalites()
        
        print("=" * 50)
        print("Test terminé")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nERREUR: {e}")
        import traceback
        traceback.print_exc()
