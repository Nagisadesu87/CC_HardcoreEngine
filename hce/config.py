from mcdreforged.utils.serializer import Serializable

class permissionConfig(Serializable):
    # 0:guest 1:user 2:helper 3:admin 4:owner
    start : int = 3
    config : int = 3

class systemConfig(Serializable):
    rconAddress : str = "127.0.0.1"
    rconPort : int = 25575
    rconPassword : str = "password"

class gameConfig(Serializable):
    roundCount : int = 6
    roundTime : list[int] = [1200, 1200, 1200, 1200, 1200, 1200]
    borderRadius : list[int] = [2500, 2000, 1500, 1000, 500, 50]
    borderTime : list[int] = [300, 300, 300, 300, 300, 360]
    borderWarningTime : int = 15
    borderFinalCenterRandom : bool = True
    borderFinalCenterRange : list = [20, 20]

class bossbarConfig(Serializable):
    showRoundCountdown : bool = True
    barColor: str = "yellow"

class sidebarConfig(Serializable):
    titleText : dict = {"text":"2486生存戰", "color":"aqua", "bold":"true"}
    showEliminateRank : bool = True
    eliminateRankText : str = "排名"
    showNextBorderRadius : bool = True
    nextBorderRadiusText : str = "下次邊界半徑"

class actionbarConfig(Serializable):
    playerBorderDistanceMode : str = "permanent"
    playerBorderDistanceTime : int = 300

class chatConfig(Serializable):
    playerPosMode: str = "roundEnd"

class infoConfig(Serializable):
    updateInterval : float = 0.5
    bossbar : bossbarConfig = bossbarConfig()
    sidebar : sidebarConfig = sidebarConfig()
    actionbar : actionbarConfig = actionbarConfig()
    chat : chatConfig = chatConfig()

class Config(Serializable):
    permission : permissionConfig = permissionConfig()
    system : systemConfig = systemConfig()
    game : gameConfig = gameConfig()
    info : infoConfig = infoConfig()