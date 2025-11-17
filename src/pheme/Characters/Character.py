from typing import TYPE_CHECKING

from .Emotions import Emotions
from .Personality import Personality

if TYPE_CHECKING:
    from ..Interactions.Interaction import Interaction


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

        self.knownInteractions = set()

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

    def learnAboutInteraction(self, interaction: 'Interaction'):
        self.knownInteractions.add(interaction)

    def forgetInteractionsOlderThan(self, currentTimestamp: float, maxInteractionAge: float):
        self.knownInteractions = {
            interaction for interaction in self.knownInteractions
            if interaction.timestamp >= (currentTimestamp - maxInteractionAge)
        }
