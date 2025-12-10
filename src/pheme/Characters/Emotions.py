import numpy as np


class Emotions:
    """Représente les émotions d'un character avec des valeurs float entre 0 et 1."""
    happiness: float
    sadness: float
    anger: float
    fear: float
    surprise: float
    disgust: float

    def __init__(self, happiness: float = 0.0,
                 sadness: float = 0.0,
                 anger: float = 0.0,
                 fear: float = 0.0,
                 surprise: float = 0.0,
                 disgust: float = 0.0):
        """Init les émotions avec clamp [0,1]."""
        self.happiness = max(0.0, min(1.0, happiness))
        self.sadness = max(0.0, min(1.0, sadness))
        self.anger = max(0.0, min(1.0, anger))
        self.fear = max(0.0, min(1.0, fear))
        self.surprise = max(0.0, min(1.0, surprise))
        self.disgust = max(0.0, min(1.0, disgust))

    def updateEmotions(self, change):
        self.updateGoodEmotions(change)
        self.updateBadEmotions(change)

    def updateGoodEmotions(self, change):
        self.happiness = max(0.0, min(1.0, self.happiness + change * 0.38 / 2))
        self.surprise = max(0.0, min(1.0, self.surprise + change * 0.59 / 2))

    def updateBadEmotions(self, change):
        self.sadness = max(0.0, min(1.0, self.sadness - change * 0.35 / 2))
        self.anger = max(0.0, min(1.0, self.anger - change * 0.48 / 2))
        self.fear = max(0.0, min(1.0, self.fear - change * 0.41 / 2))
        self.disgust = max(0.0, min(1.0, self.disgust - change * 0.54 / 2))

    def __repr__(self) -> str:
        return (f"Emotions(happiness={self.happiness:.2f}, "
                f"sadness={self.sadness:.2f}, "
                f"anger={self.anger:.2f}, "
                f"fear={self.fear:.2f}, "
                f"surprise={self.surprise:.2f}, "
                f"disgust={self.disgust:.2f})")

    def __str__(self):
        return self.__repr__()

    def asArray(self):
        return np.array([
            self.happiness,
            self.sadness,
            self.anger,
            self.fear,
            self.surprise,
            self.disgust
        ])
