# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, Item

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value, format_state_prog_items_key, ProgItemsCat

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

# used by generate_tc_pool and random school choice
import random, math

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################

def generate_tc_pool(pool_size: int, world: World, multiworld: MultiWorld, player: int):
    # order is counterclockwise based on school position in Ravenwood
    school_names = ["Storm","Ice","Fire","Death","Life","Myth"] # balance not included because no Balance Shield or Balance Trap
    halloween_option = get_option_value(multiworld, player, "halloween")

    # hits
    subpool_rank1 = ["Scarab","Thunder Snake","Ice Beetle","Fire Cat","Dark Sprite","Blood Bat","Imp"]
    subpool_rank2 = ["Scorpion","Lightning Bats","Snow Serpent","Fire Elf","Ghoul","Troll","Leprechaun"]
    subpool_rank3 = ["Locust Swarm","Storm Shark","Evil Snowman","Sunbird","Banshee","Cyclops","Nature's Wrath"]
    subpool_rank4 = ["Sandstorm","Kraken","Ice Wyvern","Meteor Strike","Vampire","Humongofrog","Seraph"]
    subpool_misc_hits = ["Spectral Blast","Stormzilla","Phoenix","Skeletal Pirate","Minotaur"]
    pool_hits = subpool_rank1 * 3 + subpool_rank2 * 5 + subpool_rank3 * 3 + subpool_rank4 + subpool_misc_hits

    # defense
    subpool_single_shields = [s + " Shield" for s in school_names] + ["Snow Shield"]
    subpool_single_shields.remove("Ice Shield") # why are you like this KI
    subpool_set_shields = [s + " Shield" for s in ["Thermic","Volcanic","Glacial","Ether","Legend","Dream"]]
    subpool_misc_defense = ["Stun Block","Tower Shield","Weakness","Sprite","Fairy","Spirit Armor"]
    pool_defense = subpool_single_shields * 5 + subpool_set_shields * 2 + subpool_misc_defense

    # buffs
    subpool_single_blades = [s + "blade" for s in school_names]
    subpool_single_traps = [s + " Trap" for s in school_names]
    subpool_set_blades = [s + " Blade" for s in ["Elemental","Spirit"]]
    subpool_set_traps = [s + " Trap" for s in ["Elemental","Spirit"]]
    subpool_misc_buffs = ["Balanceblade","Hex"] # not included in the other pool due to how expensive they are
    pool_buffs = subpool_single_blades + subpool_single_traps * 3 + subpool_set_blades * 3 + subpool_set_traps * 3 + subpool_misc_buffs

    # other pools -- drawing without replacement from these tripled pools creates a slight bias against repeat values
    pool_drops = ["Ghost Touch","Fire Elf","Troll","Ghoul","Evil Snowman","Banshee"] * 3
    pool_useful = ["Lightning Bats","Storm Shark","Sunbird","Kraken","Storm Trap","Meteor Strike"] * 3
    pool_exotic = ["Harvest Lord","Tough","Tempest","Keen Eyes","Reshuffle"] # not tripled, max 1 copy of these
    pool_any = ["Any Rank 1","Any Rank 2","Any Rank 3","Any Rank 4+","Any Trap","Any Blade","Any Shield","Any TC"] * 3

    # in the spirit of the randomizer, any TCs you can get from a quest will always be there
    pool_quest_rewards = ["Kraken","Ghoul","Blood Bat","Sprite"]
    # add black cats for halloween
    if halloween_option:
        pool_quest_rewards += ["Black Cat"] * 9

    random.shuffle(pool_hits)
    random.shuffle(pool_defense)
    random.shuffle(pool_buffs)
    random.shuffle(pool_drops)
    random.shuffle(pool_useful)
    random.shuffle(pool_exotic)
    random.shuffle(pool_any)
    random.shuffle(pool_quest_rewards)

    random_pool_size = pool_size - len(pool_quest_rewards) # size of the random section of the pool, to determine the appropriate amount of each category to include

    # the divisors are all coprime so that no two amounts ever go up at the same time until n = 30
    defense_amount = math.ceil(random_pool_size / 19)
    buffs_amount = math.ceil(random_pool_size / 17)
    drops_amount = math.ceil(random_pool_size / 11)
    useful_amount = math.ceil(random_pool_size / 6)
    exotic_amount = math.ceil(random_pool_size / 23)
    any_amount = math.ceil(random_pool_size / 5)

    # frontloads the most important stuff (including all quest rewards), then adds plenty of extra random hits to the end
    pool = pool_quest_rewards + pool_useful[:useful_amount] + pool_any[:any_amount] + pool_drops[:drops_amount] + pool_buffs[:buffs_amount] + pool_defense[:defense_amount] + pool_exotic[:exotic_amount] + pool_hits[:pool_size]
    
    # failsafe for extremely large pools (n > 150), this code should never run in practice
    while len(pool) < pool_size:
        pool += pool

    # returns the first n entries in the pool, meaning small pools always go [useful, any, drop, buff, ...] instead of potentially having filler hits
    return pool[:pool_size]

# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove: list[str] = [] # List of location names

    # 0 = none, 1 = all, 2 = ore
    reagents_option = get_option_value(multiworld, player, "reagents")
    
    # If option is none or ore, remove all items but ore
    if reagents_option % 2 == 0:
        reagent_locations = world.location_name_groups["09 Reagents"]
        locationNamesToRemove.extend(reagent_locations)
    # add back ore for ore option
    if reagents_option == 2:
        locationNamesToRemove.remove("Ore")

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)

# This hook allows you to access the item names & counts before the items are created. Use this to increase/decrease the amount of a specific item in the pool
# Valid item_config key/values:
# {"Item Name": 5} <- This will create qty 5 items using all the default settings
# {"Item Name": {"useful": 7}} <- This will create qty 7 items and force them to be classified as useful
# {"Item Name": {"progression": 2, "useful": 1}} <- This will create 3 items, with 2 classified as progression and 1 as useful
# {"Item Name": {0b0110: 5}} <- If you know the special flag for the item classes, you can also define non-standard options. This setup
#       will create 5 items that are the "useful trap" class
# {"Item Name": {ItemClassification.useful: 5}} <- You can also use the classification directly
def before_create_items_all(item_config: dict[str, int|dict], world: World, multiworld: MultiWorld, player: int) -> dict[str, int|dict]:
    return item_config

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove: list[str] = [] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.

    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)

    item_names_to_add: list[str] = []

    schools = ["Balance","Storm","Ice","Fire","Death","Myth","Life","Any","Random"]
    primary_school = schools[get_option_value(multiworld, player, "primary_school")]
    secondary_school = schools[get_option_value(multiworld, player, "secondary_school")]

    # roll a random school if Random was chosen
    if primary_school == "Random":
        valid_primary_schools = schools.copy()
        valid_primary_schools.remove("Any")
        valid_primary_schools.remove("Random")
        primary_school = random.choice(valid_primary_schools)
    if secondary_school == "Random":
        valid_secondary_schools = schools.copy()
        valid_secondary_schools.remove("Random")
        secondary_school = random.choice(valid_secondary_schools)

    # choose a random secondary school if primary and secondary are the same
    if primary_school == secondary_school:
        non_primary_schools = schools.copy()
        non_primary_schools.remove(primary_school)
        non_primary_schools.remove("Any")
        secondary_school = random.choice(non_primary_schools)

    primary_school_spells = world.item_name_groups["School-" + primary_school]
    secondary_school_spells = world.item_name_groups["School-" + secondary_school]

    item_names_to_add.extend(primary_school_spells)
    item_names_to_add.extend(secondary_school_spells)

    for item_name in item_names_to_add:
        item_pool.append(world.create_item(item_name))

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # we do this here to let the generator's existing code figure out how many filler items to add, then we just replace them
    filler_item_name = world.filler_item_name
    
    to_remove = [] # items to remove from pool
    # populate to_remove with all default filler items
    for item in item_pool:
        if item.name == filler_item_name:
            to_remove.append(item)

    tc_pool = generate_tc_pool(len(to_remove),world,multiworld,player)

    # remove the specified items. doing this at the end prevents index errors when iterating
    for item in to_remove:
        item_pool.remove(item)
    
    # finally, add the specified items (currently just treasure cards)
    for tc_name in tc_pool:
        item_pool.append(world.create_item("TreasureCard-" + tc_name))

    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run every time an item is added to the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be cancelled/undone in after_remove_item
def after_collect_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you add to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] += 1
    pass

# This method is run every time an item is removed from the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be first done in after_collect_item
def after_remove_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you undo the addition to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] -= 1
    pass


# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:

    ### Example way to use this hook:
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string

    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass
