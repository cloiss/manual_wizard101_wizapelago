# Wizapelago (Wizard101 Randomizer)
This is a randomizer for Wizard101 developed by Fraxker, Cloiss, and ItzGray. It requires creating a fresh character on a free-to-play account and playing through the first world of the game, completing quests and other objectives to gain randomized abilities and items. A solo game can range from about 2-5 hours depending on settings and luck.

## Getting Started

### Software
You will need the following software:
- [Archipelago ver. 0.6.7](https://github.com/ArchipelagoMW/Archipelago/releases/tag/0.6.7)
- [Manual_Stable_20260319](https://github.com/ManualForArchipelago/Manual/releases/tag/manual_stable_20260319)
- [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases/tag/Tracker_v0.2.32)
- [Wizapelago apworld (Latest Release)](https://github.com/cloiss/manual_wizard101_wizapelago/releases/latest)

Follow the getting started instructions for [Archipelago](https://archipelago.gg/tutorial/Archipelago/setup_en) and [Manual](https://github.com/ManualForArchipelago/Manual/blob/main/docs/manual/overview.md) to learn how to generate, host, and use the Manual client. Universal Tracker is an apworld that you can install to improve the Manual client's functionality.

### Yamls
Six yamls are provided in the repo in the `yamls` folder:
- **Beginner:** Favorable starting inventory, item locations, and logic. Good for a first playthrough.
- **Recommended:** For general play with standard settings. 
- **Insane:** For those looking for a longer or more challenging game with a lot more checks and very limited starting items.
- **Module-Short:** For a short, introductory game, with Harvest Lord as the goal. 
- **Module-Medium:** For a medium-length game, with Melweena Smite as the goal.
- **Module-Long:** For a longer module-based game, ending at Foulgaze. This is perfect if the typical Nightshade ending is just a litle too long.

**It is highly recommended to start from one of these as a baseline when creating your yaml, as playing without the recommended excluded locations is a very bad idea.**

### Auto von WizMark
Auto von WizMark is a separate client we have developed that can automatically mark most of the locations in the game. This is recommended for a more streamlined experience, but not required. **In order for it to work, you must open Wizard101 BEFORE opening Auto von WizMark.** 

It currently has support for automatically marking quest locations, goal locations, some books, and `Talk to Nick Jonas`. Reagents, chests, housing items, smiths, and books must be marked manually.

### Basic Setup

To set up and generate a game of Wizapelago for the first time, follow these steps:

1. **Install the Game apworld**:
   - Download the `manual_wizard101_wizapelago.apworld` file from the [Latest Release on GitHub](https://github.com/cloiss/manual_wizard101_wizapelago/releases/latest) (or locate the [manual_wizard101_wizapelago.apworld](manual_wizard101_wizapelago.apworld) file in the root of this repository).
   - Double-click the downloaded `.apworld` file to automatically install it to Archipelago.

2. **Choose and Position your YAML**:
   - Go to the [yamls](yamls) folder and choose a starting template (e.g., `02-Recommended.yaml`).
   - Open the **Archipelago Launcher**, click **Open Players Folder**, and paste your chosen YAML file there.
   - Open the YAML file in a text editor and change the `name:` field to your desired player name. You can also customize any other options if you wish (see [docs/Options.md](docs/Options.md)).

3. **Generate the Game**:
   - In the **Archipelago Launcher**, click the **Generate** button.
   - This will read the YAML file in the `Players` folder, generate a compressed `.zip` file containing your game data, and place it in the Archipelago `output` directory (the launcher will open this folder automatically once generation completes).

4. **Host the Game on archipelago.gg**:
   - Go to [archipelago.gg](https://archipelago.gg) and navigate to the **Host Game** section (or go directly to [archipelago.gg/uploads](https://archipelago.gg/uploads)).
   - Upload the generated `.zip` file from your local `output` directory.
   - Click **Create Room** to start your server. Make note of the server address and port (e.g. `archipelago.gg:38241`) so you can connect your client.

5. **Connect and Play**:
   - Start **Wizard101** first and log in with your fresh character.
   - (Optional) Launch **Auto von WizMark** if you are using auto-tracking. **Crucial:** You must open Wizard101 *before* launching Auto von WizMark so it can hook into the game correctly.
   - In the **Archipelago Launcher**, launch the **Manual Client**.
   - Enter your server address (e.g., `archipelago.gg:38241`), your slot name (the name from your YAML file), and click **Connect** to link your game to the Archipelago server.

## Read More
For more specific information on the features of Wizapelago, please consult the documents below.

- [Items](https://github.com/cloiss/manual_wizard101_wizapelago/blob/main/docs/Items.md)
- [Locations](https://github.com/cloiss/manual_wizard101_wizapelago/blob/main/docs/Locations.md)
- [Modules](https://github.com/cloiss/manual_wizard101_wizapelago/blob/main/docs/Modules.md)
- [Options](https://github.com/cloiss/manual_wizard101_wizapelago/blob/main/docs/Items.md)
