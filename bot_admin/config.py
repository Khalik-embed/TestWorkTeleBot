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
    debug : bool
    lang : str
@dataclass
class Config:
    django_config : DJangoConfigClass
    db_config : DBConfig



def load_config( path : None | str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        django_config = DJangoConfigClass(
            secret_key = env('DJ_SECRET_KEY'),
            debug = True if env('DEBUG') == 'True' else False,
            lang = env('LANGUAGE')),
        db_config = DBConfig(
            name = env('POSTGRES_DB'),
            user = env('POSTGRES_USER'),
            password = env('POSTGRES_PASSWORD'),
            host = env('DB_HOST'),
            port = env('POSTGRES_PORT')))

CONFIG = load_config()