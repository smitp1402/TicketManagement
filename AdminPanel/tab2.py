import tkinter as tk

def create_tab2(notebook):
    tab2_frame = tk.Frame(notebook)
    notebook.add(tab2_frame, text="Tab2")
    # Add content for Tab2
    tk.Label(tab2_frame, text="This is the content of Tab2").pack(pady=20)
