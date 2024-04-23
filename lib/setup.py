from lib.actions.attack.attack import setupAttack
from lib.actions.clean.clean import locateDropContainer
from lib.actions.destroy.destroy import setup_destroy
from lib.actions.heal.heal import setupHeal
from lib.actions.walk.walk import setupWalk
from lib.config import *
from lib.utils.console import Console
from lib.utils.folder_manager import FolderManager
from lib.utils.window_manager import WindowManager


def setup() -> None:
    """
    Configures the player's character behavior, based on global settings.
    Prints logs indicating the enabled features and their specific settings.

    Returns:
        None
    """
    Console.clear()
    if getProjector():
        WindowManager.activate("Projector")
    else:
        WindowManager.activate("Tibia -")

    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    FolderManager.clear_folder(SESSION_DIR)

    if HEAL:
        setupHeal()
    if DESTROY:
        setup_destroy()
    if ATTACK:
        setupAttack()
    if DROP:
        locateDropContainer()
    if WALK:
        setupWalk()

    FolderManager.open_folder(SESSION_DIR)
    WindowManager.activate("Tibia -")
    WindowManager.activate("session")
    if getProjector():
        WindowManager.activate("Projector")
