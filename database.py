import psycopg2
import config as pd


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=pd.host,
            user=pd.user,              
            password=pd.password,
            database=pd.db_name
            
        )  #В файле config.py лежат переменные, в которых содержатся данные для подключения к БД
        self.cursor = self.connection.cursor()


    def add_user(self,user_id,user_name):
        with self.connection:
            self.cursor.execute('INSERT INTO users (user_id, user_name) VALUES (%s, %s);', (user_id, user_name))
            self.connection.commit()


    def select_user_by_id(self, user_id):
        with self.connection:
            self.cursor.execute('SELECT user_name FROM users WHERE user_id = %s;',(user_id,))
            data = self.cursor.fetchone()
            if data != None:
                return ''.join(data)
            else:
                return None

    def delete_user_by_id(self, user_id):
        with self.connection:
            self.cursor.execute("DELETE FROM users WHERE user_id = %s;",(user_id,))
            self.connection.commit()
    
    def select_all_users(self):
        array = []
        with self.connection:
            self.cursor.execute("SELECT user_id FROM users;")
            data = self.cursor.fetchall()
            for row in data:
                array.append(row[0])
            return array
    #-------------------DEBUG--------------------------------        
    def check_table_data(self):
        with self.connection:
            self.cursor.execute('SELECT * FROM users;')
            return self.cursor.fetchall()


p = Database()

# print(p.select_all_users())
print(p.check_table_data())