import pymysql
import config


class Mysql_queries:

    def __init__(self):
        self.connection = pymysql.connect(user=config.user,
                                          password=config.password,
                                          host=config.host,
                                          database=config.database,
                                          cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            self.cursor.execute('SELECT * FROM Music')
            results = self.cursor.fetchall()
            return results

    def select_single(self, id):
        """ Получаем одну строку с номером id """
        with self.connection:
            self.cursor.execute('SELECT * FROM Music WHERE id = ?', (id,))
            results = self.cursor.fetchall()[0]
            return results

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
