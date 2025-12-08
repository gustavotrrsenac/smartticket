from peewee import MySQLDatabase
import os
from dotenv import load_dotenv

load_dotenv()

db = MySQLDatabase(
    os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "3306")),
    charset='utf8mb4'
)
