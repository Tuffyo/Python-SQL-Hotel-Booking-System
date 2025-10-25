import tkinter as tk
from tkinter import messagebox

def password_window():
    global root, password_entry
    
    root = tk.Tk()
    root.title("Password")
    root.geometry("1920x1080")
    root.configure(bg="green")

    frame = tk.Frame(root, bg="darkgreen")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    password_label = tk.Label(frame, text="Password:", font=("Century Gothic", 14), bg="darkgreen", fg="white")
    password_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            
    password_entry = tk.Entry(frame, show="*", font=("Century Gothic", 14))
    password_entry.grid(row=0, column=1, padx=10, pady=10)

    login_button = tk.Button(frame, text="Login", command=imainmenu, font=("Century Gothic", 14))
    login_button.grid(row=1, columnspan=2, pady=20)
    
    # creates the logout button
    return_button = tk.Button(root, text="Return", command=root.destroy, font=("Century Gothic", 20), bg="red", fg="white", padx=20, pady=10)
    return_button.place(relx=1, rely=1, anchor="se")

    root.mainloop()

def imainmenu():
    password = password_entry.get()
    if password.lower() == "investor":
        open_main_menu()
    else:
        messagebox.showerror("Error", "Incorrect password. Please try again.")

def open_main_menu():
    global mainmenu_window
    mainmenu_window = tk.Toplevel()
    mainmenu_window.title("Main Menu")
    mainmenu_window.geometry("1920x1080")
    mainmenu_window.configure(bg="green")

    # creates a frame to hold the buttons
    button_frame = tk.Frame(mainmenu_window, bg="darkgreen")
    button_frame.place(relx=0.5, rely=0.5, anchor="center")

    # creates the analytics button
    analytics_button = tk.Button(button_frame, text=" 📈 Analytics", command=analytic, font=("Century Gothic", 50), bg="white", padx=10, pady=5)
    analytics_button.grid(row=0, column=2, padx=10)

    # creates the logout button
    logout_button = tk.Button(mainmenu_window, text="Logout", command=logout, font=("Century Gothic", 20), bg="red", fg="white", padx=20, pady=10)
    logout_button.place(relx=1, rely=1, anchor="se")
    
def analytic():
    from starlight import analytics
    analytics()

def logout():
    mainmenu_window.destroy()