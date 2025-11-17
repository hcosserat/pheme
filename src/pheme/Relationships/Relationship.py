import os
import sys

import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .TypeRelationship import TypeRelationship
from Characters.Character import Character


class Relationship:
    """
    Classe représentant une relation entre deux personnes
    """

    def __init__(self, source: Character, target: Character, typeRelationship: TypeRelationship):
        """
        Args:
            source (Character): Personne qui émet la relation
            target (Character): Personne qui reçoit la relation
            typeRelationship (TypeRelationship): Type de relation
        """
        self.source = source
        self.target = target
        self.typeRelationship = typeRelationship
        self.intensity = typeRelationship.getIntensity()
        self.confidence = self.newConfidence()

    def newConfidence(self):
        """
        Calcule la confiance basée sur l'engagement et la passion
        """

        baseConfidence = (self.typeRelationship.privacy + self.typeRelationship.commitment) / 2

        if baseConfidence < 0:
            confidence = max(0, 20 + (baseConfidence * 20))  # 0-20%     pour les relations négatives
        else:
            confidence = 20 + (baseConfidence * 80)  # 20-100%   pour les relations positives

        return max(0, min(100, confidence))

    def updateRelationship(self, newPrivacy=None, newCommitment=None, newPassion=None):
        """
        Met à jour la relation (L'intimité, l'engagement et la passion)
        """

    def asArray(self):
        return np.array([
            self.typeRelationship.privacy,
            self.typeRelationship.commitment,
            self.typeRelationship.passion
        ])
