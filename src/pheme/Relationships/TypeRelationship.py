class TypeRelationship:
    """
    Classe pour définir le type de relation basé sur la théorie de l'amour de Sternberg (L'intimité, l'engagement et la passion)
    """

    def __init__(self, privacy, commitment, passion):
        """
        Args:
            privacy (float): Niveau d'intimité (-1 à 1)
            commitment (float): Niveau d'engagement (-1 à 1) 
            passion (float): Niveau de passion (-1 à 1)
        """
        self.privacy = max(-1.0, min(1.0, privacy))
        self.commitment = max(-1.0, min(1.0, commitment))
        self.passion = max(-1.0, min(1.0, passion))
        self.nom = self.identifyName()

    def identifyName(self):
        """
        Détermine le nom du type de relation basé sur l'intimité, l'engagement et la passion
        """
        # Calcul de la tendance globale
        average = (self.privacy + self.commitment + self.passion) / 3

        if average > 0.6:
            return "Amour"
        elif average > 0.3:
            if self.commitment > self.passion:
                return "Ami proche"
            else:
                return "Amour naissant"
        elif average > 0.1:
            if self.commitment > 0.2:
                return "Collègue proche"
            else:
                return "Connaissance"
        elif average > -0.1:
            return "Neutre"
        elif average > -0.3:
            if self.passion < -0.2:
                return "Rivalité"
            else:
                return "Désaccord"
        elif average > -0.6:
            return "Hostilité"
        else:
            return "Haine"

    def getIntensity(self):
        """
        Calcule l'intensité globale basée sur les valeurs absolues
        """
        return (abs(self.privacy) + abs(self.commitment) + abs(self.passion)) / 3.0

    def update(self, change):
        self.privacy = max(-1.0, min(1.0, self.surprise - change * 0.1))
        self.commitment = max(-1.0, min(1.0, self.surprise - change * 0.15))
        self.passion = max(-1.0, min(1.0, self.surprise - change * 0.1))

        self.nom = self.identifyName()

    def getAverage(self):
        return (self.privacy + self.commitment + self.passion) / 3.0

    def __str__(self):
        return (f"{self.nom} (I:{self.privacy:.2f}, E:{self.commitment:.2f}, P:{self.passion:.2f})")


# Fast conception type
def newRelatioship_Lovely(privacy=0.8, commitment=0.7, passion=0.9):
    return TypeRelationship(privacy, commitment, passion)


def newRelatioship_Friendly(privacy=0.6, commitment=0.5, passion=0.1):
    return TypeRelationship(privacy, commitment, passion)


def newRelatioship_Family(privacy=0.7, commitment=0.8, passion=0.0):
    return TypeRelationship(privacy, commitment, passion)


def newRelatioship_Professionally(privacy=0.1, commitment=0.6, passion=0.0):
    return TypeRelationship(privacy, commitment, passion)


def newRelatioship_Unfriendly(privacy=-0.5, commitment=-0.3, passion=-0.6):
    return TypeRelationship(privacy, commitment, passion)
