from typing import TYPE_CHECKING

# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import ItemClassification, MultiWorld, CollectionState, Item

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

if TYPE_CHECKING:
    from .. import ManualWorld

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import get_option_value, format_state_prog_items_key, ProgItemsCat

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

def get_option_value_regen(multiworld: MultiWorld, player: int, option_name: str):
    if hasattr(multiworld, "re_gen_passthrough"):
       return multiworld.re_gen_passthrough["Manual_Wizard101_Cloiss"][option_name]
    else:
       return get_option_value(multiworld, player, option_name)

def generate_tc_pool(pool_size: int, world: World, multiworld: MultiWorld, player: int):
    # order is counterclockwise based on school position in Ravenwood
    school_names = ["Storm","Ice","Fire","Death","Myth","Life"] # balance not included because no Balance Shield or Balance Trap
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
    subpool_set_shields = [s + " Shield" for s in ["Thermic","Volcanic","Glacial","Legend","Ether","Dream"]]
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
    pool_drops = ["Ghost Touch","Fire Elf","Troll","Ghoul","Evil Snowman","Banshee","Cyclops"] * 3
    pool_useful = ["Lightning Bats","Storm Shark","Sunbird","Kraken","Storm Trap","Meteor Strike"] * 3
    pool_exotic = ["Harvest Lord","Tough","Tempest","Keen Eyes","Reshuffle"] # not tripled, max 1 copy of these
    pool_any = ["Any Rank 1","Any Rank 2","Any Rank 3","Any Rank 4+","Any Shield","Any Blade","Any Trap","Any TC"] * 3

    # in the spirit of the randomizer, any TCs you can get from a quest will always be there
    pool_quest_rewards = ["Kraken","Ghoul","Blood Bat","Sprite"]
    # add black cats for halloween
    if halloween_option:
        pool_quest_rewards += ["Black Cat"] * 10

    # Use multiworld random here to ensure consistency with seed
    multiworld.random.shuffle(pool_hits)
    multiworld.random.shuffle(pool_defense)
    multiworld.random.shuffle(pool_buffs)
    multiworld.random.shuffle(pool_drops)
    multiworld.random.shuffle(pool_useful)
    multiworld.random.shuffle(pool_exotic)
    multiworld.random.shuffle(pool_any)
    multiworld.random.shuffle(pool_quest_rewards)

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

# returns the first "School" category of an item (most have just one, except Pixie)
def get_item_school(item_name: str, world: World):
    item_categories = world.item_name_to_item[item_name].get("category",[])
    for category in item_categories:
        if category.startswith("School"):
            return category
    logging.error(f"Item {item_name} does not have a valid school.")
    return None

def format_starting_item_block(item_name: str):
    return {"items": [item_name]}

# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Before anything happens, edit the options for primary and secondary school
    schools = ["Balance","Storm","Ice","Fire","Death","Myth","Life","Any","Random"]

    primary_school = schools[get_option_value_regen(multiworld, player, "primary_school")]
    secondary_school = schools[get_option_value_regen(multiworld, player, "secondary_school")]

    valid_schools = schools.copy()
    valid_schools.remove("Any")
    valid_schools.remove("Random")

    # roll a random school if Random was chosen
    if primary_school == "Random":
        primary_school = multiworld.random.choice(valid_schools)
    if secondary_school == "Random":
        secondary_school = multiworld.random.choice(valid_schools)

    # choose a random secondary school if primary and secondary are the same
    if primary_school == secondary_school:
        valid_schools.remove(primary_school)
        secondary_school = multiworld.random.choice(valid_schools)

    # modify the world options directly
    world.options.primary_school.value = schools.index(primary_school)
    world.options.secondary_school.value = schools.index(secondary_school)

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    location_names_to_remove: list[str] = [] # List of location names

    # Handle Optional Locations from Yaml Options
    # 0 = none, 1 = all, 2 = ore
    reagents_option = get_option_value(multiworld, player, "reagents")
    
    # If option is none or ore, remove all items but ore
    if reagents_option % 2 == 0:
        reagent_locations = world.location_name_groups["Reagents"]
        location_names_to_remove.extend(reagent_locations)
    # add back ore for ore option
    if reagents_option == 2:
        location_names_to_remove.remove("Ore")

    # Handle Wooden Chest Locations
    # 0 = none, 1 = anywhere, 2 = all
    wooden_chests_option = get_option_value(multiworld, player, "wooden_chests")

    wooden_chest_locations = world.location_name_groups.get("WoodenChests",[])
    # If option is none, remove all wooden chest locations
    if wooden_chests_option == 0:
            location_names_to_remove.extend(wooden_chest_locations)
    # If option is anywhere, remove all but the anywhere one
    elif wooden_chests_option == 1:
            location_names_to_remove.extend(wooden_chest_locations)
            location_names_to_remove.remove("Wooden Chest: Anywhere")
    # If option is all, only remove the anywhere one
    elif wooden_chests_option == 2:
            location_names_to_remove.append("Wooden Chest: Anywhere")

    # Handle School-Based Locations
    schools = ["Balance","Storm","Ice","Fire","Death","Myth","Life"]
    primary_school = schools[get_option_value(multiworld, player, "primary_school")]
    
    for school in schools:
        if school != primary_school:
            school_key = "School-" + school
            if school_key in world.location_name_groups:
                school_locations = list(world.location_name_groups[school_key])
                location_names_to_remove.extend(school_locations)

    # Actual Remove Code
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in location_names_to_remove:
                    region.locations.remove(location)

    # Fake Events system
    # Add Quest Mirror for each location
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                location_dict = world.location_name_to_location[location.name]
                try:
                    categories: list[str] = location_dict["category"]
                    if "Quest" in categories:
                        e_item = ManualItem("[QI]" + location.name, ItemClassification.progression, None, player=player) # Create the event item
                        e_loc = ManualLocation(player, "[QL]" + location.name, None, region) # create the event location
                        region.locations.append(e_loc) # put the event location in the region
                        e_loc.place_locked_item(e_item) # place the event item at the event location
                except:
                    pass


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
    item_names_to_add: list[str] = []

    schools = ["Balance","Storm","Ice","Fire","Death","Myth","Life","Any","Random"]
    primary_school = schools[get_option_value(multiworld, player, "primary_school")]
    secondary_school = schools[get_option_value(multiworld, player, "secondary_school")]

    primary_school_spells = list(world.item_name_groups["School-" + primary_school])
    secondary_school_spells = list(world.item_name_groups["School-" + secondary_school])
    primary_only_spells = world.item_name_groups["PrimaryOnly"]

    for spell in primary_only_spells:
        if spell in secondary_school_spells:
            secondary_school_spells.remove(spell)

    item_names_to_add.extend(primary_school_spells)
    item_names_to_add.extend(secondary_school_spells)

    for item_name in item_names_to_add:
        item_pool.append(world.create_item(item_name))

    ### Handle Modifications to the Starting Inventory
    # for x_location, a value of 0 means starting inventory, hence the "not"
    option_item_pairs = [
        (not(get_option_value(multiworld, player, "mark_location")),"Teleport-Mark"),
        (not(get_option_value(multiworld, player, "mount_location")),"Slot-Mount")
    ]

    for option, item in option_item_pairs:
        starting_item_block = format_starting_item_block(item)
        if option: # add to starting item if option enabled
            world.starting_items.append(starting_item_block)
        elif starting_item_block in world.starting_items: # remove if option not enabled (prevents issues with multiple worlds overlapping)
            world.starting_items.remove(starting_item_block)
    
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

    # weird workaround: this "deduces" what your secondary school is and adds the corresponding rank 1 spell to the pool. if it was added before, it would get put in the starting inventory accidentally.
    schools = ["Balance","Storm","Ice","Fire","Death","Myth","Life","Any","Random"]
    secondary_school = "School-" + schools[get_option_value(multiworld, player, "secondary_school")]
    rank_1_spells = list(world.item_name_groups["SpellCard-Rank 1"])
    
    # find the secondary rank 1 spell and add it to the pool
    for spell_name in rank_1_spells:
        if get_item_school(spell_name,world) == secondary_school:
            item_names_to_add.append(spell_name)

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
    
    to_add = [] # items to add to pool
    to_remove = [] # items to remove from pool
    # populate to_remove with all default filler items
    for item in item_pool:
        if item.name == filler_item_name:
            to_remove.append(item)

    # determine needed items, and amount of non-tc filler
    items_needed = len(to_remove)
    filler_needed = math.floor(items_needed / 5) - 2 # add a non-tc filler every 5 items starting at 11 items
    items_needed -= filler_needed

    useful_filler = list(world.item_name_groups["UsefulFiller"]) # useful filler (rank 2 item cards) is prioritized
    filler_items = list(world.item_name_groups["FillerItem"])

    # remove anything that's already in the pool to avoid duplicate items
    for item in item_pool:
        if item.name in useful_filler:
            useful_filler.remove(item.name)
        if item.name in filler_items:
            filler_items.remove(item.name)

    # populate to_add with enough filler items, prioritizing useful filler
    while filler_needed > 0:
        if useful_filler and multiworld.random.random() < 0.7: # 70% chance for filler item to be useful, while useful items are available in the pool
            item = multiworld.random.choice(useful_filler)
            useful_filler.remove(item)
        else:
            item = multiworld.random.choice(filler_items)
            filler_items.remove(item)
        to_add.append(item)
        filler_needed -= 1

        # break out of the loop if we run out of filler to add (only happens with tons of extra locations)
        if len(useful_filler) + len(filler_items) == 0:
            break

    tc_pool = generate_tc_pool(items_needed,world,multiworld,player)
    for tc_name in tc_pool:
        to_add.append("TreasureCard-" + tc_name)

    # remove the specified items. doing this at the end prevents index errors when iterating
    for item in to_remove:
        item_pool.remove(item)
    # finally, add the specified items
    for item in to_add:
        item_pool.append(world.create_item(item))

    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location
    
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name.startswith("[QL]"):
                    m_loc = multiworld.get_location(location.name[4:], player)
                    location.access_rule = m_loc.access_rule

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
def after_collect_item(world: "ManualWorld", state: CollectionState, Changed: bool, item: Item):
    # Handle Quest Items
    if item.name.startswith("[QI]"):
        # Remove '[QI]' from the item name so item name = location name
        loc_name = item.location.name[4:]
        location_dict = world.location_name_to_location[loc_name]

        try:
            xp = int(location_dict["xp"])
        except KeyError:
            xp = 0 

        if xp > 0:
            state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "xp")] += xp

# This method is run every time an item is removed from the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be first done in after_collect_item
def after_remove_item(world: "ManualWorld", state: CollectionState, Changed: bool, item: Item):
    # Handle Quest Items
    if item.name.startswith("[QI]"):
        # Remove '[QI]' from the item name so item name = location name
        loc_name = item.location.name[4:]
        location_dict = world.location_name_to_location[loc_name]

        try:
            xp = int(location_dict["xp"])
        except KeyError:
            xp = 0 

        if xp > 0:
            state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "xp")] -= xp


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
