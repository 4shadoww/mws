from core import config_loader
import user_config
import mwapi

session = None

def create():
  global session
  session = mwapi.Session(config_loader.config["site"], user_agent="MwsBot/1.0", api_path=config_loader.config["api_path"])

def login():
  session.login(user_config.username, user_config.password)
  return True
