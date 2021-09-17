import configparser
import os
import re
from pathlib import Path
from icecream import ic


def database_link():
    pre_database_url = os.environ.get('DATABASE_URL')
    if pre_database_url is None:
        return None
    print('database: ', pre_database_url)
    arr = re.split(pattern=r'[:|@|/]', string=pre_database_url)
    while '' in arr:
        arr.remove('')

    name = arr[5]
    print(name)
    print('info from arr ', len(arr))
    user = arr[1]
    password = arr[2]
    host_db = arr[3]
    port = arr[4]
    db_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(user, password, host_db, name)
    return db_path


base_dir = Path(__file__).resolve().parent
config = configparser.ConfigParser()
print(base_dir)
config.read(os.path.join(base_dir, "config.ini"))
# solved create database in heroku

BOT_TOKEN = config['Bot']['bot_token'] or os.environ.get('bot_token')
alchemy_db_path_local = 'sqlite:///' + os.path.join(base_dir, config['DataBase']['sql_alchemy_path'])

alchemy_db_path = database_link() or alchemy_db_path_local
ic(alchemy_db_path)
host = config['Server']['host'] or os.environ.get('host')
protocol = config['Server']['protocol'] or os.environ.get('protocol')
api_key = config['Server']['api_key'] or os.environ.get('server_api_key')
manager_link = config['Links']['manager_link'] or os.environ.get('manager_link')

