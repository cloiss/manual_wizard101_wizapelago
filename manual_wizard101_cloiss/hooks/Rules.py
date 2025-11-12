from ..Helpers import get_option_value, format_state_prog_items_key, ProgItemsCat
from BaseClasses import MultiWorld, CollectionState
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import ManualWorld

def wizReach(location: str):
    locations_dict = {
        # "$y" references the logic for "y" elsewhere in this table using recursion
        # "x OR y OR z" will return true if any of "x", "y", or "z" are true (can be used with any number of args)
        # Note this list is incomplete; it only has the locations that are necessary for the randomizer to work
        "PostUW": "|Area-Unicorn Way| and |Building-Rattlebones| and |Area-The Commons| and {advDamage(250)} and {specialItemCheck(Rattlebones)}",
        "To Muldoon": "{wizReach(PostUW)} and |Area-Ravenwood| and |Area-Olde Town| and (|Area-Shopping District| or |Teleport-Friendly|)",
        "Judd": "{wizReach(To Muldoon)} and |Building-Judd| and |Slot-Pet| and {specialItemCheck(Judd)}",
        "Golem Court": "|Area-Golem Court| and ({wizReach(PostUW)} or |Teleport-Friendly|)",
        "Shopping District": "|Area-Shopping District| and ({wizReach(PostUW)} or (|Teleport-Majid| and {hasLevel(5)}) or (|Area-Olde Town| and |Teleport-Friendly|))",
        "Apples": "{hasLevel(5)} and |Area-The Commons| and {wizReach(Golem Court)} and {wizReach(Shopping District)}", # to collapse the very lengthy logic for the second half of the Ghosts/Apple questline
        "Fodder": "|Area-Dark Cave| or ((|Area-Triton Avenue| or |Building-Apprentice Tower|) and {YamlDisabled(beginner)})" # used for armorless and bastilla
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

# Custom function to do a more advanced damage check to properly screen how much damage a player has
def advDamage(world: "ManualWorld", multiworld: MultiWorld, state: CollectionState, player: int, damage: str | int) -> bool:
    if not isinstance(damage, int):
        damage: int = int(damage)

    # Calculate how much damage a player has at this point
    playerDmg = 0

    for item, _ in state.prog_items[player].items():
        item_dict: dict[str] = world.item_name_to_item.get(item, {})
        dmg = item_dict.get("value", {}).get("damage", 0)
        if dmg <= 0:
            continue

        item_dict = world.item_name_to_item.get(item, {})
        item_categories: list[str] = item_dict.get("category",[])

        if "05 SpellCard" in item_categories and canTrainSpell(item_categories, multiworld, state, player):
            playerDmg += dmg
        
        if "06 ItemCard" in item_categories:
            playerDmg += dmg

        # TODO Add other non spell card damage

        # TODO Add enemy resistance check

    return playerDmg >= damage

def getSpellRank(categories: list[str]) -> int:
    rank_dict = {
        "SpellCard-Rank 1": 1,
        "SpellCard-Rank 2": 2,
        "SpellCard-Rank 3": 3,
        "SpellCard-Rank 4": 4,
        "SpellCard-Rank 5": 5,
        "SpellCard-Rank 6": 6,
        "SpellCard-Rank 7": 7,
        "SpellCard-Rank 8": 8,
        "SpellCard-Rank 9": 9,
        "SpellCard-Rank 10": 10
    }

    # Check if any category in the categories list matches a spell card rank
    for category in categories:
        if category in rank_dict:
            return rank_dict[category]
    
    return 0

def canTrainSpell(categories: list[str], multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    spell_rank = getSpellRank(categories)
    schools = ["Balance","Storm","Ice","Fire","Death","Myth","Life"]
    primary_school = schools[get_option_value(multiworld, player, "primary_school")]

    # TODO Add can reach ravenwood 
    if "School-" + primary_school in categories:
        match spell_rank:
            case 1:
                return True
            case 2:
                return hasLevel(state, player, 5)
            case 3:
                # TODO handle special case for natures wrath
                return hasLevel(state, player, 10)
    elif "School-" + primary_school not in categories:
        match spell_rank:
            case 1:
                return hasTrainingPoints(state, player, 1)
            case 2:
                return hasTrainingPoints(state, player, 2)
            case 3:
                return hasTrainingPoints(state, player, 4)

def hasTrainingPoints(state: CollectionState, player: int, tp: int | str) -> bool:
    if not isinstance(tp, int):
        tp: int = int(tp)

    playerTP = 0

    # Levels 1-20: 1 Training Point every 4 levels (4, 8, 12, 16, 20)
    for level in range(4, 21, 4):
        if hasLevel(state, player, level):
            playerTP += 1
        else:
            break
    
    # Levels 20-170: 1 Training Point every 5 levels (25, 30, 35, ..., 170)
    # Start at 25 since level 20 was already counted above
    for level in range(25, 171, 5):
        if hasLevel(state, player, level):
            playerTP += 1
        else:
            break

    if state.has("[QI]*To Ravenwood*", player):
        playerTP += 1
    
    return playerTP >= tp
