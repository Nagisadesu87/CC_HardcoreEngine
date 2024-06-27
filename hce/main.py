from mcdreforged.api.rcon import rcon
from mcdreforged.api.rcon import RconConnection
import mcdreforged.api.all as mcdr
import time, random

from .util import *

class Main:
    def __init__(self) -> None:
        global game_time, game_status, border_id, server, mc_api
        server = mcdr.ServerInterface
        mc_api = server.get_plugin_instance(plugin_id="minecraft_data_api")
        game_status = False

        # rcon connect
        RconConnection(
            address=get_config_value("system.rconAddress"),
            port=get_config_value("system.rconPort"),
            password=get_config_value("system.rconPassword")
        )
        
        # get game time
        roundTime = get_config_value("game.roundTime")
        game_time = sum(roundTime)

    def annouce_player_pos(self):
        # Implementation needed
        return

    def border_warn(self):
        # Implementation needed
        return

    @mcdr.new_thread("main_thread")
    def main_logic(self):
        self.main_timer(timer_switch = True)

        rcon.send_command(
            f"spreadplayers 0 0 {get_config_value('game.borderRadius')*2 / player_count} "
            f"{get_config_value('game.borderRadius')[0]} false @a[team=game_player]"
        )  # Spread all players in the range

        global border_id
        while border_id < (get_config_value("game.roundCount") - 1):
            if 1 <= border_id <= (get_config_value("game.roundCount") - 2):
                if border_id == 1:
                    rcon.send_command(f"team modify game_player friendlyFire true")
                elif border_id == 4:
                    border_center_pos = [
                        random.randint(get_config_value("game.borderFinalCenterRange")[0], get_config_value("game.borderFinalCenterRange")[1]),
                        random.randint(get_config_value("game.borderFinalCenterRange")[0], get_config_value("game.borderFinalCenterRange")[1])
                    ]
            time.sleep(get_config_value("game.roundTime")[border_id])
            
            self.annouce_player_pos()
            self.border_warn()
            rcon.send_command(
                f"worldborder set {get_config_value('game.borderRadius')[border_id + 1] * 2} {get_config_value('game.borderTime')[0]}"
            )
            
            border_id += 1
        else:
            winner_rawtext = [
                {"text": "獲勝者為 ", "color": "white", "bold": False},
                {"text": "@a[team = game_player]", "color": "yellow", "bold": True},
                {"text": "！", "color": "white", "bold": False}
            ]
            rcon.send_command(f"title @a {winner_rawtext}")

        return
    
    @mcdr.new_thread("timer_thread")
    def main_timer(self, timer_switch: bool = False) -> None:
        global countdown_time
        countdown_time = game_time
        while game_status and timer_switch and countdown_time > 0:
            time.sleep(1.0)
            countdown_time -= 1
        return

    @mcdr.new_thread("info_thread")
    def info_logic(self) -> None:
        # Implementation needed
        return

    def game_start(self, countdown_time: int = 0) -> None:
        global game_status, border_id, border_center_pos, player_count
        while countdown_time > 0:
            time.sleep(1)
            countdown_time -= 1
        
        # initialize
        game_status = True
        border_id = 0
        rcon.send_command(f"team modify game_player friendlyFire false")
        border_center_pos = [0, 0]
        player_count = mc_api.get_player_coordinate()

        # start game
        self.main_logic()

        return
