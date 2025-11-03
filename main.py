from pmmnTypes import *
import requests

class Move:
    def __init__(self, name, description, typing, category, isStatus, power, accuracy):
        self.name = name #str
        self.description = description #str
        self.typing = typing #Type
        self.category = category #str
        self.isStatus = isStatus #bool
        self.power = power #int
        self.accuracy = accuracy #int

class Pokemon:
    def __init__(self, id, name, typing, species, height, weight, abilities, evYield, catchRate, baseFriendship, baseExp, growtRate, eggGroup, genderRatio, baseStats, moveset, evolutionLine):
        # Pokedex data
        self.id = id #int
        self.name = name #str
        self.typing = typing #Type list
        self.species = species #str
        self.height = height #float
        self.weight = weight #float
        self.abilites = abilities #Abilities list

        # Training
        self.evYield = evYield #str
        self.catchRate = catchRate #int
        self.baseFriendship = baseFriendship #int
        self.baseExp = baseExp #int
        self.growthRate = growtRate #str

        # Breeding
        self.eggGroup = eggGroup #str list
        self.genderRatio = genderRatio #int

        # Base stats
        self.baseStats = baseStats #dict
        self.bst = sum(baseStats.values()) #int

        # Moveset
        self.moveset = moveset #Move list

        # Misc
        self.evolutionLine = evolutionLine #int list

def displayEntry(p):
    print("Pokemon Data:")
    print(f"\nNational dex number: {p.id}")
    print(f"Name: {p.name}")
    print(f"Typing: {p.typing}")
    print(f"Species: {p.species}")
    print(f"Height: {p.height}")
    print(f"Weight: {p.weight}")
    print(f"Abilities: {p.abilities}")

BASEURL = "https://pokeapi.co/api/v2/"

def getPokemonData(pokemonID):
    url = f"{BASEURL}pokemon/{pokemonID}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Couldn't fetch pokemon from API")
        return None

