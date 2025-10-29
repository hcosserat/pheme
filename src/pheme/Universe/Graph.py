import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Characters.Character import Character
from Relationships.Relationship import Relationship
import networkx as nx

class Graph :
    """
    Classe représantant le graphe de relation
    """

    def __init__(self):
        
        self.listNodeAsCharacters = []
        self.listEdgeAsRelationship = []
        self.nxGraph = nx.DiGraph()

    def addCharacterAsNode(self, name, caractere, personality):
        newCharacter = Character(name, caractere, personality)
        self.listNodeAsCharacters.append(newCharacter)

        info = {'caractere':caractere, 'personality':personality}
        self.nxGraph.add_node(name, **info)

    def addRelationshipAsEdge(self, source, target, typeRelationship):
        newRelationship = Relationship(source, target, typeRelationship)
        self.listEdgeAsRelationship.append(newRelationship)

        info = {'typeRelationship':typeRelationship}
        self.nxGraph.add_node(source, target, **info)

    def removeNodeAsCharacter(self, character):
        self.listNodeAsCharacters = [node for node in self.listNodeAsCharacters if node != character]
        self.listEdgeAsRelationship = [edge for edge in self.listEdgeAsRelationship if edge.source != character and edge.target != character]
        self.nxGraph.remove_node(character)

    def removeEdgeAsRelationship(self, source, target):
        self.listEdgeAsRelationship = [edge for edge in self.listEdgeAsRelationship if edge.source != source and edge.target != target]
        self.nxGraph.remove_node(source, target)

    def getRelationshipAsEdge(self, source, target):
        for edge in self.listEdgeAsRelationship :
            if edge.source == source and edge.target == target:
                return edge
        return None

    def getCharacterAsNode(self, name):
        for node in self.listNodeAsCharacters:
            if node.name == name:
                return node
        return None
    
    def toNetworkx(self):
        return self.nxGraph
    
    def getNodeName(self):
        return [node.name for node in self.listNodeAsCharacters]
    
    