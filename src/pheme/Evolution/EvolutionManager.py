import random

from pheme.Characters.Personality import Personality
from pheme.Relationships.TypeRelationship import TypeRelationship
from pheme.Universe.Graph import Graph


class EvolutionManager:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.probRelationship = 0.3
        self.decayEmotion = 0.05

    def evolve(self):
        self.createRelationship()
        self.updateRelationships()
        self.updateEmotions()

    def createRelationship(self):
        characters = self.graph.listNode

        for characterIntermediaire in characters:
            relationship_characterIntermediaire = self.getListRelationship(characterIntermediaire.name)
            listRelationship = list(relationship_characterIntermediaire.items())
            for i, (nameA, relationshipA) in enumerate(listRelationship):
                for j, (nameB, relationshipB) in enumerate(listRelationship):
                    if i != j and not self.alreadyRelationship(nameA, nameB):
                        self.tryCreateRelationship(nameA, nameB, relationshipA, relationshipB)

    def tryCreateRelationship(self, nameA, nameB, relationshipA, relationshipB):
        characterA = self.graph.getNode(nameA)
        characterB = self.graph.getNode(nameB)

        if not characterA or not characterB:
            return

        probability = self.getProbaRelationship(relationshipA, relationshipB, characterA, characterB)

        if random.random() < probability:
            typeRelationship = self.getTypeRelationship(relationshipA, relationshipB, characterA, characterB)
            self.graph.addEdge(nameA, nameB, typeRelationship)
            self.updateEmotionRelationship(nameA, nameB, typeRelationship)

    def getProbaRelationship(self, relationshipA, relationshipB, characterA, characterB):
        intensiteA = relationshipA.typeRelationship.getIntensity()
        intensiteB = relationshipB.typeRelationship.getIntensity()
        intensite = (intensiteA + intensiteB) / 2.0

        samePersonality = 1 + Personality.getMixPersonality(characterA.personality, characterB.personality)
        togetherRelationship = self.getTogetherRelationship(relationshipA, relationshipB)

        probability = self.probRelationship * intensite * samePersonality * togetherRelationship

        return min(0.9, max(0.05, probability))

    def getTogetherRelationship(self, relationshipA, relationshipB):
        polarityA = relationshipA.typeRelationship.getAverage()
        polarityB = relationshipB.typeRelationship.getAverage()

        if polarityA * polarityB > 0:
            return 1.2
        elif polarityA * polarityB < 0:
            return 0.6
        else:
            return 1.0

    def getTypeRelationship(self, relationshipA, relationshipB, characterA, characterB):
        mixPrivacy = (relationshipA.typeRelationship.privacy + relationshipB.typeRelationship.privacy) / 2.0
        mixCommitment = (relationshipA.typeRelationship.commitment + relationshipB.typeRelationship.commitment) / 2.0
        mixPassion = (relationshipA.typeRelationship.passion + relationshipB.typeRelationship.passion) / 2.0

        mixRelationship = Personality.getMixPersonality(characterA.personality, characterB.personality)
        mixRelationship = (mixRelationship - 0.5) * 0.3 + mixPrivacy * 0.2 + mixCommitment * 0.3 + mixPassion * 0.2

        privacy = self.getMix(mixPrivacy, mixRelationship)
        commitment = self.getMix(mixCommitment, mixRelationship)
        passion = self.getMix(mixPassion, mixRelationship)

        return TypeRelationship(privacy, commitment, passion)

    def getMix(self, mixBase, mix):
        variance = random.uniform(-0.1, 0.1)
        return max(-1.0, min(1.0, mixBase + mix + variance))

    def updateEmotionRelationship(self, nameA, nameB, typeRelationship):
        characterA = self.graph.getNode(nameA)
        characterB = self.graph.getNode(nameB)

        if not characterA or not characterB:
            return

        if typeRelationship.getAverage() > 0:
            characterA.emotions.updateEmotions(typeRelationship.getIntensity())
            characterB.emotions.updateEmotions(typeRelationship.getIntensity())
        else:
            characterA.emotions.updateEmotions(-1 * typeRelationship.getIntensity())
            characterB.emotions.updateEmotions(-1 * typeRelationship.getIntensity())

    def updateRelationships(self):
        for relationship in self.graph.listEdge:
            source = self.graph.getNode(relationship.source)
            target = self.graph.getNode(relationship.target)

            personality = Personality.getMixPersonality(source.personality, target.personality)
            personality = (personality - 0.5) * 0.1

            relationship.typeRelationship.update(self.getMix(0, personality))

    def updateEmotions(self):
        for character in self.graph.listNode:
            character.emotions.updateEmotions(self.decayEmotion)

            averageRelationship = self.getAverageRelationship(character.name)

            if averageRelationship > 0.3:
                character.emotions.updateEmotions(averageRelationship)
            elif averageRelationship < -0.2:
                character.emotions.updateEmotions(averageRelationship)

    def getAverageRelationship(self, name):
        listRelationships = []
        for relationship in self.graph.listEdge:
            if relationship.source == name or relationship.target == name:
                listRelationships.append(relationship.typeRelationship.getAverage())
        return sum(listRelationships) / len(listRelationships) if listRelationships else 0

    def getListRelationship(self, name):
        listRelationships = {}
        for relationship in self.graph.listEdge:
            if relationship.source == name:
                listRelationships[relationship.target] = relationship
            elif relationship.target == name:
                listRelationships[relationship.source] = relationship
        return listRelationships

    def alreadyRelationship(self, nameA, nameB):
        for relationship in self.graph.listEdge:
            if ((relationship.source == nameA and relationship.target == nameB) or (
                    relationship.target == nameA and relationship.source == nameB)):
                return True
        return False
