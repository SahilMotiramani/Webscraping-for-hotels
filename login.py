import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
import sqlite3
import os
import recent  

def login():
    email = entry_username.get()
    password = entry_password.get()

    try:
        con = sqlite3.connect("webscrape.db")
        cursor = con.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()

        if user:
            con.close() 
            open_home_page()  
        else:
            messagebox.showerror("Error", "Incorrect email or password")

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error accessing database: {e}")

def open_register_page():
    root.destroy()
    os.system("python register.py")

def open_home_page():
    root.destroy()
    os.system("python recent.py")
    recent.display_home_page()

root = tk.Tk()
bgImage = ImageTk.PhotoImage(file='4.png')
bglabel = tk.Label(root, image=bgImage)
bglabel.place(x=0, y=0)

root_width = 800
root_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_coordinate = (screen_width - root_width) // 2
y_coordinate = (screen_height - root_height) // 2

root.geometry(f"{root_width}x{root_height}+{x_coordinate}+{y_coordinate}")
root.title("Login Page")

heading = tk.Label(root, text="USER LOGIN", font=('Cambria', 15, 'bold'), bg="white")
heading.place(x=535, y=160)

username = tk.Label(root, text="Email", font=('Cambria', 12, 'bold'), bg="white")
username.place(x=480, y=220)

password = tk.Label(root, text="Password", font=('Cambria', 12, 'bold'), bg="white")
password.place(x=480, y=255)

entry_username = tk.Entry(root, font=('Cambria', 10), relief="solid")
entry_username.place(x=580, y=220)

entry_password = tk.Entry(root, show='*', font=('Cambria', 10), relief="solid")
entry_password.place(x=580, y=255)

button_signin = tk.Button(root, text="Login", command=login, font=('Cambria', 12, 'bold'), bg="white")
button_signin.place(x=580, y=320)

separator = tk.Frame(root, height=0.1, bd=0.1, bg="black")
separator.place(x=460, y=380, width=280)

label_forgot_password = tk.Label(root, text="Forgot Password?", font=('Cambria', 10, 'underline'), bg="white")
label_forgot_password.place(x=620, y=285)

label_dont_have_account = tk.Label(root, text="Don't have an account?", font=('Cambria', 10), bg="white")
label_dont_have_account.place(x=550, y=400)

label_register = tk.Button(root, text="Register", command=open_register_page, font=('Cambria', 10, 'bold'), bg="white")
label_register.place(x=580, y=425)

root.mainloop()
