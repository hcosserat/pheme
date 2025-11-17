import math
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Graph import Graph
from TimeManager import TimeManager
from ..Characters.Emotions import Emotions
from ..Characters.Personality import Personality
from ..Evolution.EvolutionManager import EvolutionManager
from ..Relationships.TypeRelationship import TypeRelationship


class GraphDraw:
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
        self.pos = None  # Cache pour les positions des nœuds

        # Système temporel
        self.time_manager = TimeManager(tick_duration=2.0)  # 1 tick toutes les 2 secondes
        self.time_manager.register_callback(self.on_tick)

        # Gestionnaire d'évolution
        self.evolution_manager = EvolutionManager(self.graph)

        self.setupUserInterface()
        self.start_time_loop()  # Démarrer la boucle temporelle

    def setupUserInterface(self):
        mainFrame = ttk.Frame(self.master)
        mainFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame de gauche avec scrollbar
        leftFrame = ttk.Frame(mainFrame, width=400)
        leftFrame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        leftFrame.pack_propagate(False)

        # Canvas avec scrollbar pour le panneau de contrôle
        canvas = tk.Canvas(leftFrame, width=380)
        scrollbar = ttk.Scrollbar(leftFrame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interne scrollable
        controlFrame = ttk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=controlFrame, anchor="nw")

        # Mise à jour de la zone scrollable
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=event.width)

        controlFrame.bind("<Configure>", configure_scroll)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        graphFrame = ttk.Frame(mainFrame)
        graphFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setup_ControlPanel(controlFrame)
        self.setupGraph(graphFrame)

    def setup_ControlPanel(self, frame):

        self.setup_ControlPanel_Character(frame)

        self.setup_ControlPanel_Relationship(frame)

        self.setup_ControlPanel_Time(frame)

        frameControlPanel = ttk.LabelFrame(frame, text="Control Panel", padding=10)
        frameControlPanel.pack(fill=tk.X, pady=5)

        ttk.Button(frameControlPanel,
                   text="Supprimer Sélection",
                   command=self.deleteSelected
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

        # Nom du personnage
        ttk.Label(self.frameCharacter,
                  text="Nom"
                  ).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.varName = ttk.Entry(self.frameCharacter, width=20)
        self.varName.grid(row=0, column=1, columnspan=2, sticky=tk.EW, pady=2, padx=(5, 0))

        # Séparateur Personnalité
        ttk.Separator(self.frameCharacter, orient='horizontal').grid(row=1, column=0, columnspan=3, sticky=tk.EW, pady=5)
        ttk.Label(self.frameCharacter, text="Personnalité", font=('TkDefaultFont', 9,
                                                                  'bold')).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=2)

        # Personality sliders (de -1 à 1)
        row = 3
        self.personality_scales = {}
        personality_traits = [
            ("Ouverture", "openness"),
            ("Conscience", "conscientiousness"),
            ("Extraversion", "extraversion"),
            ("Agréabilité", "agreeableness"),
            ("Névrosisme", "neuroticism")
        ]

        for label, key in personality_traits:
            ttk.Label(self.frameCharacter, text=f"{label}:").grid(row=row, column=0, sticky=tk.W, pady=1)
            scale = tk.Scale(self.frameCharacter, from_=-1.0, to=1.0, resolution=0.1,
                             orient=tk.HORIZONTAL, length=150, showvalue=True)
            scale.set(0.0)
            scale.grid(row=row, column=1, columnspan=2, sticky=tk.EW, pady=1, padx=(5, 0))
            self.personality_scales[key] = scale
            row += 1

        # Séparateur Émotions
        ttk.Separator(self.frameCharacter, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=tk.EW, pady=5)
        row += 1
        ttk.Label(self.frameCharacter, text="Émotions", font=('TkDefaultFont', 9,
                                                              'bold')).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=2)
        row += 1

        # Emotions sliders (de 0 à 1)
        self.emotion_scales = {}
        emotion_traits = [
            ("Bonheur", "happiness"),
            ("Tristesse", "sadness"),
            ("Colère", "anger"),
            ("Peur", "fear"),
            ("Surprise", "surprise"),
            ("Dégoût", "disgust")
        ]

        for label, key in emotion_traits:
            ttk.Label(self.frameCharacter, text=f"{label}:").grid(row=row, column=0, sticky=tk.W, pady=1)
            scale = tk.Scale(self.frameCharacter, from_=0.0, to=1.0, resolution=0.1,
                             orient=tk.HORIZONTAL, length=150, showvalue=True)
            scale.set(0.0)
            scale.grid(row=row, column=1, columnspan=2, sticky=tk.EW, pady=1, padx=(5, 0))
            self.emotion_scales[key] = scale
            row += 1

        # Boutons
        self.frameCharacter_btnCharacter = ttk.Frame(self.frameCharacter)
        self.frameCharacter_btnCharacter.grid(row=row, column=0, columnspan=3, sticky=tk.EW, pady=5)
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
        self.comboSource.grid(row=0, column=1, sticky=tk.EW, pady=2, padx=(5, 0))
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
        self.varType = tk.StringVar(value="Ami proche")
        self.comboType = ttk.Combobox(self.frameRelationship, textvariable=self.varType,
                                      values=["Amour", "Ami proche", "Amour naissant", "Collègue proche",
                                              "Connaissance", "Neutre", "Rivalité", "Désaccord",
                                              "Hostilité", "Haine"],
                                      state="readonly", width=17)
        self.comboType.grid(row=2, column=1, sticky=tk.EW, pady=2, padx=(5, 0))

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
            self.pos = None  # Forcer le recalcul du layout
            self.showInfo(f"Relation entre {source} et {target} supprimée")
        elif self.selectedCharacter:
            character = self.graph.getNode(self.selectedCharacter)
            if character:
                self.graph.removeNode(character)
                self.showInfo("Personnage supprimé")
            else:
                self.showInfo("Erreur: Personnage introuvable")
            self.selectedCharacter = None
            self.pos = None  # Forcer le recalcul du layout
        else:
            self.showInfo("Aucun élément sélectionné")

        self.updateCharacterCombos()
        self.clearForm()
        self.updateBtn()
        self.drawGraph()

    def clearForm(self):
        self.varName.delete(0, tk.END)
        # Réinitialiser les sliders de personnalité à 0
        for scale in self.personality_scales.values():
            scale.set(0.0)
        # Réinitialiser les sliders d'émotions à 0
        for scale in self.emotion_scales.values():
            scale.set(0.0)
        self.varSource.set('')
        self.varTarget.set('')
        self.varType.set("Ami proche")

    def updateBtn(self):
        if self.selectedCharacter and self.editMode == 'node':
            self.btnCharacter_add.config(state="disable")
            self.btnCharacter_update.config(state="normal")
        else:
            self.btnCharacter_add.config(state="normal")
            self.btnCharacter_update.config(state="disable")

        if self.selectedRelationship and self.editMode == 'edge':
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

        # Récupérer les valeurs de personnalité depuis les sliders
        personality = Personality(
            openness=self.personality_scales["openness"].get(),
            conscientiousness=self.personality_scales["conscientiousness"].get(),
            extraversion=self.personality_scales["extraversion"].get(),
            agreeableness=self.personality_scales["agreeableness"].get(),
            neuroticism=self.personality_scales["neuroticism"].get()
        )

        # Récupérer les valeurs d'émotions depuis les sliders
        emotion = Emotions(
            happiness=self.emotion_scales["happiness"].get(),
            sadness=self.emotion_scales["sadness"].get(),
            anger=self.emotion_scales["anger"].get(),
            fear=self.emotion_scales["fear"].get(),
            surprise=self.emotion_scales["surprise"].get(),
            disgust=self.emotion_scales["disgust"].get()
        )

        self.graph.addNode(name, personality, emotion)  # ORDER: name, personality, emotion
        self.pos = None  # Forcer le recalcul du layout
        self.clearForm()
        self.updateCharacterCombos()
        self.drawGraph()
        self.showInfo(f"Personnage '{name}' build success")

    def updateCharacter(self):
        if not self.selectedCharacter:
            self.showInfo("Erreur: Pas de personnage selectionné")
            return

        name = self.varName.get().strip()
        if not name:
            self.showInfo("Erreur: Pas de nom de personnage")
            return

        # Récupérer les valeurs de personnalité depuis les sliders
        personality = Personality(
            openness=self.personality_scales["openness"].get(),
            conscientiousness=self.personality_scales["conscientiousness"].get(),
            extraversion=self.personality_scales["extraversion"].get(),
            agreeableness=self.personality_scales["agreeableness"].get(),
            neuroticism=self.personality_scales["neuroticism"].get()
        )

        # Récupérer les valeurs d'émotions depuis les sliders
        emotion = Emotions(
            happiness=self.emotion_scales["happiness"].get(),
            sadness=self.emotion_scales["sadness"].get(),
            anger=self.emotion_scales["anger"].get(),
            fear=self.emotion_scales["fear"].get(),
            surprise=self.emotion_scales["surprise"].get(),
            disgust=self.emotion_scales["disgust"].get()
        )

        # Vérifier si le nouveau nom existe déjà (sauf si c'est le même personnage)
        if name != self.selectedCharacter and self.graph.getNode(name):
            self.showInfo(f"Erreur: Personnage '{name}' existe déjà")
            return

        if not self.graph.getNode(self.selectedCharacter):
            self.showInfo("Erreur: Personnage MAJ introuvable")
            return

        self.graph.updateNode(self.selectedCharacter, name, personality, emotion)  # ORDER: oldName, newName, personality, emotion
        self.pos = None  # Forcer le recalcul du layout (le nom du nœud change)
        self.selectedCharacter = name
        self.editMode = None
        self.clearForm()
        self.updateCharacterCombos()
        self.updateBtn()
        self.drawGraph()
        self.showInfo(f"Personnage '{name}' MAJ success")

    def createRelationship(self):
        if len(self.graph.listNode) < 2:
            self.showInfo("Erreur: Il faut au moins 2 personnages")
            return

        source = self.varSource.get()
        target = self.varTarget.get()
        typeRelationshipText = self.varType.get()

        if not source or not target:
            self.showInfo("Errer: Select correct personnage source et cible")
            return

        if source == target:
            self.showInfo("ErReur: Select differents personnages")
            return

        if not typeRelationshipText:
            self.showInfo("Errevr: Il faut un type de relation")
            return

        if self.graph.getEdge(source, target):
            self.showInfo(f"ErrEur: Relation existe entre {source} et {target}")
            return

        relationship_map = {
            "Amour": (0.8, 0.7, 0.9),
            "Ami proche": (0.6, 0.5, 0.1),
            "Amour naissant": (0.5, 0.3, 0.5),
            "Collègue proche": (0.2, 0.4, 0.1),
            "Connaissance": (0.15, 0.15, 0.1),
            "Neutre": (0.0, 0.0, 0.0),
            "Rivalité": (-0.2, -0.2, -0.3),
            "Désaccord": (-0.2, -0.2, -0.1),
            "Hostilité": (-0.5, -0.5, -0.4),
            "Haine": (-0.8, -0.8, -0.8)
        }

        # Créer l'objet TypeRelationship avec les valeurs appropriées
        privacy, commitment, passion = relationship_map.get(typeRelationshipText, (0.6, 0.5, 0.1))
        typeRelationship = TypeRelationship(privacy, commitment, passion)

        self.graph.addEdge(source, target, typeRelationship)
        self.pos = None  # Forcer le recalcul du layout
        self.clearForm()
        self.drawGraph()
        self.showInfo(f"Relation '{typeRelationship.nom}' entre '{source}' et '{target}'")

    def updateRelationship(self):
        if not self.selectedRelationship:
            self.showInfo("€reur: Relation pas Select")
            return

        source, target = self.selectedRelationship
        typeRelationshipText = self.varType.get()
        if not typeRelationshipText:
            self.showInfo("Errevr: Il faut un type de relation")
            return

        if not self.graph.getEdge(source, target):
            self.showInfo("Erreer: Relation introuvable")
            return

        # Mapper le nom sélectionné vers les valeurs appropriées
        relationship_map = {
            "Amour": (0.8, 0.7, 0.9),
            "Ami proche": (0.6, 0.5, 0.1),
            "Amour naissant": (0.5, 0.3, 0.5),
            "Collègue proche": (0.2, 0.4, 0.1),
            "Connaissance": (0.15, 0.15, 0.1),
            "Neutre": (0.0, 0.0, 0.0),
            "Rivalité": (-0.2, -0.2, -0.3),
            "Désaccord": (-0.2, -0.2, -0.1),
            "Hostilité": (-0.5, -0.5, -0.4),
            "Haine": (-0.8, -0.8, -0.8)
        }

        # Créer l'objet TypeRelationship avec les valeurs appropriées
        privacy, commitment, passion = relationship_map.get(typeRelationshipText, (0.6, 0.5, 0.1))
        typeRelationship = TypeRelationship(privacy, commitment, passion)

        self.graph.updateEdge(source, target, typeRelationship)

        self.selectedRelationship = None
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

        # Recalculer le layout seulement si nécessaire (première fois ou après modification du graphe)
        if self.pos is None or set(self.pos.keys()) != set(self.graph.toNetworkx().nodes()):
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
            self.editMode = None
            self.updateBtn()  # Désactiver les boutons de modification
            self.clearInfo()

        self.drawGraph()

    def onClick_Node(self, node):
        self.selectedCharacter = node
        self.selectedRelationship = None
        self.editMode = 'node'
        if self.graph.getNode(node):
            character = self.graph.getNode(node)
            # Charger le nom
            self.varName.delete(0, tk.END)
            self.varName.insert(0, character.name)

            # Charger les valeurs de personnalité dans les sliders
            self.personality_scales["openness"].set(character.personality.openness)
            self.personality_scales["conscientiousness"].set(character.personality.conscientiousness)
            self.personality_scales["extraversion"].set(character.personality.extraversion)
            self.personality_scales["agreeableness"].set(character.personality.agreeableness)
            self.personality_scales["neuroticism"].set(character.personality.neuroticism)

            # Charger les valeurs d'émotions dans les sliders
            self.emotion_scales["happiness"].set(character.emotions.happiness)
            self.emotion_scales["sadness"].set(character.emotions.sadness)
            self.emotion_scales["anger"].set(character.emotions.anger)
            self.emotion_scales["fear"].set(character.emotions.fear)
            self.emotion_scales["surprise"].set(character.emotions.surprise)
            self.emotion_scales["disgust"].set(character.emotions.disgust)

        self.updateBtn()
        self.displayNodeInfo(node)

    def onClick_Edge(self, edge):
        self.selectedRelationship = edge
        self.selectedCharacter = None
        self.editMode = 'edge'
        source, target = edge
        if self.graph.getEdge(source, target):
            self.varSource.set(source)
            self.varTarget.set(target)

            rel = self.graph.getEdge(source, target).typeRelationship

            self.varType.set(rel.nom if hasattr(rel, 'nom') else "Ami proche")
        self.updateBtn()
        self.displayEdgeInfo(edge)

    def findNode(self, x, y):
        """Trouve un nœud à la position donnée"""
        if not hasattr(self, 'pos') or x is None or y is None:
            return None

        for node, (node_x, node_y) in self.pos.items():
            distance = math.sqrt((node_x - x) ** 2 + (node_y - y) ** 2)
            if distance < 0.1:
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
            line_length = math.sqrt((v_x - u_x) ** 2 + (v_y - u_y) ** 2)
            if line_length == 0:
                continue
            t = ((x - u_x) * (v_x - u_x) + (y - u_y) * (v_y - u_y)) / (line_length ** 2)
            t = max(0, min(1, t))
            proj_x = u_x + t * (v_x - u_x)
            proj_y = u_y + t * (v_y - u_y)

            distance = math.sqrt((x - proj_x) ** 2 + (y - proj_y) ** 2)
            if distance < 0.05:
                return edge

        return None

    def displayNodeInfo(self, node):
        character = self.graph.getNode(node)
        if not character:
            return

        info = f"=== PERSONNAGE ===\n"
        info += f"Nom: {character.name}\n"
        info += f"Emotions: {character.emotions}\n"
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

    # ========== MÉTHODES TEMPORELLES ==========

    def setup_ControlPanel_Time(self, frame):
        """Configure le panneau de contrôle temporel."""
        self.frameTime = ttk.LabelFrame(frame, text="Contrôle Temporel", padding=10)
        self.frameTime.pack(fill=tk.X, pady=5)

        # Label de statut
        self.time_status_var = tk.StringVar(value="⏸ Pause | Tick: 0")
        ttk.Label(self.frameTime, textvariable=self.time_status_var,
                  font=('TkDefaultFont', 9, 'bold')).pack(pady=5)

        # Boutons de contrôle
        btn_frame = ttk.Frame(self.frameTime)
        btn_frame.pack(fill=tk.X, pady=5)

        self.btn_play = ttk.Button(btn_frame, text="▶ Play", command=self.start_time)
        self.btn_play.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self.btn_pause = ttk.Button(btn_frame, text="⏸ Pause", command=self.pause_time, state="disabled")
        self.btn_pause.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        ttk.Button(btn_frame, text="⏹ Reset", command=self.reset_time).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # Contrôle de vitesse
        ttk.Label(self.frameTime, text="Vitesse (secondes/tick):").pack(pady=(10, 2))
        self.speed_var = tk.DoubleVar(value=2.0)
        speed_scale = ttk.Scale(self.frameTime, from_=0.5, to=10.0, variable=self.speed_var,
                                orient=tk.HORIZONTAL, command=self.on_speed_change)
        speed_scale.pack(fill=tk.X, padx=5)

        self.speed_label = ttk.Label(self.frameTime, text="2.0s")
        self.speed_label.pack()

    def start_time(self):
        """Démarre ou reprend la simulation temporelle."""
        if self.time_manager.current_tick == 0:
            self.time_manager.start()
        else:
            self.time_manager.resume()

        self.btn_play.config(state="disabled")
        self.btn_pause.config(state="normal")
        self.update_time_status()

    def pause_time(self):
        """Met en pause la simulation temporelle."""
        self.time_manager.pause()
        self.btn_play.config(state="normal")
        self.btn_pause.config(state="disabled")
        self.update_time_status()

    def reset_time(self):
        """Réinitialise la simulation temporelle."""
        self.time_manager.stop()
        self.time_manager.reset()
        self.btn_play.config(state="normal")
        self.btn_pause.config(state="disabled")
        self.update_time_status()

    def on_speed_change(self, value):
        """Appelé quand la vitesse change."""
        speed = float(value)
        self.time_manager.set_tick_duration(speed)
        self.speed_label.config(text=f"{speed:.1f}s")

    def on_tick(self, tick: int):
        """
        Appelé à chaque tick.
        Fait évoluer les personnages et relations via le EvolutionManager.
        """
        # Faire évoluer tous les aspects (émotions, personnalités, relations)
        self.evolution_manager.evolve(tick)

        # Mettre à jour l'interface
        self.update_time_status()
        self.refresh_selected_display()

        # Redessiner le graphe tous les 5 ticks (pour performance)
        if tick % 5 == 0:
            self.drawGraph()

    def update_time_status(self):
        """Met à jour l'affichage du statut temporel."""
        status = "▶ Running" if self.time_manager.is_running else "⏸ Pause"
        tick = self.time_manager.get_current_tick()
        self.time_status_var.set(f"{status} | Tick: {tick}")

    def refresh_selected_display(self):
        """Rafraîchit l'affichage du personnage ou de la relation sélectionné."""
        if self.selectedCharacter:
            self.displayNodeInfo(self.selectedCharacter)
            character = self.graph.getNode(self.selectedCharacter)
            if character:
                self.personality_scales["openness"].set(character.personality.openness)
                self.personality_scales["conscientiousness"].set(character.personality.conscientiousness)
                self.personality_scales["extraversion"].set(character.personality.extraversion)
                self.personality_scales["agreeableness"].set(character.personality.agreeableness)
                self.personality_scales["neuroticism"].set(character.personality.neuroticism)

                self.emotion_scales["happiness"].set(character.emotions.happiness)
                self.emotion_scales["sadness"].set(character.emotions.sadness)
                self.emotion_scales["anger"].set(character.emotions.anger)
                self.emotion_scales["fear"].set(character.emotions.fear)
                self.emotion_scales["surprise"].set(character.emotions.surprise)
                self.emotion_scales["disgust"].set(character.emotions.disgust)

        elif self.selectedRelationship:
            self.displayEdgeInfo(self.selectedRelationship)

    def start_time_loop(self):
        """Démarre la boucle"""

        def time_loop():
            self.time_manager.tick()
            self.master.after(100, time_loop)

        time_loop()
