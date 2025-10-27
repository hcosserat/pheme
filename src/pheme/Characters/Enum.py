from enum import Enum


class Caractere(Enum):
    """Enum représentant les différents types de caractère d'un personnage."""
    COURAGEUX = "courageux"
    TIMIDE = "timide"
    AGRESSIF = "agressif"
    CALME = "calme"
    IMPULSIF = "impulsif"
    PATIENT = "patient"
    JOYEUX = "joyeux"
    MELANCOLIQUE = "mélancolique"


# class Personnalite(Enum):
#     """Enum représentant les différents types de personnalité d'un personnage."""
#     OPTIMISTE = "optimiste"
#     PESSIMISTE = "pessimiste"
#     PRAGMATIQUE = "pragmatique"
#     REVEUR = "rêveur"
#     INTROVERTI = "introverti"
#     EXTRAVERTI = "extraverti"
#     ANALYTIQUE = "analytique"
#     CREATIF = "créatif"
