from flask import Flask, render_template, request, jsonify
from minecraft_calc import recipes, calculate_materials, format_stacks, calculate_multiple, save_recipes, load_recipes, load_lists, save_lists

app = Flask(__name__)

@app.route("/")
def index():
    current_recipes = load_recipes()
    
    raw_materials = set()
    for item_data in current_recipes.values():
        for recipe in item_data["recipes"]:
            for ingredient in recipe:
                if ingredient != "output" and ingredient not in current_recipes:
                    raw_materials.add(ingredient)
    
    return render_template("index.html", recipes=sorted(current_recipes), raw_materials=sorted(raw_materials))

@app.route("/get_choices", methods=["POST"])
def get_choices():
    data = request.get_json()
    current_recipes = load_recipes()
    
    needed_choices = {}
    
    for entry in data["items"]:
        item = entry["item"]
        if item in current_recipes:
            item_recipes = current_recipes[item]["recipes"]
            if len(item_recipes) > 1:
                needed_choices[item] = {
                    "options": [
                        {
                            "index": i,
                            "ingredients": {k: v for k, v in r.items() if k != "output"},
                            "output": r["output"]
                        }
                        for i, r in enumerate(item_recipes)
                    ]
                }
    
    return jsonify(needed_choices)

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    current_recipes = load_recipes()
    
    import minecraft_calc
    minecraft_calc.recipes = current_recipes

    mat_list = {}
    for entry in data["items"]:
        item = entry["item"]
        quantity = int(entry["quantity"])
        mat_list[item] = mat_list.get(item, 0) + quantity

    choices = {k: int(v) for k, v in data.get("choices", {}).items()}
    materials = calculate_multiple(mat_list, choices)

    results = []
    for material, amount in materials.items():
        results.append({
            "material": material,
            "amount": int(amount),
            "formatted": format_stacks(amount)
        })

    return jsonify(results)

@app.route("/add_recipe", methods=["POST"])
def add_recipe():
    data = request.get_json()

    item_name = data["item_name"].strip().lower().replace(" ", "_")
    output = int(data["output"])
    ingredients = data["ingredients"]

    recipe = {"output": output}
    for ingredient in ingredients:
        name = ingredient["name"].strip().lower().replace(" ", "_")
        amount = int(ingredient["amount"])
        recipe[name] = amount

    current_recipes = load_recipes()

    if item_name in current_recipes:
        current_recipes[item_name]["recipes"].append(recipe)
    else:
        current_recipes[item_name] = {"recipes": [recipe]}

    save_recipes(current_recipes)

    import minecraft_calc
    minecraft_calc.recipes = current_recipes

    return jsonify({"success": True, "item": item_name})

@app.route("/delete_recipe", methods=["POST"])
def delete_recipe():
    data = request.get_json()
    item_name = data["item_name"]
    variant_index = data.get("variant_index", None)

    current_recipes = load_recipes()

    if item_name not in current_recipes:
        return jsonify({"success": False, "error": "Recipe not found"})

    if variant_index is not None and len(current_recipes[item_name]["recipes"]) > 1:
        current_recipes[item_name]["recipes"].pop(int(variant_index))
    else:
        del current_recipes[item_name]

    save_recipes(current_recipes)

    import minecraft_calc
    minecraft_calc.recipes = current_recipes

    return jsonify({"success": True})

@app.route("/edit_recipe", methods=["POST"])
def edit_recipe():
    data = request.get_json()
    item_name = data["item_name"]
    variant_index = int(data["variant_index"])
    output = int(data["output"])
    ingredients = data["ingredients"]

    current_recipes = load_recipes()

    if item_name not in current_recipes:
        return jsonify({"success": False, "error": "Recipe not found"})

    new_recipe = {"output": output}
    for ingredient in ingredients:
        name = ingredient["name"].strip().lower().replace(" ", "_")
        amount = int(ingredient["amount"])
        new_recipe[name] = amount

    current_recipes[item_name]["recipes"][variant_index] = new_recipe
    save_recipes(current_recipes)

    import minecraft_calc
    minecraft_calc.recipes = current_recipes

    return jsonify({"success": True})

@app.route("/get_all_recipes")
def get_all_recipes():
    return jsonify(load_recipes())

@app.route("/get_all_lists")
def get_all_lists():
    return jsonify(load_lists())

@app.route("/save_list", methods=["POST"])
def save_list():
    data = request.get_json()
    name = data["name"].strip()
    items = data["items"]

    if not name:
        return jsonify({"success": False, "error": "No name provided"})

    current_lists = load_lists()
    current_lists[name] = {"items": items}
    save_lists(current_lists)

    return jsonify({"success": True})

@app.route("/delete_list", methods=["POST"])
def delete_list():
    data = request.get_json()
    name = data["name"]

    current_lists = load_lists()
    if name in current_lists:
        del current_lists[name]
        save_lists(current_lists)

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)