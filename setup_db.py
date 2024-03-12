import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database(dbname, user, password, host='localhost', port='5433'):
    """This script is needed for un-containerized env."""
    # Connection string to connect to the default database
    conn_string = f"dbname='postgres' user='{user}' host='{host}' password='{password}' port='{port}'"
    print(conn_string)
    conn = psycopg2.connect(conn_string)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    try:
        # Create database command
        cursor.execute(f"CREATE DATABASE {dbname}")
        print(f"Database {dbname} created successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

create_database('tododb', 'todolist_user', '1234')
