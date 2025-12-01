import random

from ..Characters.Personality import Personality
from ..Relationships.TypeRelationship import TypeRelationship
from ..Universe.Graph import Graph


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
            relationship_characterIntermediaire = self.getOutgoingRelationships(characterIntermediaire.name)
            listRelationship = list(relationship_characterIntermediaire.items())
            for i, (nameA, relationshipA) in enumerate(listRelationship):
                for j, (nameB, relationshipB) in enumerate(listRelationship):
                    if i != j and not self.alreadyRelationship(nameA, nameB):
                        self.tryCreateRelationship(nameA, nameB, relationshipA, relationshipB)

    def tryCreateRelationship(self, source, target, relationship_source, relationship_target):
        character_source = self.graph.getNode(source)
        character_target = self.graph.getNode(target)

        if not character_source or not character_target:
            return

        probability = self.getProbaRelationship(relationship_source, relationship_target, character_source, character_target)

        if random.random() < probability:
            typeRelationship = self.getTypeRelationship(relationship_source, relationship_target, character_source, character_target)
            self.graph.addEdge(source, target, typeRelationship)
            self.updateEmotionRelationship(source, target, typeRelationship)

    def getProbaRelationship(self, relationship_source, relationship_target, character_source, character_target):
        intensite_source = relationship_source.typeRelationship.getIntensity()
        intensite_target = relationship_target.typeRelationship.getIntensity()
        intensite = (intensite_source + intensite_target) / 2.0

        samePersonality = 1 + Personality.getMixPersonality(character_source.personality, character_target.personality)
        togetherRelationship = self.getTogetherRelationship(relationship_source.typeRelationship, relationship_target.typeRelationship)

        probability = self.probRelationship * intensite * samePersonality * togetherRelationship

        return min(0.9, max(0.05, probability))

    def getTogetherRelationship(self, relationship_source, relationship_target):
        polarity_source = relationship_source.typeRelationship.getAverage()
        polarity_target = relationship_target.typeRelationship.getAverage()

        if polarity_source > 0.3 and polarity_target > 0.3:
            return 1.4
        elif polarity_source > 0.3 and polarity_target < -0.3:
            return 0.4
        elif polarity_source < -0.3 and polarity_target > 0.3:
            return 0.3
        elif polarity_source < -0.3 and polarity_target < -0.3:
            return 1.2
        else:
            return 1.0

    def getTypeRelationship(self, relationship_source, relationship_target, character_source, character_target):
        mixPrivacy = relationship_source.typeRelationship.privacy *0.3 + relationship_target.typeRelationship.privacy *0.7
        mixCommitment = relationship_source.typeRelationship.commitment *0.3 + relationship_target.typeRelationship.commitment *0.7
        mixPassion = relationship_source.typeRelationship.passion *0.3 + relationship_target.typeRelationship.passion *0.7

        mixRelationship = Personality.getMixPersonality(character_source.personality, character_target.personality)
        mixRelationship = (mixRelationship - 0.5) * 0.4 + mixPrivacy * 0.2 + mixCommitment * 0.3 + mixPassion * 0.2

        personality = (character_source.extraversion + character_target.extraversion)*0.1 + (character_source.agreeableness + character_target.agreeableness)*0.15 - (character_source.neuroticism + character_target.neuroticism )*0.1

        variance = random.uniform(-0.15, 0.15)

        privacy = self.getMix(mixPrivacy, mixRelationship, personality, variance)
        commitment = self.getMix(mixCommitment, mixRelationship, personality, variance)
        passion = self.getMix(mixPassion, mixRelationship, personality, variance)

        return TypeRelationship(privacy, commitment, passion)

    def getMix(self, mixBase, mix, personality, variance):
        return max(-1.0, min(1.0, mixBase + mix + personality + variance))

    def updateEmotionRelationship(self, character_source, character_target, typeRelationship):
        characterA = self.graph.getNode(character_source)
        characterB = self.graph.getNode(character_target)

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

    def alreadyRelationship(self, character_source, character_target):
        for relationship in self.graph.listEdge:
            if ((relationship.source == character_source and relationship.target == character_target) or (
                    relationship.target == character_source and relationship.source == character_target)):
                return True
        return False
