import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image
import mysql.connector

# Global variable to track the sign-in status
signed_in = False

# Function to handle sign-in
def sign_in():
    global signed_in
    # Get username and password from entry widgets
    username = username_entry.get()
    password = password_entry.get()

    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysqlaccount",
        database="final"
    )
    cursor = conn.cursor()

    # Check if the entered credentials match a user in the database
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Success", "Sign-in successful!")
        signed_in = True
        enable_conversion_button()
    else:
        messagebox.showerror("Error", "Invalid username or password!")

    conn.close()

# Function to enable conversion button after successful sign-in
def enable_conversion_button():
    select_images_btn.config(state="normal")
    select_pdf_btn.config(state="normal")
    convert_btn.config(state="normal")

# Function to insert data into MySQL database
def insert_data():
    firstname = entry_firstname.get()
    lastname = entry_lastname.get()
    email = entry_email.get()
    age = int(entry_age.get())  # Convert age to an integer

    insert_query = "INSERT INTO user_2 (firstname, lastname, email, age) VALUES (%s, %s, %s, %s)"
    vals = (firstname, lastname, email, age)
    cursor.execute(insert_query, vals)
    connection.commit()
    messagebox.showinfo("Success", "Data has been successfully inserted into the database.")

# Function to convert images to PDF
def images_to_pdf(images, pdf_name):
    try:
        # Create a new PDF file
        pdf = Image.open(images[0])
        pdf.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
        messagebox.showinfo("Success", "Images have been successfully converted to PDF.")
    except Exception as e:
        messagebox.showerror("Error", "Failed to convert images to PDF.\nError: " + str(e))

# Function to select images
def select_images():
    images = filedialog.askopenfilenames(title="Select Images", filetypes=(("Image files", "*.jpg;*.jpeg;*.png"),("All files", "*.*")), initialdir="C:/")
    return images

# Function to select PDF name and path
def select_pdf():
    pdf = filedialog.asksaveasfilename(title="Save PDF As", defaultextension=".pdf", initialdir="C:/", filetypes=(("PDF files", "*.pdf"),("All files", "*.*")))
    return pdf

# Create MySQL database connection
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='mysqlaccount',
    port='3306',
    database='test_py'
)
cursor = connection.cursor()

# Create the tkinter GUI
root = tk.Tk()
root.title("Convert Images to PDF")

# Create and place labels and entry widgets for username and password for sign-in
frame_signin = tk.Frame(root)
frame_signin.pack()

username_label = tk.Label(frame_signin, text="Username:", font=('Verdana', 12))
username_label.grid(row=0, column=0)

password_label = tk.Label(frame_signin, text="Password:", font=('Verdana', 12))
password_label.grid(row=1, column=0)

username_entry = tk.Entry(frame_signin, font=('Verdana', 12))
username_entry.grid(row=0, column=1)

password_entry = tk.Entry(frame_signin, font=('Verdana', 12), show="*")  # Use show="*" to hide the password
password_entry.grid(row=1, column=1)

sign_in_button = tk.Button(frame_signin, text="Sign-In", font=('Verdana', 12), command=sign_in)
sign_in_button.grid(row=2, column=0, columnspan=2)

# Create widgets for data insertion
frame_insert = tk.Frame(root)
frame_insert.pack()

label_firstname = tk.Label(frame_insert, text="First Name:", font=('Verdana', 12))
entry_firstname = tk.Entry(frame_insert, font=('Verdana', 12))

label_lastname = tk.Label(frame_insert, text="Last Name:", font=('Verdana', 12))
entry_lastname = tk.Entry(frame_insert, font=('Verdana', 12))

label_email = tk.Label(frame_insert, text="Email:", font=('Verdana', 12))
entry_email = tk.Entry(frame_insert, font=('Verdana', 12))

label_age = tk.Label(frame_insert, text="Age:", font=('Verdana', 12))
entry_age = tk.Entry(frame_insert, font=('Verdana', 12))

button_insert = tk.Button(frame_insert, text="Insert Data", font=('Verdana', 12), command=insert_data)

label_firstname.grid(row=0, column=0)
entry_firstname.grid(row=0, column=1)

label_lastname.grid(row=1, column=0)
entry_lastname.grid(row=1, column=1)

label_email.grid(row=2, column=0)
entry_email.grid(row=2, column=1)

label_age.grid(row=3, column=0)
entry_age.grid(row=3, column=1)

button_insert.grid(row=4, column=0, columnspan=2)

# Create widgets for image to PDF conversion
frame_convert = tk.Frame(root)
frame_convert.pack()

select_images_btn = tk.Button(frame_convert, text="Select Images", state="disabled", command=select_images)
select_pdf_btn = tk.Button(frame_convert, text="Select PDF", state="disabled", command=select_pdf)
convert_btn = tk.Button(frame_convert, text="Convert Images to PDF", state="disabled", command=lambda: images_to_pdf(select_images(), select_pdf()))

select_images_btn.grid(row=0, column=0, padx=10, pady=10)
select_pdf_btn.grid(row=0, column=1, padx=10, pady=10)
convert_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Function to create the "users" table in the database
def create_table(cursor):
    cursor.execute("SHOW TABLES")
    temp = cursor.fetchall()
    tables = [item[0] for item in temp]

    if "users" not in tables:
        cursor.execute("""CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE,
            password VARCHAR(100)
        )""")
        connection.commit()

# Function to handle sign-up
def sign_up():
    # Get username and password from entry widgets
    username = username_entry.get()
    password = password_entry.get()

    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysqlaccount",
        database="final"
    )
    cursor = conn.cursor()

    # Insert user data into the database
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

    conn.close()

# Call the create_table function to ensure the "users" table exists
create_table(cursor)

# Start the tkinter main loop
root.mainloop()
