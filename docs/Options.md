# Options
Some other settings are available for configuring the game's difficulty and length as desired.

## Special Item Locations
Some items can be guaranteed to be found before specific major progress checkpoints: Start, Rattlebones, Muldoon, or Mid-Streets. Selecting `start` will grant the item in the starting inventory, while selecting `anywhere` will place no restriction. The `mid-streets` option refers to the Cyclops/Fodder/Bubbles, Harvest Lord/Nexus, and Fodder/Bastilla quests.

These items are:
- `Teleport-Mark`: Starting item by default. Placing this into the world makes earlygame traversal take longer until it is found. 
- `Slot-Mount`: Starting item by default. Placing this into the world makes earlygame traversal take MUCH longer - selecting anything past Rattlebones is strongly discouraged.
- `Rank 2 Spell`: Can be anywhere by default, but can be guaranteed earlier to ensure consistent, reliable damage by the midgame if desired.
- `Teleport Button`: Can be anywhere by default. This refers to World, Commons, or Home teleports which can be used for faster questing.

## Starting Inventory
Certain key items (beyond Mark and Mount) can be configured in the starting inventory. This is broken down into two sections: non-combat and combat.

### Non-Combat Items
- `Vendor-Library`: Included by default, this allows TreasureCard items to be useful early in a pinch. 
- `Vendor-Potions`: Excluded by default, but recommended for beginners just for smoother, faster play if deaths are common. 
- `All Vendors`: Excluded by default, this is primarily useful when playing with settings that have very few locations (e.g. the Short and Medium module settings)
- `Teleport-Dungeon`: Included by default to avoid issues with retrying bosses and towers. Turn this off for an extra challenge (e.g. Insane settings)
- `All Teleports`: Excluded by default, this is for those who want the randomizer not to restrict how fast you can get from quest to quest, streamlining the game.

### Combat Items
The default recommended starting kit for combat includes your primary level 1 spell (e.g. Frost Beetle for Ice wizards) and 3 random rank 1 item cards for use with the starting wand. This is enough damage to defeat Rattlebones, but not do much else. Reducing starting damage past this point is possible (e.g. Insane settings starts with no damage) but may lead to a frustrating or slow Unicorn Way.

- `ItemCard-Thunder Snake` - Excluded by default, but recommended for beginners or for a faster Unicorn Way. You are otherwise at the mercy of RNG to start with a 'good' spell.
- `SpellCard-Pixie` - Excluded by default, but recommended for beginners only who may struggle with an early lack of healing or defensive options.
- `Primary Rank 1` - (e.g. Frost Beetle for Ice wizards) Included by default, and highly recommended. 
- `Primary Rank 2` - (e.g. Snow Serpent for Ice wizards) Excluded by default, and strongly discouraged as it may make combat portions of the game too straightforward. 
- `Rank 1 Item Cards` - Set to 3 by default, can be anything from 0 to 7. This does not include the Thunder Snake from the setting above. 

## Miscellaneous Options

### Friendly Teleports
Use the Social button to teleport to any friendly player. Expected uses are to reach Golem Court via the Drains, Olde Town via the Bazaar, and any of the Three Streets via teleporting to a random person. This is given as a starting item if `friendly_teleports` is enabled, and otherwise is disallowed. This creates a more varied earlygame which can involve visiting some locations out of order. 

### Beginner Logic
Beginner Logic does two things:
- **Easier Combat**: Difficult sections such as Golem Tower have higher requirements for damage or player level before they are required in logic.
- **Straightforward Logic**: Logic which requires specific quest knowledge, such as defeating Rotting Fodders or Haunted Minions in unintended locations, is disabled. 