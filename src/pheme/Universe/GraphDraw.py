import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.patches as mpatches
import math

from Graph import Graph

class GraphDraw :
    """
    Classe de d'interface utilisateur graphique pour le graphe de relation
    """
    def __init__(self, master, graph: Graph):
        """
        Args:
            master: Fenêtre parent (Pour Tkinter)
        """
        self.master = master
        self.master.title("Editeur")
        
        self.graph = graph
        self.selectedCharacter = None
        self.selectedRelationship = None
    
        self.setupUserInterface()

    def setupUserInterface(self):
        mainFrame = ttk.Frame(self.master).pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        controlFrame = ttk.Frame(mainFrame, width=200)
        controlFrame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        controlFrame.pack_propagate(False)

        graphFrame = ttk.Frame(mainFrame).pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setupControl(controlFrame)
        self.setupGraph(graphFrame)

    def setupControl(self, frame):
        ttk.Label(frame, text="Graphe de Relation", font=('Arial',12,'bold')).pack(pady=10)
        ttk.Button(frame, text="+ Character", command=self.addCharacterAsNode).pack(fill=tk.X, pady=5)
        ttk.Button(frame, text="+ Relationship", command=self.addRelationshipAsEdge).pack(fill=tk.X, pady=5)
        ttk.Button(frame, text="Delete", command=self.delecteSelected).pack(fill=tk.X, pady=10)
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(frame, text="Name", font=('Arial',10,'bold')).pack(anchor=tk.W)
        self.name = tk.Text(frame, height=15, width=25).pack(fill=tk.BOTH, expand=True, pady=5)
        ttk.Button(frame, text="Refresh Graph", command=self.drawGraph).pack(fill=tk.X, pady=5)
    
    def delecteSelected(self):
        if self.selectedRelationship != None :
            self.graph.removeRelationship(self.selectedRelationship)
        elif self.selectedCharacter != None :
            self.graph.removeCharacter(self.selectedCharacter)

    def setupGraph(self, frame):
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect('button_press_event', self.onClick)

        self.drawGraph()

    def addCharacterAsNode(self):
        

    def drawGraph(self):
        self.ax.clear()

        if not self.graph.listCharacter:
            self.ax.text(0.5, 0.5, "Aucun personnage dans l'univers", ha='center', va='center', transform=self.ax.transAxes)
            self.canvas.draw()
            return

        pos = nx.spring_layout(self.graph, k=3, iterations=50)
        
        nodeColor = ['red' if character == self.selectedCharacter else 'skyblue' for character in self.graph.listCharacter]
        nx.draw_networkx_nodes(self.graph, pos, node_color=nodeColor, node_size=500, ax=self.ax)
        nx.draw_networkx_nodes(self.graph, pos, ax=self.ax)

        linkColor = ['red' if relationship == self.selectedRelationship else 'black' for relationship in self.graph.listRelationship]
        nx.draw_networkx_edges(self.graph, pos, edge_color=linkColor, arrows=True, arrowstyle=20, ax=self.ax)
        
        self.ax.set_axis_off()
        self.canvas.draw()
    
    def onClick(self, event):
        if event.inaxes != self.ax:
            return
        
        clickNode = self.findNode(self, event.xdata, event.ydata)
        clickEdge = self.findEdge(self, event.xdata, event.ydata)

        if clickNode :
            self.selectedRelationship = None
            self.selectedCharacter = clickNode
        elif clickEdge :
            self.selectedRelationship = clickEdge
            self.selectedCharacter = None
        else :
            self.selectedRelationship = None
            self.selectedCharacter = None
        
        self.drawGraph()

    def findNode(self, x, y):
        for node, (node_x, node_y) in self.node_positions.items():
            distance = math.sqrt((node_x - x)**2 + (node_y - y)**2)
            if distance < 0.5:  # Rayon du nœud
                return node
        return None

    def findEdge(self, x, y):
        for edge in self.graph.edges:
            if edge.source in self.node_positions and edge.target in self.node_positions:
                x1, y1 = self.node_positions[edge.source]
                x2, y2 = self.node_positions[edge.target]
                
                num = abs((y2-y1)*x - (x2-x1)*y + x2*y1 - y2*x1)
                den = math.sqrt((y2-y1)**2 + (x2-x1)**2)
                distance = num / den if den != 0 else float('inf')

                if distance < 0.3:  # Seuil de détection
                    return (edge.source, edge.target)
        return None


