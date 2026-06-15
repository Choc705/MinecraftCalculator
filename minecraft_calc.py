#from statistics import quantiles
import json
import os

RECIPES_FILE = "recipes.json"

def load_recipes():
    if not os.path.exists(RECIPES_FILE):
        return {}

    with open(RECIPES_FILE, "r") as f:
        return json.load(f)
    
def save_recipes(recipes):
    with open(RECIPES_FILE, "w") as f:
        json.dump(recipes, f, indent=2)

recipes = load_recipes()

# recipes = {
#     "oak_planks": {"oak_log": 1, "output": 4},
#     "oak_trapdoor": {"oak_planks": 6, "output": 2},
#     "sticks": {"oak_planks": 2, "output": 4},
#     "oak_fence": {"sticks": 2, "oak_planks": 4, "output": 3},
#     "oak_fence_gate": {"sticks": 4, "oak_planks": 2, "output": 1},
#     "oak_stairs": {"oak_planks": 6, "output": 4},
#     "oak_slab": {"oak_planks": 3, "output": 6}
# }

def calculate_materials(item, quantity_needed):
    if item not in recipes:
        return {item: quantity_needed}

    recipe = recipes[item]
    output_per_craft = recipe["output"]
    times_to_craft = -(-quantity_needed // output_per_craft)

    total_materials = {}

    for ingredient, amount_per_craft in recipe.items():
        if ingredient == "output":
            continue

        total_ingredients_needed = amount_per_craft * times_to_craft
        sub_materials = calculate_materials(ingredient, total_ingredients_needed)

        for raw_material, raw_amount in sub_materials.items():
            if raw_material in total_materials:
                total_materials[raw_material] += raw_amount
            else:
                total_materials[raw_material] = raw_amount

    return total_materials

def format_stacks(amount):
    stacks = amount // 64
    remainder = amount % 64

    if stacks == 0:
        return f"{remainder} items"
    elif remainder == 0:
        return f"{stacks} stack(s)"
    else:
        return f"{stacks} stack(s) + {remainder} items"

def calculate_multiple(mat_list):
    total_materials = {}

    for item, quantity in mat_list.items():
        materials = calculate_materials(item, quantity)

        for raw_material, amount in materials.items():
            if raw_material in total_materials:
                total_materials[raw_material] += amount
            else:
                total_materials[raw_material] = amount

    return total_materials