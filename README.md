# Phēmē

Le système Phēmē est un ensemble d'algorithmes d'intelligence artificielle permettant de mettre en place des relations
sociales entre des personnages joueurs ou non-joueurs de jeux d'aventure, d'action ouvert, solos ou multi-joueurs.
Ce systeme donne une ame aux personnages en leur attribuant une personnalite,des emotions et un lien avec les autres
personnages
en fonction de leurs proximités relationnelles et geographique.

## Installation

Assurez-vous d'avoir Python 3.10+ installé sur votre système.

## Utilisation

### Lancer l'interface graphique

Pour visualiser graphiquement les relations entre personnages, vous pouvez lancer l'interface graphique de plusieurs
façons :

```bash
python tests/TestGraphique.py
```

L'interface graphique affichera un exemple avec trois personnages (Alice, Jacky, Peter) et leurs relations dans une
fenêtre tkinter de 1200x800 pixels.

### Utiliser le module dans votre code

Vous pouvez importer et utiliser les composants de Phēmē dans votre propre projet :

```python
from pheme import Character, Emotions, Personality, Relationship
from pheme import newRelatioship_Lovely, newRelatioship_Unfriendly
from pheme.Universe.Graph import Graph

# Créer un graphe de relations
graph = Graph()

# Ajouter des personnages avec leur personnalité et émotions
graph.addNode("Alice",
              Personality(agreeableness=0.2, extraversion=0.1),
              Emotions(happiness=0.2, fear=0.8))

graph.addNode("Bob",
              Personality(agreeableness=0.8, extraversion=0.5),
              Emotions(happiness=0.8, fear=0.1))

# Créer des relations entre personnages
graph.addEdge("Alice", "Bob", newRelatioship_Lovely())
graph.addEdge("Bob", "Alice", newRelatioship_Lovely())
```

## Composants principaux

- **Characters** : Gestion des personnages, leurs personnalités et émotions
- **Relationships** : Système de relations entre personnages
- **Universe** : Graphe de relations et visualisation
- **Interactions** : Moteur d'interactions entre personnages

