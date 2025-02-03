import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

def view_attendance():
    # Ask the user to select an attendance Excel file
    file_path = filedialog.askopenfilename(
        title="Select Attendance File",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    if not file_path:
        return  # User cancelled

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Could not read the file:\n{e}")
        return

    # Create a new window to display the data
    view_window = tk.Toplevel()
    view_window.title(f"Attendance - {file_path}")
    view_window.geometry("600x400")

    # Create a Treeview widget
    tree = ttk.Treeview(view_window)
    tree.pack(expand=True, fill='both')

    # Set up the columns in the Treeview using the DataFrame columns
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"  # Hide the first empty column

    for col in df.columns:
        tree.heading(col, text=col)
        # Optionally, adjust the column width
        tree.column(col, width=150)

    # Insert rows into the Treeview
    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    # Add a scrollbar for vertical scrolling
    scrollbar = ttk.Scrollbar(view_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
