from db_connection import get_conn

def main():
    conn = get_conn()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES;")
        print("Bases de datos disponibles:")
        for db in cursor:
            print(f" - {db[0]}")
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
