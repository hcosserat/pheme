import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk

from Characters.Character import Character
from Characters.Emotions import Emotions
from Characters.Personality import Personality
from Relationships.Relationship import Relationship
from Relationships.TypeRelationship import TypeRelationship
from Relationships.TypeRelationship import newRelatioship_Professionally, newRelatioship_Lovely, newRelatioship_Unfriendly
from Graph import Graph
from GraphDraw import GraphDraw

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