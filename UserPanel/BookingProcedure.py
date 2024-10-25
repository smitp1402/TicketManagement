import string
import random
import mysql.connector
from mysql.connector import Error
from UserPanel import Registration  # Import the module where the getters are defined

# Database connection
try:
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='smit',
        database='ticketbookingsystem'
    )
    if db_connection.is_connected():
        cursor = db_connection.cursor()
        print("Database connection successful")
except Error as err:
    print(f"Error: {err}")
    exit(1)  # Exit if connection fails


def bookingProcedure(event_name):
    # Retrieve stored user data using getter functions
    first_name = Registration.get_first_name()
    last_name = Registration.get_last_name()
    email = Registration.get_email()
    role = Registration.get_role()

    # Debugging print to ensure proper data retrieval
    print(f"Booking procedure called for event: {event_name}")
    print(f"User: {first_name} {last_name}, Email: {email}, Role: {role}")

    try:
        # Step 1: Check if the user already exists
        cursor.execute("SELECT user_id FROM USER WHERE email = %s LIMIT 1", (email,))
        result = cursor.fetchone()
        user_id = result[0] if result else None

        Registration.set_userId(user_id)


        # Step 2: If the user doesn't exist, insert a new user
        if user_id is None:
            cursor.execute(
                "INSERT INTO USER (first_name, last_name, email, role) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, email, role)
            )
            db_connection.commit()
            user_id = cursor.lastrowid  # Get the generated user_id
            Registration.set_userId(user_id)


        # Step 3: Generate a random seat number in the format A1 to Z50
        random_seat = f"{random.choice(string.ascii_uppercase)}{random.randint(1, 50)}"

        # Step 4: Get the maximum ticket_id and increment by 1
        cursor.execute("SELECT IFNULL(MAX(ticket_id), 0) + 1 FROM TICKET")
        ticket_id = cursor.fetchone()[0]

        # Step 5: Insert a new row into the TICKET table with manually incremented ticket_id
        cursor.execute(
            "INSERT INTO TICKET (ticket_id, seat_details, event_id, venue_id, purchase_date) "
            "VALUES (%s, %s, (SELECT event_id FROM EVENT WHERE event_name = %s), (SELECT venue_id FROM EVENT WHERE event_name = %s), CURDATE())",
            (ticket_id, random_seat, event_name, event_name)
        )
        db_connection.commit()

        # Step 6: Decrease the available tickets for the event
        # Step 6: Get the event_id first and then update the available tickets
        cursor.execute("SELECT event_id FROM EVENT WHERE event_name = %s", (event_name,))
        event_id = cursor.fetchone()[0]

        # Update the available tickets using the event_id
        cursor.execute(
            "UPDATE EVENT SET available_tickets = available_tickets - 1 WHERE event_id = %s",
            (event_id,)
        )
        db_connection.commit()

        # Step 7: Get the maximum booking_id and increment by 1
        cursor.execute("SELECT IFNULL(MAX(booking_id), 0) + 1 FROM BOOKING")
        booking_id = cursor.fetchone()[0]

        # Step 8: Insert a new entry into the BOOKING table with manually incremented booking_id
        cursor.execute(
            "INSERT INTO BOOKING (booking_id, ticket_id, user_id, status) "
            "VALUES (%s, %s, %s, %s)",
            (booking_id, ticket_id, user_id, 'Confirmed')
        )
        db_connection.commit()

        print(f"Booking confirmed! Booking ID: {booking_id}, Ticket ID: {ticket_id}")

    except Exception as err:
        print(f"Error: {err}")
        db_connection.rollback()

    finally:
        if cursor:
            cursor.close()
        if db_connection.is_connected():
            db_connection.close()
            print("Database connection closed")

