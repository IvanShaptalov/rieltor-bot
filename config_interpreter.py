import configparser

config = configparser.ConfigParser()
config.read("config.ini")
BOT_TOKEN = config['Bot']['bot_token']

alchemy_db_path = config['DataBase']['sql_alchemy_path']
host = config['Server']['host']
protocol = config['Server']['protocol']
api_key = config['Server']['api_key']
