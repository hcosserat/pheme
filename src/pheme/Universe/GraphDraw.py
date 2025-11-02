import networkx as nx
import tkinter as tk
from tkinter import ttk, messagebox

import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Characters.Enum import Caractere
from Characters.Personality import Personality
from Graph import Graph

class GraphDraw :
    """
    Classe de d'interface utilisateur graphique pour le graphe de relation
    """
    def __init__(self, master, graph: Graph):
        self.master = master
        self.master.title("Editeur de Graphe de Relations")
        
        self.graph = graph
        self.selectedCharacter = None
        self.selectedRelationship = None
        self.editMode = None

        self.setupUserInterface()

    def setupUserInterface(self):
        mainFrame = ttk.Frame(self.master)
        mainFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        controlFrame = ttk.Frame(mainFrame, width=400)
        controlFrame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        controlFrame.pack_propagate(False)

        graphFrame = ttk.Frame(mainFrame)
        graphFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setup_ControlPanel(controlFrame)
        self.setupGraph(graphFrame)

    def setup_ControlPanel(self, frame):

        self.setup_ControlPanel_Character(frame)

        self.setup_ControlPanel_Relationship(frame)

        frameControlPanel = ttk.LabelFrame(frame, text="Control Panel", padding=10)
        frameControlPanel.pack(fill=tk.X, pady=5)
        
        ttk.Button(frameControlPanel,
                   text="Supprimer Sélection",
                   command=self.deleteSelected
                   ).pack(fill=tk.X, pady=2)
        ttk.Button(frameControlPanel,
                   text="Refresh Graph",
                   command=self.drawGraph
                   ).pack(fill=tk.X, pady=2)
        ttk.Button(frameControlPanel,
                   text="Cancel MAJ",
                   command=self.cancelEdit
                   ).pack(fill=tk.X, pady=2)

        frameInfo = ttk.LabelFrame(frame,
                                   text="Info",
                                   padding=10)
        frameInfo.pack(fill=tk.BOTH, expand=True, pady=5)
        self.infoText = tk.Text(frameInfo, height=15, width=30)
        self.infoText.pack(fill=tk.BOTH, expand=True)

    def setup_ControlPanel_Character(self, frame):
        self.frameCharacter = ttk.LabelFrame(frame,
                                             text="Personnage",
                                             padding=10)
        self.frameCharacter.pack(fill=tk.X, pady=5)
        ttk.Label(self.frameCharacter,
                  text="Nom"
                  ).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.varName = ttk.Entry(self.frameCharacter, width=20)
        self.varName.grid(row=0, column=1, sticky=tk.EW, pady=2, padx=(5, 0))
        ttk.Label(self.frameCharacter,
                  text="Caractère:"
                  ).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.varPersonality  = tk.StringVar(value="Calme")
        self.comboPersonality = ttk.Combobox(self.frameCharacter, textvariable=self.varPersonality, 
                                             values=["Joyeux", "Enervé"], 
                                             state="readonly", width=17)
        self.comboPersonality.grid(row=1, column=1, sticky=tk.EW, pady=2, padx=(5, 0))
        

        self.frameCharacter_btnCharacter = ttk.Frame(self.frameCharacter)
        self.frameCharacter_btnCharacter.grid(rows=2, column=0, columnspan=2, sticky=tk.EW, pady=5)
        self.btnCharacter_add = ttk.Button(self.frameCharacter_btnCharacter,
                                              text="New Perso",
                                              command=self.createCharacter)
        self.btnCharacter_add.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))
        self.btnCharacter_update = ttk.Button(self.frameCharacter_btnCharacter,
                                              text="MAJ Perso",
                                              command=self.updateCharacter,
                                              state="disabled")
        self.btnCharacter_update.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        self.frameCharacter.columnconfigure(1, weight=1)

    def setup_ControlPanel_Relationship(self, frame):
        self.frameRelationship = ttk.LabelFrame(frame,
                                                text="Relation",
                                                padding=10)
        self.frameRelationship.pack(fill=tk.X, pady=5)
        ttk.Label(self.frameRelationship,
                  text="Source :"
                  ).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.varSource = tk.StringVar()
        self.comboSource = ttk.Combobox(self.frameRelationship, textvariable=self.varSource,
                                        width=17)
        self.comboSource.grid(row=1, column=1, sticky=tk.EW, pady=2, padx=(5, 0))
        ttk.Label(self.frameRelationship,
                  text="Target :"
                  ).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.varTarget = tk.StringVar()
        self.comboTarget = ttk.Combobox(self.frameRelationship, textvariable=self.varTarget,
                                        width=17)
        self.comboTarget.grid(row=1, column=1, sticky=tk.EW, pady=2, padx=(5, 0))
        ttk.Label(self.frameRelationship,
                  text="Type :"
                  ).grid(row=2, column=0, sticky=tk.W, pady=2)
        self.varType = tk.Entry(self.frameRelationship, width=20)
        self.varType.grid(row=2, column=1, sticky=tk.EW, pady=2, padx=(5, 0))
        
        self.frameRelationship_btnRelationship = ttk.Frame(self.frameRelationship)
        self.frameRelationship_btnRelationship.grid(rows=2, column=0, columnspan=2, sticky=tk.EW, pady=5)
        self.btnRelationship_add = ttk.Button(self.frameRelationship_btnRelationship,
                                              text="New Relation",
                                              command=self.createRelationship)
        self.btnRelationship_add.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))
        self.btnRelationship_update = ttk.Button(self.frameRelationship_btnRelationship,
                                              text="MAJ Relation",
                                              command=self.updateRelationship,
                                              state="disabled")
        self.btnRelationship_update.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        self.frameRelationship.columnconfigure(1, weight=1)

        self.updateCharacterCombos()

    def updateCharacterCombos(self):
        characters = self.graph.getNodeNames()
        self.comboSource['values'] = characters
        self.comboTarget['values'] = characters

    def deleteSelected(self):
        if self.selectedRelationship:
            source, target = self.selectedRelationship
            self.graph.removeEdge(source, target)
            self.selectedRelationship = None
            self.showInfo(f"Relation entre {source} et {target} supprimée")
        elif self.selectedCharacter:
            self.graph.removeNode(self.selectedCharacter)
            self.selectedCharacter = None
            self.showInfo("Personnage supprimé")
        else:
            self.showInfo("Aucun élément sélectionné")

        self.updateCharacterCombos()
        self.clearForm()
        self.updateBtn()
        self.drawGraph()

    def cancelEdit(self):
        self.editMode = None
        self.selectedCharacter = None
        self.selectedRelationship = None
        self.clearForm()
        self.drawGraph()
        self.showInfo("MAJ annule")
    
    def clearForm(self):
        self.varName.delete(0, tk.END)
        self.varPersonality.set("Calme")
        self.varSource.set('')
        self.varTarget.set('')
        self.varType.delete(0, tk.END)

    def updateBtn(self):
        if self.selectedCharacter and self.editMode == 'node':
            self.btnCharacter_add.config(state="disable")
            self.btnCharacter_update.config(state="normal")
        else:
            self.btnCharacter_add.config(state="normal")
            self.btnCharacter_update.config(state="disable")
        
        if self.selectedRelationship and self.editMode == 'node':
            self.btnRelationship_add.config(state="disable")
            self.btnRelationship_update.config(state="normal")
        else:
            self.btnRelationship_add.config(state="normal")
            self.btnRelationship_update.config(state="disable")

    def setupGraph(self, frame):
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect('button_press_event', self.onClick)

        self.drawGraph()

    def createCharacter(self):
        name = self.varName.get().strip()
        if not name:
            self.showInfo("Err0r: Pas de nom de personnage")
            return
        
        if self.graph.getNode(name):
            self.showInfo(f"Error: Personnage '{name}' existe")
            return
        
        try:
            personality = getattr(Caractere, self.varPersonality.get())
        except AttributeError:
            personality = Caractere.CALME
        
        personalityV2 = Personality(0, 0, 0, 0, 0)

        self.graph.addNode(name, personality, personalityV2)
        self.clearForm()
        self.updateCharacterCombos()
        self.drawGraph()
        self.showInfo(f"Personnage '{name}' build success")

    def updateCharacter(self):
        if not self.selectedCharacter:
            self.showInfo("€rreur: Pas de personnage select")
            return
    
        name = self.varName.get.strip()
        if not name:
            self.showInfo("Err0r: Pas de nom de personnage")
            return
        
        try :
            personality = getattr(Caractere, self.varPersonality.get())
        except AttributeError:
            personality = Caractere.CALME
        
        if self.graph.getNode(name):
            self.showInfo(f"Error: Personnage '{name}' existe")
            return

        if not self.graph.getNode(self.selectedCharacter):
            self.showInfo("ERror: Pesonnage MAJ introuvable")
            return
        
        personalityV2 = Personality(0, 0, 0, 0, 0)

        self.graph.updateNode(self.selectedCharacter, name, personality, personalityV2)
        self.selectedCharacter = name
        self.editMode = None
        self.clearForm()
        self.updateCharacterCombos()
        self.updateBtn()
        self.drawGraph()
        self.showInfo(f"Personnage {name} MAJ success")

    def createRelationship(self):
        if len(self.graph.listNode) < 2:
            self.showInfo("Erreur: Il faut au moins 2 personnages")
            return
        
        source = self.varSource.get()
        target = self.varTarget.get()
        typeRelationship = self.varType.get().strip()
        
        if not source or not target:
            self.showInfo("Errer: Select correct personnage source et cible")
            return
            
        if source == target:
            self.showInfo("ErReur: Select differents personnages")
            return
            
        if not typeRelationship:
            self.showInfo("Errevr: Il faut un type de relation")
            return

        if self.graph.getRelationship(source, target):
            self.showInfo(f"ErrEur: Relation existe entre {source} et {target}")
            return

        self.graph.addRelationship(source, target, typeRelationship)
        self.clearForm()
        self.drawGraph()
        self.showInfo(f"Relation '{typeRelationship}' entre '{source}' et '{target}'")

    def updateRelationship(self):
        if not self.selectedRelationship:
            self.showInfo("€reur: Relation pas Select")
            return
    
        source, target = self.selectedRelationship
        typeRelationship = self.varType.get().strip()
        if not typeRelationship:
            self.showInfo("Errevr: Il faut un type de relation")
            return
        
        if not self.graph.getEdge(source, target):
            self.showInfo("Erreer: Relation introuvable")
            return

        self.graph.updateEdge(source, target, typeRelationship)

        self.selectedRelationship = None
        for edge in self.graph.toNetworkx().edges():
            if edge == [source, target]:
                self.selectedRelationship = edge
                break
        self.editMode = None
        self.clearForm()
        self.updateBtn()
        self.drawGraph()
        self.showInfo(f"Relation '{typeRelationship}' entre '{source}' et '{target}'")

    def drawGraph(self):
        self.ax.clear()

        if not self.graph.listNode:
            self.ax.text(0.5, 0.5, "Y a rien dans l'univers",
                         ha='center', va='center', transform=self.ax.transAxes)
            self.canvas.draw()
            return

        self.pos = nx.spring_layout(self.graph.toNetworkx(), k=3, iterations=50)
        
        node_colors = []
        for node in self.graph.toNetworkx().nodes():
            if node == self.selectedCharacter:
                node_colors.append('red')
            else:
                node_colors.append('skyblue')
        nx.draw_networkx_nodes(self.graph.toNetworkx(), self.pos,
                               node_color=node_colors,
                               node_size=500, ax=self.ax)
        nx.draw_networkx_labels(self.graph.toNetworkx(), self.pos, ax=self.ax)

        edge_colors = []
        edge_widths = []
        for edge in self.graph.toNetworkx().edges():
            if edge == self.selectedRelationship:
                edge_colors.append('red')
                edge_widths.append(3)
            else:
                edge_colors.append('black')
                edge_widths.append(1)
        nx.draw_networkx_edges(self.graph.toNetworkx(), self.pos,
                               edge_color=edge_colors,
                               width=edge_widths,
                               arrows=True, arrowsize=20, ax=self.ax)
        
        self.ax.set_axis_off()
        self.canvas.draw()
    
    def onClick(self, event):
        if event.inaxes != self.ax:
            return
        
        clickNode = self.findNode(event.xdata, event.ydata)
        clickEdge = self.findEdge(event.xdata, event.ydata)

        if clickNode:
            self.onClick_Node(clickNode)
        elif clickEdge:
            self.onClick_Edge(clickEdge)
        else:
            self.selectedRelationship = None
            self.selectedCharacter = None
            self.clearInfo()

        self.drawGraph()

    def onClick_Node(self, node):
        self.selectedCharacter = node
        self.selectedRelationship = None
        self.editMode = 'node'
        if self.graph.getNode(node):
            self.varName.delete(0, tk.END)
            self.varName.insert(0, self.graph.getNode(node).name)
            self.varPersonality.set(str(self.graph.getNode(node).caractere))
        self.displayNodeInfo(node)

    def onClick_Edge(self, edge):
        self.selectedRelationship = edge
        self.selectedCharacter = None
        self.editMode = 'edge'
        source, target = edge
        if self.graph.getEdge(source, target):
            self.varSource.set(source)
            self.varTarget.set(target)
            self.varType.delete(0, tk.END)
            self.varType.insert(0, self.graph.getEdge(source, target).typeRelationship)
        self.displayEdgeInfo(edge)

    def findNode(self, x, y):
        """Trouve un nœud à la position donnée"""
        if not hasattr(self, 'pos') or x is None or y is None:
            return None
            
        for node, (node_x, node_y) in self.pos.items():
            distance = math.sqrt((node_x - x)**2 + (node_y - y)**2)
            if distance < 0.1:  # Seuil de détection
                return node
        return None

    def findEdge(self, x, y):
        if not hasattr(self, 'pos') or x is None or y is None:
            return None
        nx_graph = self.graph.toNetworkx()
        for edge in nx_graph.edges():
            u, v = edge
            u_x, u_y = self.pos[u]
            v_x, v_y = self.pos[v]
            line_length = math.sqrt((v_x - u_x)**2 + (v_y - u_y)**2)
            if line_length == 0:
                continue
            t = ((x - u_x) * (v_x - u_x) + (y - u_y) * (v_y - u_y)) / (line_length**2)
            t = max(0, min(1, t))
            proj_x = u_x + t * (v_x - u_x)
            proj_y = u_y + t * (v_y - u_y)

            distance = math.sqrt((x - proj_x)**2 + (y - proj_y)**2)
            if distance < 0.05:
                return edge

        return None
    
    def displayNodeInfo(self, node):
        character = self.graph.getNode(node)
        if not character:
            return
            
        info = f"=== PERSONNAGE ===\n"
        info += f"Nom: {character.name}\n"
        info += f"Caractère: {character.caractere}\n"
        info += f"Personnalité: {character.personality}\n"
        
        outgoing = [edge for edge in self.graph.listEdge if edge.source == character]
        if outgoing:
            info += f"\nRelations sortantes:\n"
            for edge in outgoing:
                info += f"-> {edge.target} ({edge.typeRelationship})\n"
                
        self.showInfo(info)
    
    def displayEdgeInfo(self, edge):
        source, target = edge
        relationship = self.graph.getEdge(source, target)
        if not relationship:
            return
            
        info = f"=== RELATION ===\n"
        info += f"De: {source}\n"
        info += f"Vers: {target}\n"
        info += f"Type: {relationship.typeRelationship}\n"
        
        self.showInfo(info)

    def showInfo(self, text):
        self.infoText.delete(1.0, tk.END)
        self.infoText.insert(1.0, text)

    def clearInfo(self):
        self.infoText.delete(1.0, tk.END)