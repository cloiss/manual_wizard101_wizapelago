from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value, get_option_value
from BaseClasses import MultiWorld, CollectionState

import re

# Custom function for determining if the player can reach a specific location.
def wizReachLocation(state: CollectionState, player: int, location: str) -> bool:
    location = state.multiworld.get_location(location, player)
    items_table = {
        # "x~y" means "x" yaml option is required for "y" to be factored in
        # "table$y" is a way to reference the table for "y" in this list
        # "x OR y" means what you think it means
        # Note this list is incomplete; it only has the locations that are necessary for the randomizer to work
        "To Muldoon": ["Area-Olde Town", "Building-Rattlebones", "Area-Shopping District OR Teleport-Friendly"],
        "Photomancy 1": ["Area-Golem Court", "table$To Muldoon OR Teleport-Friendly"],
        "Nightshade": ["Area-Haunted Cave", "Building-Nightshade", "Area-Olde Town", "Building-Foulgaze", "Area-Cyclops Lane", "Area-Shopping District", "Area-Dark Cave", "akilles_skip~Building-Akilles", "Area-Triton Avenue", "Building-Harvest Lord", "Area-Firecat Alley", "Building-Bastilla", "Building-Alicane"],
        "UW to Merle": ["Building-Rattlebones"],
        "Judd": ["table$To Muldoon", "Building-Judd", "Slot-Pet"],
        "Apple: Shopping District": ["Area-Shopping District", "Area-Golem Court"],
        "Ghosts: Cyclops Lane": ["Area-Cyclops Lane", "table$Apple: Shopping District", "table$UW to Merle OR Teleport-Friendly"],
        "Apple: Ravenwood": ["Area-Ravenwood", "table$Ghosts: Cyclops Lane"],
        "Ghosts: Firecat Alley": ["Area-Firecat Alley", "table$Apple: Ravenwood"]
    }
    ret_vals = []
    # Get items
    items = state.multiworld.get_items()
    if location.name in items_table:
        # Loop through the list depending on which location's table you wish to grab
        for item_name in items_table[location.name]:
            ret_val = []
            # For loop to support OR conditional
            for item_name_name in item_name.split(" OR "):
                # "~" signifies yaml option, so check for that
                if "~" in item_name_name:
                    req = item_name_name.split("~")[0]
                    if not get_option_value(state.multiworld, player, req):
                        continue
                # "$" signifies table reference, so check for that
                if "$" in item_name_name:
                    ret_val.append(wizReachLocation(state, player, item_name_name.split("$")[1]))
                else:
                    # Iterate through items list until it finds a match
                    for item in items:
                        if item.name == item_name_name and item.player == player:
                            player_item = item.name
                            break
                    # More OR conditional stuff baked in here
                    if state.has(player_item, player):
                        ret_val.append(True)
                    else:
                        ret_val.append(False)
            ret_vals.append(any(ret_val))
             
    return all(ret_vals)

# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with {function_name()}.
def overfishedAnywhere(world: World, state: CollectionState, player: int):
    """Has the player collected all fish from any fishing log?"""
    for cat, items in world.item_name_groups:
        if cat.endswith("Fishing Log") and state.has_all(items, player):
            return True
    return False

# You can also pass an argument to your function, like {function_name(15)}
# Note that all arguments are strings, so you'll need to convert them to ints if you want to do math.
def anyClassLevel(state: CollectionState, player: int, level: str):
    """Has the player reached the given level in any class?"""
    for item in ["Figher Level", "Black Belt Level", "Thief Level", "Red Mage Level", "White Mage Level", "Black Mage Level"]:
        if state.count(item, player) >= int(level):
            return True
    return False

# You can also return a string from your function, and it will be evaluated as a requires string.
def requiresMelee():
    """Returns a requires string that checks if the player has unlocked the tank."""
    return "|Figher Level:15| or |Black Belt Level:15| or |Thief Level:15|"
