from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import ManualWorld

from ..Helpers import format_state_prog_items_key, ProgItemsCat, get_items_with_value
from BaseClasses import CollectionState, MultiWorld


def wizReach(location: str) -> bool:
    locations_dict = {
        # "$y" references the logic for "y" elsewhere in this table using recursion
        # "x OR y OR z" will return true if any of "x", "y", or "z" are true (can be used with any number of args)
        # Note this list is incomplete; it only has the locations that are necessary for the randomizer to work
        "PostUW": "|Area-Unicorn Way| and |Building-Rattlebones| and |Area-The Commons| and {ItemValue(damage:26)}",
        "To Muldoon": "{wizReach(PostUW)} and |Area-Ravenwood| and |Area-Olde Town| and (|Area-Shopping District| or |Teleport-Friendly|)",
        "Judd": "{wizReach(To Muldoon)} and |Building-Judd| and |Slot-Pet| and |Slot-Mount|",
        "Golem Court": "|Area-Golem Court| and ({wizReach(PostUW)} or |Teleport-Friendly|)",
        "Shopping District": "|Area-Shopping District| and ({wizReach(PostUW)} or (|Teleport-Majid| and {hasLevel(5)}) or (|Area-Olde Town| and |Teleport-Friendly|))",
        "Apples": "|Area-The Commons| and {wizReach(Golem Court)} and {wizReach(Shopping District)}" # to collapse the very lengthy logic for the second half of the Ghosts/Apple questline
    }
    return "(" + locations_dict[location] + ")" # not wrapping these strings in parentheses can break logic in subtle ways

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
    
    return hasXP(state, player, str(required_xp))
