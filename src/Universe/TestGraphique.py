import tkinter as tk

from Graph import Graph
from GraphDraw import GraphDraw
from ..Characters.Emotions import Emotions
from ..Characters.Personality import Personality
from ..Relationships.TypeRelationship import newRelatioship_Lovely, newRelatioship_Unfriendly
import sys
import os


if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))
src_root = os.path.dirname(base_path)
if src_root not in sys.path:
    sys.path.append(src_root)
print(f"Base path: {base_path}")
print(f"Python path: {sys.path}")


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
