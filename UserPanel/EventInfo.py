import tkinter as tk
from tkinter import ttk
from ConnectingDatabase import cursor
from BookingProcedure import bookingProcedure  # Import the booking procedure function


# Function to fetch event data
def fetch_event_data():
    query = """
    SELECT 
        e.event_name,
        e.event_date,
        ec.category_name AS event_category,
        e.available_tickets,
        e.total_price,
        e.start_time,
        p.performer_name,
        p.genre,
        v.venue_name,
        v.address,
        v.city,
        v.state,
        v.zip_code,
        v.capacity,
        r.rating
    FROM 
        EVENT e
    JOIN 
        EVENTCATEGORY ec ON e.event_category = ec.category_id
    JOIN 
        VENUE v ON e.venue_id = v.venue_id
    LEFT JOIN 
        REVIEW r ON e.event_id = r.event_id -- Left join to include events with no reviews
    LEFT JOIN 
        PERFORMER p ON e.event_id = p.performer_id; -- Assuming you have a relation between event and performer
    """
    cursor.execute(query)
    return cursor.fetchall()

# Function to handle booking action
def book_event(event_name):
    # Call the booking procedure when "Book" button is clicked
    bookingProcedure(event_name)


# Function to create the event info tab
def create_tab1(notebook):
    tab1_frame = tk.Frame(notebook)
    notebook.add(tab1_frame, text="EventInfo")

    # Create a Scrollbar for the event info display
    canvas = tk.Canvas(tab1_frame)
    scrollbar = ttk.Scrollbar(tab1_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Fetch event data from the database
    event_data = fetch_event_data()

    # Create a frame for each event and display its data with a "Booking" button
    for event in event_data:
        event_name = event[0]

        # Create a frame for each event record
        event_frame = ttk.Frame(scrollable_frame, borderwidth=2, relief="ridge", padding=10)
        event_frame.pack(fill=tk.X, padx=10, pady=5)

        # Display event details
        event_details = (
            f"Event Name: {event[0]}\n"
            f"Event Date: {event[1]}\n"
            f"Category: {event[2]}\n"
            f"Available Tickets: {event[3]}\n"
            f"Total Price: ${event[4]}\n"
            f"Start Time: {event[5]}\n"
            f"Performer: {event[6]}\n"
            f"Genre: {event[7]}\n"
            f"Venue: {event[8]}, {event[9]}, {event[10]}, {event[11]} {event[12]}\n"
            f"Capacity: {event[13]}\n"
            f"Rating: {event[14] if event[14] is not None else 'No rating'}"
        )

        label = tk.Label(event_frame, text=event_details, justify="left")
        label.pack(side="left", padx=10)

        # Add a "Booking" button for each event
        button = tk.Button(event_frame, text="Book", command=lambda en=event_name: book_event(en))
        button.pack(side="right")


# Ensure the application runs only when this script is executed directly
if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    root.title("Event Management")
    root.geometry("700x600")

    # Create a notebook (tabbed interface)
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Create the Event Info tab
    create_tab1(notebook)

    # Start the GUI event loop
    root.mainloop()
