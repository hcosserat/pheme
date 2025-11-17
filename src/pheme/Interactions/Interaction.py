from random import random
from typing import Optional

import numpy as np

from ..Characters.Character import Character


class Interaction:
    """
    Classe représentant une interaction entre deux personnages.
    Une interaction est définie par un vecteur à 5 dimensions selon le modèle circomplexe interpersonnel.
    """

    # Personnages impliqués dans l'interaction
    actor: Character  # personnage qui initie l'action
    target: Character  # personnage qui reçoit l'action
    description: str  # description textuelle de l'interaction
    timestamp: float  # heure de l'interaction

    # Dimensions de l'interaction
    agency: float  # assertivité/dominance de l'acteur (-1 à +1)
    communion: float  # prosocial vs antisocial envers la cible (-1 à +1)
    intensity: float  # niveau d'énergie/activation (0 à 1)
    physical_contact: float  # contact physique vs verbal/psychologique (0 à 1)
    valence: float  # positif vs négatif pour la cible (-1 à +1)

    def __init__(self, actor: Character, target: Character, description: str, timestamp: float,
                 agency: Optional[float] = None,
                 communion: Optional[float] = None,
                 intensity: Optional[float] = None,
                 physical_contact: Optional[float] = None,
                 valence: Optional[float] = None):
        """Initialise l'interaction avec les personnages, description et valeurs données ou aléatoires."""
        self.actor = actor
        self.target = target
        self.description = description
        self.timestamp = timestamp
        self.agency = self._initialize_bipolar_trait(agency)
        self.communion = self._initialize_bipolar_trait(communion)
        self.intensity = self._initialize_unipolar_trait(intensity)
        self.physical_contact = self._initialize_unipolar_trait(physical_contact)
        self.valence = self._initialize_bipolar_trait(valence)

    @staticmethod
    def _initialize_bipolar_trait(value: Optional[float]) -> float:
        """Initialise un trait bipolaire (-1 à +1)."""
        if value is not None:
            return max(-1.0, min(1.0, value))
        return random() * 2 - 1  # Valeur aléatoire entre -1 et 1

    @staticmethod
    def _initialize_unipolar_trait(value: Optional[float]) -> float:
        """Initialise un trait unipolaire (0 à 1)."""
        if value is not None:
            return max(0.0, min(1.0, value))
        return random()  # Valeur aléatoire entre 0 et 1

    def __repr__(self) -> str:
        return (f"Interaction({self.actor.name} → {self.target.name}: '{self.description}' | "
                f"agency={self.agency:.2f}, "
                f"communion={self.communion:.2f}, "
                f"intensity={self.intensity:.2f}, "
                f"physical_contact={self.physical_contact:.2f}, "
                f"valence={self.valence:.2f})")

    def __str__(self):
        return self.__repr__()

    def asArray(self):
        return np.array([
            self.agency,
            self.communion,
            self.intensity,
            self.physical_contact,
            self.valence
        ])
