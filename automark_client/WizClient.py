from CommonClient import gui_enabled, get_base_parser, server_loop, CommonContext, ClientCommandProcessor, logger
from worlds.LauncherComponents import icon_paths
import Utils
import asyncio
import typing
import time
import sys
import os
import requests
import subprocess
import json
import pkgutil

# This does some minor changes to CommonContext to change the window title and mirror the login behavior of Manual
class WizContext(CommonContext):
    items_handling = 0b111
    # Change name in window
    def make_gui(self) -> "type[kvui.GameManager]":
        from kvui import GameManager

        class TextManager(GameManager):
            base_title = "Archipelago Manual Wizard101 Auto-Marker Client"

        return TextManager
    
    # Pretty much entirely taken from TextContext in Archipelago text client
    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(WizContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game="Manual_Wizard101_Cloiss")

# blatantly copied from Manual, which coincidentally also blatantly copies this from the Minecraft apworld. What a cycle
def load_data_file(fname: str) -> dict:
    try:
        filedata = json.loads(pkgutil.get_data(__name__, fname).decode())
    except:
        filedata = []

    return filedata

# The main automark loop
async def automark_loop(ctx: WizContext):
    # Get Wizard101 client path
    path = subprocess.run(["powershell", "-Command", "(Get-Process", "-Name", "WizardGraphicalClient", ").Path", ], capture_output=True).stdout.decode("utf-8")
    # If path is empty (meaning the game is not open), stop the loop function
    if path == "":
        ctx.exit_event.set()
        logger.info("ERROR: Wizard101 client is not running. The automark client will not work. Please start Wizard101, reopen the client and try again.")
        return
    log_path = f"{path.split("\\WizardGraphicalClient.exe")[0]}\\WizardClient.log"
    old_length = 0
    # Load location data
    try:
        locations_data = load_data_file("locations.json")
        main_log_msg_dict = {}
        for id, location in enumerate(locations_data["data"], start=1):
            log_msg = location.get("log_msg", None)
            if log_msg is not None:
                main_log_msg_dict[log_msg] = id
    # If locations.json isn't found (likely because of a packaging error), stop the loop function
    except Exception as e:
        ctx.exit_event.set()
        logger.info("ERROR: Could not load locations.json file. The automark client will not work. Please ensure the file exists, reopen the client and try again.")
        logger.info(f"Exception details: {e}")
        return
    await asyncio.sleep(0.1)
    # Actual main automark loop
    while not ctx.exit_event.is_set():
        log_str = ""
        # Read log
        with open(log_path, "r") as log:
            while log_str == "":
                try:
                    log.seek(0)
                    log_lines = log.readlines()
                    new_length = len(log_lines)
                    if old_length == 0:
                        old_length = new_length
                        continue
                    if new_length >= old_length:
                        log_lines = log_lines[old_length - 1:]
                    log_str = "".join(log_lines)
                    old_length = new_length
                except Exception as e:
                    logger.info(f"Error reading log file: {e}")
                await asyncio.sleep(0.1)
        # Process log lines and, if a match is found with a location's log message, mark it
        for msg in main_log_msg_dict:
            if msg in log_str:
                id = main_log_msg_dict[msg]
                ctx.locations_checked.add(id)
                sync_msg = [{"cmd": "Sync"}, {"cmd": "LocationChecks", "locations": [id]}]
                await ctx.send_msgs(sync_msg)
        await asyncio.sleep(0.1)

# This function and the launch function are both mangled Manual code
async def main(args):
    ctx = WizContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()
    main_automark_loop = asyncio.create_task(
        automark_loop(ctx), name="WizAutomarkLoop")

    await ctx.exit_event.wait()
    ctx.server_address = None

    await main_automark_loop

    await ctx.shutdown()

def launch() -> None:
    import colorama

    parser = get_base_parser(description="Manual Wizard101 Auto-Marker Client")

    args = sys.argv[1:]
    args, rest = parser.parse_known_args(args=args)
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()

    if not os.path.exists(icon_paths["w101"]):
        # Download the icon for next time
        icon_url = "https://manualforarchipelago.github.io/ManualBuilder/images/ap-manual-discord-logo-square-96x96.png"
        with open(icon_paths["w101"], 'wb') as f:
            f.write(requests.get(icon_url).content)

if __name__ == '__main__':
    launch()