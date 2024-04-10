from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token : str
    public_name : str

@dataclass
class DBConfig:
    name : str
    user : str
    password : str
    host : str
    port : str

@dataclass
class Config:
    tg_bot :  TgBot
    db_config : DBConfig

def load_config( path : None | str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot = TgBot(token=env('BOT_TOKEN'),
                                public_name=env('PUBLIC_NAME')),
                  db_config = DBConfig(   name = env('DB_NAME'),
                                            user = env('DB_USER'),
                                            password = env('DB_PASSWORD'),
                                            host = env('DB_HOST'),
                                            port = env('DB_PORT')))

CONFIG : Config = load_config()