import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk

from Characters.Character import Character
from Characters.Enum import Caractere
from Characters.Personality import Personality
from Relationships.Relationship import Relationship
from Relationships.TypeRelationship import TypeRelationship
from Relationships.TypeRelationship import newRelatioship_Professionally as Professionally
from Graph import Graph
from GraphDraw import GraphDraw

if __name__ == "__main__":

    newgraph = Graph()

    p1 = Character("Peter", Caractere.CALME, Personality(neuroticism=0.9, openness=-0.9))
    p2 = Character("Jack", Caractere.AGRESSIF, Personality(neuroticism=0.7, openness=-0.3))

    newgraph.addCharacterAsNode(p1)
    newgraph.addCharacterAsNode(p2)

    r1 = Relationship(p1, p2, Professionally())

    newgraph.addRelationshipAsEdge(r1)

    root = tk.Tk()
    root.geometry("1200x800")
    app = GraphDraw(root, newgraph)
    root.mainloop()