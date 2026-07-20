from katsuba.op import * # type: ignore
from katsuba.wad import Archive # type: ignore
import json
import time
from pathlib import Path

SCHOOL_RESIST_EFFECT_NAMES = {
    b"CanonicalAllReduceDamage": "All",
    b"CanonicalFireReduceDamage": "Fire",
    b"CanonicalIceReduceDamage": "Ice",
    b"CanonicalStormReduceDamage": "Storm",
    b"CanonicalLifeReduceDamage": "Life",
    b"CanonicalMythReduceDamage": "Myth",
    b"CanonicalDeathReduceDamage": "Death",
    b"CanonicalBalanceReduceDamage": "Balance",
    b"CanonicalStarReduceDamage": "Star",
    b"CanonicalMoonReduceDamage": "Moon",
    b"CanonicalSunReduceDamage": "Sun",
    b"CanonicalShadowReduceDamage": "Shadow",
    b"ReduceDamageInvunerable": "Invulnerable",
}

# Need to install the katsuba and wiztype libraries for this script to work
# Put Root.wad from the game in the scripts folder
# This script will only work if the game is open or if a previously obtained types.json from wiztype is placed in the scripts folder
def make_creatures(root_wad_path: str, type_list_path: str):
    root_wad = Archive.mmap(root_wad_path)
    print("Obtaining types...")
    try:
        types = TypeList.open(type_list_path)
    except:
        import wiztype
        type_tree = wiztype.get_type_tree()

        # Code from wiztype to get the real dict but strip out the output to a file part
        dumper = wiztype.JsonTypeDumperV2(type_tree)
        formatted_type_tree = {
            "version": 2,
            "classes": {},
        }
        for formatted_class in dumper.class_loop(type_tree):
            formatted_type_tree["classes"].update(formatted_class)

        types = TypeList(json.dumps(formatted_type_tree))
    print("Obtained types")

    serializer_options = SerializerOptions()
    serializer_options.flags = 1
    serializer_options.shallow = False
    serializer_options.skip_unknown_types = True
    serializer = Serializer(serializer_options, types)

    manifest = root_wad.deserialize("TemplateManifest.xml", serializer)
    manifest_dict = {}
    for entry in manifest["m_serializedTemplates"]:
        manifest_dict[entry["m_id"]] = entry["m_filename"].decode("utf-8")

    final_json = {}
    final_json["data"] = {}
    print("Processing mobs...")
    for file in root_wad.iter_glob("ObjectData/**/*.xml"):
        deserialized_file = root_wad.deserialize(file, serializer)
        if not deserialized_file.type_hash == 701229577: # not GameObjectTemplate
            continue
        obj_name = deserialized_file["m_objectName"].decode("utf-8")

        behaviors = deserialized_file["m_behaviors"]
        wizard_equipment_behavior = None
        npc_behavior = None
        duelist_behavior = None
        for behavior in behaviors:
            try:
                behavior_name = behavior["m_behaviorName"]
                if behavior_name == b"WizardEquipmentBehavior":
                    wizard_equipment_behavior = behavior
                if behavior_name == b"NPCBehavior":
                    npc_behavior = behavior
                if behavior_name == b"DuelistBehavior":
                    duelist_behavior = behavior
            except:
                continue
        
        if not duelist_behavior: # not mob
            continue

        final_json["data"][obj_name] = {}

        name_lookup = deserialized_file["m_displayName"].decode("utf-8")
        name_lookup_split = name_lookup.split("_")
        name = ""
        try:
            lang_file = root_wad[f"Locale/en-US/{name_lookup_split[0]}.lang"].decode("utf-16")
            lang_file_lines = lang_file.split("\n")
            lookup_id = "_".join(name_lookup_split[1:])
            for line in range(len(lang_file_lines)):
                if lang_file_lines[line][:-1] == lookup_id:
                    name = lang_file_lines[line + 2][:-1]
                    break
        except Exception as e:
            pass
        
        final_json["data"][obj_name]["name"] = name
        
        final_json["data"][obj_name]["school"] = npc_behavior["m_schoolOfFocus"].decode("utf-8")
        final_json["data"][obj_name]["health"] = npc_behavior["m_nStartingHealth"]

        mob_stats = npc_behavior["m_baseEffects"]
        resists = {}
        all_resist = 0
        for effect in mob_stats:
            effect_name = effect["m_effectName"]
            if effect_name in SCHOOL_RESIST_EFFECT_NAMES.keys():
                if SCHOOL_RESIST_EFFECT_NAMES[effect_name] not in resists.keys():
                    resists[SCHOOL_RESIST_EFFECT_NAMES[effect_name]] = 0
                if effect["m_lookupIndex"] >= 100:
                    resists[SCHOOL_RESIST_EFFECT_NAMES[effect_name]] += effect["m_lookupIndex"] - 99
                else:
                    resists[SCHOOL_RESIST_EFFECT_NAMES[effect_name]] += effect["m_lookupIndex"] - 100
                if effect_name == b"CanonicalAllReduceDamage":
                    if effect["m_lookupIndex"] >= 100:
                        all_resist += effect["m_lookupIndex"] - 99
                    else:
                        all_resist += effect["m_lookupIndex"] - 100

        item_list = wizard_equipment_behavior["m_itemList"]
        for item in item_list:
            deserialized_item = root_wad.deserialize(manifest_dict[item], serializer)
            equip_effects = deserialized_item["m_equipEffects"]
            for effect in equip_effects:
                effect_name = effect["m_effectName"]
                if effect_name == b"CanonicalMaxHealth":
                    final_json["data"][obj_name]["health"] += effect["m_lookupIndex"] + 1
                if effect_name in SCHOOL_RESIST_EFFECT_NAMES.keys():
                    if SCHOOL_RESIST_EFFECT_NAMES[effect_name] not in resists.keys():
                        resists[SCHOOL_RESIST_EFFECT_NAMES[effect_name]] = 0
                    if effect["m_lookupIndex"] >= 100:
                        resists[SCHOOL_RESIST_EFFECT_NAMES[effect_name]] += effect["m_lookupIndex"] - 99
                    else:
                        resists[SCHOOL_RESIST_EFFECT_NAMES[effect_name]] += effect["m_lookupIndex"] - 100
                    if effect_name == b"CanonicalAllReduceDamage":
                        if effect["m_lookupIndex"] >= 100:
                            all_resist += effect["m_lookupIndex"] - 99
                        else:
                            all_resist += effect["m_lookupIndex"] - 100
        
        if all_resist:
            for resist in resists.keys():
                if resist != "All":
                    resists[resist] = all_resist + resists[resist]
        
        boosts = {}
        for resist in resists.keys():
            boosts[resist] = resists[resist] * -1
        
        final_json["data"][obj_name]["boosts"] = boosts
    
    print("Processed mobs")
    with open(f"{Path(__file__).parent.parent}\\manual_wizard101_wizapelago\\data\\creatures.json", "w") as creatures_json:
        json.dump(final_json, creatures_json, indent=4)

if __name__ == "__main__":
    start = time.time()
    make_creatures("Root.wad", "types.json")
    print(f"Done in {round(time.time() - start, 2)} seconds!")