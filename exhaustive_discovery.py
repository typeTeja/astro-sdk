import swisseph as swe
import json
import inspect

def get_pyswisseph_inventory():
    inventory = {
        "constants": {},
        "functions": {},
        "others": []
    }
    
    for item in dir(swe):
        if item.startswith("__"):
            continue
            
        attr = getattr(swe, item)
        
        if isinstance(attr, int):
            inventory["constants"][item] = attr
        elif callable(attr):
            doc = attr.__doc__ or "No documentation available."
            inventory["functions"][item] = {
                "name": item,
                "doc": doc.strip().split("\n")[0] if doc else "No doc",
                "full_doc": doc
            }
        else:
            inventory["others"].append(item)
            
    return inventory

if __name__ == "__main__":
    inventory = get_pyswisseph_inventory()
    with open("pyswisseph_full_inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    print(f"Extracted {len(inventory['constants'])} constants and {len(inventory['functions'])} functions.")
