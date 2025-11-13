import pickle
import os
from pkmnTypes import types
from pkmnAbilities import abilities
from apiRequestFunctions import getPokemonData, getSpeciesData

POKEMON_SAVE_PATH = "cached/pokemon.pkl"
NUM_OF_POKEMON = 3


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


class Pokemon:
    def __init__(self, pokemonData, speciesData):
        # Pokedex data
        self.id = pokemonData["id"]  # int
        self.types = self.getTypes(pokemonData)  # Types list

        self.name = pokemonData["name"]  # str
        self.genus = self.getGenus(speciesData)  # str
        self.height = pokemonData["height"]  # float
        self.weight = pokemonData["weight"]  # float
        self.abilities = self.getAbilities(pokemonData)  # dict list

        # Training
        self.evYield = self.getStats(pokemonData, True)  # dict
        self.catchRate = speciesData["capture_rate"]  # int
        self.baseFriendship = speciesData["base_happiness"]  # int
        self.baseExp = pokemonData["base_experience"]  # int
        self.growthRate = speciesData["growth_rate"]["name"]  # str

        # Breeding
        self.eggGroups = [e["name"] for e in speciesData["egg_groups"]]  # str list
        self.genderRatio = speciesData["gender_rate"]  # float
        self.eggCycles = speciesData["hatch_counter"]  # int

        # Classification
        self.isBaby = speciesData["is_baby"]  # bool
        self.isLegendary = speciesData["is_legendary"]  # bool
        self.isMythical = speciesData["is_mythical"]  # bool

        # Visual info
        self.color = speciesData["color"]["name"]  # str
        self.shape = speciesData["shape"]["name"]  # str
        self.hasGenderDifferences = speciesData["has_gender_differences"]  # bool

        # Base stats
        self.baseStats = self.getStats(pokemonData, False)  # dict
        self.bst = sum(self.baseStats.values())  # int

        # Evolution line
        self.evoLineId = self.getEvoLineId(speciesData)

        # Moveset
        self.moveSet = self.getMoveset(pokemonData)  # dict

    def getEvoLineId(self, data):
        rawUrl = data["evolution_chain"]["url"]
        baseUrl = "https://pokeapi.co/api/v2/evolution-chain/"
        return int(rawUrl.replace(baseUrl, "")[:-1])

    def getGenus(self, data):
        entries = data.get("genera", [])
        for e in entries:
            if e["language"]["name"] == "en":
                return e["genus"]

    def getMoveset(self, data):
        entries = data.get("moves", [])
        moveSet = {}
        for e in entries:
            moveDetails = {}
            latestGame = e["version_group_details"][len(e["version_group_details"]) - 1]
            moveDetails["level_learned_at"] = latestGame["level_learned_at"]
            moveDetails["move_learn_method"] = latestGame["move_learn_method"]["name"]
            moveSet[e["move"]["name"]] = moveDetails
        return moveSet

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
        abilityList = []
        for i, j in enumerate(abilityNames):
            ability = {}
            for a in abilities:
                if j == a.name:
                    ability["ability"] = a
                    ability["hidden"] = data["abilities"][i]["is_hidden"]
                    abilityList.append(ability)
                    break
        return abilityList

    def getStats(self, data, evYield):
        stats = {}
        for s in data["stats"]:
            if evYield:
                if s["effort"] > 0:
                    stats[s["stat"]["name"]] = s["effort"]
            else:
                stats[s["stat"]["name"]] = s["base_stat"]
        return stats


pokemon = loadPokemon()
