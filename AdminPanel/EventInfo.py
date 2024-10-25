import tkinter as tk
from tkinter import ttk, messagebox
from ConnectingDatabase import cursor, db_connection
from datetime import datetime


def fetch_event_data():
    query = "SELECT event_id, event_name, event_date, start_time, end_time, venue_id FROM EVENT"
    cursor.execute(query)
    return cursor.fetchall()


def create_tab1(notebook, role):
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

    # Fetch and display event data in the Treeview
    event_data = fetch_event_data()
    for event in event_data:
        tree.insert('', tk.END, values=event)

    # Add a label for context
    tk.Label(tab1_frame, text="Event Information", font=("Arial", 14)).pack(pady=10)

    # Add event creation button for Admins and Organizations only
    if role in ["Admin", "Organization"]:
        add_event_button = tk.Button(tab1_frame, text="Add New Event", command=lambda: add_event_popup(role))
        add_event_button.pack(pady=10)

    # Add event deletion button for Admins only
    if role == "Admin":
        delete_event_button = tk.Button(tab1_frame, text="Delete Selected Event", command=lambda: delete_event(tree, role))
        delete_event_button.pack(pady=10)

def add_event_popup(role):
    # Check if the user is Admin
    if role not in ["Admin", "Organization"]:
        messagebox.showerror("Permission Denied", "Only admins and organizations can add events.")
        return

    # Create a popup window to add a new event
    add_event_window = tk.Toplevel()
    add_event_window.title("Add New Event")

    # Event fields
    tk.Label(add_event_window, text="Event Name").grid(row=0, column=0, padx=10, pady=10)
    event_name_entry = tk.Entry(add_event_window)
    event_name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(add_event_window, text="Event Category ID").grid(row=1, column=0, padx=10, pady=10)
    event_category_entry = tk.Entry(add_event_window)
    event_category_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(add_event_window, text="Event Date (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=10)
    event_date_entry = tk.Entry(add_event_window)
    event_date_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(add_event_window, text="Start Time (HH:MM:SS)").grid(row=3, column=0, padx=10, pady=10)
    start_time_entry = tk.Entry(add_event_window)
    start_time_entry.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(add_event_window, text="End Time (HH:MM:SS)").grid(row=4, column=0, padx=10, pady=10)
    end_time_entry = tk.Entry(add_event_window)
    end_time_entry.grid(row=4, column=1, padx=10, pady=10)

    tk.Label(add_event_window, text="Venue ID").grid(row=5, column=0, padx=10, pady=10)
    venue_id_entry = tk.Entry(add_event_window)
    venue_id_entry.grid(row=5, column=1, padx=10, pady=10)

    tk.Label(add_event_window, text="Available Tickets").grid(row=6, column=0, padx=10, pady=10)
    available_tickets_entry = tk.Entry(add_event_window)
    available_tickets_entry.grid(row=6, column=1, padx=10, pady=10)

    tk.Label(add_event_window, text="Total Price").grid(row=7, column=0, padx=10, pady=10)
    total_price_entry = tk.Entry(add_event_window)
    total_price_entry.grid(row=7, column=1, padx=10, pady=10)

    tk.Label(add_event_window, text="Organizer ID").grid(row=8, column=0, padx=10, pady=10)
    organizer_id_entry = tk.Entry(add_event_window)
    organizer_id_entry.grid(row=8, column=1, padx=10, pady=10)

    def save_event():
        event_name = event_name_entry.get()
        event_category = event_category_entry.get()
        event_date = event_date_entry.get()
        start_time = start_time_entry.get()
        end_time = end_time_entry.get()
        venue_id = venue_id_entry.get()
        available_tickets = available_tickets_entry.get()
        total_price = total_price_entry.get()
        organizer_id = organizer_id_entry.get()

        # Validate input: All fields must be filled
        if not all(
                [event_name, event_category, event_date, start_time, end_time, venue_id, available_tickets, total_price,
                 organizer_id]):
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        try:
            # Combine event_date and start_time, end_time to compare them
            start_datetime = datetime.strptime(f"{event_date} {start_time}", "%Y-%m-%d %H:%M:%S")
            end_datetime = datetime.strptime(f"{event_date} {end_time}", "%Y-%m-%d %H:%M:%S")

            # Check if start time is before end time
            if start_datetime >= end_datetime:
                messagebox.showerror("Invalid Time", "Start time must be earlier than end time.")
                return
        except ValueError:
            messagebox.showerror("Invalid Date/Time", "Please enter valid date and time in the correct format.")
            return

        # Check if the organizer_id exists in the USER table and has the role of Organizer
        query = "SELECT role FROM USER WHERE user_id = %s"
        cursor.execute(query, (organizer_id,))
        result = cursor.fetchone()

        if result is None or result[0] != "organization":
            messagebox.showerror("Invalid Organizer",
                                 "Organizer ID must belong to a user with the role of 'Organizer'.")
            return

        # Check if event_category exists in the EVENT_CATEGORY table
        query = "SELECT COUNT(*) FROM EVENTCATEGORY WHERE category_id = %s"
        cursor.execute(query, (event_category,))
        result = cursor.fetchone()

        if result[0] == 0:
            messagebox.showerror("Invalid Category", "Event Category does not exist in the EVENT_CATEGORY table!")
            return

        # Check if venue_id exists in the VENUE table
        query = "SELECT COUNT(*) FROM VENUE WHERE venue_id = %s"
        cursor.execute(query, (venue_id,))
        result = cursor.fetchone()

        if result[0] == 0:
            messagebox.showerror("Invalid Venue", "Venue ID does not exist in the VENUE table!")
            return

        # Insert the new event into the database
        query = """
        INSERT INTO EVENT (event_name, event_category, event_date, start_time, end_time, venue_id, available_tickets, total_price, organizer_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            event_name, event_category, event_date, start_time, end_time, venue_id, available_tickets, total_price,
            organizer_id))
        db_connection.commit()

        # Get the last inserted event_id
        event_id = cursor.lastrowid

        # Ask for performers after the event is created
        add_performer_popup(event_id)

        messagebox.showinfo("Success", "Event added successfully!")
        add_event_window.destroy()

    # Add Save button
    save_button = tk.Button(add_event_window, text="Save Event", command=save_event)
    save_button.grid(row=9, column=0, columnspan=2, pady=20)


def delete_event(tree, role):
    # Check if the user is an Admin
    if role != "Admin":
        messagebox.showerror("Permission Denied", "Only admins can delete events.")
        return

    # Get selected item
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an event to delete.")
        return

    # Get event ID from selected item
    event_id = tree.item(selected_item, 'values')[0]

    # Confirm before deleting
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this event?")
    if not confirm:
        return

    try:
        # Fetch performer IDs associated with the event
        query = "SELECT performer_id FROM eventperformer WHERE event_id = %s"
        cursor.execute(query, (event_id,))
        performer_ids = cursor.fetchall()

        # Delete records from eventperformer table for the event
        query = "DELETE FROM eventperformer WHERE event_id = %s"
        cursor.execute(query, (event_id,))

        # Delete the event from the EVENT table
        query = "DELETE FROM EVENT WHERE event_id = %s"
        cursor.execute(query, (event_id,))

        # For each performer, check if they are associated with any other events
        for performer_id in performer_ids:
            query = "SELECT COUNT(*) FROM eventperformer WHERE performer_id = %s"
            cursor.execute(query, (performer_id[0],))
            count = cursor.fetchone()[0]

            # If no other event uses this performer, delete the performer from the PERFORMER table
            if count == 0:
                query = "DELETE FROM PERFORMER WHERE performer_id = %s"
                cursor.execute(query, (performer_id[0],))

        # Commit the transaction
        db_connection.commit()

        # Remove the selected item from the Treeview
        tree.delete(selected_item)

        messagebox.showinfo("Success", "Event and associated performers deleted successfully!")

    except Exception as e:
        db_connection.rollback()
        messagebox.showerror("Error", f"Failed to delete event: {e}")
    pass


def add_performer_popup(event_id):
    # Create a popup window to add performers
    performer_window = tk.Toplevel()
    performer_window.title("Add Performers")

    tk.Label(performer_window, text="Performer ID").grid(row=0, column=0, padx=10, pady=10)
    performer_id_entry = tk.Entry(performer_window)
    performer_id_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(performer_window, text="Performer Name").grid(row=1, column=0, padx=10, pady=10)
    performer_name_entry = tk.Entry(performer_window)
    performer_name_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(performer_window, text="Genre").grid(row=2, column=0, padx=10, pady=10)
    genre_entry = tk.Entry(performer_window)
    genre_entry.grid(row=2, column=1, padx=10, pady=10)

    def save_performer():
        performer_id = performer_id_entry.get()

        # Validate input: Performer ID must be filled
        if not performer_id:
            messagebox.showwarning("Input Error", "Performer ID is required!")
            return

        # Check if the performer_id exists in the PERFORMER table
        query = "SELECT COUNT(*) FROM PERFORMER WHERE performer_id = %s"
        cursor.execute(query, (performer_id,))
        result = cursor.fetchone()

        if result[0] == 0:
            # If the performer does not exist, collect details for the new performer
            performer_name = performer_name_entry.get()
            genre = genre_entry.get()

            # Validate input for new performer
            if not performer_name or not genre:
                messagebox.showwarning("Input Error", "Performer Name and Genre are required!")
                return

            # Insert the new performer into the PERFORMER table
            query = """
            INSERT INTO PERFORMER (performer_id, performer_name, genre)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (performer_id, performer_name, genre))
            db_connection.commit()

            messagebox.showinfo("Success", "New performer added successfully!")

        # Insert the performer into the eventperformer table
        query = """
        INSERT INTO eventperformer (event_id, performer_id)
        VALUES (%s, %s)
        """
        cursor.execute(query, (event_id, performer_id))
        db_connection.commit()

        messagebox.showinfo("Success", "Performer added to event successfully!")
        performer_window.destroy()

    # Add Save button for performer
    save_performer_button = tk.Button(performer_window, text="Save Performer", command=save_performer)
    save_performer_button.grid(row=3, column=0, columnspan=2, pady=20)
    pass

# Main code to create the application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Event Manager")
    notebook = ttk.Notebook(root)

    # Assume "Admin" as role for demonstration
    create_tab1(notebook, "Admin")

    notebook.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
