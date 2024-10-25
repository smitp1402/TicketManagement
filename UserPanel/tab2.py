
#
# def create_tab2(notebook):
#     tab2_frame = tk.Frame(notebook)
#     notebook.add(tab2_frame, text="Tab2")
#     # Add content for Tab2
#     tk.Label(tab2_frame, text="This is the content of Tab2").pack(pady=20)

import string
import random
import tkinter as tk
import mysql.connector
from mysql.connector import Error
from UserPanel import Registration  # Import the module where the getters are defined

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


def TicketList(notebook):
        tab2_frame = tk.Frame(notebook)
        notebook.add(tab2_frame, text="Tab2")
        # Add content for Tab2
        tk.Label(tab2_frame, text="This is the content of Tab2").pack(pady=20)
