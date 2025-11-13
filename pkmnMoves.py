from apiRequestFunctions import getMoveData
from pkmnTypes import types
import pickle
import os

MOVES_SAVE_PATH = "cached/moves.pkl"
NUM_OF_MOVES = 919


def loadMoves():
    if os.path.exists(MOVES_SAVE_PATH):
        with open(MOVES_SAVE_PATH, "rb") as f:
            return pickle.load(f)
    else:
        return buildMoves()


def buildMoves():
    moves = []
    for i in range(1, NUM_OF_MOVES + 1):
        data = getMoveData(i)
        if data:
            moves.append(Move(data))
    with open(MOVES_SAVE_PATH, "wb") as f:
        pickle.dump(moves, f)
    return moves


class Move:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]  # str
        self.description = self.getDescription(data)
        self.typing = self.getType(data)  # Type
        self.category = data["damage_class"]["name"]  # str
        self.power = data["power"]  # int
        self.pp = data["pp"]  # int
        self.priority = data["priority"]  # int
        self.accuracy = data["accuracy"]  # int
        self.statChanges = self.getStatChanges(data)  # dict
        self.target = data["target"]["name"]  # str

        # data['meta'] <- missing

    def getType(self, data):
        for t in types:
            if data["type"]["name"] == t.name:
                return t

    def getDescription(self, data):
        entries = data.get("effect_entries", [])
        for e in entries:
            if e["language"]["name"] == "en":
                return e["effect"]

    def getStatChanges(self, data):
        changes = data.get("stat_changes", [])
        stats = {}
        for c in changes:
            stats[c["stat"]["name"]] = c["change"]
        return stats


moves = loadMoves()
