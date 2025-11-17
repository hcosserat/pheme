import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Characters.Character import Character
from Characters.Enum import Caractere
from Characters.Personality import Personality
from Relationships.Relationship import Relationship
from Relationships.TypeRelationship import TypeRelationship
from Relationships.TypeRelationship import newRelatioship_Professionally as Professionally

if __name__ == "__main__":
    Garçon = Character("Peter",
                       Caractere.CALME,
                       Personality(neuroticism=0.9, openness=-0.9))
    Frere = Character("Jack",
                      Caractere.AGRESSIF, 
                      Personality(neuroticism=0.7, openness=-0.3))
    # Un garçon déteste son frère
    relationship_1 = Relationship(
        source= Garçon,
        target= Frere, 
        typeRelationship= TypeRelationship(privacy=-0.7, commitment=-0.5, passion=-0.8)
    )

    Roi = Character("Francois I",
                    Caractere.CALME,
                    Personality(neuroticism=0.7, openness=-0.3))
    General = Character("Napoleon",
                        Caractere.COURAGEUX, 
                        Personality(neuroticism=0.8, openness=0.5))
    # Roi envers son général (relation professionnelle)
    relationship_2 = Relationship(
        source=Roi,
        target=General,
        typeRelationship=Professionally()
    )
    
    print("=== Fratrie conflictuelle ===")
    print(relationship_1)
    
    print("\n=== Relation professionnelle ===")
    print(relationship_2)
    
    # Test de mise à jour
    print("\n=== Après amélioration de la relation fraternelle ===")
    relationship_1.updateRelationship(newPrivacy=0.3, newCommitment=0.4, newPassion=0.1)
    print(relationship_1)