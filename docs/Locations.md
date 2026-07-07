# Locations (AKA Checks)
Every default location (except `Talk to Nick Jonas`) is a Wizard City quest which is completable on a free-to-play account prior to reaching Level 12. This includes, for example, the first two Photomancy quests, but excludes Gardening and all of Colossus Boulevard.

Quests are named as follows in the randomizer:
**Questgiver: Quest Name (Clarifier)**

- `Questgiver`: The name of the person who gives the quest, or MAIN for main quests.
- `Quest Name`: The exact name of the quest in-game for reference.
- `Clarifier`: A shorthand for what the quest expects from you if the quest name is unclear.

With Universal Tracker enabled, all locations will be highlighted in green when they can be accessed in logic. **Note that some quests may have unintuitive requirements or end points that you are not aware of, such as the Foulgaze quest ending in Haunted Cave.**

Additionally, some quests (e.g. Iron Golem) may be technically reachable but deemed too difficult due to a lack of spells, health, level, or utilities like Dungeon Recall. These will typically still appear as green in Universal Tracker, even if they are not technically in logic.

## Reagents
The `reagents` option enables checks for collecting specific reagents, as well as an additional check for getting any rare reagent. These checks can be area-specific (e.g. `Cat Tail (Unicorn Way)`) or general (e.g. `Cat Tail (Anywhere)`). This refers to any reagent found in the "Rare Harvest" category of the reagent menu in-game.

There is also an additional `ore` setting within the `reagents` option that enables only a single check for finding Ore anywhere.

## Housing Items
The `housing_items` option enables checks for collecting each interactable housing item that can be found out in the open in Wizard City. The naming and categorization of these checks will help inform you on where these are located.

## Wooden and Silver Chests
The `wooden_chests` and `silver_chests` options enable checks for Wooden and Silver Chests respectively in Wizard City. Similar to Reagents, these can be area-specific (e.g. `Wooden Chest (Unicorn Way)`) or general (e.g. `Wooden Chest (Anywhere)`).

## Smiths
The `find_the_smiths` option enables checks for reaching each of the hidden Smiths for Prospector Zeke's quest "Find the Smiths". Note that having access to the quest is required before you can begin collecting these checks. 

There is a secret option to have a single combined check for finding all accessible Smiths, but this is currently hidden due to being unintuitive.

## Books
The `find_the_books` option enables checks for reading various books throughout Wizard City. With the `bosses` option, only the 6 available books from Boris Tallstaff's quest "The Lore You Know" are included. The `all` option includes several other quests. Some of these books have audio, meaning Auto von WizMark will mark them for you, but others do not. 

There is a secret option to have a single combined check for finding all accessible Books for "The Lore You Know", but this is currently hidden due to being unintuitive.

## Halloween
During the Hallowe'en and Eerie April events, 19 additional quests are available from Jack Hallow in The Commons. This option adds a check for each of these quests, as well as some checks in Apprentice Tower. It is highly recommended to be enabled when the event is active to add some variety to the game. 

## Goal
Currently, the default goal location is to defeat Lord Nightshade. Unlike other locations, this goal can be claimed as soon as the boss is defeated, so returning to Daisy Willowmancer to turn in the quest is not required. This also means that the two remaining main quests in Wizard City after the boss are not part of the randomizer. The goal can also be set to a number of other Wizard City bosses for a shorter game (see [Modules](https://github.com/cloiss/manual_wizard101_wizapelago/blob/main/docs/Modules.md)). In all cases, the goal is to defeat the boss, and all associated quests thereafter are not part of the randomizer.
