import pickle
import os
from pmmnTypes import types
from pkmnAbilities import abilities
from apiRequestFunctions import getPokemonData, getSpeciesData

POKEMON_SAVE_PATH = "pokemon.pkl"
NUM_OF_POKEMON = 151


def loadPokemon():
    if os.path.exists(POKEMON_SAVE_PATH):
        with open(POKEMON_SAVE_PATH, "rb") as f:
            return pickle.load(f)
    else:
        return buildPokemon()


def buildPokemon():
    pokemon = []
    for i in range(1, NUM_OF_POKEMON + 1):
        data = [getPokemonData(i), getSpeciesData(i)]
        if data:
            pokemon.append(Pokemon(data[0], data[1]))
    with open(POKEMON_SAVE_PATH, "wb") as f:
        pickle.dump(pokemon, f)
    return pokemon


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
    def __init__(self, pokemonData, speciesData):
        # Pokedex data
        self.id = pokemonData["id"]  # int
        self.types = self.getTypes(pokemonData)  # Types list

        self.name = pokemonData["name"]  # str
        self.genus = self.getGenus(speciesData)
        self.height = pokemonData["height"]  # float
        self.weight = pokemonData["weight"]  # float
        self.abilities = self.getAbilities(pokemonData)  # Abilities list

        # Training
        self.evYield = self.getStats(pokemonData, True)  # dict
        self.catchRate = speciesData["capture_rate"]  # int
        self.baseFriendship = speciesData["base_happiness"]  # int
        self.baseExp = pokemonData["base_experience"]  # int
        self.growthRate = speciesData["growth_rate"]["name"]  # str

        # Breeding
        self.eggGroups = [e["name"] for e in speciesData["egg_groups"]]  # str list
        self.genderRatio = (speciesData["gender_rate"] / 8) * 100  # float
        self.eggCycles = speciesData["hatch_counter"]  # int

        # Base stats
        self.baseStats = self.getStats(pokemonData, False)  # dict
        self.bst = sum(self.baseStats.values())  # int

        # Moveset
        # self.moveset = moveset  # dict

    def getGenus(self, data):
        entries = data.get("genera", [])
        for e in entries:
            if e["language"]["name"] == "en":
                return e["genus"]

    def getTypes(self, data):
        typeNames = [t["type"]["name"] for t in data["types"]]
        ts = []
        for t in types:
            for j in typeNames:
                if j == t.name.lower():
                    ts.append(t)
        return ts

    def getAbilities(self, data):
        abilityNames = [a["ability"]["name"] for a in data["abilities"]]
        ab = []
        for a in abilities:
            for j in abilityNames:
                if j == a.name:
                    ab.append(a)
        return ab

    def getStats(self, data, evYield):
        stats = {}
        for s in data["stats"]:
            if evYield:
                if s["effort"] > 0:
                    stats[s["stat"]["name"]] = s["effort"]
            else:
                stats[s["stat"]["name"]] = s["base_stat"]
        return stats


def searchForPokemon(s):
    for p in pokemon:
        if type(s) == int:
            if p.id == s:
                return p
        elif type(s) == str:
            if p.name.lower() == s.lower():
                return p


def displayEntry(p):
    ### Pokedex data
    print(f"\nDex number: {p.id}")
    print(f"\nName: {p.name.capitalize()}")
    if len(p.types) > 1:
        print(f"Types: {p.types[0].name}, {p.types[1].name}")
    else:
        print(f"Type: {p.types[0].name}")
    print(f"Genus: {p.genus}")
    print(f"Height: {p.height/10}m")
    print(f"Weight: {p.weight/10}kg")
    print("\nAbilities:")
    for a in p.abilities:
        print(f"{a.name.capitalize()} - {a.shortDescription}")

    ### Training
    print("\nEV yield:")
    for y in p.evYield.keys():
        print(f"{y}: {p.evYield[y]}")
    print(f"\nCatch rate: {p.catchRate}")
    print(f"Base friendship: {p.baseFriendship}")
    print(f"Base Exp.: {p.baseExp}")
    print(f"Growth Rate: {p.growthRate}")

    ### Breeding
    print("\nEgg groups:", end=" ")
    for e in p.eggGroups:
        print(f"{e},", end=" ")
    print(f"\nGender Ratio: {100-p.genderRatio}% Male, {p.genderRatio}% Female")
    print(f"Egg Cycles: {p.eggCycles}")

    ### Stats
    print("\nStats:")
    for s in p.baseStats.keys():
        print(f"{s}: {p.baseStats[s]}")
    print(f"Total: {p.bst}")


pokemon = loadPokemon()
displayEntry(searchForPokemon(1))
