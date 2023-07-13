from tkinter import *
from tkinter import messagebox
from password_generator import generate_password
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    password = generate_password()
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    # print(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "username": username,
            "password": password,
        }
    }

    if website == "" or username == "" or password == "":
        messagebox.showinfo(title="Oops", message="Don't leave and fields empty!")
        return

    is_okay = messagebox.askokcancel(title="Confirm Details",
                                     message=f"These are the details entered: \nUsername: {username}"
                                             f"\nPassword: {password} \nAre these correct?")
    if is_okay:
        # check if 'data.json' file exists
        try:
            with open("data.json", "r") as file:
                # Reading old data
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                # Write new data
                json.dump(new_data, file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as file:
                # Saving new data
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showinfo(title="Oops", message="Don't leave website field empty!")
        return

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No data file found")
    else:
        if website in data:
            username = data[website]["username"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"username: {username} \npassword: {password}")
        else:
            messagebox.showinfo(title="Oops", message=f"No details for {website} exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

canvas = Canvas(width=200, height=200, highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website: ")
website_label.grid(row=1, column=0)
username_label = Label(text="Email/Username: ")
username_label.grid(row=2, column=0)
password_label = Label(text="Password: ")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=24)
website_entry.grid(row=1, column=1)
website_entry.focus()
username_entry = Entry(width=44)
username_entry.grid(row=2, column=1, columnspan=2)
username_entry.insert(0, "alan@gmail.com")
password_entry = Entry(width=24)
password_entry.grid(row=3, column=1)

# Buttons
generate_pwd_btn = Button(text="Generate Password", command=generate)
generate_pwd_btn.grid(row=3, column=2)
add_btn = Button(text="Add", width=41, command=save)
add_btn.grid(row=4, column=1, columnspan=2)
search_btn = Button(text="Search", width=15, command=search)
search_btn.grid(row=1, column=2)

window.mainloop()
