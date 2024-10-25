# registration.py

# Global variables
first_name = ""
last_name = ""
email = ""
role = ""

# Setter functions
def set_first_name(value):
    global first_name
    first_name = value

def set_last_name(value):
    global last_name
    last_name = value

def set_email(value):
    global email
    email = value

def set_role(value):
    global role
    role = value

# Getter functions
def get_first_name():
    return first_name

def get_last_name():
    return last_name

def get_email():
    return email

def get_role():
    return role
