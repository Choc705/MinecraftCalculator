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

LISTS_FILE = "lists.json"

def load_lists():
    if not os.path.exists(LISTS_FILE):
        return {}
    with open(LISTS_FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return {}
        return json.loads(content)

def save_lists(lists):
    with open(LISTS_FILE, "w") as f:
        json.dump(lists, f, indent=2)

def calculate_materials(item, quantity_needed, choices={}):
    if item not in recipes:
        return {item: quantity_needed}
    
    item_recipes = recipes[item]["recipes"]
    
    if len(item_recipes) == 1:
        recipe = item_recipes[0]
    elif item in choices:
        recipe = item_recipes[choices[item]]
    else:
        recipe = item_recipes[0]
    
    output_per_craft = recipe["output"]
    times_to_craft = -(-quantity_needed // output_per_craft)
    
    total_materials = {}
    
    for ingredient, amount_per_craft in recipe.items():
        if ingredient == "output":
            continue
        
        total_ingredient_needed = amount_per_craft * times_to_craft
        sub_materials = calculate_materials(ingredient, total_ingredient_needed, choices)
        
        for raw_material, raw_amount in sub_materials.items():
            if raw_material in total_materials:
                total_materials[raw_material] += raw_amount
            else:
                total_materials[raw_material] = raw_amount
    
    return total_materials

def calculate_multiple(shopping_list, choices={}):
    total_materials = {}
    
    for item, quantity in shopping_list.items():
        materials = calculate_materials(item, quantity, choices)
        
        for raw_material, amount in materials.items():
            if raw_material in total_materials:
                total_materials[raw_material] += amount
            else:
                total_materials[raw_material] = amount
    
    return total_materials

def format_stacks(amount):
    stacks = amount // 64
    remainder = amount % 64
    
    if stacks == 0:
        return f"{remainder} items"
    elif remainder == 0:
        return f"{stacks} stack(s)"
    else:
        return f"{stacks} stack(s) + {remainder}"