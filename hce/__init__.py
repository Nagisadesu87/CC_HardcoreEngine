import time, json
from typing import Dict, Any
from typing import List, Tuple
import mcdreforged.api.all as mcdr
from mcdreforged.utils.serializer import Serializable

from .config import Config as cfg
from .command import Command as cmd

global __mcdr_server

# RCON相關
def rcon_execute(command: str):
    global stop_status
    if __mcdr_server.is_rcon_running():
        result = __mcdr_server.rcon_query(command)
        if result == "":
            result = None
    else:
        if not stop_status:
            __mcdr_server.logger.error("伺服器未開啟RCON或伺服器核心已關閉！")
        stop_status = True
        result = None
    return result
    

# 插件載入
def on_load(server: mcdr.PluginServerInterface):
    global __mcdr_server, stop_status
    __mcdr_server = server
    stop_status = False

    # load config
    config = __mcdr_server.load_config_simple(target_class=cfg)

    #load command
    cmd(__mcdr_server, config.permission)
    
# 插件卸載
def on_unload(_):
    global stop_status
    stop_status = True

def on_server_startup(_):
    stop_status = False