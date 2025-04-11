import sqlite3
import tkinter as tk
from tkinter import messagebox
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

def calculate_real_size(microscope_size, magnification):
    if magnification <= 0:
        raise ValueError("Magnification must be a positive number.")
    return microscope_size / magnification

# Example usage:
microscope_size = float(input("Enter the size under the microscope (μm): "))
magnification = float(input("Enter the magnification: "))
real_size = calculate_real_size(microscope_size, magnification)
print(f"Real-life size: {real_size} μm")



def initialize_database():
    conn = sqlite3.connect("specimens.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS specimens (
            username TEXT,
            microscope_size REAL,
            magnification REAL,
            actual_size REAL
        )
    """)
    conn.commit()
    conn.close()

def store_specimen(username, microscope_size, magnification, actual_size):
    conn = sqlite3.connect("specimens.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO specimens (username, microscope_size, magnification, actual_size)
        VALUES (?, ?, ?, ?)
    """, (username, microscope_size, magnification, actual_size))
    conn.commit()
    conn.close()

initialize_database()

# Example usage:
username = input("Enter your username: ")
microscope_size = float(input("Enter the size under the microscope (μm): "))
magnification = float(input("Enter the magnification: "))
actual_size = calculate_real_size(microscope_size, magnification)
store_specimen(username, microscope_size, magnification, actual_size)
print(f"Real-life size: {actual_size} μm (stored in database)")



def calculate_and_store():
    try:
        username = username_entry.get()
        microscope_size = float(microscope_size_entry.get())
        magnification = float(magnification_entry.get())
        actual_size = microscope_size / magnification
        actual_size_label.config(text=f"Actual size: {actual_size} μm")

        # Store in database
        conn = sqlite3.connect("specimens.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO specimens (username, microscope_size, magnification, actual_size)
            VALUES (?, ?, ?, ?)
        """, (username, microscope_size, magnification, actual_size))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Data stored successfully!")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter numbers.")

# Initialize GUI
root = tk.Tk()
root.title("Microscope Size Calculator")

tk.Label(root, text="Username:").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Microscope size (μm):").pack()
microscope_size_entry = tk.Entry(root)
microscope_size_entry.pack()

tk.Label(root, text="Magnification:").pack()
magnification_entry = tk.Entry(root)
magnification_entry.pack()

calculate_button = tk.Button(root, text="Calculate and Store", command=calculate_and_store)
calculate_button.pack()

actual_size_label = tk.Label(root, text="Actual size: ")
actual_size_label.pack()

root.mainloop()



app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("specimens.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        microscope_size = float(request.form["microscope_size"])
        magnification = float(request.form["magnification"])
        actual_size = microscope_size / magnification

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO specimens (username, microscope_size, magnification, actual_size)
            VALUES (?, ?, ?, ?)
        """, (username, microscope_size, magnification, actual_size))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    conn = get_db_connection()
    specimens = conn.execute("SELECT * FROM specimens").fetchall()
    conn.close()
    return render_template("index.html", specimens=specimens)

if __name__ == "__main__":
    app.run(debug=True)