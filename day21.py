from collections import Counter


def load_food_list(file_name):
    allergen_possibles = {}
    ingredient_master_list = []
    with open(f"inputs/{file_name}") as f:
        raw_foods = f.read().strip().split("\n")

    for food in raw_foods:
        food = food.split(" (contains ")
        ingredients, allergens = food[0], food[1]
        ingredients = ingredients.split(" ")
        ingredient_master_list += ingredients
        allergens = allergens.split(", ")
        allergens[-1] = allergens[-1][:-1]
        for a in allergens:
            if a in allergen_possibles:
                allergen_possibles[a] = allergen_possibles[a] & set(ingredients)
            else:
                allergen_possibles[a] = set(ingredients)

    return allergen_possibles, Counter(ingredient_master_list)


def collapse_allergens(allergens):
    allergens_to_process = set(allergens.keys())
    while allergens_to_process:
        solo_allergens = [
            a for a in allergens_to_process if len(allergens[a]) == 1
        ]
        for solo in solo_allergens:
            allergens_to_process.remove(solo)
            for a in allergens_to_process:
                allergens[a] -= allergens[solo]

    return allergens


def find_free_ingredients(allergens, ingredients):
    free_ingredients = ingredients.copy()
    for a, i in allergens.items():
        del free_ingredients[next(iter(i))]
    return free_ingredients


def get_bad_ingredients(allergens):
    baddies = ""
    bad_ingredients = ([next(iter(allergens[k])) for k in sorted(allergens.keys())])
    for b in bad_ingredients[:-1]:
        baddies += b + ","
    baddies += bad_ingredients[-1]
    return baddies


def part1():
    allergens, ingredients = load_food_list("day21_test.txt")
    allergens = collapse_allergens(allergens)
    allergen_free_ingredients = find_free_ingredients(allergens, ingredients)
    total = sum(allergen_free_ingredients.values())
    assert total == 5
    b = get_bad_ingredients(allergens)
    assert b == "mxmxvkd,sqjhc,fvjkl"

    allergens, ingredients = load_food_list("day21.txt")
    allergens = collapse_allergens(allergens)
    allergen_free_ingredients = find_free_ingredients(allergens, ingredients)
    total = sum(allergen_free_ingredients.values())
    print(f"Part 1 total: {total}")
    b = get_bad_ingredients(allergens)
    print(f"Part 2 bad list: {b}")
    assert b == "kllgt,jrnqx,ljvx,zxstb,gnbxs,mhtc,hfdxb,hbfnkq"


part1()
