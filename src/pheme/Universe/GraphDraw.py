import math
import time
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .Graph import Graph
from .TimeManager import TimeManager
from ..Characters.Emotions import Emotions
from ..Characters.Personality import Personality
from ..Evolution.EvolutionManager import EvolutionManager
from ..Interactions import Interactions
from ..Interactions.InteractionsEngine import InteractionsEngine
from ..Relationships.TypeRelationship import TypeRelationship


class GraphDraw:
    """
    Classe de d'interface utilisateur graphique pour le graphe de relation
    """

    # Dictionnaire de traduction des interactions (Français -> Anglais pour les fonctions)
    INTERACTION_TRANSLATIONS = {
        "a aidé": "helped",
        "a enlacé": "hugged",
        "a embrassé": "kissed",
        "a complimenté": "praised",
        "a réconforté": "comforted",
        "a insulté": "insulted",
        "a menacé": "threatened",
        "s'est moqué de": "laughed_at",
        "a ignoré": "ignored",
        "a tué": "killed"
    }

    # Dictionnaire inverse pour l'affichage (Anglais -> Français)
    INTERACTION_DISPLAY = {
        "helped": "a aidé",
        "hugged": "a enlacé",
        "kissed": "a embrassé",
        "praised": "a complimenté",
        "comforted": "a réconforté",
        "insulted": "a insulté",
        "threatened": "a menacé",
        "laughed_at": "s'est moqué de",
        "laughed at": "s'est moqué de",
        "ignored": "a ignoré",
        "killed": "a tué"
    }

    def __init__(self, master, graph: Graph):
        self.master = master
        self.master.title("Phēmē")

        self.graph = graph
        self.interactionEngine = InteractionsEngine(graph)
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

        # Frame de gauche avec scrollbar (Personnages)
        leftFrame = ttk.Frame(mainFrame, width=300)
        leftFrame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        leftFrame.pack_propagate(False)

        # Canvas avec scrollbar pour le panneau de contrôle gauche
        canvas = tk.Canvas(leftFrame, width=380)
        scrollbar = ttk.Scrollbar(leftFrame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interne scrollable
        controlFrameLeft = ttk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=controlFrameLeft, anchor="nw")

        # Mise à jour de la zone scrollable
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=event.width)

        controlFrameLeft.bind("<Configure>", configure_scroll)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        # Frame centrale pour le graphe
        graphFrame = ttk.Frame(mainFrame)
        graphFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame de droite avec scrollbar (Relations et Temps)
        rightFrame = ttk.Frame(mainFrame, width=400)
        rightFrame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        rightFrame.pack_propagate(False)

        # Canvas avec scrollbar pour le panneau de contrôle droit
        canvas_right = tk.Canvas(rightFrame, width=380)
        scrollbar_right = ttk.Scrollbar(rightFrame, orient="vertical", command=canvas_right.yview)
        scrollbar_right.pack(side=tk.RIGHT, fill=tk.Y)
        canvas_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas_right.configure(yscrollcommand=scrollbar_right.set)

        # Frame interne scrollable droite
        controlFrameRight = ttk.Frame(canvas_right)
        canvas_right_window = canvas_right.create_window((0, 0), window=controlFrameRight, anchor="nw")

        # Mise à jour de la zone scrollable droite
        def configure_scroll_right(event):
            canvas_right.configure(scrollregion=canvas_right.bbox("all"))
            canvas_right.itemconfig(canvas_right_window, width=event.width)

        controlFrameRight.bind("<Configure>", configure_scroll_right)
        canvas_right.bind("<Configure>", lambda e: canvas_right.itemconfig(canvas_right_window, width=e.width))

        self.setup_ControlPanel_Left(controlFrameLeft)
        self.setup_ControlPanel_Right(controlFrameRight)
        self.setupGraph(graphFrame)

    def setup_ControlPanel_Left(self, frame):
        """Panneau de gauche : Personnages et Informations"""
        self.setup_ControlPanel_Character(frame)

        frameInfo = ttk.LabelFrame(frame,
                                   text="Informations",
                                   padding=10)
        frameInfo.pack(fill=tk.BOTH, expand=True, pady=5)
        self.infoText = tk.Text(frameInfo, height=15, width=30)
        self.infoText.pack(fill=tk.BOTH, expand=True)

    def setup_ControlPanel_Right(self, frame):
        """Panneau de droite : Relations, Interactions, Contrôle Temporel et Actions"""
        self.setup_ControlPanel_Relationship(frame)

        self.setup_ControlPanel_Interaction(frame)

        self.setup_ControlPanel_Time(frame)

        frameControlPanel = ttk.LabelFrame(frame, text="Actions", padding=10)
        frameControlPanel.pack(fill=tk.X, pady=5)

        ttk.Button(frameControlPanel,
                   text="Supprimer Sélection",
                   command=self.deleteSelected
                   ).pack(fill=tk.X, pady=2)

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
                                           text="Nouv Perso",
                                           command=self.createCharacter)
        self.btnCharacter_add.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))
        self.btnCharacter_update = ttk.Button(self.frameCharacter_btnCharacter,
                                              text="MAJ Perso",
                                              command=self.updateCharacter,
                                              state="disabled")
        self.btnCharacter_update.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        self.frameCharacter.columnconfigure(1, weight=1)

    def setup_ControlPanel_Relationship(self, frame):
        self.frameRelationship = ttk.LabelFrame(frame, text="Relation", padding=10)
        self.frameRelationship.pack(fill=tk.X, pady=5)

        ttk.Label(self.frameRelationship, text="Perso A :").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.varSource = tk.StringVar()
        self.comboSource = ttk.Combobox(self.frameRelationship, textvariable=self.varSource, width=17)
        self.comboSource.grid(row=0, column=1, sticky=tk.EW, pady=2, padx=(5, 0))

        ttk.Label(self.frameRelationship, text="Perso B :").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.varTarget = tk.StringVar()
        self.comboTarget = ttk.Combobox(self.frameRelationship, textvariable=self.varTarget, width=17)
        self.comboTarget.grid(row=1, column=1, sticky=tk.EW, pady=2, padx=(5, 0))

        # Type de relation
        ttk.Label(self.frameRelationship, text="Type :").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.varType = tk.StringVar(value="Ami proche")
        self.comboType = ttk.Combobox(self.frameRelationship, textvariable=self.varType,
                                      values=["Amour", "Ami proche", "Amour naissant", "Collègue proche",
                                              "Connaissance", "Neutre", "Rivalité", "Désaccord",
                                              "Hostilité", "Haine"],
                                      state="readonly", width=17)
        self.comboType.grid(row=2, column=1, sticky=tk.EW, pady=2, padx=(5, 0))

        ttk.Label(self.frameRelationship, text="Dist. Info :").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.varDistance = tk.IntVar(value=1)
        self.spinDistance = tk.Spinbox(self.frameRelationship, from_=1, to=100,
                                       textvariable=self.varDistance, width=16)
        self.spinDistance.grid(row=3, column=1, sticky=tk.EW, pady=2, padx=(5, 0))

        self.frameRelationship_btnRelationship = ttk.Frame(self.frameRelationship)
        self.frameRelationship_btnRelationship.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=5)

        self.btnRelationship_add = ttk.Button(self.frameRelationship_btnRelationship,
                                              text="Nouvelle Relation",
                                              command=self.createRelationship)
        self.btnRelationship_add.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))
        self.btnRelationship_update = ttk.Button(self.frameRelationship_btnRelationship,
                                                 text="MAJ Relation",
                                                 command=self.updateRelationship,
                                                 state="disabled")
        self.btnRelationship_update.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))

        self.frameRelationship.columnconfigure(1, weight=1)

        self.updateCharacterCombos()

    def setup_ControlPanel_Interaction(self, frame):
        """Panneau pour déclencher des interactions entre personnages"""
        self.frameInteraction = ttk.LabelFrame(frame, text="Interaction", padding=10)
        self.frameInteraction.pack(fill=tk.X, pady=5)

        ttk.Label(self.frameInteraction,
                  text="Acteur :"
                  ).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.varInteractionActor = tk.StringVar()
        self.comboInteractionActor = ttk.Combobox(self.frameInteraction, textvariable=self.varInteractionActor, width=17)
        self.comboInteractionActor.grid(row=0, column=1, sticky=tk.EW, pady=2, padx=(5, 0))

        ttk.Label(self.frameInteraction, text="Cible :").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.varInteractionTarget = tk.StringVar()
        self.comboInteractionTarget = ttk.Combobox(self.frameInteraction, textvariable=self.varInteractionTarget, width=17)
        self.comboInteractionTarget.grid(row=1, column=1, sticky=tk.EW, pady=2, padx=(5, 0))

        ttk.Label(self.frameInteraction, text="Type :").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.varInteractionType = tk.StringVar(value="a aidé")
        self.comboInteractionType = ttk.Combobox(self.frameInteraction, textvariable=self.varInteractionType,
                                                 values=["a aidé", "a enlacé", "a embrassé", "a complimenté",
                                                         "a réconforté", "a insulté", "a menacé",
                                                         "s'est moqué de", "a ignoré", "a tué"],
                                                 state="readonly", width=17)
        self.comboInteractionType.grid(row=2, column=1, sticky=tk.EW, pady=2, padx=(5, 0))

        ttk.Label(self.frameInteraction, text="Portée :").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.varInteractionScope = tk.StringVar(value="Privé (diffusion bouche à oreille)")
        self.comboInteractionScope = ttk.Combobox(self.frameInteraction,
                                                  textvariable=self.varInteractionScope,
                                                  values=["Secret (eux seuls)", "Privé (diffusion bouche à oreille)",
                                                          "Public (tout le monde)"],
                                                  state="readonly", width=17)
        self.comboInteractionScope.grid(row=3, column=1, sticky=tk.EW, pady=2, padx=(5, 0))

        # Bouton
        ttk.Button(self.frameInteraction,
                   text="Déclencher Interaction",
                   command=self.triggerInteraction
                   ).grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=5)

        self.frameInteraction.columnconfigure(1, weight=1)
        self.updateCharacterCombos()

    def triggerInteraction(self):
        """Déclenche une interaction entre deux personnages"""
        actorName = self.varInteractionActor.get()
        targetName = self.varInteractionTarget.get()
        interactionTypeFr = self.varInteractionType.get()
        scope = self.varInteractionScope.get()  # Récupérer la portée

        if not actorName or not targetName:
            self.showInfo("Erreur: Sélectionner un acteur et une cible")
            return

        if actorName == targetName:
            self.showInfo("Erreur: L'acteur et la cible doivent être différents")
            return

        actor = self.graph.getNode(actorName)
        target = self.graph.getNode(targetName)

        if not actor or not target:
            self.showInfo("Erreur: Personnage introuvable")
            return

        # Créer l'interaction
        timestamp = time.time()  # On utilise le temps réel pour l'ID unique, mais la logique est sur les ticks
        current_tick = self.time_manager.get_current_tick()

        # Traduction du type d'interaction français vers le nom de fonction anglais
        interactionType = self.INTERACTION_TRANSLATIONS.get(interactionTypeFr)
        if not interactionType:
            self.showInfo(f"Type d'interaction inconnu: {interactionTypeFr}")
            return

        # Récupération de la fonction d'interaction
        interaction_func = getattr(Interactions, interactionType, None)
        if not interaction_func:
            self.showInfo(f"Fonction d'interaction introuvable: {interactionType}")
            return

        interaction = interaction_func(actor, target, timestamp)

        # === GESTION DE LA DIFFUSION ET DU TRAITEMENT ===

        # 1. Les participants savent et réagissent TOUJOURS immédiatement
        actor.learnAboutInteraction(interaction)
        target.learnAboutInteraction(interaction)

        # Le moteur traite l'impact émotionnel/relationnel direct
        self.interactionEngine.processInteractionForCharacter(actor, interaction)
        self.interactionEngine.processInteractionForCharacter(target, interaction)

        # 2. Gestion selon la portée
        if "Public" in scope:
            # Tout le monde l'apprend et le traite instantanément
            self.interactionEngine.processInteractionForAll(interaction)
            for char in self.graph.listNode:
                char.learnAboutInteraction(interaction)
            self.showInfo(f"Information publique : {actor.name} {interactionTypeFr} {target.name}")

        elif "Privé" in scope:
            # On lance la propagation depuis l'acteur et la cible
            # Ils vont en parler à leurs voisins, qui recevront l'info dans X ticks
            self.interactionEngine.diffuseInteraction(actor, interaction, current_tick)
            self.interactionEngine.diffuseInteraction(target, interaction, current_tick)
            self.showInfo(f"Information privée : {actor.name} {interactionTypeFr} {target.name}")

        else:
            self.showInfo(f"Information secrète : {actor.name} {interactionTypeFr} {target.name}")

        self.refresh_selected_display()

    def updateCharacterCombos(self):
        characters = self.graph.getNodeNames()
        self.comboSource['values'] = characters
        self.comboTarget['values'] = characters
        # Mettre à jour aussi les combos d'interactions si ils existent
        if hasattr(self, 'comboInteractionActor'):
            self.comboInteractionActor['values'] = characters
        if hasattr(self, 'comboInteractionTarget'):
            self.comboInteractionTarget['values'] = characters

    def deleteSelected(self):
        if self.selectedRelationship:
            source, target = self.selectedRelationship
            self.graph.removeEdge(source, target)
            self.selectedRelationship = None
            # Pas besoin de recalculer le layout pour une arête
            self.showInfo(f"Relation entre {source} et {target} supprimée")
        elif self.selectedCharacter:
            character = self.graph.getNode(self.selectedCharacter)
            if character:
                # Supprimer la position du cache avant de supprimer le noeud
                if self.pos and self.selectedCharacter in self.pos:
                    del self.pos[self.selectedCharacter]
                self.graph.removeNode(character)
                self.showInfo("Personnage supprimé")
            else:
                self.showInfo("Erreur: Personnage introuvable")
            self.selectedCharacter = None
            # Forcer le recalcul du layout après suppression d'un noeud
            self.pos = None
        else:
            self.showInfo("Aucun élément sélectionné")

        self.updateCharacterCombos()
        self.clearForm()
        self.updateBtn()
        self.drawGraph()

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
            self.showInfo("Erreur: Pas de nom de personnage")
            return

        if self.graph.getNode(name):
            self.showInfo(f"Erreur: Personnage '{name}' existe")
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
        self.showInfo(f"Personnage '{name}' créé avec succès")

    def updateCharacter(self):
        if not self.selectedCharacter:
            self.showInfo("Erreur: Pas de personnage sélectionné")
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
        self.showInfo(f"Personnage '{name}' mis à jour avec succès")

    def createRelationship(self):
        if len(self.graph.listNode) < 2:
            self.showInfo("Erreur: Il faut au moins 2 personnages")
            return

        source = self.varSource.get()
        target = self.varTarget.get()
        typeRelationshipText = self.varType.get()

        try:
            distance = int(self.varDistance.get())
        except ValueError:
            distance = 1

        if not source or not target:
            self.showInfo("Erreur: Sélectionner un personnage source et cible")
            return

        if source == target:
            self.showInfo("Erreur: Sélectionner des personnages différents")
            return

        if not typeRelationshipText:
            self.showInfo("Erreur: Il faut un type de relation")
            return

        if self.graph.getEdge(source, target):
            self.showInfo(f"Erreur: Relation existe entre {source} et {target}")
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

        privacy, commitment, passion = relationship_map.get(typeRelationshipText, (0.6, 0.5, 0.1))
        typeRelationship = TypeRelationship(privacy, commitment, passion)

        self.graph.addEdge(source, target, typeRelationship, informational_distance=distance)

        self.pos = None
        self.clearForm()
        self.drawGraph()
        self.showInfo(f"Relation '{typeRelationship}' (Dist: {distance}) entre '{source}' et '{target}'")

    def updateRelationship(self):
        if not self.selectedRelationship:
            self.showInfo("Erreur: Relation non sélectionnée")
            return

        source, target = self.selectedRelationship
        typeRelationshipText = self.varType.get()

        try:
            distance = int(self.varDistance.get())
        except ValueError:
            distance = 1

        if not typeRelationshipText:
            self.showInfo("Erreur: Il faut un type de relation")
            return

        edge = self.graph.getEdge(source, target)
        if not edge:
            self.showInfo("Erreur: Relation introuvable")
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

        privacy, commitment, passion = relationship_map.get(typeRelationshipText, (0.6, 0.5, 0.1))

        # Mise à jour des valeurs
        typeRelationship = TypeRelationship(privacy, commitment, passion)

        # On met à jour l'objet Relationship directement via le Graph
        # (Comme updateEdge supprime et recrée, on utilise la méthode du graphe)
        self.graph.updateEdge(source, target, typeRelationship)

        # updateEdge dans Graph.py supprime et recrée l'arête.
        # Il faut donc réappliquer la distance sur la nouvelle arête créée.
        new_edge = self.graph.getEdge(source, target)
        if new_edge:
            new_edge.informational_distance = distance

        self.selectedRelationship = None
        self.editMode = None
        self.clearForm()
        self.updateBtn()
        self.drawGraph()
        self.showInfo(f"Relation '{typeRelationship}' (Dist: {distance}) mise à jour")

    def drawGraph(self):
        self.ax.clear()

        if not self.graph.listNode:
            self.ax.text(0.5, 0.5, "Il n'y a rien dans l'univers !",
                         ha='center', va='center', transform=self.ax.transAxes)
            self.canvas.draw()
            return

        if self.pos is None or set(self.pos.keys()) != set(self.graph.toNetworkx().nodes()):
            self.pos = nx.spring_layout(self.graph.toNetworkx(), k=3, iterations=50, seed=42)

        # Dessin des Noeuds
        node_colors = []
        nx_graph = self.graph.toNetworkx()
        for node in nx_graph.nodes():
            color = 'red' if node == self.selectedCharacter else 'skyblue'
            node_colors.append(color)

        nx.draw_networkx_nodes(nx_graph, self.pos, node_color=node_colors, node_size=500, ax=self.ax)
        nx.draw_networkx_labels(nx_graph, self.pos, ax=self.ax)

        # === PRÉPARATION DES ARÊTES ===
        self.straight_edges_data = []
        self.curved_edges_data = []

        straight_colors = []
        straight_widths = []
        curved_colors = []
        curved_widths = []

        for u, v in nx_graph.edges():
            color = 'red' if (u, v) == self.selectedRelationship else 'black'
            width = 3 if (u, v) == self.selectedRelationship else 1

            if nx_graph.has_edge(v, u):
                self.curved_edges_data.append((u, v))
                curved_colors.append(color)
                curved_widths.append(width)
            else:
                self.straight_edges_data.append((u, v))
                straight_colors.append(color)
                straight_widths.append(width)

        # === DESSIN DES ARÊTES ===
        self.straight_artist = []
        self.curved_artist = []

        # 1. Arêtes droites
        if self.straight_edges_data:
            # draw_networkx_edges retourne une liste de FancyArrowPatch quand arrows=True
            self.straight_artist = nx.draw_networkx_edges(
                nx_graph, self.pos,
                edgelist=self.straight_edges_data,
                edge_color=straight_colors,
                width=straight_widths,
                arrows=True, arrowsize=20, ax=self.ax
            )
            # On active le picker manuellement sur chaque flèche
            for arrow in self.straight_artist:
                arrow.set_picker(5)  # Tolérance de 5 pixels

        # 2. Arêtes courbées
        if self.curved_edges_data:
            self.curved_artist = nx.draw_networkx_edges(
                nx_graph, self.pos,
                edgelist=self.curved_edges_data,
                edge_color=curved_colors,
                width=curved_widths,
                connectionstyle='arc3, rad=0.2',
                arrows=True, arrowsize=20, ax=self.ax
            )
            # On active le picker manuellement
            for arrow in self.curved_artist:
                arrow.set_picker(5)

        self.ax.set_axis_off()
        self.canvas.draw()

    def onClick(self, event):
        if event.inaxes != self.ax:
            return

        clickNode = self.findNode(event.xdata, event.ydata)
        clickEdge = self.findEdge(event)  # <-- On passe 'event' directement

        if clickNode:
            self.onClick_Node(clickNode)
        elif clickEdge:
            self.onClick_Edge(clickEdge)
        else:
            self.selectedRelationship = None
            self.selectedCharacter = None
            self.editMode = None
            self.updateBtn()
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

        relationship = self.graph.getEdge(source, target)
        if relationship:
            self.varSource.set(source)
            self.varTarget.set(target)

            rel_type = relationship.typeRelationship
            self.varType.set(rel_type.nom if hasattr(rel_type, 'nom') else "Ami proche")

            # AJOUT : Chargement de la distance
            self.varDistance.set(relationship.informational_distance)

        self.updateBtn()
        self.displayEdgeInfo(edge)

    def clearForm(self):
        self.varName.delete(0, tk.END)
        for scale in self.personality_scales.values():
            scale.set(0.0)
        for scale in self.emotion_scales.values():
            scale.set(0.0)
        self.varSource.set('')
        self.varTarget.set('')
        self.varType.set("Ami proche")
        self.varDistance.set(1)

    def findNode(self, x, y):
        """Trouve un nœud à la position donnée"""
        if not hasattr(self, 'pos') or x is None or y is None:
            return None

        for node, (node_x, node_y) in self.pos.items():
            distance = math.sqrt((node_x - x) ** 2 + (node_y - y) ** 2)
            if distance < 0.1:
                return node
        return None

    def findEdge(self, event):
        """
        Trouve une arête en utilisant la détection native de Matplotlib.
        """

        # Fonction utilitaire pour vérifier une liste d'artistes
        def check_artists(artists, data):
            if not artists:
                return None
            # On parcourt chaque flèche pour voir si l'événement la concerne
            for i, arrow in enumerate(artists):
                is_hit, _ = arrow.contains(event)
                if is_hit:
                    return data[i]
            return None

        # 1. Vérifier les arêtes droites
        edge = check_artists(self.straight_artist, self.straight_edges_data)
        if edge:
            return edge

        # 2. Vérifier les arêtes courbées
        edge = check_artists(self.curved_artist, self.curved_edges_data)
        if edge:
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

        # Affichage des interactions connues (Les 5 dernières)
        info += f"\nMémoire (Derniers événements appris):\n"
        if character.knownInteractions:
            # On trie par timestamp inverse pour avoir les plus récents
            sorted_interactions = sorted(list(character.knownInteractions),
                                         key=lambda x: x.timestamp, reverse=True)

            for interaction in sorted_interactions[:5]:
                # Traduction de la description en français
                description_fr = self.INTERACTION_DISPLAY.get(interaction.description, interaction.description)
                info += f"• {interaction.actor.name} {description_fr} {interaction.target.name}\n"
        else:
            info += "(Aucune interaction connue)\n"

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
        info += f"Distance informationnelle: {relationship.informational_distance} tick(s)\n"
        info += f"Confiance: {relationship.confidence:.1f}%\n"

        self.showInfo(info)

    def showInfo(self, text):
        self.infoText.delete(1.0, tk.END)
        self.infoText.insert(1.0, text)

    def clearInfo(self):
        self.infoText.delete(1.0, tk.END)

    # Methode de la gestion du temps
    def setup_ControlPanel_Time(self, frame):
        """panneau de contrôle du temps"""
        self.frameTime = ttk.LabelFrame(frame, text="Contrôle Temporel", padding=10)
        self.frameTime.pack(fill=tk.X, pady=5)

        # Label de statut
        self.time_status_var = tk.StringVar(value="⏸ Pause | Tick: 0")
        ttk.Label(self.frameTime, textvariable=self.time_status_var,
                  font=('TkDefaultFont', 9, 'bold')).pack(pady=5)

        # Boutons de contrôle
        btn_frame = ttk.Frame(self.frameTime)
        btn_frame.pack(fill=tk.X, pady=5)

        self.btn_play = ttk.Button(btn_frame, text="▶ Démarrer", command=self.start_time)
        self.btn_play.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self.btn_pause = ttk.Button(btn_frame, text="⏸ Pause", command=self.pause_time, state="disabled")
        self.btn_pause.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        ttk.Button(btn_frame, text="⏹ Réinitialiser", command=self.reset_time).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # Contrôle de vitesse
        ttk.Label(self.frameTime, text="Vitesse (secondes/tick):").pack(pady=(10, 2))
        self.speed_var = tk.DoubleVar(value=2.0)
        speed_scale = ttk.Scale(self.frameTime, from_=0.5, to=10.0, variable=self.speed_var,
                                orient=tk.HORIZONTAL, command=self.on_speed_change)
        speed_scale.pack(fill=tk.X, padx=5)

        self.speed_label = ttk.Label(self.frameTime, text="2.0s")
        self.speed_label.pack()

    def start_time(self):
        """Démarre ou reprend."""
        if self.time_manager.current_tick == 0:
            self.time_manager.start()
        else:
            self.time_manager.resume()

        self.btn_play.config(state="disabled")
        self.btn_pause.config(state="normal")
        self.update_time_status()

    def pause_time(self):
        """Met en pause."""
        self.time_manager.pause()
        self.btn_play.config(state="normal")
        self.btn_pause.config(state="disabled")
        self.update_time_status()

    def reset_time(self):
        """Réinitialise la simulation"""
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
        Fait évoluer les personnages, relations et propage les interactions.
        """
        # 1. Évolution naturelle (émotions qui descendent, traits qui bougent...)
        self.evolution_manager.evolve()

        # 2. Moteur d'interactions (Diffusion des rumeurs/infos)
        # C'est ici que les informations "arrivent" après avoir parcouru la distance
        self.interactionEngine.tick(tick)

        # 3. Mettre à jour l'interface
        self.update_time_status()
        self.refresh_selected_display()

        # Redessiner le graphe tous les 5 ticks (pour performance)
        if tick % 5 == 0:
            self.drawGraph()

    def update_time_status(self):
        """Met à jour l'affichage du statut temporel."""
        status = "▶ En cours" if self.time_manager.is_running else "⏸ Pause"
        tick = self.time_manager.get_current_tick()
        self.time_status_var.set(f"{status} | Tick: {tick}")

    def refresh_selected_display(self):
        """Rafraîchit l'affichage du personnage ou de la relation"""
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
