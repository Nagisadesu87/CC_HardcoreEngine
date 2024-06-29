import mcdreforged.api.all as mcdr
from mcdreforged.api.rtext import RColor, RText, RStyle
import time, random

import minecraft_data_api as mc_api

from .util import *

def annouce_player_pos(server):
    # Implementation needed
    
    return

def border_start(server):
    server.execute(
        f"worldborder set {get_config_value('game.borderRadius')[border_id + 1] * 2} {get_config_value('game.borderTime')[0]}"
    )
    return

def actionbar_display(server, display_type: bool, player_in_range: bool, player_edge_distance: float, player_id: str) -> None:
    if display_type and player_in_range:
        # Border is moving
        if player_in_range:
            # Player in the border range
            msg_rtext = RText("距離次圈邊界", color=RColor.white) + RText(f" {player_edge_distance} m", color=RColor.green, styles=RStyle.bold)
        else:
            # Player not in the range
            msg_rtext = RText("距離次圈邊界", color=RColor.white) + RText(f" {player_edge_distance} m", color=RColor.red, styles=RStyle.bold)
    else:
        # Border is not moving
        if player_in_range:
            # Player in the range
            msg_rtext = RText("距離本圈邊界", color=RColor.white) + RText(f" {player_edge_distance} m", color=RColor.green, styles=RStyle.bold)
        else:
            # Player not in the border range
            msg_rtext = RText("距離本圈邊界", color=RColor.white) + RText(f" {player_edge_distance} m", color=RColor.red, styles=RStyle.bold)
        
    server.execute(f"title {player_id} actionbar {msg_rtext.to_json_str()}")

    return

def bossbar_display(server, display_type: bool) -> None:
    countdown_min, countdown_sec = sec_time_format(countdown_time)
    if display_type:
        # Border is moving
        msg_rtext = RText(f"回合{border_id + 1} / ", color=RColor.white) + RText(f"{countdown_min}:{countdown_sec} ", color=RColor.white, styles=RStyle.bold) + RText(f"(邊界移動中)", color=RColor.gold, styles=RStyle.underlined)
    else:
        # Border is not moving
        border_time_min, border_time_sec = sec_time_format(get_config_value("game.borderTime")[border_id])
        msg_rtext = RText(f"回合{border_id + 1} / ", color=RColor.white) + RText(f"{countdown_min}:{countdown_sec} ", color=RColor.white, styles=RStyle.bold) + RText(f"(邊界移動開始 - {border_time_min}:{border_time_sec})", color=RColor.yellow)
    
    server.execute(f"bossbar set hce_bossbar max {get_config_value('game.borderTime')[border_id]}")
    server.execute(f"bossbar set hce_bossbar value {countdown_time}")
    server.execute(f"bossbar set hce_bossbar name {msg_rtext.to_json_str()}")
    return

def sidebar_display(server, display_type: bool, radius_value: int = 0) -> None:
    if display_type:
        # Final round
        server.execute(f"scoreboard objectives modify hce_sidebar numberformat blank")
        server.execute(f"scoreboard players reset 下次邊界半徑 hce_sidebar")
        server.execute(f"scoreboard players set 最後回合 hce_sidebar 0")
    else:
        # Not final round
        server.execute(f"scoreboard players set 下次邊界半徑 hce_sidebar {radius_value}")
    return

def chat_display(server, player_id: str, player_coord: list) -> None:
    # Implementation needed
    return

@mcdr.new_thread("main_thread")
def main_logic(server = mcdr.ServerInterface):
    server.execute(f"say game start")
    main_timer(server=server, timer_switch=True)
    
    server.execute(
        f"spreadplayers 0 0 {get_config_value('game.borderRadius') * 2 / player_count} "
        f"{get_config_value('game.borderRadius')[0]} false @a[team=game_player]"
    )  # Spread all players in the range

    global border_id
    while border_id < (get_config_value("game.roundCount") - 1):
        if border_id == 1:
            server.execute(f"team modify game_player friendlyFire true")
        elif border_id == (get_config_value("game.roundCount") - 2):
            border_center_pos = [
                random.randint(get_config_value("game.borderFinalCenterRange")[0], get_config_value("game.borderFinalCenterRange")[1]),
                random.randint(get_config_value("game.borderFinalCenterRange")[0], get_config_value("game.borderFinalCenterRange")[1])
            ]
        time.sleep(get_config_value("game.roundTime")[border_id])

        border_id += 1
    else:
        winner_rtext = RText("遊戲結束！", color=RColor.yellow, styles=RStyle.bold)
        server.execute(f"title @a {winner_rtext.to_json_str()}")

    return

@mcdr.new_thread("timer_thread")
def main_timer(server, timer_switch: bool = False) -> None:
    global countdown_time
    while game_status and timer_switch and border_id < get_config_value("game.roundCount"):
        countdown_time = get_config_value("game.roundTime")[border_id]
        while game_status and timer_switch and countdown_time > 0:
            if countdown_time <= get_config_value("game.borderTime")[border_id]:
                server.border_start()
                server.annouce_player_pos()
            time.sleep(1.0)
            countdown_time -= 1
    return

@mcdr.new_thread("info_thread")
def info_logic(server) -> None:
    global has_annouced
    has_annouced = False
    while game_status:
        player_list = mc_api.get_server_player_list()
        for player in player_list:
            temp_coord = mc_api.get_player_coordinate(player)
            player_coord = [temp_coord.x, temp_coord.y, temp_coord.z]
            player_edge_distance = get_edge_distance(player_pos=player_coord)
            border_moving = countdown_time <= get_config_value("game.borderTime")[border_id]
            actionbar_display(server, border_moving, if_pos_in_edge, player_edge_distance, player)
        
        # Round process display logic
        if countdown_time <= get_config_value("game.borderTime")[border_id]:  # Roundtime left <= border time
            bossbar_display(server, False)
        else:
            bossbar_display(server, True)

        # Sidebar display logic
        if border_id < get_config_value("game.roundCount") - 1:
            sidebar_display(server, False, get_config_value("game.borderRadius")[border_id + 1])
        else:
            sidebar_display(server, True, 0)

        # Coordinates announcement logic
        if get_config_value("info.chat.playerPosMode") == "roundEnd":
            if countdown_time == 0 and not has_annouced:
                has_annouced = True
            elif countdown_time != 0 and has_annouced:
                has_annouced = False
        elif get_config_value("info.chat.playerPosMode") == "finalRound":
            if countdown_time == 0 and not has_annouced and border_id == (get_config_value("game.roundCount") - 1):
                has_annouced = True
            elif countdown_time != 0 and has_annouced:
                has_annouced = False

        time.sleep(get_config_value("info.updateInterval"))
    return

def game_start(server = mcdr.ServerInterface, start_countdown_time: int = 0) -> None:
    global game_status, border_id, border_center_pos, player_count, player_list, mc_api

    import sys
    print(sys.path)

    while start_countdown_time > 0:
        time.sleep(1)
        start_countdown_time -= 1
    
    # initialize
    game_status = True
    border_id = 0

    server.execute(f"team add game_player")
    server.execute(f"team join game_player @a")
    server.execute(f"team modify game_player friendlyFire false")

    bossbar_inittext = RText("HCE: Bossbar display is now initializing...")
    server.execute(f"bossbar add hce_bossbar {bossbar_inittext.to_json_str()}")
    server.execute(f"bossbar set hce_bossbar color yellow")
    server.execute(f"bossbar set hce_bossbar style progress")
    server.execute(f"bossbar set hce_bossbar players @a")

    sidebar_titletext = RText(f"2486生存戰", color=RColor.aqua, styles=RStyle.bold)
    server.execute(f"scoreboard objectives add hce_sidebar dummy {sidebar_titletext.to_json_str()}")
    server.execute(f"scoreboard objectives setdisplay sidebar hce_sidebar")
    server.execute(f"scoreboard players set 下次邊界半徑 hce_sidebar {get_config_value('game.borderRadius')[0]}")

    border_center_pos = [0, 0]
    player_count, server_player_limit, player_list = mc_api.get_server_player_list()

    # start game
    main_logic(server=server)
    info_logic()

    return
