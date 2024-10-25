import tkinter as tk

# Function to display user profile information
def show_profile(first_name, last_name, email, role):
    # Create a new window for the user profile
    profile_window = tk.Tk()
    profile_window.title("User Profile")
    profile_window.geometry("400x300")

    # Create a frame for the profile content
    profile_frame = tk.Frame(profile_window)
    profile_frame.pack(padx=20, pady=20)

    # Display the entered user information
    tk.Label(profile_frame, text="First Name: " + first_name).pack(pady=5)
    tk.Label(profile_frame, text="Last Name: " + last_name).pack(pady=5)
    tk.Label(profile_frame, text="Email: " + email).pack(pady=5)
    tk.Label(profile_frame, text="Role: " + role).pack(pady=5)

    # Button to close the profile window
    close_button = tk.Button(profile_frame, text="Close", command=profile_window.destroy)
    close_button.pack(pady=20)

    # Start the profile window loop
    profile_window.mainloop()
