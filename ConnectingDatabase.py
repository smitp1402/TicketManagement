import mysql.connector

# Global database connection and cursor
db_connection = mysql.connector.connect(
    host="localhost",  # or '127.0.0.1' or the IP/domain of your MySQL server
    user="root",  # the username, usually 'root'
    password="Yashmk@901",  # your password
    database="ticketbookingsystem",  # the database name
    port=3306  # the port, usually 3306
)

# Global cursor object
cursor = db_connection.cursor()

def show_tables():
    # Run a simple query to show tables
    cursor.execute("SHOW TABLES")

    # Fetch and print the result
    for table in cursor.fetchall():
        print(table)


# Example of using the global cursor to show tables
show_tables()

# No need to close the connection here, keep it open for usage in other modules
