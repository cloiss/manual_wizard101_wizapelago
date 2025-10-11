from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value, get_option_value
from BaseClasses import MultiWorld, CollectionState

import re

# Custom function for determining if the player can reach a specific location.
def wizReach(state: CollectionState, player: int, location: str) -> bool:
    location = state.multiworld.get_location(location, player)
    items_table = {
        # "$y" references the logic for "y" elsewhere in this table using recursion
        # "x OR y OR z" will return true if any of "x", "y", or "z" are true (can be used with any number of args)
        # Note this list is incomplete; it only has the locations that are necessary for the randomizer to work
        "PostUW": ["Area-Unicorn Way","Building-Rattlebones","Area-The Commons"], # TODO missing damage check
        "To Muldoon": ["$PostUW","Area-Ravenwood","Area-Olde Town","Area-Shopping District OR Teleport-Friendly"],
        "Judd": ["$To Muldoon", "Building-Judd", "Slot-Pet", "Slot-Mount"],
        "Golem Court": ["Area-Golem Court", "$PostUW OR Teleport-Friendly"],
        "Shopping District": ["Area-Shopping District", "$PostUW OR Teleport-Majid OR $SD Friendly"],
        "SD Friendly": ["Area-Olde Town","Teleport-Friendly"], #dummy conditional to support the compound logic for Shopping District
        "Apples": ["Area-The Commons", "$Golem Court", "$Shopping District"] # to collapse the very lengthy logic for the second half of the Ghosts/Apple questline
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
                # "$" signifies table reference, so check for that
                if "$" in item_name_name:
                    ret_val.append(wizReach(state, player, item_name_name.split("$")[1]))
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
