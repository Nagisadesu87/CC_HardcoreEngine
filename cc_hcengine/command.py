import mcdreforged.api.all as mcdr
from mcdreforged.utils.serializer import *

from typing import Any, Dict
import time,os,re

from .config import Config

global config_id

def get_config_id(nested_config: Dict[str, Any], parent_key: str = "", sep: str = "."):
    items = []
    for key, value in nested_config.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(get_config_id(value, new_key, sep=sep).items())
        else:
            items.append((new_key,value))
    return dict(items)

def get_config_key(flatted_config_id: str, sep: str = "."):
	if len(flatted_config_id.split(sep)) == 2:
		return [flatted_config_id.split(sep)[0],  flatted_config_id.split(sep)[1]]
	elif len(flatted_config_id.split(sep)) == 3:
		return [flatted_config_id.split(sep)[0], flatted_config_id.split(sep)[1], flatted_config_id.split(sep)[2]]
	else:
		return

class Command:
	def __init__(self, mcdr_server, permission) -> None:
		self.__mcdr_server = mcdr_server
		self.permission = permission
		self.create_command()
		pass
	
	# create command
	def create_command(self):
		builder = mcdr.SimpleCommandBuilder()
		builder.command("!!hce", self.show_help)
		builder.command("!!hce start", self.start_game)
		builder.command("!!hce start <time>", self.start_game_time)
		builder.command("!!hce config set <config_id> <value>", self.config_set)
		builder.command("!!hce config query <config_id>", self.config_query)

		builder.arg("time", mcdr.Integer)
		builder.arg("config_id", mcdr.Text)
		builder.arg("value", mcdr.Text)

		builder.register(self.__mcdr_server,)

		self.__mcdr_server.resister_help_message("!!hce", "顯示 HardcoreEngine 的指令提示列表")

	def show_help(self, source: mcdr.CommandSource):
		help_msg_lines = """
====== 生存戰系統 HardcoreEngine ======
本插件用於類UHC的極限模式生存戰
*施工中，相信之後會有的 :)*
============
"""
		help_msg_rtext = mcdr.RTextList()
		source.reply(help_msg_rtext)

	# start 指令
	def start_game(self, source: mcdr.CommandSource, context: mcdr.CommandContext):
		# 檢查權限
		if not source.has_permission_higher_than(self.permission["start"]):
			source.reply(f"§4權限不足！你至少需要 {self.permission["start"]} 級或以上！")
			return
		
		# 開始比賽

	def start_game_time(self, source: mcdr.CommandSource, context: mcdr.CommandContext):
		# 檢查權限
		if not source.has_permission_higher_than(self.permission["start"]):
			source.reply(f"§4權限不足！你至少需要 {self.permission["start"]} 級或以上！")
			return
		
		# 計時後開始比賽

	def config_set(self, source: mcdr.CommandSource, context: mcdr.CommandContext):
		# 檢查權限
		if not source.has_permission_higher_than(self.permission["config"]):
			source.reply(f"§4權限不足！你至少需要 {self.permission["config"]} 級或以上！")
			return
		
		# 取得指令參數並將設定值更改為輸入值
		config_id_dict = get_config_id(Config.get_default().serialize())
		if context["config_id"] in config_id_dict.keys():
			if len(get_config_key(context["config_id"])) == 2:
				config_id_dict[get_config_key(context["config_id"])[0]][get_config_key(context["config_id"][1])] = context["value"]
				edited_config = deserialize(config_id_dict)
			elif len(get_config_key(context["config_id"])) == 3:
				config_id_dict[get_config_key(context["config_id"])[0]][get_config_key(context["config_id"][1])][get_config_key(context["config_id"][2])] = context["value"]
				edited_config = deserialize(config_id_dict)
			mcdr.PluginServerInterface.save_config_simple(config=edited_config)
			source.reply(f"\"{context["config_id"]}\" 的設定值已變更為 \"{context["value"]}\"")
		else:
			source.reply(f"§4輸入的 Config ID 不存在")
			return

	def config_query(self, source: mcdr.CommandSource, context: mcdr.CommandContext):
		if not source.has_permission_higher_than(self.permission["config"]):
			source.reply(f"§4權限不足！你至少需要 {self.permission["config"]} 級或以上！")
			return
		
		# 取得指令參數並回覆查詢的值
		config_id_dict = get_config_id(Config.get_default().serialize())
		if context["config_id"] in config_id_dict.keys():
			cmd_config_id = context["config_id"]
			source.reply(f"Config ID \"{context["config_id"]}\" 的設定值為 \"{config_id_dict[context["config_id"]]}\"")
		else:
			source.reply(f"§4輸入的 Config ID 不存在")
			return