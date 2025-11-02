from .Enum import Caractere
from .Personality import Personality


class Character:
    """
    Classe représentant un personnage avec un nom, une personnalité et des émotions.
    """

    def __init__(self, name: str, personality: Personality, emotions: Emotions):
        """
        Initialise un personnage avec un nom, un caractère et une personnalité.
        """
        self.name = name
        self.personality = personality
        self.emotions = emotions

    def __str__(self) -> str:
        """
        Retourne une description lisible du personnage.
        """
        return f"{self.name} | Personnalité : {self.personality} | Émotions : {self.emotions}"

    def __repr__(self):
        return self.__str__()

    def changeEmotions(self, newEmotions: Emotions):
        """
        Modifie les émotions du personnage.
        """
        anciennes = self.emotions
        self.emotions = newEmotions
        print(f"{self.name} change d'émotions : '{anciennes}' → '{newEmotions}'")

    def changePersonality(self, newPersonality: Personality):
        """
        Modifie la personnalité du personnage.
        """
        ancienne = self.personality
        self.personality = newPersonality
        print(f"{self.name} change de personnalité : '{ancienne}' → '{newPersonality}'")
