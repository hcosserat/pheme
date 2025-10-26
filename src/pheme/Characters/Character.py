from Enum import Caractere, Personnalite


class Character:

    def __init__(self, name: str, caractere: Caractere, personnalite: Personnalite):
        """
        Attributs (ou propriétés)
        """
        self.name = name
        self.caractere = caractere
        self.personnalite = personnalite

    def __str__(self) -> str:
        """
        Retourne une description lisible du personnage.
        """
        return f"{self.name} | Caractère : {self.caractere.value} | Personnalité : {self.personnalite.value}"

    def decrire(self):
        print(self.__str__())


    def changer_caractere(self, nouveau_caractere: Caractere):
        """
        Modifie le caractère du personnage.
        """
        ancien = self.caractere
        self.caractere = nouveau_caractere
        print(f"{self.name} change de caractère : '{ancien.value}' → '{nouveau_caractere.value}'")

    
    def changer_personnalite(self, nouvelle_personnalite: Personnalite):
        """
        Modifie la personnalité du personnage.
        """
        ancienne = self.personnalite
        self.personnalite = nouvelle_personnalite
        print(f"{self.name} change de personnalité : '{ancienne.value}' → '{nouvelle_personnalite.value}'")

    pass
