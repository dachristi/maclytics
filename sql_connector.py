
import json

import mysql.connector

class SqlConnector(object):
    with open('mysql_config.json', 'r') as f:
        config = json.load(f)

    def __init__(self):
        self.cnx = mysql.connector.connect(user=SqlConnector.config['mysql']['user'],
                                      password=SqlConnector.config['mysql']['password'],
                                      host=SqlConnector.config['mysql']['host'],
                                      database=SqlConnector.config['mysql']['database'],
                                      auth_plugin='mysql_native_password')
        self.cursor = self.cnx.cursor(dictionary=True)
