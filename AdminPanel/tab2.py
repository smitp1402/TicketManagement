# import tkinter as tk
# from tkinter import ttk
# import mysql.connector
# from mysql.connector import Error
#
# # Database connection
# try:
#     db_connection = mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='smit',
#         database='ticketbookingsystem'
#     )
#     if db_connection.is_connected():
#         cursor = db_connection.cursor()
#         print("Database connection successful")
# except Error as err:
#     print(f"Error: {err}")
#     exit(1)  # Exit if connection fails
#
#
# def load_revenue_by_category(tab2_frame, selected_category=None, min_revenue=None, max_revenue=None):
#     # Clear existing content
#     for widget in tab2_frame.winfo_children():
#         widget.destroy()
#
#     # Modify the query to filter by category and revenue if selected
#     query = """
#         SELECT
#             EC.category_name,
#             E.event_name,
#             SUM(E.total_price) AS event_total_revenue,
#             SUM(SUM(E.total_price)) OVER (PARTITION BY EC.category_name) AS category_total_revenue
#         FROM
#             EVENT E
#         JOIN
#             TICKET T ON E.event_id = T.event_id
#         JOIN
#             EVENTCATEGORY EC ON E.event_category = EC.category_id
#     """
#     conditions = []
#     params = []
#
#     if selected_category:
#         conditions.append("EC.category_name = %s")
#         params.append(selected_category)
#
#     if min_revenue is not None:
#         conditions.append("SUM(E.total_price) >= %s")
#         params.append(min_revenue)
#
#     if max_revenue is not None:
#         conditions.append("SUM(E.total_price) <= %s")
#         params.append(max_revenue)
#
#     if conditions:
#         query += " WHERE " + " AND ".join(conditions)
#
#     query += """
#         GROUP BY
#             EC.category_name, E.event_name
#         ORDER BY
#             category_total_revenue DESC, event_total_revenue DESC;
#     """
#     cursor.execute(query, tuple(params))
#     revenue_data = cursor.fetchall()
#
#     if revenue_data:
#         current_category = None
#
#         # Display each event and its revenue
#         for category, event_name, event_total_revenue, category_total_revenue in revenue_data:
#             if current_category != category:
#                 # Add a header for a new category
#                 tk.Label(tab2_frame, text=f"Category: {category} (Total Revenue: ${category_total_revenue:.2f})",
#                          font=("Arial", 14, "bold")).pack(pady=10)
#                 current_category = category
#
#             # Create a frame for each event
#             event_frame = ttk.Frame(tab2_frame, borderwidth=2, relief="ridge", padding=10)
#             event_frame.pack(fill=tk.X, padx=10, pady=5)
#
#             # Display event details with total revenue
#             event_details = (
#                 f"Event Name: {event_name}\n"
#                 f"Event Revenue: ${event_total_revenue:.2f}"
#             )
#             label = tk.Label(event_frame, text=event_details, justify="left")
#             label.pack(side="left", padx=10)
#     else:
#         tk.Label(tab2_frame, text="No revenue data available.", font=("Arial", 12), fg="red").pack(pady=20)
#
#
# def create_tab2(notebook):
#     tab2_frame = tk.Frame(notebook)
#     notebook.add(tab2_frame, text="Revenue by Category")
#
#     # Create a canvas to hold the content and a vertical scrollbar
#     canvas = tk.Canvas(tab2_frame)
#     scrollbar = ttk.Scrollbar(tab2_frame, orient="vertical", command=canvas.yview)
#     canvas.configure(yscrollcommand=scrollbar.set)
#
#     # Create a frame inside the canvas that will hold all the widgets
#     content_frame = tk.Frame(canvas)
#
#     # Create a window in the canvas to hold the content_frame
#     canvas.create_window((0, 0), window=content_frame, anchor="nw")
#     canvas.grid(row=0, column=0, sticky="nsew")
#     scrollbar.grid(row=0, column=1, sticky="ns")
#
#     # Configure the row and column of the grid
#     tab2_frame.grid_rowconfigure(0, weight=1)
#     tab2_frame.grid_columnconfigure(0, weight=1)
#
#     # Add a title for Tab2
#     tk.Label(content_frame, text="Revenue by Category", font=("Arial", 16, "bold")).pack(pady=20)
#
#     # Add filter controls
#     filter_frame = ttk.Frame(content_frame)
#     filter_frame.pack(fill=tk.X, pady=10)
#
#     tk.Label(filter_frame, text="Filter by Category:").pack(side="left", padx=10)
#
#     # Dropdown for category selection
#     cursor.execute("SELECT DISTINCT category_name FROM EVENTCATEGORY")
#     categories = [row[0] for row in cursor.fetchall()]
#     category_var = tk.StringVar(value="All Categories")
#
#     category_dropdown = ttk.Combobox(filter_frame, textvariable=category_var, values=["All Categories"] + categories)
#     category_dropdown.pack(side="left", padx=10)
#
#     tk.Label(filter_frame, text="Min Revenue:").pack(side="left", padx=10)
#
#     min_revenue_var = tk.DoubleVar(value=0)
#     min_revenue_entry = ttk.Entry(filter_frame, textvariable=min_revenue_var)
#     min_revenue_entry.pack(side="left", padx=10)
#
#     tk.Label(filter_frame, text="Max Revenue:").pack(side="left", padx=10)
#
#     max_revenue_var = tk.DoubleVar(value=10000)
#     max_revenue_entry = ttk.Entry(filter_frame, textvariable=max_revenue_var)
#     max_revenue_entry.pack(side="left", padx=10)
#
#     def apply_filter():
#         selected_category = category_var.get() if category_var.get() != "All Categories" else None
#         min_revenue = min_revenue_var.get()
#         max_revenue = max_revenue_var.get()
#         load_revenue_by_category(content_frame, selected_category, min_revenue, max_revenue)
#
#     # Apply button for filter
#     apply_button = ttk.Button(filter_frame, text="Apply Filter", command=apply_filter)
#     apply_button.pack(side="left", padx=10)
#
#     # Call the function to load and display the revenue data
#     load_revenue_by_category(content_frame)
#
#     # Update scroll region to match the size of content
#     content_frame.update_idletasks()
#     canvas.config(scrollregion=canvas.bbox("all"))
#
#
# # Main Application Window
# def main():
#     root = tk.Tk()
#     root.title("Ticket Booking System")
#
#     notebook = ttk.Notebook(root)
#     notebook.pack(expand=True, fill="both")
#
#     # Add Tab2
#     create_tab2(notebook)
#
#     root.mainloop()
#
# # if __name__ == "__main__":
# #     main()
import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error

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


def load_revenue_by_category(tab2_frame, selected_category=None):
    # Clear existing content
    for widget in tab2_frame.winfo_children():
        widget.destroy()

    # Modify the query to filter by category if selected
    query = """
        SELECT 
            EC.category_name, 
            E.event_name, 
            SUM(E.total_price) AS event_total_revenue,
            SUM(SUM(E.total_price)) OVER (PARTITION BY EC.category_name) AS category_total_revenue
        FROM 
            EVENT E
        JOIN 
            TICKET T ON E.event_id = T.event_id
        JOIN 
            EVENTCATEGORY EC ON E.event_category = EC.category_id
    """
    conditions = []
    params = []

    if selected_category:
        conditions.append("EC.category_name = %s")
        params.append(selected_category)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += """
        GROUP BY 
            EC.category_name, E.event_name
        ORDER BY 
            category_total_revenue DESC, event_total_revenue DESC;
    """
    cursor.execute(query, tuple(params))
    revenue_data = cursor.fetchall()

    if revenue_data:
        current_category = None

        # Display each event and its revenue
        for category, event_name, event_total_revenue, category_total_revenue in revenue_data:
            if current_category != category:
                # Add a header for a new category
                tk.Label(tab2_frame, text=f"Category: {category} (Total Revenue: ${category_total_revenue:.2f})",
                         font=("Arial", 14, "bold")).pack(pady=10)
                current_category = category

            # Create a frame for each event
            event_frame = ttk.Frame(tab2_frame, borderwidth=2, relief="ridge", padding=10)
            event_frame.pack(fill=tk.X, padx=10, pady=5)

            # Display event details with total revenue
            event_details = (
                f"Event Name: {event_name}\n"
                f"Event Revenue: ${event_total_revenue:.2f}"
            )
            label = tk.Label(event_frame, text=event_details, justify="left")
            label.pack(side="left", padx=10)
    else:
        tk.Label(tab2_frame, text="No revenue data available.", font=("Arial", 12), fg="red").pack(pady=20)


def create_tab2(notebook):
    tab2_frame = tk.Frame(notebook)
    notebook.add(tab2_frame, text="Revenue by Category")

    # Create a filter section at the top
    filter_frame = ttk.Frame(tab2_frame)
    filter_frame.pack(fill=tk.X, pady=10)

    tk.Label(filter_frame, text="Filter by Category:").pack(side="left", padx=10)

    # Dropdown for category selection
    cursor.execute("""
        SELECT DISTINCT EC.category_name 
        FROM EVENTCATEGORY EC 
        WHERE EC.category_id IN (
            SELECT DISTINCT E.event_category 
            FROM EVENT E
            JOIN TICKET T ON E.event_id = T.event_id
        )
    """)

    categories = [row[0] for row in cursor.fetchall()]
    category_var = tk.StringVar(value="All Categories")

    category_dropdown = ttk.Combobox(filter_frame, textvariable=category_var, values=["All Categories"] + categories)
    category_dropdown.pack(side="left", padx=10)

    def apply_filter():
        selected_category = category_var.get() if category_var.get() != "All Categories" else None
        load_revenue_by_category(content_frame, selected_category)

    # Apply button for filter
    apply_button = ttk.Button(filter_frame, text="Apply Filter", command=apply_filter)
    apply_button.pack(side="left", padx=10)

    # Create a canvas to hold the content and a vertical scrollbar
    canvas = tk.Canvas(tab2_frame)
    scrollbar = ttk.Scrollbar(tab2_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas that will hold all the widgets
    content_frame = tk.Frame(canvas)

    # Create a window in the canvas to hold the content_frame
    canvas.create_window((0, 0), window=content_frame, anchor="nw")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Load and display the revenue data
    load_revenue_by_category(content_frame)

    # Update scroll region to match the size of content
    content_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


# Main Application Window
def main():
    root = tk.Tk()
    root.title("Ticket Booking System")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # Add Tab2
    create_tab2(notebook)

    root.mainloop()


# Uncomment the following to run the application
# if __name__ == "__main__":
#     main()



# Uncomment the following to run the application
# if __name__ == "__main__":
#     main()
