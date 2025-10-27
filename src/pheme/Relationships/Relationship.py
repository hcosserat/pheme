from TypeRelationship import TypeRelationship

class Relationship:
    """
    Classe représentant une relation entre deux personnes
    """
    
    def __init__(self, source, target, typeRelationship: TypeRelationship):
        """
        Args:
            source: Personne qui émet la relation
            cible: Personne qui reçoit la relation  
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
            confidence = max(0, 20 + (baseConfidence * 20)) # 0-20%     pour les relations négatives
        else:
            confidence = 20 + (baseConfidence * 80)         # 20-100%   pour les relations positives
        
        return max(0, min(100, confidence))
    
    def updateRelationship(self, newPrivacy=None, newCommitment=None, newPassion=None):
        """
        Met à jour la relation (L'intimité, l'engagement et la passion)
        """
        if newPrivacy is not None:
            self.typeRelationship.privacy = max(-1.0, min(1.0, newPrivacy))
        if newCommitment is not None:
            self.typeRelationship.commitment = max(-1.0, min(1.0, newCommitment))
        if newPassion is not None:
            self.typeRelationship.passion = max(-1.0, min(1.0, newPassion))
        
        # Recalculer le nom et les valeurs dérivées
        self.typeRelationship.nom = self.typeRelationship.identifyName()
        self.intensity = self.typeRelationship.getIntensity()
        self.confidence = self.newConfidence()
    
    def __str__(self):
        return (f"Relation: {self.source} → {self.target}\n"
                f"Type: {self.typeRelationship}\n"
                f"Intensité: {self.intensity:.1f}/100\n"
                f"Confiance: {self.confidence:.1f}/100")

