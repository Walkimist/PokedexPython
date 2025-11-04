import requests

BASEURL = "https://pokeapi.co/api/v2/"

def getPokemonData(pokemonID):
    url = f"{BASEURL}pokemon/{pokemonID}"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(e)
        return None

def getAbilityData(abilityID):
    url = f"{BASEURL}ability/{abilityID}"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(e)
        return None

