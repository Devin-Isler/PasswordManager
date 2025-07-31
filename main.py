from tkinter import *
from tkinter import messagebox
import re
from random import shuffle, randint, choice
import json

most_used_email = "yourmail@mail.com"
json_file = "passwords.json"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    letter_list = [choice(letters) for _ in range(nr_letters)]
    symbol_list = [choice(symbols) for _ in range(nr_symbols)]
    number_list = [choice(numbers) for _ in range(nr_numbers)]

    password_list = letter_list + symbol_list + number_list

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    new_data = {website: {
        "email": email,
        "password": password
        }
    }

    if password and website and email:
        if _ := re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email):
            is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:"
                                                                  f"\nWebsite: {website}"
                                                                  f"\nEmail: {email}\nPassword:"
                                                                  f"{password}\nIs it ok to save?")
            if is_ok:
                try:
                    with open(json_file, "r") as file:
                        #yazılı datayı oku
                        data = json.load(file)

                except:
                    with open(json_file, "w") as file:
                        json.dump(new_data, file, indent=4)
                else:
                    # eklenecek datayı eski dataya ekle
                    data.update(new_data)
                    with open(json_file, "w") as file:
                        #dosyayı silip hepsini dosyaya yaz
                        json.dump(data, file, indent=4)
                finally:
                    website_entry.delete(0, END)
                    email_entry.delete(0, END)
                    email_entry.insert(0, most_used_email)
                    password_entry.delete(0, END)
        else:
            messagebox.showerror(title="Error", message="Your email address is not valid.")
    else:
        messagebox.showerror(title="Error", message="There is some missing info.")


# ---------------------------- SEARCH ------------------------------- #
def search():
    website = website_entry.get()
    if website:
        try:
            with open(json_file, "r") as file:
                all_data = json.load(file)
                wanted_data = all_data[website]
        except KeyError or FileNotFoundError:
            messagebox.showerror(title="Error", message="No details about this website.")
        else:
            wanted_email = wanted_data["email"]
            wanted_password = wanted_data["password"]
            messagebox.showinfo(title=website, message=f"Email: {wanted_email}\nPassword: {wanted_password}")
    else:
        messagebox.showerror(title="Error", message="No details about this website.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Project Manager")
window.configure(padx=50, pady=50)

lock = PhotoImage(file="logo.png", height=200, width=200)

canvas = Canvas(width=200, height=200, highlightthickness=0)
canvas.create_image(135, 95, image=lock)
canvas.grid(column=1, row=0, sticky="EW")

website_text = Label(text="Website:")
website_text.grid(row=1, column=0)

email_text = Label(text="Email/Username:")
email_text.grid(row=2, column=0)

password_text = Label(text="Password:")
password_text.grid(row=3, column=0)

website_entry = Entry()
website_entry.grid(row=1, column=1, sticky="EW")
website_entry.focus()

email_entry = Entry()
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
email_entry.insert(0, most_used_email)

password_entry = Entry()
password_entry.grid(row=3, column=1, sticky="EW")

generator = Button(text="Generate Password", width=15, command=generate_password)
generator.grid(row=3, column=2)

add = Button(text="Add", width=35, command=save)
add.grid(row=4, column=1, columnspan=2, sticky="EW")

search_button = Button(text="Search", width=15, command=search)
search_button.grid(row=1, column=2)

window.mainloop()
