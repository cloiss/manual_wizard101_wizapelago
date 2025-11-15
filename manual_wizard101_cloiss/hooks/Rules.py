from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value, get_option_value, format_state_prog_items_key, ProgItemsCat
from BaseClasses import MultiWorld, CollectionState
import logging
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import ManualWorld

def wizReach(location: str):
    locations_dict = {
        # "$y" references the logic for "y" elsewhere in this table using recursion
        # "x OR y OR z" will return true if any of "x", "y", or "z" are true (can be used with any number of args)
        # Note this list is incomplete; it only has the locations that are necessary for the randomizer to work
        "PostUW": "|Area-Unicorn Way| and |Building-Rattlebones| and |Area-The Commons| and {ItemValue(damage:26)} and {specialItemCheck(Rattlebones)}",
        "To Muldoon": "{wizReach(PostUW)} and |Area-Ravenwood| and |Area-Olde Town| and (|Area-Shopping District| or |Teleport-Friendly|)",
        "Judd": "{wizReach(To Muldoon)} and |Building-Judd| and |Slot-Pet| and {specialItemCheck(Judd)}",
        "Golem Court": "|Area-Golem Court| and ({wizReach(PostUW)} or |Teleport-Friendly|)",
        "Shopping District": "|Area-Shopping District| and ({wizReach(PostUW)} or (|Teleport-Majid| and {hasLevel(5)}) or (|Area-Olde Town| and |Teleport-Friendly|))",
        "Apples": "{hasLevel(5)} and |Area-The Commons| and {wizReach(Golem Court)} and {wizReach(Shopping District)}", # to collapse the very lengthy logic for the second half of the Ghosts/Apple questline
        "Fodder": "|Area-Dark Cave| or ((|Area-Triton Avenue| or |Building-Apprentice Tower|) and {YamlDisabled(beginner)})", # used for armorless and bastilla
        "Ravenwood": "|Area-Ravenwood| and (|Area-The Commons| or |Teleport-Home| or |Teleport-Friendly|)"
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

    # pair option values with items
    option_item_pairs = [
        (get_option_value(multiworld, player, "mark_location"),"|Teleport-Mark|"),
        (get_option_value(multiworld, player, "mount_location"),"|Slot-Mount|"),
        (get_option_value(multiworld, player, "rank_2_spell_location"),"|@SpellCard-Rank 2|")
    ]

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

    if ret:
        return "(" + ret + ")" # not wrapping these strings in parentheses can break logic in subtle ways
    else:
        return True # no requirements here, return true

def hasXP(state: CollectionState, player: int, xp: str | int) -> bool:
    if not isinstance(xp, int):
        xp: int = int(xp)

    player_xp = state.prog_items[player].get(format_state_prog_items_key(ProgItemsCat.VALUE, "xp"), 0)

    return player_xp >= xp

def hasLevel(state: CollectionState, player: int, level: str | int) -> bool:
    if not isinstance(level, int):
        level: int = int(level)

    """Check if player has reached the specified level based on total XP."""
    level_xp_requirements = {
        1: 0,
        2: 45,
        3: 160,
        4: 365,
        5: 705,
        6: 1200,
        7: 1870,
        8: 2745,
        9: 3905,
        10: 5305,
        11: 6970,
        12: 8920,
        13: 11175,
        14: 13755,
        15: 16680
    }
    
    required_xp = level_xp_requirements.get(level, 999999999)
    
    return hasXP(state, player, required_xp)
