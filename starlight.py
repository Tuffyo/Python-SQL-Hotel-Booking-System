import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from tkinter import ttk
import MySQLdb
import pandas as pd
import cv2
from functools import partial
import sqlite3
import matplotlib.pyplot as plt
import hashlib
import database
import re

def register_user(firstname, surname, email, password, phone_number, staff_code):
    conn = sqlite3.connect("databases.db")
    cursor = conn.cursor()

    try:
        # Insert the user's data into the database
        cursor.execute("INSERT INTO accounts (firstname, surname, email, password, phone_number, staff_code) VALUES (?, ?, ?, ?, ?, ?)",
                       (firstname, surname, email, password, phone_number, staff_code))
        conn.commit()
        messagebox.showinfo("Registration Successful", "User registered successfully.")
    except sqlite3.Error as e:
        print("SQLite error:", e)
        messagebox.showerror("Registration Failed", "Failed to register user due to database error.")
    finally:
        conn.close()
        
# def login(): (old verification)
#     username = username_entry.get()
#     password = password_entry.get()

#     # login authentication
#     if username == "s" and password == "s":
#         messagebox.showinfo("Login Successful", "Welcome, {}".format(username))
#         mainmenu() # Go to main menu window after confirmation
#     elif username == "g" and password == "g":
#         messagebox.showinfo("Login Successful", "Welcome, {}".format(username))
#         from guestwin import gmainmenu
#         gmainmenu()
#     else:
#         messagebox.showerror("Login Failed", "Invalid username or password")

def login(email, password):
    global staff_code_entry
    
    conn = sqlite3.connect("databases.db")
    cursor = conn.cursor()
    
    # linear search
    try:
        cursor.execute("SELECT email, password, staff_code FROM accounts")
        rows = cursor.fetchall()

        found = False
        for row in rows:
            if row[0] == email and row[1] == password:
                found = True
                if row[2] == "yes":
                    messagebox.showinfo("Login Successful", "Welcome, {}".format(email))
                    mainmenu()
                else:
                    messagebox.showinfo("Login Successful", "Welcome, {}".format(email))
                    from guestwin import gmainmenu
                    gmainmenu()
                break

        if not found:
            messagebox.showerror("Login Failed", "Invalid email or password.")
            # Handle the login failure accordingly
    except sqlite3.Error as e:
        print("Error logging in:", e)
        messagebox.showerror("Login Failed", "Failed to login.")
    finally:
        conn.close()

def register1(first_name_entry, surname_entry, email_entry, password_entry, phone_entry, staff_code_entry):
    # Retrieve values from entry widgets
    first_name = first_name_entry.get()
    surname = surname_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    phone_number = phone_entry.get()
    staff_code = staff_code_entry.get()
    
    # Check if all required fields are filled
    if first_name and surname and email and password and phone_number:
        # Pass all the retrieved values to the register_user function
        register_user(first_name, surname, email, password, phone_number, staff_code)
        
        # Clear the entry widgets after registration
        first_name_entry.delete(0, tk.END)
        surname_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        staff_code_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please fill in all the required fields.")

def login1():
    global email_entry, password_entry

    email = email_entry.get()  # Access email directly from the global entry widget
    password = password_entry.get()  # Access password directly from the global entry widget
    
    if email and password:
        login(email, password)  
        
        # Clear the email and password entry after login
        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        root.destroy()
    else:
        messagebox.showerror("Error", "Please enter both email and password.")

def mainmenu():
    close_window()
    global mainmenu_window
    mainmenu_window = tk.Toplevel()
    mainmenu_window.title("Main Menu")
    mainmenu_window.geometry("1920x1080")
    mainmenu_window.configure(bg="#101C32")

    # creates a frame to hold the buttons
    button_frame = tk.Frame(mainmenu_window, bg="#101C32")
    button_frame.place(relx=0.5, rely=0.5, anchor="center")

    # creates the bookings button
    bookings_button = tk.Button(button_frame, text=" 📆 Bookings", command=bookings, font=("Century Gothic", 50), bg="white", padx=10, pady=5)
    bookings_button.grid(row=0, column=0, padx=7)

    # creates the security button
    security_button = tk.Button(button_frame, text=" 👮 Security", command=security, font=("Century Gothic", 50), bg="white", padx=10, pady=5)
    security_button.grid(row=0, column=1, padx=10)

    # creates the analytics button
    analytics_button = tk.Button(button_frame, text=" 📈 Analytics", command=analytics, font=("Century Gothic", 50), bg="white", padx=10, pady=5)
    analytics_button.grid(row=0, column=2, padx=10)

    # creates the logout button
    logout_button = tk.Button(mainmenu_window, text="Logout", command=logout, font=("Century Gothic", 20), bg="red", fg="white", padx=20, pady=10)
    logout_button.place(relx=1, rely=1, anchor="se")


def bookings():
    bookings_window = tk.Toplevel()
    bookings_window.title("Bookings")
    bookings_window.geometry('800x300')

    Frame1 = tk.Frame(master=bookings_window)
    Frame1.pack()

    def add_booking():
        # Connect to SQLite database
        conn = sqlite3.connect("databases.db")
        cursor = conn.cursor()

        # Get values from entry widgets
        username = username_var.get()
        bookingDate = bookingDate_var.get()
        nights = nights_var.get()
        numPpl = numPpl_var.get()
        bookingType = bookingType_var.get()
        fullName = fullName_var.get()
        contact = contact_var.get()

        # Validation checks
        if len(username) < 3 or len(username) > 20:
            messagebox.showerror("Error", "Username must be between 3 and 20 characters.")
            return
        if len(fullName) < 5 or len(fullName) > 50:
            messagebox.showerror("Error", "Full name must be between 5 and 50 characters.")
            return
        try:
            nights = int(nights)
            if nights <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Nights must be a positive integer.")
            return
        try:
            numPpl = int(numPpl)
            if numPpl <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Number of people must be a positive integer.")
            return
        # Check booking date format using regex
        if not re.match(r'\d{2}/\d{2}/\d{2}', bookingDate):
            messagebox.showerror("Error", "Booking date must be in the format dd/mm/yy.")
            return

        try:
            # Execute the INSERT command
            cursor.execute("""
                INSERT INTO bookings (
                    username, bookingDate, nights, numPpl, bookingType, fullName, contact
                ) VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (username, bookingDate, nights, numPpl, bookingType, fullName, contact))

            # Commit the changes to the database
            conn.commit()

            # Show success message
            messagebox.showinfo("Success", "Booking added successfully.")
        except sqlite3.Error as e:
            # Handle any errors that may occur during the execution of the SQL statement
            print(f"Error adding booking: {e}")
            messagebox.showerror("Error", "Failed to add booking.")

        # Close the database connection
        conn.close()

    # declare variables for the entry boxes
    username_var = tk.StringVar()
    bookingDate_var = tk.StringVar()
    nights_var = tk.IntVar()
    numPpl_var = tk.IntVar()
    bookingType_var = tk.StringVar()
    fullName_var = tk.StringVar()
    contact_var = tk.StringVar()
    bookingRef_var = tk.StringVar()

    # declare and grid the labels and entry boxes
    label_username = tk.Label(Frame1, text="Username")
    entry_username = tk.Entry(Frame1, textvariable=username_var)
    label_bookingDate = tk.Label(Frame1, text="Booking Date")
    entry_bookingDate = tk.Entry(Frame1, textvariable=bookingDate_var)
    label_nights = tk.Label(Frame1, text="Nights")
    entry_nights = tk.Entry(Frame1, textvariable=nights_var)
    label_numPpl = tk.Label(Frame1, text="Number of People")
    entry_numPpl = tk.Entry(Frame1, textvariable=numPpl_var)
    label_bookingType = tk.Label(Frame1, text="Booking Type")
    entry_bookingType = tk.Entry(Frame1, textvariable=bookingType_var)
    label_fullName = tk.Label(Frame1, text="Full Name")
    entry_fullName = tk.Entry(Frame1, textvariable=fullName_var)
    label_contact = tk.Label(Frame1, text="Contact")
    entry_contact = tk.Entry(Frame1, textvariable=contact_var)
    label_bookingRef = tk.Label(Frame1, text="BookingID to delete")
    entry_bookingRef = tk.Entry(Frame1, textvariable=bookingRef_var)

    label_username.grid(row=1, column=1)
    entry_username.grid(row=1, column=2)
    label_bookingDate.grid(row=2, column=1)
    entry_bookingDate.grid(row=2, column=2)
    label_nights.grid(row=3, column=1)
    entry_nights.grid(row=3, column=2)
    label_numPpl.grid(row=4, column=1)
    entry_numPpl.grid(row=4, column=2)
    label_bookingType.grid(row=5, column=1)
    entry_bookingType.grid(row=5, column=2)
    label_fullName.grid(row=6, column=1)
    entry_fullName.grid(row=6, column=2)
    label_contact.grid(row=7, column=1)
    entry_contact.grid(row=7, column=2)
    label_bookingRef.grid(row=8, column=1)
    entry_bookingRef.grid(row=8, column=2)

    # create a button to call add_booking
    add_booking_button = tk.Button(Frame1, text="Add Booking", command=add_booking)
    add_booking_button.grid(row=1, column=5)

    def del_booking():
        bookingRef = bookingRef_var.get()
        confirmation = messagebox.askyesno("Delete Booking", "Are you sure you want to delete this booking?")
        if confirmation:
        # Connect to SQLite database
            conn = sqlite3.connect("databases.db")
            cursor = conn.cursor()

        try:
            # execute the DELETE command in SQL
            cursor.execute("DELETE FROM bookings WHERE bookingRef = ?", (bookingRef,))

            # make changes to the database
            conn.commit()

            messagebox.showinfo("Success", "Booking deleted successfully.")
        except sqlite3.Error as e:
            # checks for any errors from SQL statement
            print(f"Error deleting booking: {e}")
            messagebox.showerror("Error", "Failed to delete booking.")

        conn.close()

    del_booking_button = tk.Button(Frame1, text="Delete Booking", command=del_booking)
    del_booking_button.grid(row=1, column=8)

    # create the main menu button
    menu_button_bookings = tk.Button(Frame1, text="Booking", command=bookings)
    menu_button_bookings.pack()

def security():
    print("Security button clicked")

    import threading

    # Define security window
    security_window = tk.Toplevel()
    security_window.title("Security")
    security_window.geometry("600x500")
    security_window.configure(bg="#101C32")

    # ===== Inner function: reset password =====
    def reset_password():
        username = username_entry.get()
        if username:
            messagebox.showinfo("Password Reset", f"Password reset link sent to {username}")
            with open("security_logs.txt", "a") as log_file:
                log_file.write(f"Password reset requested for user: {username}\n")
        else:
            messagebox.showerror("Error", "Please enter a username")

    # ===== Inner function: view cameras =====
    def view_cameras():
        camera_window = tk.Toplevel()
        camera_window.title("Live Security Feed")
        camera_window.geometry("700x550")
        camera_window.configure(bg="#101C32")

        label_info = tk.Label(
            camera_window,
            text="Press 'Stop Camera' to end the feed.\nPress 'r' to start/stop recording.",
            font=("Century Gothic", 12),
            bg="#101C32",
            fg="white"
        )
        label_info.pack(pady=10)

        # Start / Stop button logic
        running = True

        def stop_camera():
            nonlocal running
            running = False
            cap.release()
            cv2.destroyAllWindows()
            camera_window.destroy()

        stop_button = tk.Button(
            camera_window,
            text="Stop Camera",
            command=stop_camera,
            font=("Century Gothic", 14),
            bg="red",
            fg="white",
            padx=15,
            pady=5
        )
        stop_button.pack(pady=10)

        # OpenCV Camera setup
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        writer = cv2.VideoWriter("recording.mp4", fourcc, 30.0, (640, 480))
        recording = False

        def run_camera():
            nonlocal running, recording
            while running:
                ret, frame = cap.read()
                if ret:
                    cv2.imshow("Security Camera", frame)
                    if recording:
                        writer.write(frame)
                key = cv2.waitKey(1)
                if key == ord('r'):
                    recording = not recording
                    print(f"Recording: {recording}")
            cap.release()
            writer.release()
            cv2.destroyAllWindows()

        # Run camera in a separate thread
        thread = threading.Thread(target=run_camera, daemon=True)
        thread.start()

    # ===== Layout of Security Window =====
    username_label = tk.Label(
        security_window, text="Username:", font=("Century Gothic", 14), bg="#101C32", fg="white"
    )
    username_label.grid(row=0, column=0, padx=10, pady=15, sticky="w")

    username_entry = tk.Entry(security_window, font=("Century Gothic", 14))
    username_entry.grid(row=0, column=1, padx=10, pady=15)

    # Reset password button
    reset_button = tk.Button(
        security_window, text="Reset Password", command=reset_password,
        font=("Century Gothic", 14), bg="white", fg="black", padx=15, pady=5
    )
    reset_button.grid(row=1, column=0, columnspan=2, pady=10)

    # View Cameras button
    view_cameras_button = tk.Button(
        security_window, text="View Cameras", command=view_cameras,
        font=("Century Gothic", 14), bg="white", fg="black", padx=15, pady=5
    )
    view_cameras_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Insertion Sort / View Payments button
    insertion_sort_button = tk.Button(
        security_window, text="View Payments (Insertion Sort)", command=view_payments,
        font=("Century Gothic", 14), bg="white", fg="black", padx=15, pady=5
    )
    insertion_sort_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Close button
    close_button = tk.Button(
        security_window, text="Close", command=security_window.destroy,
        font=("Century Gothic", 14), bg="red", fg="white", padx=15, pady=5
    )
    close_button.grid(row=4, column=0, columnspan=2, pady=20)

    
def analytics():
    import matplotlib.pyplot as plt
    import datetime

    conn = sqlite3.connect("databases.db")
    cursor = conn.cursor()

    # --- 1. Staff bookings data ---
    cursor.execute("SELECT bookingDate, SUM(nights * numPpl) AS revenue FROM bookings GROUP BY bookingDate")
    staff_rows = cursor.fetchall()

    # --- 2. Guest payments data ---
    cursor.execute("SELECT checkin_date, SUM(total_cost) FROM payments GROUP BY checkin_date")
    guest_rows = cursor.fetchall()

    conn.close()

    # Merge data from both tables into a single dict
    revenue_by_date = {}

    # Add staff data
    for date, rev in staff_rows:
        if date not in revenue_by_date:
            revenue_by_date[date] = 0
        revenue_by_date[date] += rev if rev else 0

    # Add guest data
    for date, rev in guest_rows:
        if date not in revenue_by_date:
            revenue_by_date[date] = 0
        revenue_by_date[date] += rev if rev else 0

    # Sort by date
    try:
        dates_sorted = sorted(
            revenue_by_date.keys(),
            key=lambda d: datetime.datetime.strptime(d, "%d/%m/%y")
        )
    except Exception:
        # fallback if any dates aren't formatted
        dates_sorted = sorted(revenue_by_date.keys())

    revenues = [revenue_by_date[d] for d in dates_sorted]

    # --- Plot combined analytics ---
    plt.figure(figsize=(10, 6))
    plt.plot(dates_sorted, revenues, marker="o", linestyle="-", color="royalblue", label="Total Revenue (Guest + Staff)")
    plt.title("Hotel Revenue Over Time (Combined)")
    plt.xlabel("Date")
    plt.ylabel("Revenue ($)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def close_window():
    root.destroy()

def close_win(window):
    if window.winfo_exists(): 
        window.destroy()
        
def view_payments():
    # Connect to the payment database
    conn = sqlite3.connect("databases.db")
    cursor = conn.cursor()

    try:
        # Fetch all payments from the database
        cursor.execute("SELECT * FROM payments")
        payments = cursor.fetchall()

        # Sort payments using insertion sort based on total cost
        insertion_sort_payments(payments)

        # Create an array to store sorted payments
        sorted_payments = []

        # Append sorted payments to the array
        for payment in payments:
            sorted_payments.append(payment)

        # Display sorted payments
        for payment in sorted_payments:
            print(payment)  

    except sqlite3.Error as e:
        print("Error viewing payments:", e)
    finally:
        # Close connection
        conn.close()

def insertion_sort_payments(payments):
    for i in range(1, len(payments)):
        key = payments[i]
        j = i - 1
        while j >= 0 and (payments[j][11] is None or (key[11] is not None and payments[j][11] > key[11])):
            payments[j + 1] = payments[j]
            j -= 1
        payments[j + 1] = key
        
def register():
    # Destroy the login window
    root.destroy()

    # Create the registration window
    global registration_window
    registration_window = tk.Toplevel()
    registration_window.title("Registration")
    registration_window.geometry("1920x1080")
    registration_window.configure(bg="#101C32")

    # Registration components
    frame = tk.Frame(registration_window, bg="#233D65")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # First Name
    first_name_label = tk.Label(frame, text="First Name:", font=("Century Gothic", 14), bg="#233D65", fg="white")
    first_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    global first_name_var
    first_name_var = tk.StringVar()
    first_name_entry = tk.Entry(frame, font=("Century Gothic", 14), textvariable=first_name_var)
    first_name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Surname
    surname_label = tk.Label(frame, text="Surname:", font=("Century Gothic", 14), bg="#233D65", fg="white")
    surname_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    global surname_var
    surname_var = tk.StringVar()
    surname_entry = tk.Entry(frame, font=("Century Gothic", 14), textvariable=surname_var)
    surname_entry.grid(row=1, column=1, padx=10, pady=10)

    # Email
    email_label = tk.Label(frame, text="Email:", font=("Century Gothic", 14), bg="#233D65", fg="white")
    email_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    email_entry = tk.Entry(frame, font=("Century Gothic", 14))
    email_entry.grid(row=2, column=1, padx=10, pady=10)

    # Password
    password_label = tk.Label(frame, text="Password:", font=("Century Gothic", 14), bg="#233D65", fg="white")
    password_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    password_entry = tk.Entry(frame, show="*", font=("Century Gothic", 14))
    password_entry.grid(row=3, column=1, padx=10, pady=10)

    # Confirm Password
    confirm_password_label = tk.Label(frame, text="Confirm Password:", font=("Century Gothic", 14), bg="#233D65", fg="white")
    confirm_password_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    confirm_password_entry = tk.Entry(frame, show="*", font=("Century Gothic", 14))
    confirm_password_entry.grid(row=4, column=1, padx=10, pady=10)

    # Phone Number
    phone_label = tk.Label(frame, text="Phone Number:", font=("Century Gothic", 14), bg="#233D65", fg="white")
    phone_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

    phone_entry = tk.Entry(frame, font=("Century Gothic", 14))
    phone_entry.grid(row=5, column=1, padx=10, pady=10)

    # Staff Code
    global staff_code_entry
    staff_code_label = tk.Label(frame, text="Staff Code:", font=("Century Gothic", 14), bg="#233D65", fg="white")
    staff_code_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

    staff_code_var = tk.StringVar()
    staff_code_entry = tk.Entry(frame, font=("Century Gothic", 14), textvariable=staff_code_var)
    staff_code_entry.grid(row=6, column=1, padx=10, pady=10)

    # Return to login button
    back_button = tk.Button(frame, text="Return", command=back_to_login, font=("Century Gothic", 14))
    back_button.grid(row=7, column=0, columnspan=2, pady=10)

    def register2():
        first_name = first_name_entry.get()
        surname = surname_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        phone_number = phone_entry.get()
        staff_code = staff_code_entry.get()

        if not first_name or not surname or not email or not password or not confirm_password or not phone_number or not staff_code:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Validate first name
        if not first_name.replace(" ", "").isalpha():
            messagebox.showerror("Error", "First name must contain only alphabetic characters.")
            return

        # Validate surname
        if not surname.replace(" ", "").isalpha():
            messagebox.showerror("Error", "Surname must contain only alphabetic characters.")
            return
        
        if not (2 <= len(first_name) <= 15):
            messagebox.showerror("Error", "First name must be between 2 and 15 characters.")
            return

        # Validate surname length
        if not (2 <= len(surname) <= 15):
            messagebox.showerror("Error", "Surname must be between 2 and 15 characters.")
            return
        
        # Validate email
        if len(email) < 12 or len(email) > 30:
            messagebox.showerror("Error", "Email must be between 12 and 30 characters.")
            return
        if "@" not in email or ".co" not in email:
            messagebox.showerror("Error", "Invalid email address.")
            return

        # Validate password
        if len(password) < 8 or len(password) > 15:
            messagebox.showerror("Error", "Password must be between 8 and 15 characters.")
            return

        # Validate confirm password
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Validate phone number
        if not phone_number.isdigit() or len(phone_number) != 10:
            messagebox.showerror("Error", "Invalid phone number.")
            return

        # Validate staff code
        if len(staff_code) > 6:
            messagebox.showerror("Error", "Staff code must be 6 characters or less.")
            return
        if staff_code != "yes":
            messagebox.showerror("Error", "Staff Code is incorrect")
            return

        register1(first_name_entry, surname_entry, email_entry, password_entry, phone_entry, staff_code_entry)
        # Once registered successfully, you can close the registration window or navigate to another window

    # Register button
    register_button = tk.Button(frame, text="Register", command=register2, font=("Century Gothic", 14))
    register_button.grid(row=8, column=0, columnspan=2, pady=10)


  
# register_button = tk.Button(frame, text="Register", 
#                             command=lambda: register1(first_name_entry, surname_entry, email_entry, password_entry, phone_entry, staff_code_entry), 
#                             font=("Century Gothic", 14))
    
def back_to_login():
    # destroys the registration window
    registration_window.destroy()
    login_window()

def logout():
    # destroys main menu window to logout
    mainmenu_window.destroy()
    login_window()

def reveal():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        pass_reveal_button.config(text='🔒')  
    else:
        password_entry.config(show='*')
        pass_reveal_button.config(text='👁️ ')  

def login_window():
    global root, email_entry, password_entry, pass_reveal_button
    email_entry = None
    
    root = tk.Tk()
    root.title("Hotel Booking System")
    root.geometry("1920x1080")  # 1080p resolution
    root.configure(bg="#101C32")  # sets background color

    # header Label
    header_label = tk.Label(root, text="Starlight Hotel Booking System", font=("Century Gothic", 24, "bold"), bg="#101C32", fg="#E74C3C")
    header_label.pack(pady=100)

    # frame to center the login labels
    frame = tk.Frame(root, bg="#233D65")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # username entry
    
    username_label = tk.Label(frame, text="Username:", font=("Century Gothic", 14), bg="#233D65")
    username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    email_entry = tk.Entry(frame, font=("Century Gothic", 14))  # Define the email entry widget
    email_entry.grid(row=0, column=1, padx=10, pady=10)

    password_label = tk.Label(frame, text="Password:", font=("Century Gothic", 14), bg="#233D65")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
            
    password_entry = tk.Entry(frame, show="*", font=("Century Gothic", 14))  # Define the password entry widget
    password_entry.grid(row=1, column=1, padx=10, pady=10)
    
    pass_reveal_button = tk.Button(frame, text="👁" , command = reveal, font=("Century Gothic", 12))
    pass_reveal_button.grid(row=1, column=2, padx=10, pady=10)

    login_button = tk.Button(frame, text="Login", command=login1, font=("Century Gothic", 14))
    login_button.grid(row=2, columnspan=2, pady=20)

    register_button = tk.Button(frame, text="Register", command=register, font=("Century Gothic", 14))
    register_button.grid(row=3, columnspan=2, pady=10)

    close_button = tk.Button(frame, text="Close", command=close_window, font=("Century Gothic", 14))
    close_button.grid(row=4, columnspan=2, pady=10)

    # load and display Image
    try:
        image_path = r"starlight hotel logo circle (1).png"  # image path of the logo
        if os.path.exists(image_path):  # checks if the file from image path exists
            image = Image.open(image_path)
            image = image.resize((150, 150))  # Resize the image to desired dimensions
            image = ImageTk.PhotoImage(image)
            image_label = tk.Label(root, image=image, bg="#101C32")
            image_label.image = image  
            image_label.place(x=350, y=150, anchor=tk.CENTER)  # places image using x,y coords
        else:
            # prints a message if the image file is not found
            print("Image was not found. Make sure the image file exists.")
    except Exception as e:
        # checks if any errors occur when image is loading
        print("Error loading image:", e)

    root.mainloop()