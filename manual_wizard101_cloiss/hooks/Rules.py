from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value, get_option_value
from BaseClasses import MultiWorld, CollectionState
import logging
import re

def wizReach(location: str):
    locations_dict = {
        # "$y" references the logic for "y" elsewhere in this table using recursion
        # "x OR y OR z" will return true if any of "x", "y", or "z" are true (can be used with any number of args)
        # Note this list is incomplete; it only has the locations that are necessary for the randomizer to work
        "PostUW": "|Area-Unicorn Way| and |Building-Rattlebones| and |Area-The Commons| and {ItemValue(damage:26)} and {specialItemCheck(Rattlebones)}",
        "To Muldoon": "{wizReach(PostUW)} and |Area-Ravenwood| and |Area-Olde Town| and (|Area-Shopping District| or |Teleport-Friendly|)",
        "Judd": "{wizReach(To Muldoon)} and |Building-Judd| and |Slot-Pet|",
        "Golem Court": "|Area-Golem Court| and ({wizReach(PostUW)} or |Teleport-Friendly|)",
        "Shopping District": "|Area-Shopping District| and ({wizReach(PostUW)} or |Teleport-Majid| or (|Area-Olde Town| and |Teleport-Friendly|))",
        "Apples": "|Area-The Commons| and {wizReach(Golem Court)} and {wizReach(Shopping District)}" # to collapse the very lengthy logic for the second half of the Ghosts/Apple questline
    }
    return "(" + locations_dict[location] + ")" # not wrapping these strings in parentheses can break logic in subtle ways

# Checks for special item requirements at particular checkpoints based on yaml settings
def specialItemCheck(multiworld: MultiWorld, player: int, location: str):
    # integer value for each location in the options
    locations_dict = {
        "Rattlebones": 1,
        "Judd": 2,
        "Mid-Streets": 3
    }

    # get option values for each special item
    mark_location_option = get_option_value(multiworld, player, "mark_location")

    # pair option values with items
    option_item_pairs = [(mark_location_option,"|Teleport-Mark|")]

    logging.info(f"option item pairs: {option_item_pairs}")
    logging.info(f"locations dict location: {locations_dict[location]}")

    # compare the option values to determine which items are needed at this specific checkpoint
    special_items_needed = []
    for option, item in option_item_pairs:
        if option == locations_dict[location]:
            special_items_needed.append(item)

    # compile the special items into a requires string and return it
    ret = ""
    for item_name in special_items_needed:
        ret += item_name
        ret += " and "
    ret = ret[:-5] # remove final 'and'

    logging.info(f"value to be returned:{ret}")

    if ret:
        return "(" + ret + ")" # not wrapping these strings in parentheses can break logic in subtle ways
    else:
        return True # no requirements here, return true

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
