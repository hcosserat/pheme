import random

from ..Characters.Personality import Personality
from ..Relationships.TypeRelationship import TypeRelationship
from ..Universe.Graph import Graph


class EvolutionManager:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.probRelationship = 0.8
        self.decayEmotion = 0.05
        self.probRelationship = self.probRelationship/100.0
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
        intensite_source = relationship_source.newConfidence()
        intensite_target = relationship_target.newConfidence()
        intensite = intensite_source*0.9 + intensite_target*0.1

        samePersonality = 1 + Personality.getMixPersonality(character_source.personality, character_target.personality)
        togetherRelationship = self.getTogetherRelationship(relationship_source.typeRelationship, relationship_target.typeRelationship)
        probability = self.probRelationship * (intensite*1.2 + samePersonality*0.1 + togetherRelationship*0.2)

        return min(0.9, max(0.05, probability))

    def getTogetherRelationship(self, relationship_source, relationship_target):
        polarity_source = relationship_source.getAverage()
        polarity_target = relationship_target.getAverage()

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
        mixPrivacy = self.getMix(relationship_source.typeRelationship.privacy, relationship_target.typeRelationship.privacy, 10)
        mixCommitment = self.getMix(relationship_source.typeRelationship.commitment, relationship_target.typeRelationship.commitment, 10)
        mixPassion = self.getMix(relationship_source.typeRelationship.passion, relationship_target.typeRelationship.passion, 10)

        mixRelationship = Personality.getMixPersonality(character_source.personality, character_target.personality)
        mixRelationship = (mixRelationship - 0.5) * 0.1 + mixPrivacy * 0.3 + mixCommitment * 0.3 + mixPassion * 0.3

        personality = (character_source.personality.extraversion + character_target.personality.extraversion)*0.05 + (character_source.personality.agreeableness + character_target.personality.agreeableness)*0.10
        personality =- (character_source.personality.neuroticism + character_target.personality.neuroticism )*0.05

        variance = random.uniform(-0.05, 0.05)

        privacy = self.getMixed(mixPrivacy, mixRelationship, personality, variance)
        commitment = self.getMixed(mixCommitment, mixRelationship, personality, variance)
        passion = self.getMixed(mixPassion, mixRelationship, personality, variance)
        return TypeRelationship(privacy, commitment, passion)

    def getMix(self, aspect_source, aspect_target, base):
        base = base *100.0
        return (int((aspect_target+1)*base) % int((aspect_source+1)*base)) / base -1

    def getMixed(self, mixBase, mix, personality, variance):
        return max(-1.0, min(1.0, (mixBase + mix + personality + variance)/2.5))
                 
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
            
            variance = random.uniform(-0.15, 0.15)

            personality = Personality.getMixPersonality(source.personality, target.personality)
            personality = (personality - 0.5) * 0.1

            relationship.typeRelationship.update(self.getMixed(0, personality, 0, variance))

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
    
    def getOutgoingRelationships(self, name):
        relationships = {}
        for relationship in self.graph.listEdge:
            if relationship.source == name:
                relationships[relationship.target] = relationship
        return relationships

    def alreadyRelationship(self, character_source, character_target):
        for relationship in self.graph.listEdge:
            if (relationship.source == character_source and relationship.target == character_target):
                return True
        return False
