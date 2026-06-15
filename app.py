from flask import Flask, render_template, request, jsonify
from minecraft_calc import recipes, calculate_materials, format_stacks, calculate_multiple

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html", recipes=recipes)

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    mat_list = {}

    for entry in data["items"]:
        item = entry["item"]
        quantity = int(entry["quantity"])
        if item in recipes:
            mat_list[item] = mat_list.get(item, 0) + quantity
        
    materials = calculate_multiple(mat_list)

    results = []
    for material, amount in materials.items():
        results.append({"material": material, "amount": int(amount), "formatted": format_stacks(amount)})
    
    return jsonify(results)

@app.route("/add_recipe", methods=["POST"])
def add_recipe():
    from minecraft_calc import save_recipes
    data = request.get_json()

    item_name = data["item_name"].strip().lower().replace(" ", "_")
    output = int(data["output"])
    ingredients = data["ingredients"]

    recipe = {"output": output}
    for ingredient in ingredients:
        name = ingredient["name"].strip().lower().replace(" ", "_")
        amount = int(ingredient["amount"])
        recipe[name] = amount
    
    from minecraft_calc import recipes
    recipes[item_name] = recipe
    save_recipes(recipes)

    return jsonify({"success": True, "item": item_name})



if __name__ == "__main__":
    app.run(debug=True)