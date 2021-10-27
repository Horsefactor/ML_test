import mysql.connector as pymysql
from config import config


class ConnectionMySQL:
    __connection = None
    __cursor = None

    def __init__(self, db):
        __db_config = config['mysql']
        self.__connection = pymysql.connect(host=__db_config['host'],
                                            user=__db_config['user'],
                                            password=__db_config['password'],
                                            database=db,
                                            port=__db_config['port'])
        self.__cursor = self.__connection.cursor()

    def query(self, query, params):
        self.__cursor.execute(query, params)
        return self.__cursor

    def close(self):
        self.__connection.close()
