from random import random
from typing import Optional

import numpy as np


class Personality:
    """
    Implémentation de la personality avec le modèle Big Five:
    - ouverture à l'expérience vs conformisme
    - conscienciosité vs impulsivité
    - extraversion vs introversion
    - agréabilité vs antagonisme
    - névrosisme vs stabilité émotionnelle

    Chaque trait entre -1 et 1.
    https://fr.wikipedia.org/wiki/Mod%C3%A8le_des_Big_Five_(psychologie)
    """
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float

    def __init__(self, openness: Optional[float] = None,
                 conscientiousness: Optional[float] = None,
                 extraversion: Optional[float] = None,
                 agreeableness: Optional[float] = None,
                 neuroticism: Optional[float] = None):
        """Init la personality avec valeurs données ou random."""
        self.openness = self._initialize_trait(openness)
        self.conscientiousness = self._initialize_trait(conscientiousness)
        self.extraversion = self._initialize_trait(extraversion)
        self.agreeableness = self._initialize_trait(agreeableness)
        self.neuroticism = self._initialize_trait(neuroticism)

    @staticmethod
    def _initialize_trait(value: Optional[float]) -> float:
        if value is not None:
            return max(-1.0, min(1.0, value))

        return random() * 2 - 1  # Random entre -1 et 1

    def getMixPersonality(A, B):
        personalityA = np.array([
            A.openness,
            A.conscientiousness,
            A.extraversion,
            A.agreeableness,
            A.neuroticism
        ])
        personalityB = np.array([
            B.openness,
            B.conscientiousness,
            B.extraversion,
            B.agreeableness,
            B.neuroticism
        ])

        produit = np.dot(personalityA, personalityB)
        normeA = np.linalg.norm(personalityA)
        normeB = np.linalg.norm(personalityB)

        if normeA == 0 or normeB == 0:
            return 0.5
        similarity = produit / (normeA * normeB)
        return similarity

    def __repr__(self) -> str:
        return (f"Personality(openness={self.openness:.2f}, "
                f"conscientiousness={self.conscientiousness:.2f}, "
                f"extraversion={self.extraversion:.2f}, "
                f"agreeableness={self.agreeableness:.2f}, "
                f"neuroticism={self.neuroticism:.2f})")

    def __str__(self):
        return self.__repr__()

    def asArray(self):
        return np.array([
            self.openness,
            self.conscientiousness,
            self.extraversion,
            self.agreeableness,
            self.neuroticism
        ])
