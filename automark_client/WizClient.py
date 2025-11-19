from CommonClient import gui_enabled, get_base_parser, server_loop, CommonContext, ClientCommandProcessor, logger
from worlds.LauncherComponents import icon_paths
from NetUtils import (JSONtoTextParser, RawJSONtoTextParser)
from worlds import network_data_package
import Utils
import asyncio
import typing
import time
import sys
import os
import requests
import subprocess

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

async def automark_loop(ctx: WizContext, log_path):
    old_length = 0
    main_log_msg_dict = {
        1: "[DBGL] SoundSystem     Sound stream |Sound_Dialogue_001|WorldData|Sound/Dialogue/CerenNightchant_001_07.mp3 is ready for playing."
    }
    while not ctx.exit_event.is_set():
        real_log_str = ""
        # Read log
        with open(log_path, "r") as log:
            while real_log_str == "":
                try:
                    log.seek(0)
                    log_str = log.read()
                    new_length = len(log_str)
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
                logger.info("Automark triggered")
        await asyncio.sleep(0.1)

async def main(args):
    ctx = WizContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()
    path = subprocess.run(["powershell", "-Command", "(Get-Process", "-Name", "WizardGraphicalClient", ").Path", ], capture_output=True).stdout.decode("utf-8")
    while path == "":
        path = subprocess.run(["powershell", "-Command", "(Get-Process", "-Name", "WizardGraphicalClient", ").Path", ], capture_output=True).stdout.decode("utf-8")
        logger.info("Could not find Wizard101 log file, retrying...")
        await asyncio.sleep(1)
    real_path = path
    log_path = f"{real_path.split("\\WizardGraphicalClient.exe")[0]}\\WizardClient.log"
    main_automark_loop = asyncio.create_task(
        automark_loop(ctx, log_path), name="WizAutomarkLoop")

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