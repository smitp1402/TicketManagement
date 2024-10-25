import tkinter as tk
from tkinter import ttk
from UserPanel import UserEventInfo  # Import the Tab1 module
from UserPanel import tab2  # Import the Tab2 module


# Function to create the navigator window and display the profile
def open_navigator(first_name, last_name, email, role):
    print(f"role called for event: {role}")
    # Initialize the main window
    root = tk.Tk()
    root.title("User Navigator")
    root.geometry("400x400")

    # Create a notebook (tabbed interface) with tabs on top
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Create the "UserProfile" tab
    create_user_profile_tab(notebook, first_name, last_name, email, role)

    # Create Tab1 and Tab2 from external modules
    UserEventInfo.create_tab(notebook)  # Import content of Tab1
    tab2.TicketList(notebook)  # Import content of Tab2

    # Start the GUI event loop
    root.mainloop()


# Function to create the UserProfile tab and display user information
def create_user_profile_tab(notebook, first_name, last_name, email, role):
    user_profile_frame = tk.Frame(notebook)
    notebook.add(user_profile_frame, text="UserProfile")

    # Display the entered user information
    tk.Label(user_profile_frame, text="User Profile Information", font=("Arial", 14)).pack(pady=10)
    tk.Label(user_profile_frame, text="First Name: " + first_name).pack(pady=5)
    tk.Label(user_profile_frame, text="Last Name: " + last_name).pack(pady=5)
    tk.Label(user_profile_frame, text="Email: " + email).pack(pady=5)
    tk.Label(user_profile_frame, text="Role: " + role).pack(pady=5)
