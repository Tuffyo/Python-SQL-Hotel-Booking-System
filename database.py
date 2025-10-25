import sqlite3

def create_database():
    conn = sqlite3.connect("databases.db")
    cursor = conn.cursor()

    # Create payments table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        room_type TEXT,
                        name TEXT,
                        email TEXT,
                        checkin_date DATE, 
                        checkout_date DATE,
                        card_number TEXT,
                        cvc TEXT,
                        expiry_date TEXT,
                        num_guests INTEGER,
                        breakfast_booking BOOLEAN,
                        dinner_booking BOOLEAN,
                        total_cost REAL,
                        FOREIGN KEY (user_id) REFERENCES accounts(id) ON DELETE CASCADE
                      )''')

    # Modify bookings table to include payment_id foreign key
    cursor.execute("""CREATE TABLE IF NOT EXISTS bookings (
                    bookingRef INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    bookingDate TEXT,
                    nights INTEGER,
                    numPpl INTEGER,
                    bookingType TEXT,
                    fullName TEXT,
                    contact TEXT,
                    payment_id INTEGER,
                    FOREIGN KEY (payment_id) REFERENCES payments(id) ON DELETE CASCADE
                    )""")

    # Create accounts table if not exists
    cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT,
                surname TEXT,
                email TEXT UNIQUE,
                password TEXT,
                phone_number TEXT,
                staff_code TEXT
                )""")

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Call the function to create the database and its tables
create_database()