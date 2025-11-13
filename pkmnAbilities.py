from apiRequestFunctions import getAbilityData
import pickle
import os

ABILITIES_SAVE_PATH = "cached/abilities.pkl"
NUM_OFABILITIES = 307


def loadAbilities():
    if os.path.exists(ABILITIES_SAVE_PATH):
        with open(ABILITIES_SAVE_PATH, "rb") as f:
            return pickle.load(f)
    else:
        os.mkdir("cached")
        return buildAbilities()


def buildAbilities():
    abilities = []
    for i in range(1, NUM_OFABILITIES + 1):
        data = getAbilityData(i)
        if data:
            abilities.append(Ability(data))
    with open(ABILITIES_SAVE_PATH, "wb") as f:
        pickle.dump(abilities, f)
    return abilities


class Ability:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]  # str
        self.shortDescription = self.getDescription(data, False)
        self.fullDescription = self.getDescription(data, True)  # str

    def getDescription(self, data, full):
        entries = data.get("effect_entries", [])
        for e in entries:
            if e["language"]["name"] == "en":
                if full:
                    return e["effect"]
                else:
                    return e["short_effect"]
        return "No description available"


abilities = loadAbilities()
