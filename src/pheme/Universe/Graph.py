import networkx as nx

from ..Characters.Character import Character
from ..Relationships.Relationship import Relationship


class Graph:
    """Représente le graph de relations entre characters."""

    def __init__(self):

        self.listNode = []
        self.listEdge = []
        self.nxGraph = nx.DiGraph()

    def addNode(self, name, personality, emotions):
        newCharacter = Character(name, personality, emotions)
        self.listNode.append(newCharacter)

        info = {'personality': personality, 'emotions': emotions}
        self.nxGraph.add_node(name, **info)

    def removeNode(self, character):
        self.listNode = [node for node in self.listNode if node != character]
        self.listEdge = [edge for edge in self.listEdge if
                         edge.source != character.name and edge.target != character.name]
        self.nxGraph.remove_node(character.name)

    def updateNode(self, oldName, newName, personality, emotions):
        if oldName != newName:
            self.addNode(newName, personality, emotions)
            for edge in self.listEdge:
                if edge.source == oldName:
                    self.addEdge(newName, edge.target, edge.typeRelationship)
                    self.removeEdge(edge.source, edge.target)
                elif edge.target == oldName:
                    self.addEdge(edge.source, newName, edge.typeRelationship)
                    self.removeEdge(edge.source, edge.target)
            self.removeNode(self.getNode(oldName))
            return

        node = self.getNode(oldName)
        node.personality = personality
        node.emotions = emotions

    def getNode(self, name):
        for node in self.listNode:
            if node.name == name:
                return node
        return None

    def getNodeNames(self):
        return [node.name for node in self.listNode]

    def addEdge(self, source, target, typeRelationship, informational_distance=1):
        newRelationship = Relationship(source, target, typeRelationship, informational_distance)
        self.listEdge.append(newRelationship)

        info = {'typeRelationship': typeRelationship, 'informational_distance': informational_distance}
        self.nxGraph.add_edge(source, target, **info)

    def removeEdge(self, source, target):
        self.listEdge = [edge for edge in self.listEdge if not (edge.source == source and edge.target == target)]
        self.nxGraph.remove_edge(source, target)

    def updateEdge(self, source, target, typeRelationship):
        self.removeEdge(source, target)
        self.addEdge(source, target, typeRelationship)

    def getEdge(self, source, target):
        for edge in self.listEdge:
            if edge.source == source and edge.target == target:
                return edge
        return None

    def getNeighbors(self, character: Character) -> list:
        neighbors = []
        for edge in self.listEdge:
            if edge.source == character.name:
                target_character = self.getNode(edge.target)
                if target_character is not None:
                    neighbors.append(target_character)
        return neighbors

    def toNetworkx(self):
        return self.nxGraph
