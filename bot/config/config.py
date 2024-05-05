from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token : str
    public_name : str
    debug : bool
    lang : str

@dataclass
class Payment:
    provider_token : str

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
    payment : Payment

def load_config( path : None | str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot = TgBot(token = env('BOT_TOKEN'),
                                public_name = env('PUBLIC_NAME'),
                                debug = True if env('DEBUG') == 'True' else False,
                                lang = env('LANGUAGE')),
                  db_config = DBConfig(   name = env('POSTGRES_DB'),
                                            user = env('POSTGRES_USER'),
                                            password = env('POSTGRES_PASSWORD'),
                                            host = env('POSTGRES_HOST'),
                                            port = env('POSTGRES_PORT')),
                  payment = Payment(provider_token = env('PROVIDER_TOKEN')))

CONFIG : Config = load_config()