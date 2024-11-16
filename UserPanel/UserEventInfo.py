import tkinter as tk
from tkinter import ttk
from ConnectingDatabase import cursor
from UserPanel import BookingProcedure


# Function to fetch event data with filters
def fetch_event_data_with_filters(category=None, start_date=None, end_date=None):
    # First query: without any filter (base query)
    base_query_1 = """
    SELECT 
        e.event_name,
        e.event_date,
        ec.category_name AS event_category,
        e.available_tickets,
        e.total_price,
        e.start_time,
        v.venue_name,
        v.address,
        v.city,
        v.state,
        v.zip_code,
        v.capacity,
        COALESCE(AVG(r.rating), 0) AS average_rating  -- Handling NULL ratings
    FROM 
        EVENT e
    LEFT JOIN 
        EVENTCATEGORY ec ON e.event_category = ec.category_id
    LEFT JOIN 
        VENUE v ON e.venue_id = v.venue_id
    LEFT JOIN 
        REVIEW r ON e.event_id = r.event_id
    WHERE 1=1
    GROUP BY 
        e.event_name, e.event_date, ec.category_name, e.available_tickets,
        e.total_price, e.start_time, v.venue_name, v.address, v.city, 
        v.state, v.zip_code, v.capacity
    """
#uninon
    # Second query: with filter conditions (category, start_date, end_date)
    base_query_2 = """
    SELECT 
        e.event_name,
        e.event_date,
        ec.category_name AS event_category,
        e.available_tickets,
        e.total_price,
        e.start_time,
        v.venue_name,
        v.address,
        v.city,
        v.state,
        v.zip_code,
        v.capacity,
        COALESCE(AVG(r.rating), 0) AS average_rating  -- Handling NULL ratings
    FROM 
        EVENT e
    LEFT JOIN 
        EVENTCATEGORY ec ON e.event_category = ec.category_id
    LEFT JOIN 
        VENUE v ON e.venue_id = v.venue_id
    LEFT JOIN 
        REVIEW r ON e.event_id = r.event_id
    WHERE 1=1
    """

    # Add conditions for the second query based on user filters
    conditions = []
    params = []

    if category and category != "All":
        conditions.append("ec.category_name = %s")
        params.append(category)

    if start_date and end_date:
        conditions.append("e.event_date BETWEEN %s AND %s")
        params.extend([start_date, end_date])

    if conditions:
        base_query_2 += " AND " + " AND ".join(conditions)

    # Add the GROUP BY clause to the second query as well
    base_query_2 += """
    GROUP BY 
        e.event_name, e.event_date, ec.category_name, e.available_tickets,
        e.total_price, e.start_time, v.venue_name, v.address, v.city, 
        v.state, v.zip_code, v.capacity
    """

    # Combine both queries using UNION
    combined_query = f"({base_query_1}) INTERSECT ({base_query_2})"

    # Execute combined query
    cursor.execute(combined_query, params)
    results = cursor.fetchall()
    print("Filtered event data:", results)  # Debugging line
    return results


# Function to fetch unique event categories
def fetch_event_categories():
    query = "SELECT DISTINCT category_name FROM EVENTCATEGORY;"
    cursor.execute(query)
    categories = cursor.fetchall()
    return [category[0] for category in categories]  # Extract category names from tuples


# Function to handle booking action
def book_event(event_name):
    # Call the booking procedure when "Book" button is clicked
    BookingProcedure.bookingProcedure(event_name)


# Function to create the tab with filters
def create_tab(notebook):
    tab1_frame = tk.Frame(notebook)
    notebook.add(tab1_frame, text="EventInfo")

    # Create a frame for the filter dropdown and date range
    filter_frame = tk.Frame(tab1_frame)
    filter_frame.pack(fill=tk.X, padx=10, pady=5)

    # Add a label and dropdown for filtering by category
    filter_label = tk.Label(filter_frame, text="Filter by Category:")
    filter_label.pack(side="left", padx=5)

    categories = fetch_event_categories()
    categories.insert(0, "All")
    category_combobox = ttk.Combobox(filter_frame, state="readonly", width=20)
    category_combobox['values'] = categories
    category_combobox.set("All")
    category_combobox.pack(side="left", padx=5)

    # Add labels and entries for date range filtering
    date_range_label = tk.Label(filter_frame, text="Filter by Date Range:")
    date_range_label.pack(side="left", padx=10)

    start_date_label = tk.Label(filter_frame, text="Start Date (YYYY-MM-DD):")
    start_date_label.pack(side="left", padx=5)
    start_date_entry = ttk.Entry(filter_frame, width=12)
    start_date_entry.pack(side="left", padx=5)

    end_date_label = tk.Label(filter_frame, text="End Date (YYYY-MM-DD):")
    end_date_label.pack(side="left", padx=5)
    end_date_entry = ttk.Entry(filter_frame, width=12)
    end_date_entry.pack(side="left", padx=5)

    # Function to update event list based on filters
    def filter_events():
        selected_category = category_combobox.get()
        start_date = start_date_entry.get().strip()
        end_date = end_date_entry.get().strip()

        # Fetch filtered event data
        event_data = fetch_event_data_with_filters(
            category=selected_category if selected_category != "All" else None,
            start_date=start_date if start_date else None,
            end_date=end_date if end_date else None,
        )
        display_events(event_data)

    # Add a filter button to apply filters
    filter_button = tk.Button(filter_frame, text="Apply Filters", command=filter_events)
    filter_button.pack(side="left", padx=10)

    # Create a scrollbar for event info display
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

    # Function to display event details
    def display_events(event_data):
        # Clear previous event displays
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Create a frame for each event and display its data with a "Booking" button
        for event in event_data:
            event_name = event[0] if len(event) > 0 else "Unknown"

            event_details = (
                f"Event Name: {event[0]}\n"
                f"Event Date: {event[1]}\n"
                f"Category: {event[2]}\n"
                f"Available Tickets: {event[3]}\n"
                f"Total Price: ${event[4]}\n"
                f"Start Time: {event[5]}\n"
                f"Venue: {event[6]}, {event[7]}, {event[8]}, {event[9]} {event[10]}\n"
                f"Capacity: {event[11]}\n"
                f"Rating: {event[12]:.1f}" if event[12] is not None else "No rating"
            )

            event_frame = ttk.Frame(scrollable_frame, borderwidth=2, relief="ridge", padding=10)
            event_frame.pack(fill=tk.X, padx=10, pady=5)

            label = tk.Label(event_frame, text=event_details, justify="left")
            label.pack(side="left", padx=10)

            button = tk.Button(event_frame, text="Book", command=lambda en=event_name: book_event(en))
            button.pack(side="right")

    # Initially display all events
    display_events(fetch_event_data_with_filters())


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
    create_tab(notebook)

    # Start the GUI event loop
    root.mainloop()
