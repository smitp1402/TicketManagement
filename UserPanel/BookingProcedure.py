import Registration  # Import the module where the getters are defined
from ConnectingDatabase import cursor, db_connection  # Import the cursor and database connection


def bookingProcedure(event_name):
    # Retrieve stored user data using getter functions
    first_name = Registration.get_first_name()
    last_name = Registration.get_last_name()
    email = Registration.get_email()
    role = Registration.get_role()

    # Debugging print to ensure proper data retrieval
    print(f"Booking procedure called for event: {event_name}")
    print(f"User: {first_name} {last_name}, Email: {email}, Role: {role}")

    # try:
    #     # Call the stored procedure 'CreateTicketWithUser'
    #     cursor.callproc('CreateTicketWithUser', [first_name, last_name, email, event_name, role])
    #
    #     # Commit the transaction to the database
    #     db_connection.commit()
    #
    #     # If no errors, print success message
    #     print("Ticket successfully booked for the event:", event_name)
    #
    # except Exception as e:
    #     # Handle any potential errors during the procedure call
    #     print(f"An error occurred during booking: {e}")
    #     db_connection.rollback()  # Rollback in case of error
    #
    # finally:
    #     # Optionally, close the cursor; don't close the db_connection here if you want to reuse it
    #     # cursor.close()  # Uncomment if you're done with the cursor
    #     pass  # Remove this if you close the cursor above
