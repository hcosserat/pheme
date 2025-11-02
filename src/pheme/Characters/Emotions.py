class Emotions:
    """
    Classe représentant les émotions d'un personnage.
    Chaque émotion est représentée par une valeur flottante entre 0 et 1.
    """
    happiness: float  # bonheur
    sadness: float  # tristesse
    anger: float  # colère
    fear: float  # peur
    surprise: float  # surprise
    disgust: float  # dégoût

    def __init__(self, happiness: float = 0.0,
                 sadness: float = 0.0,
                 anger: float = 0.0,
                 fear: float = 0.0,
                 surprise: float = 0.0,
                 disgust: float = 0.0):
        """Initialise les émotions avec les valeurs données ou par défaut à 0."""
        self.happiness = max(0.0, min(1.0, happiness))
        self.sadness = max(0.0, min(1.0, sadness))
        self.anger = max(0.0, min(1.0, anger))
        self.fear = max(0.0, min(1.0, fear))
        self.surprise = max(0.0, min(1.0, surprise))
        self.disgust = max(0.0, min(1.0, disgust))

    def __repr__(self) -> str:
        return (f"Emotions(happiness={self.happiness:.2f}, "
                f"sadness={self.sadness:.2f}, "
                f"anger={self.anger:.2f}, "
                f"fear={self.fear:.2f}, "
                f"surprise={self.surprise:.2f}, "
                f"disgust={self.disgust:.2f})")

    def __str__(self):
        return self.__repr__()
