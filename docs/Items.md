# Items
Access to various abilities within the game is restricted via items. Below is a description of each item category and what you are and aren't allowed to do:

## School
You will receive a School item in the starting inventory. This tells you what school to play as. You can configure your primary and secondary school options in the yaml, which will impact which spell cards are available in the pool. If you select Random secondary school, you will not know your secondary school until you receive non-primary spell card from Ravenwood, such as Thunder Snake, Lightning Bats, Thermic Shield, or Storm Shark for Storm secondary.

## Area
At the beginning of the game, you may only enter Unicorn Way and The Commons. You need access to each other area in the game in order to enter them. This includes side areas such as Golem Court, Pet Pavilion, and Northguard. Note that areas not listed here, such as Colossus Boulevard and The Arcanum, cannot be entered. (except the Drains, see Friendly Teleports)

## Building
Buildings are anywhere you can go to fight something that is locked behind having a quest to enter it. This is mostly instances with sigils for bossfights, but also includes the solo fights Rattlebones, Blackhope, and Judd and the teleporter to the Kraken arena. Always-accessible areas like the Library, Lady Oriel, and Golem Tower are not included.

## Slot
Each equipment slot must be unlocked, except for those that you start with (Wand, Deck, and usually Mount). Once you have the item, you can equip anything to that slot. **Note that Slot-Pet is a required item to complete Judd, as you must use the Play as Pet feature within the tower.**

## Teleport
All forms of teleportation (except fleeing) are treated as a separate item. These are noted below:

- **Teleport-Commons**: Teleport to the common area of the current world.
- **Teleport-Home**: Teleport to your home in Ravenwood. Allowed even if Area-Ravenwood is not unlocked.
- **Teleport-Mark**: Recall to your marked location. Setting a mark is allowed regardless of this item.
- **Teleport-Dungeon**: Allows the use of dungeon recalls. Currently given as a starting item to avoid troublesome earlygame Golem Tower encounters.
- **Teleport-World**: Using the Crowns Shop, click on your main quest and go to the common area of that world.
- **Teleport-Majid**: Using the Crowns Shop, teleport to the Loyalty Store in the Shopping District. This can be used to access Olde Town early, and requires being Level 5.
- **Teleport-Friendly**: Use the Social button to teleport to any friendly player. Expected uses are to reach Golem Court via the Drains, Olde Town via the Bazaar, and any of the Three Streets via teleporting to a random person. This is given as a starting item if `friendly_teleports` is enabled, and otherwise is not an option.

## SpellCard
Every trainable spell card for your primary and secondary school in the accessible areas is an item. You begin with your primary rank 1 spell and must unlock access to use all other spells.

**You may still train spells that you do not have as long as you do not use them.** For example, if you have Lightning Bats but no Thunder Snake, you can still train Thunder Snake in order to train and use Lightning Bats.

## ItemCard
Every item card available on accessible equipment is a potential item. You begin with 3-4 rank 1 item cards (to use on your starting wand) and must unlock access to all other item cards. **Note that you must still have access to the appropriate Vendors and Slots to make use of them.**

Note that some less-useful spell and item cards are not guaranteed to show up in the pool, such as Ice Weakness or Guiding Light.

## TreasureCard
A random assortment of treasure card items will act as filler for any leftover space in the pool. Quest rewards, drops, and especially useful treasure cards are more likely to appear. There are about 10 treasure cards in the pool on default settings.

Treasure cards are **single-use** and may be acquired as drops, quest rewards, or bought from the Library (whose Vendor is in the starting inventory). It is recommended to use a text file to track which Treasure Cards you have used.

Some TreasureCard items give you more freedom by allowing you to use Any Shield, Any Rank 1, or even Any TC. Interpret these as freely as you would like to purchase or use any appropriate treasure card.

## Vendor
Any vendor that you can buy from is locked from the beginning of the game. Once you have the item, you can freely buy any items from that vendor. Of particular note is that the second Crafting quest cannot be completed until `Vendor-Recipes/Reagents` is unlocked.

**Note that you can always talk to Vendors for quests such as Pre-Fears, Trade Voyage, or Skullsplitter regardless of the item.**
