import json
import os
from pathlib import Path

def update_json(file_name: str):
    # Path to locations.json relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "manual_wizard101_cloiss", "data", file_name)
    
    if not os.path.exists(file_path):
        # Fallback if run from inside the manual_wizard101_cloiss folder
        file_path = os.path.join(script_dir, "data", file_name)
    
    if not os.path.exists(file_path):
        # Fallback if run from inside the scripts folder
        file_path = os.path.join(Path(script_dir).parent, "manual_wizard101_cloiss", "data", file_name)
        
    if not os.path.exists(file_path):
        print("Error: Could not locate locations.json.")
        print(f"Looked in: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    updated_count = 0
    last_category = None
    current_category = None
    counter = "000"
    for location in content.get("data", []):
        if ("log_msg" not in location) and file_name == "locations.json":
            # Prefixing with an underscore "_" sorts them before letters A-Z / a-z 
            # in both case-sensitive (Custom) and case-insensitive (Natural) sort orders.
            location["sort-key"] = "_" + location["name"]
            updated_count += 1
        else:
            current_category = location["category"][0]
            if current_category != last_category:
                counter = "000"
                last_category = current_category
            location["sort-key"] = counter + location["name"]
            counter = increment(counter)
            updated_count += 1
        print(f"{location['sort-key']}, {location['category']}")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

    print(f"Successfully updated {updated_count} manual locations in {file_name}")

def increment(num: str):
    num = str(int(num)+1)
    while len(num) < 3:
        num = "0" + num
    return num

if __name__ == "__main__":
    update_json("locations.json")
    update_json("items.json")
