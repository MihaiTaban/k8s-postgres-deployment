import psycopg2
from psycopg2 import Error

# Database connection details
DB_HOST = "localhost" # Docker Desktop K8s exposes NodePorts on localhost from Windows
DB_PORT = "30007"     # The nodePort you defined in postgres-service.yaml
DB_NAME = "mydatabase"
DB_USER = "myuser"
DB_PASSWORD = "mypassword"

def connect_db():
    """Establishes a connection to the PostgreSQL database."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connection to PostgreSQL DB successful!")
        return conn
    except Error as e:
        print(f"Error connecting to PostgreSQL DB: {e}")
        return None

def create_table(conn):
    """Creates a simple 'users' table if it doesn't exist."""
    try:
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'users' created (or already exists).")
    except Error as e:
        print(f"Error creating table: {e}")
        conn.rollback() # Rollback in case of error
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

def insert_user(conn, name, email):
    """Inserts a new user into the 'users' table."""
    try:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO users (name, email) VALUES (%s, %s);
        """
        cursor.execute(insert_query, (name, email))
        conn.commit()
        print(f"User '{name}' inserted successfully.")
    except Error as e:
        print(f"Error inserting user: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

def fetch_users(conn):
    """Fetches and prints all users from the 'users' table."""
    try:
        cursor = conn.cursor()
        fetch_query = "SELECT id, name, email FROM users;"
        cursor.execute(fetch_query)
        users = cursor.fetchall()
        print("\n--- Current Users ---")
        if users:
            for user in users:
                print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
        else:
            print("No users found.")
    except Error as e:
        print(f"Error fetching users: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

def main():
    conn = None
    try:
        conn = connect_db()
        if conn:
            create_table(conn)
            insert_user(conn, "Alice Smith", "alice@example.com")
            insert_user(conn, "Bob Johnson", "bob@example.com")
            insert_user(conn, "Charlie Brown", "charlie@example.com")
            # Try inserting a duplicate email to see the error handling
            insert_user(conn, "Alice Duplicate", "alice@example.com")
            fetch_users(conn)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")

if __name__ == "__main__":
    main()