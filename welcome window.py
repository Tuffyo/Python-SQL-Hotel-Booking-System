import tkinter as tk
from PIL import Image, ImageTk
import os
import database  

def open_guest_login():
    print("Opening Guest Login Page")
    from guestwin import glogin_window
    glogin_window()

def open_staff_login():
    print("Opening Staff Login Page")
    from starlight import login_window
    login_window()

def open_investor_login():
    print("Opening Investor Login Page")
    from investor import password_window
    password_window()


root = tk.Tk()
root.title("Welcome Page")
root.geometry("1920x1080")
root.configure(bg="#101C32")

header_frame = tk.Frame(root, bg="#101C32")
header_frame.pack(pady=40)

try:
    # fixed logo path
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "starlight hotel logo circle (1).png")
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((100, 100))
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(header_frame, image=logo_photo, bg="#101C32")
        logo_label.image = logo_photo
        logo_label.pack(side="left", padx=(0, 20))
        print(f"Logo loaded from: {logo_path}")
    else:
        print(f"⚠️ Logo not found at: {logo_path}")
except Exception as e:
    print("Error loading logo image:", e)

welcome_label = tk.Label(
    header_frame,
    text="Welcome to Starlight Hotel",
    font=("Century Gothic", 32, "bold"),
    fg="#E74C3C",
    bg="#101C32"
)
welcome_label.pack(side="left")

instruction_label = tk.Label(
    root,
    text="Choose one of the following login options below",
    font=("Calibri", 18),
    fg="white",
    bg="#101C32"
)
instruction_label.pack(pady=30)

button_frame = tk.Frame(root, bg="#101C32")
button_frame.pack(pady=40, anchor="w", padx=120)

button_style = {
    "font": ("Century Gothic", 28),
    "bg": "white",
    "padx": 20,
    "pady": 10,
    "width": 12,
}

guests_button = tk.Button(button_frame, text="🧑 Guests", command=open_guest_login, **button_style)
guests_button.grid(row=0, column=0, padx=30)

staff_button = tk.Button(button_frame, text="💼 Staff", command=open_staff_login, **button_style)
staff_button.grid(row=0, column=1, padx=30)

investor_button = tk.Button(button_frame, text="💰 Investor", command=open_investor_login, **button_style)
investor_button.grid(row=0, column=2, padx=30)

# ====== CONTACT INFO ======
email_label = tk.Label(
    root,
    text="Email: StarLightHotel2004@gmail.com",
    font=("Calibri", 14),
    fg="white",
    bg="#101C32"
)
email_label.pack(side="bottom", pady=(10, 0))

phone_label = tk.Label(
    root,
    text="Phone Number: 07123 456 789",
    font=("Calibri", 14),
    fg="white",
    bg="#101C32"
)
phone_label.pack(side="bottom", pady=(0, 20))

def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))
root.bind("<Escape>", toggle_fullscreen)

root.mainloop()
