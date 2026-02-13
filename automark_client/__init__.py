from typing import Callable, Optional

import Utils
from worlds.LauncherComponents import Component, components, Type, launch_subprocess, icon_paths

# Pretty much this entire file is mangled code from Manual
class VersionedComponent(Component):
    def __init__(self, display_name: str, script_name: Optional[str] = None, func: Optional[Callable] = None, version: int = 0, file_identifier: Optional[Callable[[str], bool]] = None, icon: Optional[str] = None):
        super().__init__(display_name=display_name, script_name=script_name, func=func, component_type=Type.CLIENT, file_identifier=file_identifier, icon=icon)
        self.version = version

def launch_client(*args):
    import CommonClient
    from .WizClient import launch as Main

    if CommonClient.gui_enabled:
        launch_subprocess(Main, name="Wizard101 Auto-Marking Client")
    else:
        Main()

def add_client_to_launcher() -> None:
    version = 0.1
    found = False

    if "w101" not in icon_paths:
        icon_paths["w101"] = Utils.user_path('data', 'wiz.png')

    for c in components:
        if c.display_name == "Wizard101 Auto-Marking Client":
            found = True
            if getattr(c, "version", 0) < version:
                c.version = version
                c.func = launch_client
                c.icon = "w101"

    if not found:
        components.append(VersionedComponent("Wizard101 Auto-Marking Client", "WizClient", func=launch_client, version=version, icon="w101"))

add_client_to_launcher()