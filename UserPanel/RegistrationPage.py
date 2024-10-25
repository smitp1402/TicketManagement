import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Navigator  # Import the navigator module to open the navigator window

global first_name, last_name, email, role
# Function to handle form submission
import Registration  # If these functions are in the same module, you don't need to import

# Function to handle form submission
def submit_data():
    # Get the form data
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    role = role_combobox.get()

    # Validate inputs
    if not first_name or not last_name or not email or not role:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    # Use the setter functions to store the data
    Registration.set_first_name(first_name)
    Registration.set_last_name(last_name)
    Registration.set_email(email)
    Registration.set_role(role)

    # Close the registration form window
    root.destroy()

    # Open the navigator page with the entered data
    Navigator.open_navigator(Registration.get_first_name(),
                             Registration.get_last_name(),
                             Registration.get_email(),
                             Registration.get_role())
# Function to create the form
def create_form():
    global frame, first_name_entry, last_name_entry, email_entry, role_combobox

    # Recreate the frame to hold the form
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Create and place the labels and input fields in the frame
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
    role_combobox = ttk.Combobox(frame, values=["Admin", "User"], state="readonly")
    role_combobox.grid(row=3, column=1, padx=10, pady=10)

    # Submit Button
    submit_button = tk.Button(frame, text="Submit", command=submit_data)
    submit_button.grid(row=4, column=0, columnspan=2, pady=20)

# Initialize the main window
root = tk.Tk()
root.title("User Information Form")
root.geometry("400x300")

# Create the form
create_form()

# Start the GUI event loop
root.mainloop()
