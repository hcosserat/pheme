from Relationship import Relationship
from TypeRelationship import TypeRelationship
from TypeRelationship import newRelatioship_Lovely
from TypeRelationship import newRelatioship_Professionally

if __name__ == "__main__":
    # Un garçon déteste son frère
    relationship_1 = Relationship(
        source="Garçon",
        target="Frère",
        typeRelationship=TypeRelationship(privacy=-0.7, commitment=-0.5, passion=-0.8)
    )

    # Roi envers son général (relation professionnelle)
    relationship_2 = Relationship(
        source="Roi",
        target="Général",
        typeRelationship=newRelatioship_Professionally(privacy=0.2, commitment=0.8, passion=0.0)
    )

    # Relation amoureuse
    relationship_3 = Relationship(
        source="Personne A",
        target="Personne B",
        typeRelationship=newRelatioship_Lovely()
    )

    print("=== Fratrie conflictuelle ===")
    print(relationship_1)

    print("\n=== Relation professionnelle ===")
    print(relationship_2)

    print("\n=== Relation amoureuse ===")
    print(relationship_3)

    # Test de mise à jour
    print("\n=== Après amélioration de la relation fraternelle ===")
    relationship_1.updateRelationship(newPrivacy=0.3, newCommitment=0.4, newPassion=0.1)
    print(relationship_1)
