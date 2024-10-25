# RegistrationPage.py
import tkinter as tk
from tkinter import ttk, messagebox
from ConnectingDatabase import cursor, db_connection
import Navigator

# Function to handle form submission
def submit_data():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    role = role_combobox.get()

    # Validate inputs
    if not first_name or not last_name or not email or not role:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    # Define role conditions based on dropdown
    if role == "Admin":
        query = """SELECT * FROM USER WHERE first_name = %s AND last_name = %s AND email = %s AND role = 'admin'"""
    elif role == "Organization":
        query = """SELECT * FROM USER WHERE first_name = %s AND last_name = %s AND email = %s AND role = 'organization'"""
    elif role == "Customer":
        query = """SELECT * FROM USER WHERE first_name = %s AND last_name = %s AND email = %s AND role = 'customer'"""
    else:
        messagebox.showerror("Invalid Role", "Invalid role selected!")
        return

    # Execute the query to check if the user exists with the matching role
    cursor.execute(query, (first_name, last_name, email))
    result = cursor.fetchone()

    if result:
        root.destroy()
        Navigator.open_navigator(first_name, last_name, email, role)
    else:
        messagebox.showerror("Login Failed", "No matching user found with the selected role and details.")

# Function to create the form
def create_form():
    global frame, first_name_entry, last_name_entry, email_entry, role_combobox

    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="First Name").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    first_name_entry = tk.Entry(frame)
    first_name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(frame, text="Last Name").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    last_name_entry = tk.Entry(frame)
    last_name_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(frame, text="Gmail").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    email_entry = tk.Entry(frame)
    email_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(frame, text="Role").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    role_combobox = ttk.Combobox(frame, values=["Admin", "Organization", "Customer"], state="readonly")
    role_combobox.grid(row=3, column=1, padx=10, pady=10)

    submit_button = tk.Button(frame, text="Submit", command=submit_data)
    submit_button.grid(row=4, column=0, columnspan=2, pady=20)

root = tk.Tk()
root.title("User Information Form")
root.geometry("400x300")
create_form()
root.mainloop()
