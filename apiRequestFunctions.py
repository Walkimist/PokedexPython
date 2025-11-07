import requests

BASE_URL = "https://pokeapi.co/api/v2/"


def getPokemonData(pokemonID):
    url = f"{BASE_URL}pokemon/{pokemonID}"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(e)
        return None


def getSpeciesData(pokemonID):
    url = f"{BASE_URL}pokemon-species/{pokemonID}"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(e)
        return None


def getAbilityData(abilityID):
    url = f"{BASE_URL}ability/{abilityID}"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(e)
        return None
