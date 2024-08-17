from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import sqlite3
import os  

def create_table_if_not_exists():
    try:
        con = sqlite3.connect("webscrape.db")
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            phone TEXT NOT NULL,
                            email TEXT NOT NULL,
                            password TEXT NOT NULL
                          )''')
        con.commit()
        con.close()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error creating table: {e}")

def sign_up():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if not name or not phone or not email or not password or not confirm_password:
        messagebox.showerror("Error", "Please fill in all fields")
    elif any(char.isdigit() for char in name):
        messagebox.showerror("Error", "Name cannot contain digits")
    elif len(phone) != 10 or not phone.isdigit():
        messagebox.showerror("Error", "Phone number must be 10 digits")
    elif '@' not in email:
        messagebox.showerror("Error", "Invalid email")
    elif len(password) < 8:
        messagebox.showerror("Error", "Password must be at least 8 characters long")
    elif password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
    else:
        try:
            con = sqlite3.connect("webscrape.db")
            cursor = con.cursor()
            cursor.execute("INSERT INTO users (name, phone, email, password) VALUES (?, ?, ?, ?)",
                           (name, phone, email, password))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Sign up successful!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error inserting user into database: {e}")

def open_login_page():
    root.destroy()
    os.system("python login.py")

root = Tk()
root.geometry('800x600')
root.title("Sign Up Page")

bgImage = ImageTk.PhotoImage(file='3.png')
bglabel = Label(root, image=bgImage)
bglabel.place(x=0, y=0)

create_table_if_not_exists()

heading = Label(root, text="USER LOGIN", font=('Cambria', 15, 'bold'), bg="white")
heading.place(x=535, y=160)

name_label = Label(root, text="Name:", font=('Cambria', 12, 'bold'), bg="white", )
name_label.place(x=480, y=210)

name_entry = Entry(root, font=('Cambria', 10), bg="white", fg="black", relief="solid", bd=1)
name_entry.place(x=580, y=210)

phone_label = Label(root, text="Phone:", font=('Cambria', 12, 'bold'),  bg="white")
phone_label.place(x=480, y=245)

phone_entry = Entry(root, font=('Cambria', 10), bg="white", fg="black", relief="solid", bd=1)
phone_entry.place(x=580, y=245)

email_label = Label(root, text="Email:", font=('Cambria', 12, 'bold'), bg="white" )
email_label.place(x=480, y=285)

email_entry = Entry(root, font=('Cambria', 10), bg="white", fg="black", relief="solid", bd=1)
email_entry.place(x=580, y=285)

password_label = Label(root, text="Password:", font=('Cambria', 12, 'bold'), bg="white" )
password_label.place(x=480, y=325)

password_entry = Entry(root, show="*", font=('Cambria', 10), relief="solid", bd=1)
password_entry.place(x=580, y=325)

confirm_password_label = Label(root, text="Confirm \n Password:", font=('Cambria', 12, 'bold'), bg="white")
confirm_password_label.place(x=480, y=355)

confirm_password_entry = Entry(root, show="*", font=('Cambria', 10) ,relief="solid", bd=1)
confirm_password_entry.place(x=580, y=365)

sign_up_button = Button(root, text="Sign Up", command=sign_up, font=('Cambria', 12, 'bold') ,relief="raised", bd=2, bg="white")
sign_up_button.place(x=580, y=410)

l1 = Label(root, text="Already have an account?", font=('Cambria', 10, 'bold'), bg="white")
l1.place(x=520, y=460)

login_label = Button(root, text="Login", font=('Cambria', 10, 'bold'), cursor="hand2", command=open_login_page,)
login_label.place(x=580, y=490)

root.mainloop()
