from random import random
from typing import Optional


class Personality:
    """
    Implémentation de la personalité grâce au modèle des 5 traits :

    - ouverture à l’expérience vd fermeture/conformisme: imagination, curiosité, intérêt pour la nouveauté vs préférence pour la routine, traditionalisme

    - conscienciosité (conscience) vs impulsivité/désorganisation: organisation, autodiscipline, fiabilité vs désordre, négligence, procrastination

    - extraversion vs introversion: sociabilité, énergie, assertivité vs réserve, orientation interne, faible recherche de stimulation sociale

    - agréabilité vs antagonisme: coopération, empathie, confiance vs compétitivité dure, méfiance, dureté interpersonnelle

    - névrosisme vs stabilité émotionnelle: tendance aux affects négatifs (anxiété, irritabilité, vulnérabilité) vs calme et résilience émotionnelle

    https://fr.wikipedia.org/wiki/Mod%C3%A8le_des_Big_Five_(psychologie)

    Chaque trait est représenté par une valeur flottante entre -1 et 1.
    """
    openness: float  # ouverture
    conscientiousness: float  # conscience
    extraversion: float  # extraversion
    agreeableness: float  # agréabilité
    neuroticism: float  # névrosisme

    def __init__(self, openness: Optional[float] = None,
                 conscientiousness: Optional[float] = None,
                 extraversion: Optional[float] = None,
                 agreeableness: Optional[float] = None,
                 neuroticism: Optional[float] = None):
        """Initialise la personnalité avec les valeurs données ou aléatoires."""
        self.openness = self._initialize_trait(openness)
        self.conscientiousness = self._initialize_trait(conscientiousness)
        self.extraversion = self._initialize_trait(extraversion)
        self.agreeableness = self._initialize_trait(agreeableness)
        self.neuroticism = self._initialize_trait(neuroticism)

    @staticmethod
    def _initialize_trait(value: Optional[float]) -> float:
        if value is not None:
            return max(-1.0, min(1.0, value))
        return random() * 2 - 1  # Valeur aléatoire entre -1 et 1

    def __repr__(self) -> str:
        return (f"Personality(openness={self.openness:.2f}, "
                f"conscientiousness={self.conscientiousness:.2f}, "
                f"extraversion={self.extraversion:.2f}, "
                f"agreeableness={self.agreeableness:.2f}, "
                f"neuroticism={self.neuroticism:.2f})")

    def __str__(self):
        return self.__repr__()
