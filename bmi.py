import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")

        # Create database and table
        self.conn = sqlite3.connect('bmi_data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                weight REAL,
                height REAL,
                bmi REAL,
                date TEXT
            )
        ''')
        self.conn.commit()

        # GUI components
        self.user_label = ttk.Label(root, text="User Name:")
        self.user_entry = ttk.Entry(root)
        self.weight_label = ttk.Label(root, text="Weight (kg):")
        self.weight_entry = ttk.Entry(root)
        self.height_label = ttk.Label(root, text="Height (m):")
        self.height_entry = ttk.Entry(root)

        self.calculate_button = ttk.Button(root, text="Calculate BMI", command=self.calculate_bmi)
        self.save_button = ttk.Button(root, text="Save Data", command=self.save_data)

        # Grid layout
        self.user_label.grid(row=0, column=0, padx=10, pady=10)
        self.user_entry.grid(row=0, column=1, padx=10, pady=10)
        self.weight_label.grid(row=1, column=0, padx=10, pady=10)
        self.weight_entry.grid(row=1, column=1, padx=10, pady=10)
        self.height_label.grid(row=2, column=0, padx=10, pady=10)
        self.height_entry.grid(row=2, column=1, padx=10, pady=10)
        self.calculate_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi = round(weight / (height ** 2), 2)
            result_text = f"BMI: {bmi}"
            tk.messagebox.showinfo("BMI Result", result_text)
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid numeric values for weight and height.")

    def save_data(self):
        try:
            user_name = self.user_entry.get()
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi = round(weight / (height ** 2), 2)
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save data to the database
            self.cursor.execute('''
                INSERT INTO bmi_records (user_name, weight, height, bmi, date)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_name, weight, height, bmi, date))
            self.conn.commit()

            tk.messagebox.showinfo("Success", "Data saved successfully.")
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid numeric values for weight and height.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()