import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk

from Characters.Character import Character
from Characters.Emotions import Emotions
from Characters.Personality import Personality
from Relationships.Relationship import Relationship
from Relationships.TypeRelationship import TypeRelationship
from Relationships.TypeRelationship import newRelatioship_Professionally as Professionally
from Graph import Graph
from GraphDraw import GraphDraw

if __name__ == "__main__":

    newgraph = Graph()

    #newgraph.addNode("Alice", Personality(agreeableness=0.8, extraversion=0.5), Emotions(happiness=0.8, fear=0.2))
    #newgraph.addNode("Jacky", Personality(agreeableness=0.8, extraversion=0.5), Emotions(happiness=0.8, fear=0.2))
    #newgraph.addEdge("Peter", "Jacky", Professionally())

    root = tk.Tk()
    root.geometry("1200x800")
    app = GraphDraw(root, newgraph)
    root.mainloop()