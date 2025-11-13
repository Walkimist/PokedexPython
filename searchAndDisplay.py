from pkmnPokedex import pokemon
from pkmnTypes import typeNames
import os

MACHINE_TO_TM = {"Machine": "TM", "Tutor": "Tutor"}  ## for display only
BOOL_TO_CHECKMARK = {True: "✓", False: "✗"}
TYPE_EFFECTIVENESS = {
    4: "Extremely effective",
    2: "Super effective",
    1: "Effective",
    0.5: "Not very effective",
    0.25: "Mostly ineffective",
    0: "Immune",
}


def searchForPokemon(s):
    try:
        intValue = int(s)
        for p in pokemon:
            if p.id == intValue:
                return p
    except ValueError:
        for p in pokemon:
            formattedString = s.replace(" ", "-").lower()
            if p.name == formattedString:
                return p
    print("Invalid Pokémon.")
    return 0


def displayEntry(p):
    if p == 0:
        return
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

    # print(f"\nEvolution Line: {p.evoLine}")


def formatText(t):
    return t.replace("-", " ").capitalize()


userInput = input("Type Pokémon name or National dex number: ")
os.system("cls")
while userInput != "":
    if userInput == "":
        break
    displayEntry(searchForPokemon(userInput))
    print("\n")
    userInput = input("Type Pokémon name or National dex number: ")
    os.system("cls")
