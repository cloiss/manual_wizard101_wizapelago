import json
import os
from pathlib import Path

def main():
    # Path to locations.json relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "manual_wizard101_cloiss", "data", "locations.json")
    
    if not os.path.exists(file_path):
        # Fallback if run from inside the manual_wizard101_cloiss folder
        file_path = os.path.join(script_dir, "data", "locations.json")
    
    if not os.path.exists(file_path):
        # Fallback if run from inside the scripts folder
        file_path = os.path.join(Path(script_dir).parent, "manual_wizard101_cloiss", "data", "locations.json")
        
    if not os.path.exists(file_path):
        print("Error: Could not locate locations.json.")
        print(f"Looked in: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    updated_count = 0
    last_category = None
    current_category = None
    keys = "abcdefghijklmnopqrstuvwxyz"
    shift = 0
    for location in content.get("data", []):
        if "log_msg" not in location:
            # Prefixing with an underscore "_" sorts them before letters A-Z / a-z 
            # in both case-sensitive (Custom) and case-insensitive (Natural) sort orders.
            location["sort-key"] = "_" + location["name"]
            updated_count += 1
        else:
            current_category = location["category"][0]
            if current_category != last_category:
                shift = 0
                last_category = current_category
            location["sort-key"] = keys[shift] + location["name"]
            shift += 1
            updated_count += 1
        print(f"{location['sort-key']}, {location['category']}")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

    print(f"Successfully updated {updated_count} manual locations in locations.json")

if __name__ == "__main__":
    main()
