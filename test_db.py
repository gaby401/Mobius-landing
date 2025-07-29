import mysql.connector

config = {
    'user': 'u145448218_ec_db_usr',
    'password': ']z2[?PM=U0',
    'host': '127.0.0.1',
    'database': 'u145448218_ec_db',
    'ssl_disabled': True
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    for (table,) in cursor.fetchall():
        print(f"📁 {table}")
    conn.close()
except mysql.connector.Error as err:
    print(f"❌ ERROR: {err}")
