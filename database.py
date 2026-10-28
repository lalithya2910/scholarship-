
import os
import mysql.connector

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", "3306")),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "root"),
    "database": os.environ.get("DB_NAME", "scholarship"),
}

if DB_CONFIG["host"] != "localhost":
    DB_CONFIG["ssl_disabled"] = False

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

