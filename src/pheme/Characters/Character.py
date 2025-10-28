from .Enum import Caractere
from .Personality import Personality


class Character:
    """
    Classe représentant un personnage avec un nom, un caractère et une personnalité.
    """

    def __init__(self, name: str, caractere: Caractere, personality: Personality):
        """
        Initialise un personnage avec un nom, un caractère et une personnalité.
        """
        self.name = name
        self.caractere = caractere
        self.personality = personality

    def __str__(self) -> str:
        """
        Retourne une description lisible du personnage.
        """
        return f"{self.name} | Caractère : {self.caractere.value} | Personnalité : {self.personality}"

    def decrire(self):
        print(self.__str__())

    def changer_caractere(self, nouveau_caractere: Caractere):
        """
        Modifie le caractère du personnage.
        """
        ancien = self.caractere
        self.caractere = nouveau_caractere
        print(f"{self.name} change de caractère : '{ancien.value}' → '{nouveau_caractere.value}'")

    def changer_personnalite(self, new_personality: Personality):
        """
        Modifie la personnalité du personnage.
        """
        ancienne = self.personality
        self.personality = new_personality
        print(f"{self.name} change de personnalité : '{ancienne}' → '{new_personality}'")
