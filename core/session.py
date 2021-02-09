from core import config_loader
import user_config
import mwapi

session = None

def create():
    global session
    session = mwapi.Session(config_loader.config["site"], user_agent="MwsBot/1.0", api_path=config_loader.config["api_path"])

def login():
    status = session.login(user_config.username, user_config.password)
    if status["status"] != "PASS": return False
    print("logged in as", user_config.username)
    return True
