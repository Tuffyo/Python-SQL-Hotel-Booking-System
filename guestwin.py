import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3
import datetime
import database
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
current_user_email = None
email_entry = None
password_entry = None

def gregister_user(firstname, surname, email, password, phone_number):
    global current_user_email
    conn = sqlite3.connect("databases.db")
    cursor = conn.cursor()

    try:
        # Insert the user's data into the database
        cursor.execute("INSERT INTO accounts (firstname, surname, email, password, phone_number) VALUES (?, ?, ?, ?, ?)",
                       (firstname, surname, email, password, phone_number))
        conn.commit()
        messagebox.showinfo("Registration Successful", "User registered successfully.")
    except sqlite3.Error as e:
        print("SQLite error:", e)
        messagebox.showerror("Registration Failed", "Failed to register user due to database error.")
    finally:
        conn.close()
        
def glogin(email, password):
    global current_user_email
    conn = sqlite3.connect("databases.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT email, password, staff_code FROM accounts")
        rows = cursor.fetchall()

        found = False
        for row in rows:
            if row[0] == email and row[1] == password and row[2] != "yes":
                found = True
                current_user_email = email  # Set current_user_email here
                messagebox.showinfo("Login Successful", "Welcome, {}".format(email))
                gmainmenu()
                break  # Exit the loop once user is found
        if not found :
            messagebox.showerror("Login Failed", "Invalid email or password.")
            # Clear email and password fields for new input
            email_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
    except sqlite3.Error as e:
        print("Error logging in:", e)
        messagebox.showerror("Login Failed", "Failed to login.")
    finally:
        conn.close()

def gregister1(first_name_entry, surname_entry, email_entry, password_entry, phone_entry):
    # Retrieve values from entry widgets
    first_name = first_name_entry.get()
    surname = surname_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    phone_number = phone_entry.get()
    
    
    # Check if all required fields are filled
    if first_name and surname and email and password and phone_number:
        # Pass all the retrieved values to the register_user function
        gregister_user(first_name, surname, email, password, phone_number, )
        
        # Clear the entry widgets after registration
        first_name_entry.delete(0, tk.END)
        surname_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please fill in all the required fields.")
        
def login1():
    global email_entry, password_entry

    email = email_entry.get()  # Access email directly from the global entry widget
    password = password_entry.get()  # Access password directly from the global entry widget
    
    if email and password:
        glogin(email, password)  
        
        # Clear the email and password entry after login
        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        root.destroy()
    else:
        messagebox.showerror("Error", "Please enter both email and password.")
        
def submit_booking(room_type, name, email, checkin_date_str, checkout_date_str, card_number, cvc, expiry_date, num_guests, breakfast_booking, dinner_booking):
    try:
        # Convert strings to date objects
        checkin_date = datetime.datetime.strptime(checkin_date_str, '%d/%m/%y')
        checkout_date = datetime.datetime.strptime(checkout_date_str, '%d/%m/%y')

        # Get the cost per night per person based on room type
        if room_type == "Standard Room":
            cost_per_night_per_person = 100
        elif room_type == "Deluxe Room":
            cost_per_night_per_person = 150
        else:
            raise ValueError("Invalid room type")

        # Calculate total cost based on room type, duration, number of guests, breakfast, and dinner bookings
        total_nights = (checkout_date - checkin_date).days
        total_cost = cost_per_night_per_person * total_nights * num_guests
        total_cost += 30 * total_nights * num_guests if breakfast_booking else 0
        total_cost += 30 * total_nights * num_guests if dinner_booking else 0
        
        # Verify CVC (must be 3 digits and an integer)
        if not (cvc.isdigit() and len(cvc) == 3):
            raise ValueError("Invalid CVC")
        
        # Verify card number (must be numeric and of appropriate length)
        if not (card_number.isdigit() and len(card_number) == 16):
            raise ValueError("Invalid card number")
        
        # Verify expiry date format (dd/mm/yy)
        try:
            datetime.datetime.strptime(expiry_date, '%d/%m/%y')
        except ValueError:
            raise ValueError("Invalid expiry date format. Please use dd/mm/yy")
        
        # Connect to the payment database
        conn = sqlite3.connect("databases.db")
        cursor = conn.cursor()

        # Insert booking and payment details into the database
        cursor.execute("INSERT INTO payments (room_type, name, email, checkin_date, checkout_date, card_number, cvc, expiry_date, num_guests, breakfast_booking, dinner_booking, total_cost) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (room_type, name, email, checkin_date_str, checkout_date_str, card_number, cvc, expiry_date, num_guests, breakfast_booking, dinner_booking, total_cost))
        conn.commit()

        # Close connection
        conn.close()

        # Show booking confirmation message
        messagebox.showinfo("Booking Confirmation", "Your booking has been submitted successfully!")
    except sqlite3.Error as e:
        print("Error submitting booking:", e)
        messagebox.showerror("Booking Error", "Failed to submit booking. Please try again.")
    except ValueError as ve:
        print("Validation error:", ve)
        messagebox.showerror("Validation Error", str(ve))
    except Exception as e:
        print("Error:", e)


def create_booking(room_type):
    # Create booking window
    booking_window = tk.Toplevel()
    booking_window.title("Booking Details")
    booking_window.geometry("1920x1080")
    booking_window.configure(bg="#4CBEB4")

    # Left frame for left side inputs
    left_frame = tk.Frame(booking_window, bg="#1A8178")
    left_frame.place(relx=0.25, rely=0.5, anchor="center")

    # Add room type label
    type_label = tk.Label(left_frame, text=f"Room Type: {room_type}", font=("Calibri", 20), fg="white", bg="#1A8178")
    type_label.pack(pady=20)
    
    # Create booking form on the left
    tk.Label(left_frame, text="Name:", font=("Calibri", 16), fg="white", bg="#1A8178").pack(pady=10)
    name_entry = tk.Entry(left_frame, font=("Calibri", 14))
    name_entry.pack(pady=10)

    tk.Label(left_frame, text="Email:", font=("Calibri", 16), fg="white", bg="#1A8178").pack(pady=10)
    email_entry = tk.Entry(left_frame, font=("Calibri", 14))
    email_entry.pack(pady=10)

    tk.Label(left_frame, text="Check-in Date:", font=("Calibri", 16), fg="white", bg="#1A8178").pack(pady=10)
    checkin_cal = Calendar(left_frame, selectmode='day', date_pattern='dd/mm/yy')
    checkin_cal.pack(pady=10)

    tk.Label(left_frame, text="Check-out Date:", font=("Calibri", 16), fg="white", bg="#1A8178").pack(pady=10)
    checkout_cal = Calendar(left_frame, selectmode='day', date_pattern='dd/mm/yy')
    checkout_cal.pack(pady=10)

    # Right frame for right-side inputs
    right_frame = tk.Frame(booking_window, bg="#1A8178")
    right_frame.place(relx=0.75, rely=0.5, anchor="center")

    # Create booking form on the right
    tk.Label(right_frame, text="Number of Guests:", font=("Calibri", 16), fg="white", bg="#1A8178").pack(pady=10)
    guests_entry = tk.Entry(right_frame, font=("Calibri", 14))
    guests_entry.pack(pady=10)

    # Checkbox for breakfast booking
    breakfast_booking = tk.BooleanVar()
    tk.Checkbutton(right_frame, text="Add Breakfast ($30 per night)", variable=breakfast_booking, font=("Calibri", 14), fg="white", bg="#1A8178").pack(pady=10)

    # Checkbox for dinner booking
    dinner_booking = tk.BooleanVar()
    tk.Checkbutton(right_frame, text="Add Dinner ($30 per night)", variable=dinner_booking, font=("Calibri", 14), fg="white", bg="#1A8178").pack(pady=10)

    tk.Label(right_frame, text="Card Number:", font=("Calibri", 16), fg="white", bg="#1A8178").pack(pady=10)
    card_number_entry = tk.Entry(right_frame, font=("Calibri", 14))
    card_number_entry.pack(pady=10)

    tk.Label(right_frame, text="CVC:", font=("Calibri", 16), fg="white", bg="#1A8178").pack(pady=10)
    cvc_entry = tk.Entry(right_frame, font=("Calibri", 14))
    cvc_entry.pack(pady=10)

    tk.Label(right_frame, text="Expiry Date:", font=("Calibri", 16), fg="white", bg="#1A8178").pack(pady=10)
    expiry_entry = tk.Entry(right_frame, font=("Calibri", 14))
    expiry_entry.pack(pady=10)

    # Create submit button
    submit_button = tk.Button(right_frame, text="Submit", command=lambda: submit_booking(room_type, name_entry.get(), email_entry.get(), checkin_cal.get_date(), checkout_cal.get_date(), card_number_entry.get(), cvc_entry.get(), expiry_entry.get(), int(guests_entry.get()), breakfast_booking.get(), dinner_booking.get()), font=("Calibri", 14))
    submit_button.pack(pady=20)

    # Return button
    return_button = tk.Button(booking_window, text="Return", command=booking_window.destroy, font=("Century Gothic", 17), bg="red", fg="white", width=12, height=3)
    return_button.place(relx=1, rely=1, anchor="se")


def view_bookings_window(current_user_email):
    # Create new or refresh an existing window
    view_bookings_window = tk.Toplevel()
    view_bookings_window.title("View Bookings")
    view_bookings_window.geometry("900x600")
    view_bookings_window.configure(bg="#4CBEB4")

    # Scrollable frame setup (for multiple bookings)
    container = tk.Frame(view_bookings_window, bg="#4CBEB4")
    container.pack(fill="both", expand=True, padx=20, pady=20)

    canvas = tk.Canvas(container, bg="#4CBEB4", highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#4CBEB4")

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Fetch bookings fresh each time
    conn = sqlite3.connect("databases.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, room_type, checkin_date, checkout_date, total_cost FROM payments WHERE email=?",
        (current_user_email,),
    )
    bookings = cursor.fetchall()
    conn.close()

    # Display bookings
    if bookings:
        for booking in bookings:
            booking_id, room_type, checkin, checkout, total = booking
            frame = tk.Frame(scrollable_frame, bg="#1A8178", padx=20, pady=10)
            frame.pack(fill="x", pady=10)

            tk.Label(frame, text=f"Booking ID: {booking_id}", font=("Century Gothic", 14), bg="#1A8178", fg="white").pack(anchor="w")
            tk.Label(frame, text=f"Room Type: {room_type}", font=("Century Gothic", 14), bg="#1A8178", fg="white").pack(anchor="w")
            tk.Label(frame, text=f"Check-in: {checkin}   Check-out: {checkout}", font=("Century Gothic", 14), bg="#1A8178", fg="white").pack(anchor="w")
            tk.Label(frame, text=f"Total: ${total:.2f}", font=("Century Gothic", 14), bg="#1A8178", fg="white").pack(anchor="w")

            refund_button = tk.Button(frame, text="Refund", font=("Century Gothic", 12), bg="white", command=lambda id=booking_id: refund_booking(id))
            refund_button.pack(anchor="e", pady=5)
    else:
        tk.Label(scrollable_frame, text="No bookings found.", font=("Century Gothic", 16), bg="#4CBEB4", fg="white").pack(pady=20)


def refund_booking(id):
    # Function to handle refund confirmation
    def confirm_refund():
        # Connect to the payment database
        conn = sqlite3.connect("databases.db")
        cursor = conn.cursor()

        try:
            # Check if the booking exists
            cursor.execute("SELECT * FROM payments WHERE id=?", (id,))
            booking = cursor.fetchone()

            if booking:
                # Delete the booking from the database
                cursor.execute("DELETE FROM payments WHERE id=?", (id,))
                conn.commit()

                messagebox.showinfo("Refund", f"Booking with ID {id} has been refunded and deleted.")
            else:
                messagebox.showerror("Error", f"No booking found with ID: {id}")
        except sqlite3.Error as e:
            print("Error refunding booking:", e)
            messagebox.showerror("Error", "Failed to refund booking. Please try again.")
        finally:
            # Close connection
            conn.close()

    # Display confirmation dialog
    confirmation = messagebox.askyesno("Confirm Refund", f"Are you sure you want to refund booking ID: {id}?")

    # If user confirms, proceed with the refund
    if confirmation:
        confirm_refund()




def gmainmenu():
    global current_user_email
    global gmainmenu_window
    gmainmenu_window = tk.Toplevel()
    gmainmenu_window.title("Main Menu")
    gmainmenu_window.geometry("1920x1080")
    gmainmenu_window.configure(bg="#4CBEB4")
    
    gheader_label = tk.Label(gmainmenu_window, text="Welcome to the Main Menu", font=("Century Gothic", 24, "bold"), bg="#1A8178", fg="#E74C3C")
    gheader_label.pack(pady=100)

    # creates a frame to hold the buttons
    gbutton_frame = tk.Frame(gmainmenu_window, bg="#1A8178")
    gbutton_frame.place(relx=0.5, rely=0.5, anchor="center")

    # creates the Add Booking button
    addbookings_button = tk.Button(gbutton_frame, text="📅 Book a Room", command=create_room_listing, font=("Century Gothic", 50), bg="white", padx=10, pady=5)
    addbookings_button.grid(row=0, column=0, padx=7)

    # creates the View Booking button
    viewbookings_button = tk.Button(gbutton_frame, text="💻 View Booking", command=lambda: view_bookings_window(current_user_email), font=("Century Gothic", 50), bg="white", padx=10, pady=5)
    viewbookings_button.grid(row=0, column=1, padx=7)

    # creates the Logout button
    glogout_button = tk.Button(gmainmenu_window, text="Logout", command=logout, font=("Century Gothic", 20), bg="red", fg="white", padx=20, pady=10)
    glogout_button.place(relx=1, rely=1, anchor="se")

    gmainmenu_window.mainloop()

def logout():
    gmainmenu_window.destroy()  # Close the guest main menu window


def create_room_listing():
    # Create room listing window
    room_listing_window = tk.Toplevel()
    room_listing_window.title("Room Listing")
    room_listing_window.geometry("1920x1080")
    room_listing_window.configure(bg="#4CBEB4")

    # Header label
    header_label = tk.Label(
        room_listing_window,
        text="Available Rooms",
        font=("Century Gothic", 30, "bold"),
        bg="#1A8178",
        fg="white",
        padx=20,
        pady=20
    )
    header_label.pack(fill="x", pady=(0, 30))

    # Frame to hold all room cards
    content_frame = tk.Frame(room_listing_window, bg="#4CBEB4")
    content_frame.pack(expand=True, fill="both")

    # Sample room details
    room_details = [
    {"type": "Standard Room", "price": "$100 per night", "image_path": os.path.join(BASE_DIR, "room1.jpg")},
    {"type": "Deluxe Room", "price": "$150 per night", "image_path": os.path.join(BASE_DIR, "room2.jpg")}
    ]


    # Keep references to images to prevent garbage collection
    image_refs = []

    for i, room in enumerate(room_details):
        # Create a frame for each room
        room_frame = tk.Frame(content_frame, bg="#1A8178", padx=20, pady=20, relief="raised", bd=4)
        room_frame.grid(row=0, column=i, padx=50, pady=20)

        # Load and display room image
        try:
            if os.path.exists(room["image_path"]):
                image = Image.open(room["image_path"])
                image = image.resize((400, 300))
                photo = ImageTk.PhotoImage(image)
                image_refs.append(photo)  # Keep reference
                img_label = tk.Label(room_frame, image=photo, bg="#1A8178")
                img_label.image = photo
                img_label.pack(pady=10)
            else:
                tk.Label(room_frame, text="Image Not Found", font=("Calibri", 14), bg="#1A8178", fg="white").pack(pady=10)
        except Exception as e:
            print("Error loading image:", e)
            tk.Label(room_frame, text="Error loading image", font=("Calibri", 14), bg="#1A8178", fg="white").pack(pady=10)

        # Room info
        tk.Label(room_frame, text=room["type"], font=("Century Gothic", 20, "bold"), bg="#1A8178", fg="white").pack(pady=10)
        tk.Label(room_frame, text=room["price"], font=("Century Gothic", 16), bg="#1A8178", fg="white").pack(pady=5)

        # Book Now button
        book_button = tk.Button(
            room_frame,
            text="Book Now",
            command=lambda rt=room["type"]: create_booking(rt),
            font=("Century Gothic", 16),
            bg="white",
            fg="black",
            padx=10,
            pady=5
        )
        book_button.pack(pady=10)

    # Return button
    return_button = tk.Button(
        room_listing_window,
        text="Return",
        command=room_listing_window.destroy,
        font=("Century Gothic", 17),
        bg="red",
        fg="white",
        width=12,
        height=2
    )
    return_button.pack(side="bottom", pady=30)


def gregister():
    global email_entry, password_entry

    # Destroy the login window
    root.destroy()

    # Create the registration window
    global gregistration_window
    gregistration_window = tk.Toplevel()
    gregistration_window.title("Registration")
    gregistration_window.geometry("1920x1080")
    gregistration_window.configure(bg="#4CBEB4")

    # Registration components
    frame = tk.Frame(gregistration_window, bg="#1A8178")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # First Name
    first_name_label = tk.Label(frame, text="First Name:", font=("Century Gothic", 14), bg="#1A8178", fg="white")
    first_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    global first_name_var
    first_name_var = tk.StringVar()
    first_name_entry = tk.Entry(frame, font=("Century Gothic", 14), textvariable=first_name_var)
    first_name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Surname
    surname_label = tk.Label(frame, text="Surname:", font=("Century Gothic", 14), bg="#1A8178", fg="white")
    surname_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    global surname_var
    surname_var = tk.StringVar()
    surname_entry = tk.Entry(frame, font=("Century Gothic", 14), textvariable=surname_var)
    surname_entry.grid(row=1, column=1, padx=10, pady=10)

    # Email
    email_label = tk.Label(frame, text="Email:", font=("Century Gothic", 14), bg="#1A8178", fg="white")
    email_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    email_entry = tk.Entry(frame, font=("Century Gothic", 14))  # Use the global email_entry
    email_entry.grid(row=2, column=1, padx=10, pady=10)

    # Password
    password_label = tk.Label(frame, text="Password:", font=("Century Gothic", 14), bg="#1A8178", fg="white")
    password_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    password_entry = tk.Entry(frame, show="*", font=("Century Gothic", 14))  # Use the global password_entry
    password_entry.grid(row=3, column=1, padx=10, pady=10)

    # Confirm Password
    confirm_password_label = tk.Label(frame, text="Confirm Password:", font=("Century Gothic", 14), bg="#1A8178", fg="white")
    confirm_password_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    confirm_password_entry = tk.Entry(frame, show="*", font=("Century Gothic", 14))
    confirm_password_entry.grid(row=4, column=1, padx=10, pady=10)

    # Phone Number
    phone_label = tk.Label(frame, text="Phone Number:", font=("Century Gothic", 14), bg="#1A8178", fg="white")
    phone_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

    phone_entry = tk.Entry(frame, font=("Century Gothic", 14))
    phone_entry.grid(row=5, column=1, padx=10, pady=10)

    # Return to login button
    back_button = tk.Button(frame, text="Return", command=gback_to_login, font=("Century Gothic", 14))
    back_button.grid(row=7, column=0, columnspan=2, pady=10)

    def gregister2():
        first_name = first_name_entry.get()
        surname = surname_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        phone_number = phone_entry.get()

        if not first_name or not surname or not email or not password or not confirm_password or not phone_number :
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


        gregister1(first_name_entry, surname_entry, email_entry, password_entry, phone_entry)
        # Once registered successfully, you can close the registration window or navigate to another window

    # Register button
    register_button = tk.Button(frame, text="Register", command=gregister2, font=("Century Gothic", 14))
    register_button.grid(row=8, column=0, columnspan=2, pady=10)
    
def gback_to_login():
    # destroys the registration window
    gregistration_window.destroy()
    glogin_window()

def gclose_window():
    root.destroy()

def greveal():
    global password_entry
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        pass_reveal_button.config(text='🔒')  
    else:
        password_entry.config(show='*')
        pass_reveal_button.config(text='👁️ ') 


def glogin_window():
    global root, email_entry, password_entry, pass_reveal_button
    
    root = tk.Tk()
    root.title("Hotel Booking System")
    root.geometry("1920x1080")  # 1080p resolution
    root.configure(bg="#4CBEB4")  # sets background color

    # header Label
    header_label = tk.Label(root, text="Starlight Hotel Booking System", font=("Century Gothic", 24, "bold"), bg="#4CBEB4", fg="#E74C3C")
    header_label.pack(pady=100)

    # frame to center the login labels
    frame = tk.Frame(root, bg="#1A8178")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # username entry
    
    username_label = tk.Label(frame, text="Username:", font=("Century Gothic", 14), bg="#1A8178")
    username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    email_entry = tk.Entry(frame, font=("Century Gothic", 14))  # Define the email entry widget
    email_entry.grid(row=0, column=1, padx=10, pady=10)

    password_label = tk.Label(frame, text="Password:", font=("Century Gothic", 14), bg="#1A8178")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
            
    password_entry = tk.Entry(frame, show="*", font=("Century Gothic", 14))  # Define the password entry widget
    password_entry.grid(row=1, column=1, padx=10, pady=10)
    
    pass_reveal_button = tk.Button(frame, text="👁" , command = greveal, font=("Century Gothic", 12))
    pass_reveal_button.grid(row=1, column=2, padx=10, pady=10)

    login_button = tk.Button(frame, text="Login", command=login1, font=("Century Gothic", 14))
    login_button.grid(row=2, columnspan=2, pady=20)

    register_button = tk.Button(frame, text="Register", command=gregister, font=("Century Gothic", 14))
    register_button.grid(row=3, columnspan=2, pady=10)

    close_button = tk.Button(frame, text="Close", command=gclose_window, font=("Century Gothic", 14))
    close_button.grid(row=4, columnspan=2, pady=10)

    # load and display Image
    try:
        image_path = r"starlight hotel logo circle (1).png"  # image path of the logo
        if os.path.exists(image_path):  # checks if the file from image path exists
            image = Image.open(image_path)
            image = image.resize((150, 150))  # Resize the image to desired dimensions
            image = ImageTk.PhotoImage(image)
            image_label = tk.Label(root, image=image, bg="#1A8178")
            image_label.image = image  
            image_label.place(x=350, y=150, anchor=tk.CENTER)  # places image using x,y coords
        else:
            # prints a message if the image file is not found
            print("Image was not found. Make sure the image file exists.")
    except Exception as e:
        # checks if any errors occur when image is loading
        print("Error loading image:", e)

    root.mainloop()