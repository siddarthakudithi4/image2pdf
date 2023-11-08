import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import Image
from tkinter import filedialog

# Global variable to track the sign-in status
signed_in = False

# Function to insert data into MySQL database
def insert_data_into_database(username):
    # You can implement data insertion here
    # Replace this with your actual code
    pass

# Function to sign up a new user
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

# Function to sign in
def sign_in():
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
        global signed_in
        signed_in = True
        messagebox.showinfo("Success", "Sign-in successful!")
    else:
        messagebox.showerror("Error", "Invalid username or password!")

    conn.close()

# Function to enable image-to-PDF conversion after successful sign-in
def enable_image_to_pdf_conversion():
    global signed_in
    signed_in = True
    messagebox.showinfo("Success", "Sign-in successful!")
    # Enable image-to-PDF conversion button or any other functionality you want to enable
    convert_to_pdf_button.config(state="normal")

# Function to convert images to PDF
def convert_images_to_pdf():
    if not signed_in:
        messagebox.showerror("Error", "You must sign in to convert images to PDF.")
        return

    images = filedialog.askopenfilenames(title="Select Images", filetypes=(("Image files", "*.jpg;*.jpeg;*.png"),("All files", "*.*")), initialdir="C:/")

    if images:
        pdf_name = filedialog.asksaveasfilename(title="Save PDF As", defaultextension=".pdf", initialdir="C:/", filetypes=(("PDF files", "*.pdf"),("All files", "*.*")))
        
        if pdf_name:
            try:
                # Create a new PDF file
                pdf = Image.open(images[0])
                pdf.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
                messagebox.showinfo("Success", "Images have been successfully converted to PDF.")
            except Exception as e:
                messagebox.showerror("Error", "Failed to convert images to PDF.\nError: " + str(e))

# Create the main application window
root = tk.Tk()
root.title("Sign-Up/Sign-In and Image-to-PDF Conversion")

# Create and place labels and entry widgets for username and password
username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")  # Use show="*" to hide the password
password_entry.pack()

# Create and place the sign-up button
sign_up_button = tk.Button(root, text="Sign-Up", command=sign_up)
sign_up_button.pack()

# Create and place the sign-in button
sign_in_button = tk.Button(root, text="Sign-In", command=lambda: enable_image_to_pdf_conversion() if sign_in() else None)
sign_in_button.pack()

# Create and place the image-to-PDF conversion button (initially disabled)
convert_to_pdf_button = tk.Button(root, text="Convert Images to PDF", command=convert_images_to_pdf, state="disabled")
convert_to_pdf_button.pack()

# Start the tkinter main loop
root.mainloop()
