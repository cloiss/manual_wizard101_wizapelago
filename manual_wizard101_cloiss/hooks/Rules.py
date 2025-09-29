from worlds.AutoWorld import World
from BaseClasses import CollectionState

# Dict of every item and there damage value
dmgDict: dict[str, int] = {
    "SpellCard-Primary L1": 195,
    "SpellCard-Primary L5": 465,
    "SpellCard-Secondary L1": 240,
    "SpellCard-Secondary L5": 735,
    "ItemCard-Thunder Snake": 95,
    "ItemCard-Fire Cat": 70,
    "ItemCard-Ice Beetle": 55,
    "ItemCard-Scarab": 55,
    "ItemCard-Blood Bat": 60,
    "ItemCard-Imp": 55,
    "ItemCard-Dark Sprite": 55,
    "ItemCard-Pet Assist": 130, #? Why is this not 45
    "TreasureCard-Rank 1": 90,
    "TreasureCard-Rank 2": 280,
    "TreasureCard-Rank 3": 340
}

# Custom function to do a more advanced damage check to properly screen how much damage a player has
def damageCheck(state: CollectionState, player: int, requiredDmg: str) -> bool:
    # Convert damage to int
    dmg = int(requiredDmg)
    
    # Calculate how much damage a player has at this point
    playerDmg = 0
    for item, itemDmg in dmgDict.items():
        # If player has this item, add the value to player
        if state.count(item, player) > 0:
            match item:
                # Handle special cases
                # Secondary Level 5 cannot be trained until after rattlebones
                case "SpellCard-Secondary L5":
                    rattleLoc = state.multiworld.regions.location_cache[player]["Rattlebones"]
                    if rattleLoc in state.locations_checked: # This might not work and need to use can_reach instead
                        playerDmg += itemDmg
                # If there are no rules, just add the item value to the total damage
                case _:
                    playerDmg += itemDmg

    return playerDmg >= dmg

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
