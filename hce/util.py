import mcdreforged.api.all as mcdr
from mcdreforged.utils.serializer import Serializable
from typing import Any, Dict, List, Tuple
import math

from .config import Config as cfg

def get_config_id_dict(nested_config: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict:
    """
    Make nested config dictionary to flatted config dictionary, which is seperated with "."
    """
    items = []
    for key, value in nested_config.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(get_config_id_dict(value, new_key, sep=sep).items())
        else:
            items.append((new_key,value))
    return dict(items)

def get_config_key(config_id: str, sep: str = ".") -> List:
    """
    Spilt config id by "." to keys.
    """
    items = []
    for i in config_id.split(sep):
        items.append(i)
    return items

def get_config_value(config_id: str, config_dict: Dict[str, Any] = cfg) -> Any:
    """
    Get the config value by config id.
    """
    return get_config_id_dict(config_dict.get_default().serialize())[config_id]

def get_edge_distance(player_pos: list[float, float], edge_center_pos: list[int, int], edge_radius: float) -> float:
    """
    Get the player's distance to the edge.
    """
    intersection = [0, 0]
    if edge_center_pos[0] == player_pos[0]:
        intersection[0] = edge_center_pos[0]
        intersection[1] = edge_center_pos[1] + edge_radius if player_pos[1] > edge_center_pos[1] else edge_center_pos[1] - edge_radius
    else:
        m = (player_pos[1] - edge_center_pos[1]) / (player_pos[0] - edge_center_pos[0])
        if abs(m) <= 1:
            if player_pos[0] > edge_center_pos[0]:
                intersection[0] = edge_center_pos[0] + edge_radius
            else:
                intersection[0] = edge_center_pos[0] - edge_radius
            intersection[1] = edge_center_pos[1] + m * (intersection[0] - edge_center_pos[0])

    d = math.sqrt((intersection[0] - player_pos[0]) ** 2 + (intersection[1] - player_pos[1]) ** 2)
    return d

def if_pos_in_edge(player_pos: list[float, float], edge_center_pos: list[int, int], edge_radius: float) -> bool:
    """
    Calculate player is inside the edge or not.
    """
    return (edge_center_pos[0] - edge_radius <= player_pos[0] <= edge_center_pos[0] + edge_radius) and (edge_center_pos[1] - edge_radius <= player_pos[1] <= edge_center_pos[1] + edge_radius)

def sec_time_format(sec_time:int) -> Tuple:
    """
    Exchange the time from second to formatted time (mm:ss).
    """
    return (sec_time//60, sec_time%60)