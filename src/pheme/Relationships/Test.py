from Relationship import Relationship
from TypeRelationship import TypeRelationship
from TypeRelationship import newRelatioship_Professionally
from TypeRelationship import newRelatioship_Lovely


if __name__ == "__main__":
    # Un garçon déteste son frère
    relationship_1 = Relationship(
        source="Garçon",
        target="Frère", 
        type_relation=TypeRelationship(intimite=-0.7, engagement=-0.5, passion=-0.8)
    )
    
    # Roi envers son général (relation professionnelle)
    relationship_2 = Relationship(
        source="Roi",
        target="Général",
        type_relation=newRelatioship_Professionally(intimite=0.2, engagement=0.8, passion=0.0)
    )
    
    # Relation amoureuse
    relationship_3 = Relationship(
        source="Personne A",
        target="Personne B",
        type_relation=newRelatioship_Lovely()
    )
    
    print("=== Fratrie conflictuelle ===")
    print(relationship_1)
    
    print("\n=== Relation professionnelle ===")
    print(relationship_2)
    
    print("\n=== Relation amoureuse ===")
    print(relationship_3)
    
    # Test de mise à jour
    print("\n=== Après amélioration de la relation fraternelle ===")
    relationship_1.updateRelationship(nouvelle_intimite=0.3, nouvel_engagement=0.4, nouvelle_passion=0.1)
    print(relationship_1)