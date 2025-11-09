import pickle
import os
from pkmnTypes import types, typeNames, TYPE_EFFECTIVENESS
from pkmnAbilities import abilities
from apiRequestFunctions import getPokemonData, getSpeciesData

POKEMON_SAVE_PATH = "pokemon.pkl"
NUM_OF_POKEMON = 151
MACHINE_TO_TM = {"Machine": "TM", "Tutor": "Tutor"}  ## for display only
BOOL_TO_CHECKMARK = {True: "✓", False: "✗"}


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

        # Moveset
        self.moveSet = self.getMoveset(pokemonData)  # dict

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
    print(f"Name: {formatText(p.name)}")
    if len(p.types) > 1:
        print(f"Types: {p.types[0].name}, {p.types[1].name}")
    else:
        print(f"Type: {p.types[0].name}")
    print(f"Genus: {p.genus}")
    print(f"Height: {p.height/10}m")
    print(f"Weight: {p.weight/10}kg")
    print("\nAbilities:")
    for a in p.abilities:
        if a["hidden"]:
            print(
                f"{formatText(a['ability'].name)} - Hidden - {a['ability'].shortDescription}"
            )
        else:
            print(f"{formatText(a['ability'].name)} - {a['ability'].shortDescription}")

    ### Training
    print("\nEV Yield:")
    for y in p.evYield.keys():
        print(f"{formatText(y)}: {p.evYield[y]}")
    print(f"\nCatch Rate: {p.catchRate}")
    print(f"Base Friendship: {p.baseFriendship}")
    print(f"Base Exp.: {p.baseExp}")
    print(f"Growth Rate: {formatText(p.growthRate)}")

    ### Breeding
    print("\nEgg Groups: ", end="")
    for e in p.eggGroups:
        print(f"{formatText(e)}", end="")
        if e != p.eggGroups[-1]:
            print(",", end=" ")
    if p.genderRatio > -1:
        print(
            f"\nGender Ratio: {100-(p.genderRatio / 8) * 100}% Male, {(p.genderRatio / 8) * 100}% Female"
        )
    else:
        print(f"\nGender: Genderless")
    print(f"Egg Cycles: {p.eggCycles}")

    ### Stats
    print("\nStats:")
    for s in p.baseStats.keys():
        print(f"{formatText(s)}: {p.baseStats[s]}")
    print(f"Total: {p.bst}")

    ### Type defenses
    print("\nType Defenses:")
    for t in typeNames:
        if len(p.types) > 1:
            totalEffectiveness = p.types[0].getAttackEffectiveness(t) * p.types[
                1
            ].getAttackEffectiveness(t)
        else:
            totalEffectiveness = p.types[0].getAttackEffectiveness(t)
        print(f"{t}: {TYPE_EFFECTIVENESS[totalEffectiveness]}")

    ### Classification
    print("\nClassification:")
    print(f"Baby: {BOOL_TO_CHECKMARK[p.isBaby]}")
    print(f"Legendary: {BOOL_TO_CHECKMARK[p.isLegendary]}")
    print(f"Mythical: {BOOL_TO_CHECKMARK[p.isMythical]}")

    ### Visual info
    print("\nVisual Data:")
    print(f"Color: {formatText(p.color)}")
    print(f"Shape: {formatText(p.shape)}")
    print(f"Gender differences: {BOOL_TO_CHECKMARK[p.hasGenderDifferences]}")

    ### Moves
    print("\nMoves by Level:")
    for m in p.moveSet.keys():
        if p.moveSet[m]["move_learn_method"] == "level-up":
            print(f"{formatText(m)} - {p.moveSet[m]["level_learned_at"]}")

    print("\nMoves by TM/Tutor:")
    for m in p.moveSet.keys():
        if (
            p.moveSet[m]["move_learn_method"] != "level-up"
            and p.moveSet[m]["move_learn_method"] != "egg"
        ):
            print(
                f"{formatText(m)} - {MACHINE_TO_TM[formatText(p.moveSet[m]['move_learn_method'])]}"
            )

    print("\nEgg moves:")
    for m in p.moveSet.keys():
        if p.moveSet[m]["move_learn_method"] == "egg":
            print(f"{formatText(m)} - {formatText(p.moveSet[m]['move_learn_method'])}")


def formatText(t):
    return t.replace("-", " ").capitalize()


pokemon = loadPokemon()
displayEntry(searchForPokemon("Mewtwo"))
