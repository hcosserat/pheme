import tkinter as tk

from .Graph import Graph
from .GraphDraw import GraphDraw
from ..Characters.Emotions import Emotions
from ..Characters.Personality import Personality
from ..Relationships.TypeRelationship import newRelatioship_Lovely, newRelatioship_Unfriendly


def main():
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
