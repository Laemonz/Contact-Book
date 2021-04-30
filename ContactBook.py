import sqlite3

COLS = ("first_name", "last_name", "phone", "email", "address")
COL_NAMES = ("First Name", "Last Name", "Phone Number", "Email Address", "Address")
COMMANDS = ("view_all", "search", "add", "update", "delete", "exit")


def connect():
    """ Connect to the database
    """
    con = sqlite3.connect("contacts.db")
    return con


def create_table():
    """ Create the table for the database"""
    con = connect()
    con.cursor().execute('''CREATE TABLE contacts(
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        phone TEXT,
        email TEXT,
        address TEXT);''')
    con.commit()


def populate():
    con = connect()
    cur = con.cursor()

    cur.execute("DROP TABLE contacts")
    create_table()

    users = [("John", "Doe", "1234567890", "john.doe@gmail.com", "123 Something Road"),
             ("Bob", "Doe", "1231237890", "bob.doe@gmail.com", "456 ABC Avenue"),
             ("Jane", "Doe", "0987654321", "jane.doe@gmail.com", "321 Something Road")]

    cur.executemany('''INSERT INTO contacts (first_name, last_name, phone, email, address)
        VALUES(?, ?, ?, ?, ?)''', users)
    con.commit()


def add_contact(first_name, last_name, phone, email, address):
    con = connect()
    cur = con.cursor()
    cur.execute('''INSERT INTO contacts (first_name, last_name, phone, email, address)
                VALUES (?, ?, ?, ?, ?)''', (first_name, last_name, phone, email, address))
    con.commit()


def get_contact(my_id: str):
    """Get a contact given an ID"""
    cur = connect().cursor()
    cur.execute('''SELECT * FROM contacts WHERE id=?''', my_id)
    return cur.fetchone()


def update(my_id: str, field: str, new_info: str):
    """Update a contact's information given an ID"""
    con = connect()
    cur = con.cursor()
    if field == COLS[0]:
        cur.execute("UPDATE contacts SET first_name = ? WHERE id=?", (new_info, my_id))
    elif field == COLS[1]:
        cur.execute("UPDATE contacts SET last_name = ? WHERE id=?", (new_info, my_id))
    elif field == COLS[2]:
        cur.execute("UPDATE contacts SET phone = ? WHERE id=?", (new_info, my_id))
    elif field == COLS[3]:
        cur.execute("UPDATE contacts SET email = ? WHERE id=?", (new_info, my_id))
    elif field == COLS[4]:
        cur.execute("UPDATE contacts SET address = ? WHERE id=?", (new_info, my_id))
    con.commit()


def remove_contact(my_id: str):
    """Remove a contact given an ID"""
    con = connect()
    con.cursor().execute('''DELETE FROM contacts WHERE id=?''', my_id)
    con.commit()


def search(field: str, value: str):
    """Search for a contact using a given criteria"""
    cur = connect().cursor()
    if field == COLS[0]:
        cur.execute("SELECT * FROM contacts WHERE first_name=?", (value,))
    elif field == COLS[1]:
        cur.execute("SELECT * FROM contacts WHERE last_name=?", (value,))
    elif field == COLS[2]:
        cur.execute("SELECT * FROM contacts WHERE phone=?", (value,))
    elif field == COLS[3]:
        cur.execute("SELECT * FROM contacts WHERE email=?", (value,))
    elif field == COLS[4]:
        cur.execute("SELECT * FROM contacts WHERE address=?", (value,))
    all_rows = cur.fetchall()

    for row in all_rows:
        print('{0} | {1} {2} | {3} | {4} | {5}'.format(row[0], row[1], row[2], row[3], row[4], row[5]))


def print_all():
    """Print all the rows in the table"""
    cur = connect().cursor()
    cur.execute('''SELECT * FROM contacts''')
    all_rows = cur.fetchall()

    for row in all_rows:
        print('{0} | {1} {2} | {3} | {4} | {5}'.format(row[0], row[1], row[2], row[3], row[4], row[5]))


def get_int_input(min_val: int, max_val: int):
    in_range = False
    is_int = False
    while not in_range:
        while not is_int:
            try:
                val = input()
                my_int = int(val)
                is_int = True
            except ValueError as e:
                print(e)
        if min_val <= my_int <= max_val:
            in_range = True
        else:
            print("Please enter an integer from " + str(min_val) + " to " + str(max_val) + " inclusive!")
            is_int = False
    return my_int


def print_gui():
    print("Please enter a command:")
    print(COMMANDS)
    return execute_command()


def execute_command():
    valid_input = False

    while not valid_input:
        val = input()

        if val in COMMANDS:
            valid_input = True
        else:
            print("Please enter a valid command!")

    if val == COMMANDS[0]:  # view
        print_all()

    elif val == COMMANDS[1]:  # search
        print("Please enter which criteria you wish to search with")
        for i in range(len(COL_NAMES)):
            print(str(i) + ": " + COL_NAMES[i])
        x = get_int_input(0, len(COL_NAMES) - 1)

        print("Please enter the contact's " + COL_NAMES[x])
        search_val = input()

        search(COLS[x], search_val)

    elif val == COMMANDS[2]:  # add
        new_contact = []
        for x in COL_NAMES:
            print("Please enter the contact's " + x)
            info = input()
            new_contact.append(info)

        add_contact(new_contact[0], new_contact[1], new_contact[2], new_contact[3], new_contact[4])
        print("Contact added")

    elif val == COMMANDS[3]:  # update
        print("Please enter the contact's ID")
        contact_id = input()

        print("Please enter which criteria you wish to update")
        for i in range(len(COL_NAMES)):
            print(str(i) + ": " + COL_NAMES[i])
        x = get_int_input(0, len(COL_NAMES) - 1)

        print("Please enter the contact's new" + COL_NAMES[x])
        update_val = input()

        update(contact_id, COLS[x], update_val)

    elif val == COMMANDS[4]:  # delete
        print("Please enter the contact's ID")
        contact_id = input()
        remove_contact(contact_id)
        print("Contact deleted")

    elif val == "exit":
        return True
    print("\n")
    return False


def main():
    exit = False
    while not exit:
        exit = print_gui()


if __name__ == '__main__':
    # populate()
    main()
