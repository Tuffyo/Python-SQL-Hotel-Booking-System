import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sqlite3
from starlight import analytics  # Reuse the same analytics chart

# Staff Login Window

def login_window():
    global root, email_entry, password_entry, pass_reveal_button

    root = tk.Tk()
    root.title("Starlight Hotel - Staff Login")
    root.geometry("1920x1080")
    root.configure(bg="#003300")  # green background

    # Header
    header_label = tk.Label(
        root,
        text="Starlight Hotel Staff Portal",
        font=("Century Gothic", 28, "bold"),
        bg="#003300",
        fg="#E0E0E0",
    )
    header_label.pack(pady=100)

    # Frame for login inputs
    frame = tk.Frame(root, bg="#004d00", padx=30, pady=30)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Email Label and Entry
    email_label = tk.Label(frame, text="Email:", font=("Century Gothic", 16), bg="#004d00", fg="white")
    email_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    email_entry = tk.Entry(frame, font=("Century Gothic", 16), width=25)
    email_entry.grid(row=0, column=1, padx=10, pady=10)

    # Password Label and Entry
    password_label = tk.Label(frame, text="Password:", font=("Century Gothic", 16), bg="#004d00", fg="white")
    password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    password_entry = tk.Entry(frame, show="*", font=("Century Gothic", 16), width=25)
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    pass_reveal_button = tk.Button(
        frame, text="👁", command=reveal_password, font=("Century Gothic", 12)
    )
    pass_reveal_button.grid(row=1, column=2, padx=10, pady=10)

    # Login Button
    login_button = tk.Button(
        frame, text="Login", command=login, font=("Century Gothic", 16), bg="white", fg="black"
    )
    login_button.grid(row=2, columnspan=3, pady=20)

    # Close Button
    close_button = tk.Button(
        frame, text="Close", command=root.destroy, font=("Century Gothic", 14), bg="red", fg="white"
    )
    close_button.grid(row=3, columnspan=3, pady=10)

    # Logo
    try:
        image_path = r"starlight hotel logo circle (1).png"
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((150, 150))
            logo = ImageTk.PhotoImage(image)
            image_label = tk.Label(root, image=logo, bg="#003300")
            image_label.image = logo
            image_label.place(x=350, y=150, anchor=tk.CENTER)
        else:
            print("Logo not found, skipping image load.")
    except Exception as e:
        print("Error loading logo:", e)

    root.mainloop()


def login():
    email = email_entry.get()
    password = password_entry.get()

    if not email or not password:
        messagebox.showerror("Error", "Please enter both email and password.")
        return

    conn = sqlite3.connect("databases.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT email, password, staff_code FROM accounts")
        rows = cursor.fetchall()

        for row in rows:
            if row[0] == email and row[1] == password and row[2] == "yes":
                messagebox.showinfo("Login Successful", f"Welcome, {email}")
                root.destroy()
                staff_mainmenu()
                return

        messagebox.showerror("Login Failed", "Invalid credentials or not a staff account.")
    except sqlite3.Error as e:
        print("Database error:", e)
        messagebox.showerror("Error", "Database connection failed.")
    finally:
        conn.close()


def reveal_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        pass_reveal_button.config(text="🔒")
    else:
        password_entry.config(show="*")
        pass_reveal_button.config(text="👁")



# Staff Main Menu
def staff_mainmenu():
    mainmenu = tk.Tk()
    mainmenu.title("Starlight Hotel - Staff Dashboard")
    mainmenu.geometry("1920x1080")
    mainmenu.configure(bg="#004d00")

    header = tk.Label(
        mainmenu,
        text="Staff Main Menu",
        font=("Century Gothic", 26, "bold"),
        bg="#004d00",
        fg="white",
    )
    header.pack(pady=100)

    button_frame = tk.Frame(mainmenu, bg="#004d00")
    button_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Book Guest button
    book_button = tk.Button(
        button_frame,
        text="📘 Book Guest",
        command=book_guest,
        font=("Century Gothic", 48),
        bg="white",
        fg="black",
        padx=20,
        pady=10,
    )
    book_button.grid(row=0, column=0, padx=30)

    # Analytics button
    analytics_button = tk.Button(
        button_frame,
        text="📈 Analytics",
        command=analytics,
        font=("Century Gothic", 48),
        bg="white",
        fg="black",
        padx=20,
        pady=10,
    )
    analytics_button.grid(row=0, column=1, padx=30)

    # Logout button
    logout_button = tk.Button(
        mainmenu,
        text="Logout",
        command=mainmenu.destroy,
        font=("Century Gothic", 20),
        bg="red",
        fg="white",
        padx=20,
        pady=10,
    )
    logout_button.place(relx=1, rely=1, anchor="se")

    mainmenu.mainloop()


# ======================
# Book Guest Window
# ======================
def book_guest():
    booking_window = tk.Toplevel()
    booking_window.title("Book Guest Room")
    booking_window.geometry("1920x1080")
    booking_window.configure(bg="#006633")

    tk.Label(
        booking_window,
        text="Book Guest Room",
        font=("Century Gothic", 24, "bold"),
        bg="#006633",
        fg="white",
    ).pack(pady=50)

    # Basic booking form
    form_frame = tk.Frame(booking_window, bg="#004d00", padx=20, pady=20)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(form_frame, text="Guest Name:", font=("Century Gothic", 14), bg="#004d00", fg="white").grid(row=0, column=0, pady=10, sticky="w")
    name_entry = tk.Entry(form_frame, font=("Century Gothic", 14))
    name_entry.grid(row=0, column=1, pady=10)

    tk.Label(form_frame, text="Room Type:", font=("Century Gothic", 14), bg="#004d00", fg="white").grid(row=1, column=0, pady=10, sticky="w")
    room_entry = tk.Entry(form_frame, font=("Century Gothic", 14))
    room_entry.grid(row=1, column=1, pady=10)

    tk.Label(form_frame, text="Nights:", font=("Century Gothic", 14), bg="#004d00", fg="white").grid(row=2, column=0, pady=10, sticky="w")
    nights_entry = tk.Entry(form_frame, font=("Century Gothic", 14))
    nights_entry.grid(row=2, column=1, pady=10)

    tk.Label(form_frame, text="Guests:", font=("Century Gothic", 14), bg="#004d00", fg="white").grid(row=3, column=0, pady=10, sticky="w")
    guests_entry = tk.Entry(form_frame, font=("Century Gothic", 14))
    guests_entry.grid(row=3, column=1, pady=10)

    # Submit Button
    submit_button = tk.Button(
        form_frame,
        text="Submit Booking",
        command=lambda: submit_booking(
            name_entry.get(),
            room_entry.get(),
            nights_entry.get(),
            guests_entry.get(),
            booking_window,
        ),
        font=("Century Gothic", 14),
        bg="white",
        fg="black",
        padx=20,
        pady=5,
    )
    submit_button.grid(row=4, columnspan=2, pady=20)


def submit_booking(name, room_type, nights, guests, window):
    if not name or not room_type or not nights or not guests:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        nights = int(nights)
        guests = int(guests)
    except ValueError:
        messagebox.showerror("Error", "Nights and guests must be numbers.")
        return

    messagebox.showinfo("Booking Complete", f"Guest '{name}' booked {room_type} for {nights} nights, {guests} guests.")
    window.destroy()