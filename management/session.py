from os import path
from typing import NamedTuple
import json
import psycopg2


Session = NamedTuple('Session', (
    ('config', dict),
    ('connection', psycopg2.extensions.connection),
))


def load_config(filename: str) -> dict:
    with open(filename, 'r') as f:
        config = json.load(f)
    return config


def make_session() -> Session:
    base_path = path.dirname(path.dirname(path.abspath(__file__)))
    config_file = path.join(base_path, 'config.json')
    config = load_config(config_file)
    connection=psycopg2.connect(
        dbname=config['DB_NAME'],
        user=config['DB_USER'],
    )
    session = Session(config=config, connection=connection)
    return session
