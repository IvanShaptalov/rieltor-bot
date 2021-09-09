import configparser
import os
from pathlib import Path

base_dir = Path(__file__).resolve().parent
config = configparser.ConfigParser()
print(base_dir)
config.read(os.path.join(base_dir, "config.ini"))
BOT_TOKEN = config['Bot']['bot_token']

alchemy_db_path = config['DataBase']['sql_alchemy_path']
host = config['Server']['host']
protocol = config['Server']['protocol']
api_key = config['Server']['api_key']
