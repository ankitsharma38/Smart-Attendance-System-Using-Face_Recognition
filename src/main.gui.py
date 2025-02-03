import tkinter as tk
from tkinter import simpledialog, messagebox
from view_attendance import view_attendance
import threading

# Import your existing modules
import enroll      # Contains enroll_student(...)
import recognize   # Contains recognize_students

# Import view_attendance (from the code above)
from tkinter import filedialog
import pandas as pd
from tkinter import ttk

def enroll_student_gui():
    student_name = simpledialog.askstring("Enroll Student", "Enter student name:")
    if not student_name:
        return
    enrollment_id = simpledialog.askstring("Enroll Student", "Enter enrollment ID:")
    if not enrollment_id:
        return
    messagebox.showinfo("Enrollment", "Enrollment process started. Please follow the on-screen instructions.")
    threading.Thread(target=enroll.enroll_student, args=(student_name, enrollment_id), daemon=True).start()

def recognize_students_gui():
    messagebox.showinfo("Recognition", "Starting attendance recognition. Press 'q' in the video window to quit.")
    threading.Thread(target=recognize.recognize_students, daemon=True).start()

def view_attendance_gui():
    # Call the view_attendance function defined above.
    view_attendance()  # This function opens a file dialog and displays the file in a new window.

def create_main_window():
    root = tk.Tk()
    root.title("Smart Attendance System")
    root.geometry("300x250")

    enroll_button = tk.Button(root, text="Enroll Student", command=enroll_student_gui, width=25, height=2)
    enroll_button.pack(pady=5)

    recognize_button = tk.Button(root, text="Recognize Attendance", command=recognize_students_gui, width=25, height=2)
    recognize_button.pack(pady=5)

    view_button = tk.Button(root, text="View Attendance", command=view_attendance_gui, width=25, height=2)
    view_button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", command=root.destroy, width=25, height=2)
    exit_button.pack(pady=5)

    root.mainloop()

if __name__ == '__main__':
    create_main_window()
