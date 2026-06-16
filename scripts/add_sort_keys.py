import json
import os

def main():
    # Path to locations.json relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "manual_wizard101_cloiss", "data", "locations.json")
    
    if not os.path.exists(file_path):
        # Fallback if run from inside the manual_wizard101_cloiss folder
        file_path = os.path.join(script_dir, "data", "locations.json")
        
    if not os.path.exists(file_path):
        print("Error: Could not locate locations.json.")
        print(f"Looked in: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    updated_count = 0
    for location in content.get("data", []):
        if "log_msg" not in location:
            # Prefixing with an underscore "_" sorts them before letters A-Z / a-z 
            # in both case-sensitive (Custom) and case-insensitive (Natural) sort orders.
            location["sort-key"] = "_" + location["name"]
            updated_count += 1
        else:
            # Clean up sort-key on auto-completed locations to let them sort normally
            if "sort-key" in location:
                del location["sort-key"]

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

    print(f"Successfully updated {updated_count} manual locations in locations.json")

if __name__ == "__main__":
    main()
