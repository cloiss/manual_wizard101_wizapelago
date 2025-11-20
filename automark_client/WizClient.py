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

async def automark_loop(ctx: WizContext):
    path = subprocess.run(["powershell", "-Command", "(Get-Process", "-Name", "WizardGraphicalClient", ").Path", ], capture_output=True).stdout.decode("utf-8")
    if path == "":
        ctx.exit_event.set()
        logger.info("ERROR: Wizard101 client is not running. The automark client will not work. Please start Wizard101, reopen the client and try again.")
        return
    real_path = path
    log_path = f"{real_path.split("\\WizardGraphicalClient.exe")[0]}\\WizardClient.log"
    old_length = 0
    try:
        locations_data = load_data_file("locations.json")
        main_log_msg_dict = {}
        id_counter = 1
        for location in locations_data["data"]:
            try:
                main_log_msg_dict[id_counter] = location["log_msg"]
            except:
                pass
            id_counter += 1
    except Exception as e:
        ctx.exit_event.set()
        logger.info("ERROR: Could not load locations.json file. The automark client will not work. Please ensure the file exists, reopen the client and try again.")
        logger.info(f"Exception details: {e}")
        return
    await asyncio.sleep(0.1)
    while not ctx.exit_event.is_set():
        real_log_str = ""
        # Read log
        with open(log_path, "r") as log:
            while real_log_str == "":
                try:
                    log.seek(0)
                    log_str = log.read()
                    new_length = len(log_str)
                    if old_length == 0:
                        old_length = new_length
                        continue
                    if log_str[-1] == "\n":
                        log_str = log_str[:-1]
                    if new_length > old_length:
                        real_log_str = log_str[old_length:]
                    elif new_length < old_length:
                        real_log_str = log_str
                    old_length = new_length
                except Exception as e:
                    logger.info(f"Error reading log file: {e}")
                await asyncio.sleep(0.1)
        # Process log lines
        for key, value in main_log_msg_dict.items():
            if value in real_log_str:
                ctx.locations_checked.add(key)
                sync_msg = [{"cmd": "Sync"}, {"cmd": "LocationChecks", "locations": [key]}]
                await ctx.send_msgs(sync_msg)
        await asyncio.sleep(0.1)

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