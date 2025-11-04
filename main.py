from pmmnTypes import *
from pkmnAbilities import *
from apiRequestFunctions import getPokemonData


class Move:
    def __init__(self, name, description, typing, category, isStatus, power, accuracy):
        self.name = name  # str
        self.description = description  # str
        self.typing = typing  # Type
        self.category = category  # str
        self.isStatus = isStatus  # bool
        self.power = power  # int
        self.accuracy = accuracy  # int


class Pokemon:
    def __init__(self, data):
        # Pokedex data
        self.id = data["id"]  # int
        self.types = self.getTypes(data)  # Types list

        self.name = data["name"].capitalize()  # str
        self.height = data["height"]  # float
        self.weight = data["weight"]  # float
        self.abilites = self.getAbilities(data)  # Abilities list

        # Training
        self.evYield = self.getStats(data, True)  # dict
        self.baseExp = baseExp  # int
        self.growthRate = growtRate  # str

        # Breeding
        self.eggGroup = eggGroup  # str list
        self.genderRatio = genderRatio  # int

        # Base stats
        self.baseStats = baseStats  # dict
        self.bst = sum(baseStats.values())  # int

        # Moveset
        self.moveset = moveset  # Move list

        # Misc
        self.evolutionLine = evolutionLine  # int list

    def getTypes(self, data):
        typeNames = [t["type"]["name"] for t in data["types"]]
        ts = []
        for t in types:
            for j in typeNames:
                if j == t.lower():
                    ts.append(t)
        return ts

    def getAbilities(self, data):
        abilityNames = [a["ability"]["name"] for a in data["abilities"]]
        ab = []
        for a in abilities:
            for j in abilityNames:
                if j.lower() == a.name:
                    ab.append(a)
        return ab

    def getStats(self, data, evYield):
        stats = {}
        for s in data["stats"]:
            if evYield:
                if s["effort"] > 0:
                    stats[s["stat"]["name"]] = s["effort"]
            else:
                stats[s["stat"]["name"]] = s["base-stat"]
        return stats


def displayEntry(p):
    print("Pokemon Data:")
    print(f"\nNational dex number: {p.id}")
    print(f"Name: {p.name}")
    print(f"Typing: {p.typing}")
    print(f"Species: {p.species}")
    print(f"Height: {p.height}")
    print(f"Weight: {p.weight}")
    print(f"Abilities: {p.abilities}")
