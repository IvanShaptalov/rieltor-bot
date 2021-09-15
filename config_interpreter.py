import configparser
import os
from pathlib import Path

from icecream import ic

base_dir = Path(__file__).resolve().parent
config = configparser.ConfigParser()
print(base_dir)
config.read(os.path.join(base_dir, "config.ini"))
BOT_TOKEN = config['Bot']['bot_token']

alchemy_db_path = 'sqlite:///' + os.path.join(base_dir, config['DataBase']['sql_alchemy_path'])
ic(alchemy_db_path)
host = config['Server']['host']
protocol = config['Server']['protocol']
api_key = config['Server']['api_key']
manager_link = os.environ.get('manager_link') or config['Links']['manager_link']
