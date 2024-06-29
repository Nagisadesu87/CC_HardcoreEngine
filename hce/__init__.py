import collections
from typing import Dict, Any, Optional, Union, Tuple, List
from typing import List, Tuple
import mcdreforged.api.all as mcdr
from mcdreforged.utils.serializer import Serializable
import sys

from .config import Config as cfg
from .command import Command as cmd

global __mcdr_server

# 插件載入
def on_load(server: mcdr.PluginServerInterface, prev):
    global __mcdr_server, stop_status, player_data_getter, server_data_getter
    
    __mcdr_server = server


    # if hasattr(prev, 'player_data_getter'):
    #     player_data_getter.queue_lock = prev.player_data_getter.queue_lock
    #     player_data_getter.work_queue = prev.player_data_getter.work_queue
    # if hasattr(prev, 'server_data_getter'):
    #     server_data_getter.player_list = prev.server_data_getter.player_list
    
    stop_status = False
    # load config
    config = __mcdr_server.load_config_simple(target_class=cfg)
    server.logger.info(sys.path)
    #load command
    cmd(__mcdr_server, config.permission)
    

# 插件卸載
def on_unload(_):
    global stop_status
    stop_status = True

def on_server_startup(_):
    stop_status = False
