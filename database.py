import mysql.connector


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "scholarship"
}


def get_db_connection():
    connection = mysql.connector.connect(**DB_CONFIG)
    return connection
