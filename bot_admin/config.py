from dataclasses import dataclass
from environs import Env

@dataclass
class DBConfig:
    name : str
    user : str
    password : str
    host : str
    port : str

@dataclass
class DJangoConfigClass:
    secret_key : str

@dataclass
class Config:
    django_config : DJangoConfigClass
    db_config : DBConfig


def load_config( path : None | str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(  django_config = DJangoConfigClass(secret_key = env('DJ_SECRET_KEY')),
                    db_config = DBConfig(   name = env('DB_NAME'),
                                            user = env('DB_USER'),
                                            password = env('DB_PASSWORD'),
                                            host = env('DB_HOST'),
                                            port = env('DB_PORT')))