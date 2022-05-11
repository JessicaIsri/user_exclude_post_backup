import os

import mysql.connector
import pathlib
import yaml
from yaml.loader import SafeLoader

cwd = pathlib.Path(__file__).parent.parent
with open(os.path.join(cwd, 'credentials.yaml')) as file:
    credentials = yaml.load(file, Loader=SafeLoader)

blacklist = credentials.get('blacklist')
blacklist_connection = mysql.connector.connect(
  host=blacklist.get('host'),
  user=blacklist.get('user'),
  password=blacklist.get('password'),
  database=blacklist.get('database')
)

blacklist_cursor = blacklist_connection.cursor()

persistent_data = credentials.get('persist_data')
persistent_data_connection = mysql.connector.connect(
  host=persistent_data.get('host'),
  user=persistent_data.get('user'),
  password=persistent_data.get('password'),
  database=persistent_data.get('database')
)

base_dir = credentials.get('base_dir')
persistent_data_cursor = persistent_data_connection.cursor()
