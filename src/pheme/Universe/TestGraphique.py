import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import tkinter as tk

from pheme.Universe.Graph import Graph
from pheme.Universe.GraphDraw import GraphDraw
from pheme.Characters.Emotions import Emotions
from pheme.Characters.Personality import Personality
from pheme.Relationships.TypeRelationship import newRelatioship_Lovely, newRelatioship_Unfriendly

if __name__ == "__main__":

    newgraph = Graph()

    newgraph.addNode("Alice", Personality(agreeableness=0.2, extraversion=0.1), Emotions(happiness=0.2, fear=0.8))
    newgraph.addNode("Jacky", Personality(agreeableness=0.8, extraversion=0.5), Emotions(happiness=0.8, fear=0.1))
    newgraph.addNode("Peter", Personality(agreeableness=0.6, extraversion=0.5), Emotions(happiness=0.8, fear=0.1))
    newgraph.addEdge("Peter", "Jacky", newRelatioship_Lovely())
    newgraph.addEdge("Jacky", "Peter", newRelatioship_Lovely())
    newgraph.addEdge("Alice", "Jacky", newRelatioship_Unfriendly())
    newgraph.addEdge("Jacky", "Alice", newRelatioship_Unfriendly())

    root = tk.Tk()
    root.geometry("1200x800")
    app = GraphDraw(root, newgraph)
    root.mainloop()