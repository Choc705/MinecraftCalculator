from statistics import quantiles


recipes = {
    "oak_planks": {"oak_log": 1, "output": 4},
    "oak_trapdoor": {"oak_planks": 6, "output": 2},
    "sticks": {"oak_planks": 2, "output": 4},
    "oak_fence": {"sticks": 2, "oak_planks": 4, "output": 3},
    "oak_fence_gate": {"sticks": 4, "oak_planks": 2, "output": 1},
    "oak_stairs": {"oak_planks": 6, "output": 4},
    "oak_slab": {"oak_planks": 3, "output": 6}
}

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



if __name__ == "__main__":
    print("- - - Material Calculator - - -")
    print("Type 'quit' to exit\n")

    while True:
        print("Modes:")
        print(" 1 - Calculate single item")
        print(" 2 - Calculate list of items")
        mode = input("Choose mode (1 or 2): ").strip()

        if mode.lower() == "q" or mode.lower() == "quit":
            break

        elif mode == "1":

            item = input("Enter item name: ").strip().lower().replace(" ", "_")

            if item.lower() == "q" or item.lower() == "quit":
                break

            if item not in recipes:
                print(f"'{item}' not found in recipes. Check Spelling.\n")
                continue

            try:
                quantity = int(input(f"How many {item}?: "))
            except ValueError:
                print("Please enter a whole number.\n")
                continue

            print(f"\nTo make {quantity} {item} you need:")
            materials = calculate_materials(item, quantity)
            for material, amount in materials.items():
                print(f" {material}: {format_stacks(amount)} ({amount})")
            print()

        elif mode == "2":
            mat_list = {}
            print("Enter each item and quantity. Type 'done' when finished.\n")
            while True:
                item = input("Item name: ").strip().lower().replace(" ", "_")
                if item.lower() == "done" or item.lower() == "d":
                    break

                if item not in recipes:
                    print(f"'{item}' not found in recipes. Check Spelling.\n")
                    continue

                try:
                    quantity = int(input(f"How many {item}?: "))
                    mat_list[item] = mat_list.get(item, 0) + quantity
                except ValueError:
                    print("Please enter a whole number.\n")
                    continue

                if mat_list:
                    print("Total required resources:")
                    materials = calculate_multiple(mat_list)
                    for material, amount in materials.items():
                        print(f" {material}: {format_stacks(amount)} ({amount})")
                    print()
                else:
                    print("No items entered.\n")

        else:
            print("Please enter 1, 2 or 'quit'.\n")