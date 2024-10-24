import tkinter as tk
from tkinter import ttk
from ConnectingDatabase import cursor
# Assuming you have a global cursor and db_connection already established
# cursor is the global MySQL cursor, db_connection is the MySQL connection

def fetch_event_data():
    query = "SELECT event_id, event_name, event_date, start_time, end_time, venue_id FROM EVENT"
    cursor.execute(query)
    return cursor.fetchall()

def create_tab1(notebook):
    tab1_frame = tk.Frame(notebook)
    notebook.add(tab1_frame, text="EventInfo")

    # Create a Treeview to display event data
    columns = ('event_id', 'event_name', 'event_date', 'start_time', 'end_time', 'venue_id')
    tree = ttk.Treeview(tab1_frame, columns=columns, show='headings')

    # Define column headings
    tree.heading('event_id', text='Event ID')
    tree.heading('event_name', text='Event Name')
    tree.heading('event_date', text='Event Date')
    tree.heading('start_time', text='Start Time')
    tree.heading('end_time', text='End Time')
    tree.heading('venue_id', text='Venue ID')

    # Set column widths
    for col in columns:
        tree.column(col, width=100)

    tree.pack(fill=tk.BOTH, expand=True)

    # Fetch event data from the database
    event_data = fetch_event_data()

    # Insert event data into the Treeview
    for event in event_data:
        tree.insert('', tk.END, values=event)

    # Add a label to provide context
    tk.Label(tab1_frame, text="Event Information", font=("Arial", 14)).pack(pady=10)

