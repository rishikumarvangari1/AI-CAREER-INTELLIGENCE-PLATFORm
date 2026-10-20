from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv(override=True)

print("DB user:", os.getenv("DB_USER"))
print("Password loaded:", bool(os.getenv("DB_PASSWORD")))
print("Database:", os.getenv("DB_NAME"))

connection = None

try:
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "career_intelligence")
    )

    print("Connected to MySQL successfully!")

    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE()")
    print("Connected database:", cursor.fetchone()[0])
    cursor.close()

except mysql.connector.Error as error:
    print("MySQL error:", error)

finally:
    if connection and connection.is_connected():
        connection.close()