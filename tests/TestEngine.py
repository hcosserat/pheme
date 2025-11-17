from src.pheme.Universe.Graph import Graph
from src.pheme.Characters.Personality import Personality
from src.pheme.Characters.Emotions import Emotions
from src.pheme.Relationships.TypeRelationship import TypeRelationship
from src.pheme.Interactions.Interaction import Interaction
from src.pheme.Interactions.InteractionsEngine import InteractionsEngine


def test_engine():
    """Test complet de l'Engine avec plusieurs personnages et interactions."""

    print("=" * 80)
    print("TEST DE L'ENGINE DU SYSTÈME DE RELATIONS SOCIALES")
    print("=" * 80)

    # Création du graphe
    graph = Graph()

    # Création des personnages
    print("\n1. CRÉATION DES PERSONNAGES")
    print("-" * 80)

    # Alice : extravertie, agréable, stable émotionnellement
    alice_personality = Personality(
        openness=0.6,
        conscientiousness=0.4,
        extraversion=0.7,
        agreeableness=0.8,
        neuroticism=-0.5
    )
    alice_emotions = Emotions(happiness=0.6, sadness=0.1, anger=0.1, fear=0.1, surprise=0.3, disgust=0.1)
    graph.addNode("Alice", alice_personality, alice_emotions)

    # Bob : introverti, consciencieux, un peu anxieux
    bob_personality = Personality(
        openness=0.3,
        conscientiousness=0.8,
        extraversion=-0.4,
        agreeableness=0.5,
        neuroticism=0.4
    )
    bob_emotions = Emotions(happiness=0.4, sadness=0.2, anger=0.1, fear=0.3, surprise=0.2, disgust=0.1)
    graph.addNode("Bob", bob_personality, bob_emotions)

    # Charlie : ouvert, peu agréable, passionné
    charlie_personality = Personality(
        openness=0.8,
        conscientiousness=0.2,
        extraversion=0.5,
        agreeableness=-0.3,
        neuroticism=0.2
    )
    charlie_emotions = Emotions(happiness=0.5, sadness=0.2, anger=0.3, fear=0.1, surprise=0.4, disgust=0.2)
    graph.addNode("Charlie", charlie_personality, charlie_emotions)

    print(f"Alice: {graph.getNode('Alice')}")
    print(f"Bob: {graph.getNode('Bob')}")
    print(f"Charlie: {graph.getNode('Charlie')}")

    # Création des relations initiales
    print("\n2. CRÉATION DES RELATIONS INITIALES")
    print("-" * 80)

    # Alice et Bob sont amis
    alice_bob_relation = TypeRelationship(privacy=0.6, commitment=0.5, passion=0.2)
    graph.addEdge("Alice", "Bob", alice_bob_relation)
    print(f"Alice → Bob: {alice_bob_relation}")

    # Bob connaît Alice
    bob_alice_relation = TypeRelationship(privacy=0.5, commitment=0.4, passion=0.1)
    graph.addEdge("Bob", "Alice", bob_alice_relation)
    print(f"Bob → Alice: {bob_alice_relation}")

    # Alice connaît Charlie
    alice_charlie_relation = TypeRelationship(privacy=0.3, commitment=0.2, passion=0.1)
    graph.addEdge("Alice", "Charlie", alice_charlie_relation)
    print(f"Alice → Charlie: {alice_charlie_relation}")

    # Charlie connaît Alice
    charlie_alice_relation = TypeRelationship(privacy=0.2, commitment=0.2, passion=0.0)
    graph.addEdge("Charlie", "Alice", charlie_alice_relation)
    print(f"Charlie → Alice: {charlie_alice_relation}")

    # Création de l'Engine
    engine = InteractionsEngine(graph)

    # Test 1 : Interaction directe entre Alice et Bob
    print("\n3. TEST 1 : INTERACTION DIRECTE POSITIVE (Alice aide Bob)")
    print("-" * 80)

    alice = graph.getNode("Alice")
    bob = graph.getNode("Bob")
    charlie = graph.getNode("Charlie")

    interaction1 = Interaction(
        actor=alice,
        target=bob,
        description="Alice aide Bob avec son travail",
        timestamp=1.0,
        agency=0.4,           # Alice prend l'initiative
        communion=0.8,        # Action très prosociale
        intensity=0.5,        # Intensité moyenne
        physical_contact=0.1, # Peu de contact physique
        valence=0.9           # Très positif pour Bob
    )

    print(f"\nInteraction: {interaction1}")
    print(f"\nAVANT:")
    print(f"  Alice émotions: {alice.emotions}")
    print(f"  Bob émotions: {bob.emotions}")
    print(f"  Alice → Bob: {graph.getEdge('Alice', 'Bob').typeRelationship}")
    print(f"  Bob → Alice: {graph.getEdge('Bob', 'Alice').typeRelationship}")

    # Alice et Bob traitent l'interaction directement
    engine.processInteractionForCharacter(alice, interaction1)
    engine.processInteractionForCharacter(bob, interaction1)

    print(f"\nAPRÈS:")
    print(f"  Alice émotions: {alice.emotions}")
    print(f"  Bob émotions: {bob.emotions}")
    print(f"  Alice → Bob: {graph.getEdge('Alice', 'Bob').typeRelationship}")
    print(f"  Bob → Alice: {graph.getEdge('Bob', 'Alice').typeRelationship}")

    # Test 2 : Interaction indirecte (Charlie observe)
    print("\n4. TEST 2 : INTERACTION INDIRECTE (Charlie observe)")
    print("-" * 80)

    print(f"\nCharlie connaît Alice, donc il est affecté indirectement")
    print(f"\nAVANT:")
    print(f"  Charlie émotions: {charlie.emotions}")
    print(f"  Charlie → Alice: {graph.getEdge('Charlie', 'Alice').typeRelationship}")

    # Charlie traite l'interaction indirectement (il connaît Alice)
    engine.processInteractionForCharacter(charlie, interaction1)

    print(f"\nAPRÈS:")
    print(f"  Charlie émotions: {charlie.emotions}")
    print(f"  Charlie → Alice: {graph.getEdge('Charlie', 'Alice').typeRelationship}")

    # Test 3 : Diffusion d'information
    print("\n5. TEST 3 : DIFFUSION D'INFORMATION")
    print("-" * 80)

    # Créer une nouvelle interaction entre Bob et Charlie
    interaction2 = Interaction(
        actor=bob,
        target=charlie,
        description="Bob critique le travail de Charlie",
        timestamp=2.0,
        agency=0.3,
        communion=-0.6,       # Action antisociale
        intensity=0.6,
        physical_contact=0.0,
        valence=-0.7          # Négatif pour Charlie
    )

    print(f"\nNouvelle interaction: {interaction2}")
    print(f"Bob diffuse cette information à ses voisins...")

    # Réinitialiser les known_interactions pour le test
    alice.knownInteractions = set()
    bob.knownInteractions = set()
    charlie.knownInteractions = set()

    print(f"\nAVANT la diffusion:")
    print(f"  Alice connaît {len(alice.knownInteractions)} interaction(s)")
    print(f"  Bob connaît {len(bob.knownInteractions)} interaction(s)")
    print(f"  Charlie connaît {len(charlie.knownInteractions)} interaction(s)")

    # Bob diffuse l'information
    engine.diffuseInteraction(bob, interaction2)

    print(f"\nAPRÈS la diffusion:")
    print(f"  Alice connaît {len(alice.knownInteractions)} interaction(s)")
    print(f"  Bob connaît {len(bob.knownInteractions)} interaction(s)")
    print(f"  Charlie connaît {len(charlie.knownInteractions)} interaction(s)")

    # Test 4 : Interaction négative
    print("\n6. TEST 4 : INTERACTION NÉGATIVE (Charlie attaque Alice)")
    print("-" * 80)

    interaction3 = Interaction(
        actor=charlie,
        target=alice,
        description="Charlie insulte Alice publiquement",
        timestamp=3.0,
        agency=0.7,           # Charlie est dominant
        communion=-0.9,       # Très antisocial
        intensity=0.8,        # Haute intensité
        physical_contact=0.0,
        valence=-0.9          # Très négatif pour Alice
    )

    print(f"\nInteraction: {interaction3}")
    print(f"\nAVANT:")
    print(f"  Alice émotions: {alice.emotions}")
    print(f"  Charlie émotions: {charlie.emotions}")
    print(f"  Alice → Charlie: {graph.getEdge('Alice', 'Charlie').typeRelationship}")
    print(f"  Charlie → Alice: {graph.getEdge('Charlie', 'Alice').typeRelationship}")

    engine.processInteractionForCharacter(alice, interaction3)
    engine.processInteractionForCharacter(charlie, interaction3)

    print(f"\nAPRÈS:")
    print(f"  Alice émotions: {alice.emotions}")
    print(f"  Charlie émotions: {charlie.emotions}")
    print(f"  Alice → Charlie: {graph.getEdge('Alice', 'Charlie').typeRelationship}")
    print(f"  Charlie → Alice: {graph.getEdge('Charlie', 'Alice').typeRelationship}")

    print("\n" + "=" * 80)
    print("FIN DES TESTS")
    print("=" * 80)


if __name__ == "__main__":
    test_engine()

