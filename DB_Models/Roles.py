import pymysql

import config


class Roles:

    def __init__(self):
        self.connection = pymysql.connect(user=config.user,
                                          password=config.password,
                                          host=config.host,
                                          database=config.database,
                                          cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def select_all(self):

        with self.connection:
            self.cursor.execute('SELECT * FROM Roles')
            results = self.cursor.fetchall()
            return results

    def select_single(self, id1):

        with self.connection:
            query = f"SELECT * FROM roles WHERE id={id1}"
            self.cursor.execute(query)
            results = self.cursor.fetchall()[0]
            return results["role_name"]

    def update_record(self, id, role_name):

        with self.connection:
            self.cursor.execute('SELECT * FROM Roles WHERE id = ?', (id,))
            result = self.cursor.fetchall()[0]
            print(result)
            # self.cursor.execute('Update Roles WHERE id = ?', (id,))
            # results = self.cursor.fetchall()[0]
            return result

    def delete_record(self, id):
        with self.connection:
            self.cursor.execute('SELECT * FROM Roles WHERE id = ?', (id,))
            results = self.cursor.fetchall()[0]
            return results


    def close(self):

        self.connection.close()