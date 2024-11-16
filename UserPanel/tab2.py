import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from UserPanel import Registration
import datetime  # For working with dates

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

def load_ticket_list(tab2_frame):
    # Clear existing content
    for widget in tab2_frame.winfo_children():
        widget.destroy()

    # Retrieve user details
    first_name = Registration.get_first_name()
    last_name = Registration.get_last_name()
    email = Registration.get_email()
    role = Registration.get_role()
    print("First Name:", first_name)
    print("Last Name:", last_name)
    print("Email:", email)
    print("Role:", role)

    # Check if user exists
    cursor.execute("SELECT user_id FROM USER WHERE email = %s LIMIT 1", (email,))
    result = cursor.fetchone()
    user_id = result[0] if result else None
    #aggregate_function
    if user_id:
        cursor.execute("""
            SELECT EVENT.event_name, EVENT.event_date, EVENT.start_time, EVENT.end_time, COUNT(BOOKING.booking_id) AS user_bookings
            FROM EVENT
            JOIN TICKET ON EVENT.event_id = TICKET.event_id
            LEFT JOIN BOOKING ON TICKET.ticket_id = BOOKING.ticket_id
            WHERE BOOKING.user_id = %s
            GROUP BY EVENT.event_name, EVENT.event_date, EVENT.start_time, EVENT.end_time;
        """, (user_id,))

        booked_events = cursor.fetchall()

        # Display each booked event in a block UI
        for event in booked_events:
            event_name, event_date, start_time, end_time, user_bookings = event

            # Create a frame for each event
            event_frame = ttk.Frame(tab2_frame, borderwidth=2, relief="ridge", padding=10)
            event_frame.pack(fill=tk.X, padx=10, pady=5)

            # Display event details including the booking count
            event_details = (
                f"Event Name: {event_name}\n"
                f"Event Date: {event_date}\n"
                f"Start Time: {start_time}\n"
                f"End Time: {end_time}\n"
                f"Bookings by User: {user_bookings}"
            )
            label = tk.Label(event_frame, text=event_details, justify="left")
            label.pack(side="left", padx=10)
    else:
        # If user does not exist, show a message
        tk.Label(tab2_frame, text="User does not exist or has not booked any events.", font=("Arial", 12), fg="red").pack(pady=20)

    # Set user ID in Registration (if needed for later use)
    Registration.set_userId(user_id)

    # Add a button below the event list
    button_frame = ttk.Frame(tab2_frame, padding=10)
    button_frame.pack(fill=tk.X, pady=10)

    # Refresh Booked Events Button
    refresh_button = ttk.Button(button_frame, text="Refresh Booked Events", command=lambda: load_ticket_list(tab2_frame))
    refresh_button.pack(side="bottom", pady=5)

    # Book New Event Button
    book_button = ttk.Button(button_frame, text="Upcoming Event", command=lambda: book_new_event(tab2_frame))
    book_button.pack(side="bottom", pady=5)

def book_new_event(tab2_frame):
    # Get today's date and calculate the date 10 days from now
    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=10)

    # Generate a list of dates from today to 10 days from now
    date_list = [(today + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(11)]

    # Convert the list of dates into a comma-separated string for the IN query
    date_string = ', '.join(f"'{date}'" for date in date_list)

    # Query to get events within the next 10 days using IN for membership query
    #membership query
    cursor.execute(f"""
        SELECT event_name, event_date, start_time, end_time
        FROM EVENT
        WHERE event_date IN ({date_string})
        ORDER BY event_date;
    """)

    upcoming_events = cursor.fetchall()

    # Clear existing content in the tab before displaying new events
    for widget in tab2_frame.winfo_children():
        widget.destroy()

    if upcoming_events:
        # Display each upcoming event in a block UI
        for event in upcoming_events:
            event_name, event_date, start_time, end_time = event

            # Create a frame for each event
            event_frame = ttk.Frame(tab2_frame, borderwidth=2, relief="ridge", padding=10)
            event_frame.pack(fill=tk.X, padx=10, pady=5)

            # Display event details
            event_details = (
                f"Event Name: {event_name}\n"
                f"Event Date: {event_date}\n"
                f"Start Time: {start_time}\n"
                f"End Time: {end_time}"
            )
            label = tk.Label(event_frame, text=event_details, justify="left")
            label.pack(side="left", padx=10)
    else:
        tk.Label(tab2_frame, text="No upcoming events in the next 10 days.", font=("Arial", 12), fg="red").pack(pady=20)

def TicketList(notebook):
    tab2_frame = tk.Frame(notebook)
    notebook.add(tab2_frame, text="Booked Event")

    # Bind event for tab switching
    def on_tab_changed(event):
        selected_tab = event.widget.index("current")
        if selected_tab == notebook.index(tab2_frame):  # Check if "Booked Events" tab is selected
            load_ticket_list(tab2_frame)

    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)
