def parse_foods(src):
    ingredients = []
    allergens = []
    for line in src:
        ingredients_list, allergens_list = line.strip().split(' (contains ')
        allergens_list = allergens_list[:-1]
        ingredients.append(set(ingredients_list.split(' ')))
        allergens.append(set(allergens_list.split(', ')))
    return (ingredients, allergens)

def find_assign(possible, part_assign={}):
    if all(keys in part_assign for keys in possible):
        return part_assign
    
    used = set(part_assign.values()) if part_assign else set()
    _, next_key = min((len(p - used), k) for k, p in possible.items() if not k in part_assign)

    for i in possible[next_key] - used:
        part_assign[next_key] = i
        res = find_assign(possible, part_assign)
        if res:
            return res

    print(part_assign)
    del part_assign[next_key]


import sys
ingredients, allergens = parse_foods(open(sys.argv[1]))

all_ingredients = set.union(*ingredients)
possible_ingredients = {}
for ingredients_set, allergens_set in zip(ingredients, allergens):
    for allergen in allergens_set:
        if allergen not in possible_ingredients:
            possible_ingredients[allergen] = ingredients_set
        else:
            possible_ingredients[allergen] = possible_ingredients[allergen].intersection(ingredients_set)

allergen_free_ingredients = all_ingredients - set.union(*possible_ingredients.values())
appearances = [sum(afi in i for i in ingredients) for afi in allergen_free_ingredients]

print('P1:', sum(appearances))

assignment = find_assign(possible_ingredients)
canonical_ingredients_list = [ingredient for allergen, ingredient in sorted(assignment.items(), key=lambda x: x[0])]
print('P2:', ','.join(canonical_ingredients_list))
