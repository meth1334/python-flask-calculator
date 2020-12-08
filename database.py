import mysql.connector 
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query, read = False):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        if read:
            return cursor.fetchall()
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")
        return e

def save_info(date, ip_addr, calculation, result, connection):
    query = f"INSERT INTO KALKULATOR(IP_ADDR, DATE, CALCULATION, RESULT) VALUES('{ip_addr}','{date}','{calculation}','{result}');"
    print(query)
    execute_query(connection, query)
   
def read_info(connection):
    query = "SELECT * FROM KALKULATOR;"
    return execute_query(connection, query, True)

def add_user(ip_addr, login, password, connection):
    query = f"INSERT INTO user(IP_ADDR, LOGIN, PASSWORD) VALUES('{ip_addr}','{login}','{password}');"
    print(query)
    instance = not isinstance(execute_query(connection, query), Error)
    print(instance)
    return instance
      #is not это проверка типа

def getUser(connection, id):
    try:
        query = f"SELECT * FROM user WHERE id = {id} LIMIT 1;"
        res = execute_query(connection, query, True)
        if not res:
            print("Пользователь не найден")
            return False 
 
        return res
    except Error as e:
        print("Ошибка получения данных из БД "+str(e))

 
    return False

def get_user_by_login(login, connection):
    try:
        query = f"SELECT * FROM user WHERE login = '{login}' LIMIT 1;"
        res = execute_query(connection, query, True)
        if not res:
            print("Пользователь не найден")
            return False 
    
        return res[0]
    except Error as e:
        print("Ошибка получения данных из БД "+str(e))