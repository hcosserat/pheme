from typing import TYPE_CHECKING

from .Emotions import Emotions
from .Personality import Personality

if TYPE_CHECKING:
    from ..Interactions.Interaction import Interaction


class Character:
    """Représente un personnage avec un nom, une personality et des émotions."""

    def __init__(self, name: str, personality: Personality, emotions: Emotions):
        """Init un character avec nom, personality et émotions."""
        self.name = name
        self.personality = personality
        self.emotions = emotions

        self.knownInteractions = set()

    def __str__(self) -> str:
        return f"{self.name} | Personnalité : {self.personality} | Émotions : {self.emotions}"

    def __repr__(self):
        return self.__str__()

    def changeEmotions(self, newEmotions: Emotions):
        anciennes = self.emotions
        self.emotions = newEmotions
        print(f"{self.name} change d'émotions : '{anciennes}' → '{newEmotions}'")

    def changePersonality(self, newPersonality: Personality):
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
