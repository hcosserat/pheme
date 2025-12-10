import numpy as np

from .TypeRelationship import TypeRelationship
from ..Characters.Character import Character


class Relationship:
    """Représente une relation entre deux characters."""

    def __init__(self, source: Character, target: Character, typeRelationship: TypeRelationship,
                 informational_distance: int = 1):
        """
        Args:
            source: Character qui émet la relation
            target: Character qui reçoit la relation
            typeRelationship: Type de relation
            informational_distance: Temps en ticks pour qu'une info traverse cette relation
        """
        self.source = source
        self.target = target
        self.typeRelationship = typeRelationship
        self.informational_distance = max(1, int(informational_distance))  # Minimum 1 tick
        self.intensity = typeRelationship.getIntensity()
        self.confidence = self.newConfidence()

    def newConfidence(self):
        """Calcule la confiance basée sur engagement et passion."""

        baseConfidence = (self.typeRelationship.privacy + self.typeRelationship.commitment) / 2

        if baseConfidence < 0:
            confidence = max(0, 20 + (baseConfidence * 20))  # 0-20% pour relations négatives
        else:
            confidence = 20 + (baseConfidence * 80)  # 20-100% pour relations positives

        return max(0, min(100, confidence))

    def updateRelationship(self, newPrivacy=None, newCommitment=None, newPassion=None):
        """Met à jour la relation (intimité, engagement et passion)."""

    def asArray(self):
        return np.array([
            self.typeRelationship.privacy,
            self.typeRelationship.commitment,
            self.typeRelationship.passion
        ])
