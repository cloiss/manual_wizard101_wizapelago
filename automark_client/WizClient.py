from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, server_loop, CommonContext
from worlds.LauncherComponents import icon_paths
import asyncio
import time
import sys
import os
import requests

SYSTEM_MESSAGE_ID = 0

class WizContext(CommonContext):
    # Change name in window
    def make_gui(self) -> "type[kvui.GameManager]":
        from kvui import GameManager

        class TextManager(GameManager):
            base_title = "Manual Wizard101 Auto-Marker Client"

        return TextManager

async def main(args):
    ctx = WizContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    ctx.server_address = None

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