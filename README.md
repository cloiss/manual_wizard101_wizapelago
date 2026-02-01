# Wizard101 Randomizer
This is a randomizer for Wizard101 developed by Fraxker, Cloiss, and ItzGray. It requires creating a fresh character on a free-to-play account and playing through the first world of the game, completing quests to gain randomized abilities and items. A solo game can range from about 2-5 hours depending on settings and luck.

## Getting Started

### Software
You will need the following software:
- [Archipelago ver. 0.6.3](https://github.com/ArchipelagoMW/Archipelago/releases/tag/0.6.3)
- [Manual_Stable_20250813](https://github.com/ManualForArchipelago/Manual/releases/tag/manual_stable_20250813)
- [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases) (not required, but highly recommended)

Follow the getting started instructions for Archipelago and Manual to learn how to generate, host, and use the Manual client. Universal Tracker is an apworld that you can install to improve the Manual client's functionality.

### Yaml
Three yamls are provided in the repo in the `yamls` folder:
- **Beginner:** Good for first-time players, avoids skips and is generous with useful items
- **Recommended:** Default settings optimized for a good experience
- **Evil:** Especially annoying and difficult settings for those who want to suffer

**It is highly recommended to start from one of these as a baseline when creating your yaml, as playing without the recommended excluded locations is a very bad idea.**

## Locations
Every default location (except `Talk to Nick Jonas`) is a Wizard City quest which is accessible on a free-to-play account prior to reaching Level 12. This includes, for example, the first two Photomancy quests, but excludes Gardening and all of Colossus Boulevard.

Quests are named as follows in the randomizer:
**Questgiver: Quest Name (Clarifier)**

- `Questgiver`: The name of the person who gives the quest, or MAIN for main quests.
- `Quest Name`: The exact name of the quest in-game for reference.
- `Clarifier`: A shorthand for what the quest expects from you if the quest name is unclear.

With Universal Tracker enabled, all locations will be highlighted in green when they can be accessed in logic. **Note that some quests may have unintuitive requirements or end points that you are not aware of, such as the Foulgaze quest ending in Haunted Cave.**

Additionally, some quests (e.g. Iron Golem) may be technically reachable but deemed too difficult due to a lack of spells, health, or utilities like Dungeon Recall. These will still appear as green in Universal Tracker, even if they are not technically in logic.

### Reagents
The `reagents` option enables checks for collecting one of each specific reagent that can be found in Wizard City, as well as an additional check for getting any rare reagent. This refers to any reagent found in the "Rare Harvest" category of the reagent menu in-game.

### Halloween
During the Hallowe'en and Eerie April events, 19 additional quests are available from Jack Hallow in The Commons. This option adds a check for each of these quests, and is highly recommended to be enabled when the event is active to add some variety to the game. 

### Modules
Some sections of Wizard City can be selectively disabled or reduced for a shorter game. For example, setting `module_cyclops` to `half` removes about half of the content in Cyclops Lane, leaving only the quests that are accessible by the time you can fight Eyus Maximus. Setting it to `none` completely removes Cyclops Lane from the game, including any quests that visit that area. For full details on what each module setting does, see the setting descriptions in the yaml. This can be used in combination with configuring the goal to be one of the earlier bosses, as described below. 

### Goal
Currently, the default goal location is to defeat Lord Nightshade. Unlike other locations, this goal can be claimed as soon as the boss is defeated, so returning to Daisy Willowmancer to turn in the quest is not required. This also means that the two remaining main quests after the boss are not part of the randomizer. The goal can also be set to a number of other Wizard City bosses for a shorter game in combination with the Modules function above. In all cases, the goal is to defeat the boss, and all associated quests on or after that boss are not part of the randomizer.

## Items
Access to various abilities within the game is restricted via items. Below is a description of each item category and what you are and aren't allowed to do:

### School
You will receive a School item in the starting inventory. This tells you what school to play as. You can configure your primary and secondary school options in the yaml, which will impact which spell cards are available in the pool. If you select Random secondary school, you will not know your secondary school until you receive non-primary spell card from Ravenwood, such as Thunder Snake, Lightning Bats, Thermic Shield, or Storm Shark for Storm secondary.

### Area
At the beginning of the game, you may only enter Unicorn Way and The Commons. You need access to each other area in the game in order to enter them. This includes side areas such as Golem Court, Pet Pavilion, and Northguard. Note that areas not listed here, such as Colossus Boulevard and The Arcanum, cannot be entered. (except the Drains, see Friendly Teleports)

### Building
Buildings are anywhere you can go to fight something that is locked behind having a quest to enter it. This is mostly instances with sigils for bossfights, but also includes the solo fights Rattlebones, Blackhope, and Judd and the teleporter to the Kraken arena. Always-accessible areas like the Library, Lady Oriel, and Golem Tower are not included.

### Slot
Each equipment slot must be unlocked, except for those that you start with (Wand, Deck, and usually Mount). Once you have the item, you can equip anything to that slot. **Note that Slot-Pet is a required item to complete Judd, as you must use the Play as Pet feature within the tower.**

### Teleport
All forms of teleportation (except fleeing) are treated as a separate item. These are noted below:

- **Teleport-Commons**: Teleport to the common area of the current world.
- **Teleport-Home**: Teleport to your home in Ravenwood. Allowed even if Area-Ravenwood is not unlocked.
- **Teleport-Mark**: Recall to your marked location. Setting a mark is allowed regardless of this item.
- **Teleport-Dungeon**: Allows the use of dungeon recalls. Currently given as a starting item to avoid troublesome earlygame Golem Tower encounters.
- **Teleport-World**: Using the Crowns Shop, click on your main quest and go to the common area of that world.
- **Teleport-Majid**: Using the Crowns Shop, teleport to the Loyalty Store in the Shopping District. This can be used to access Olde Town early, and requires being Level 5.
- **Teleport-Friendly**: Use the Social button to teleport to any friendly player. Expected uses are to reach Golem Court via the Drains, Olde Town via the Bazaar, and any of the Three Streets via teleporting to a random person. This is given as a starting item if `friendly_teleports` is enabled, and otherwise is not an option.

### SpellCard
Every trainable spell card for your primary and secondary school in the accessible areas is an item. You begin with your primary rank 1 spell and must unlock access to use all other spells.

**You may still train spells that you do not have as long as you do not use them.** For example, if you have Lightning Bats but no Thunder Snake, you can still train Thunder Snake in order to train and use Lightning Bats.

### ItemCard
Every item card available on accessible equipment is a potential item. You begin with 3-4 rank 1 item cards (to use on your starting wand) and must unlock access to all other item cards. **Note that you must still have access to the appropriate Vendors and Slots to make use of them.**

Note that some less-useful spell and item cards are not guaranteed to show up in the pool, such as Ice Weakness or Guiding Light.

### TreasureCard
A random assortment of treasure card items will act as filler for any leftover space in the pool. Quest rewards, drops, and especially useful treasure cards are more likely to appear. There are about 10 treasure cards in the pool on default settings.

Treasure cards are **single-use** and may be acquired as drops, quest rewards, or bought from the Library (whose Vendor is in the starting inventory). It is recommended to use a text file to track which Treasure Cards you have used.

Some TreasureCard items give you more freedom by allowing you to use Any Shield, Any Rank 1, or even Any TC. Interpret these as freely as you would like to purchase or use any appropriate treasure card.

### Vendor
Any vendor that you can buy from is locked from the beginning of the game. Once you have the item, you can freely buy any items from that vendor. Of particular note is that the second Crafting quest cannot be completed until `Vendor-Recipes/Reagents` is unlocked.

**Note that you can always talk to Vendors for quests such as Pre-Fears, Trade Voyage, or Skullsplitter regardless of the item.**
