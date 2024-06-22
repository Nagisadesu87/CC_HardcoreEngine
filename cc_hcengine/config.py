from mcdreforged.utils.serializer import Serializable

class permissionConfig(Serializable):
    # 0:guest 1:user 2:helper 3:admin 4:owner
    start : int = 3
    config : int = 3

class systemConfig(Serializable):
    rconPort : str = "127.0.0.1",
    rconPassword : str = "password"

class gameConfig(Serializable):
    roundCount : int = 6
    roundTime : list[int] = [1200, 1200, 1200, 1200, 1200, 1200]
    borderRadius : list[int] = [2500, 2000, 1500, 1000, 500, 50]
    borderTime : list[int] = [300, 300, 300, 300, 300, 360]
    borderWarningTime : int = 15
    borderFinalCenterRandom : bool = True
    borderFinalCenterRange : int = [20, 20]

class bossbarConfig(Serializable):
    showRoundCountdown : bool = True
    barColor: str = "yellow"

class sidebarConfig(Serializable):
    titleText : str = {"text":"2486生存戰", "color":"aqua", "bold":"true"}
    showEliminateRank : bool = True
    eliminateRankText : str = "排名"
    showNextBorderRadius : bool = True
    nextBorderRadiusText : str = "下次邊界半徑"

class actionbarConfig(Serializable):
    playerBorderDistanceMode : str = "permanent"
    playerBorderDistanceTime : int = 300

class chatConfig(Serializable):
    playerPosMode: str = "roundEnd"
    playerPosTime: int = 1200

class infoConfig(Serializable):
    bossbar : bossbarConfig = bossbarConfig()
    sidebar : sidebarConfig = sidebarConfig()
    actionbar : actionbarConfig = actionbarConfig()

class Config(Serializable):
    permission : permissionConfig = permissionConfig()
    system : systemConfig = systemConfig()
    game : gameConfig = gameConfig()
    info : infoConfig = infoConfig()

a = "info.bossbar.barColor"
t = ""
for i in a.split("."):
    t += f"[{i}]"
from typing import Dict, Any

c = Config.get_default().serialize()
def get_config_id(nested_config: Dict[str, Any], parent_key: str = "", sep: str = "."):
    """
    Flatten a nested json file.

    Args:
    nested_json (dict): The JSON object to flatten.
    parent_key (str): The base key to prepend to the keys in nested JSON.
    sep (str): The separator to use between key levels.

    Returns:
    dict: A flattened dictionary where keys are dot-separated.
    """
    items = []
    for key, value in nested_config.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(get_config_id(value, new_key, sep=sep).items())
        else:
            items.append((new_key,value))
    return dict(items)

if "system.rconPort" in get_config_id(c).keys():
    print("a")
    