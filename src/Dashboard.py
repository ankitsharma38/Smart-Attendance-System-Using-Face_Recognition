import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import pandas as pd
import os

import enroll      # Update enroll.enroll_student() to accept a third parameter for class
import recognize   # Contains recognize_students() – your actual recognition code.
from utils import load_student_data  # Loads all student data from the students folder

# View Attendance Code (remains unchanged)
def view_attendance_file():
    file_path = filedialog.askopenfilename(
        title="Select Attendance File",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    if not file_path:
        return None, None
    try:
        df = pd.read_excel(file_path)
        return df, file_path
    except Exception as e:
        messagebox.showerror("Error", f"Could not read the file:\n{e}")
        return None, None

# Dashboard Design
class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Attendance System Dashboard")
        self.geometry("900x600")
        self.configure(bg="#ECF0F1")
        
        # Configure grid layout: column 0 for sidebar, column 1 for content.
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar frame (fixed width)
        self.sidebar_frame = tk.Frame(self, bg="#2C3E50", width=200)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")
        self.sidebar_frame.grid_propagate(False)
        
        # Main content frame
        self.content_frame = tk.Frame(self, bg="#ECF0F1")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        
        # Create sidebar buttons
        self.create_sidebar_buttons()
        
        # Start with the welcome (home) page.
        self.current_page = None
        self.show_welcome_page()

    def create_sidebar_buttons(self):
        btn_config = {
            "font": ("Helvetica", 12),
            "fg": "#ECF0F1",
            "bg": "#34495E",
            "activebackground": "#1ABC9C",
            "bd": 0,
            "relief": tk.FLAT,
            "width": 20,
            "pady": 10
        }
        
        # Sidebar Buttons: Home, Add Student, Mark Attendance, View Attendance, View Students, Exit
        tk.Button(self.sidebar_frame, text="Home",
                  command=self.show_welcome_page, **btn_config).pack(pady=10)
        tk.Button(self.sidebar_frame, text="Add Student",
                  command=self.show_add_student_page, **btn_config).pack(pady=10)
        tk.Button(self.sidebar_frame, text="Mark Attendance",
                  command=self.show_mark_attendance_page, **btn_config).pack(pady=10)
        tk.Button(self.sidebar_frame, text="View Attendance",
                  command=self.show_view_attendance_page, **btn_config).pack(pady=10)
        tk.Button(self.sidebar_frame, text="View Students",
                  command=self.show_view_students_page, **btn_config).pack(pady=10)
        tk.Button(self.sidebar_frame, text="Exit",
                  command=self.quit, **btn_config).pack(pady=10)
    
    def clear_content(self):
        if self.current_page is not None:
            self.current_page.destroy()
            self.current_page = None

    # Centered Welcome Page
    def show_welcome_page(self):
        self.clear_content()
        # Create a frame to center content using place()
        page = tk.Frame(self.content_frame, bg="#ECF0F1")
        page.place(relx=0.5, rely=0.5, anchor="center")
        
        welcome_label = tk.Label(page, text="Welcome to the Smart Attendance System Dashboard",
                                 font=("Helvetica", 24, "bold"), bg="#ECF0F1", fg="#2C3E50")
        welcome_label.pack(pady=(10, 5))
        
        subtitle_label = tk.Label(page, text="Simplify Attendance Management with Face Recognition",
                                  font=("Helvetica", 16), bg="#ECF0F1", fg="#34495E")
        subtitle_label.pack(pady=(0, 20))
        
        separator = tk.Frame(page, bg="#BDC3C7", height=2, width=600)
        separator.pack(pady=10)
        
        tagline = tk.Label(page, text="Empowering Institutions with Cutting-Edge Technology",
                           font=("Helvetica", 14, "italic"), bg="#ECF0F1", fg="#7F8C8D")
        tagline.pack(pady=(10, 20))
        
        get_started_btn = tk.Button(page, text="Get Started", font=("Helvetica", 16, "bold"),
                                    bg="#1ABC9C", fg="white", padx=20, pady=10, bd=0,
                                    activebackground="#16A085", cursor="hand2",
                                    command=self.show_mark_attendance_page)
        get_started_btn.pack(pady=20)
        
        self.current_page = page

    # Updated Add Student Page with extra "Class" field
    def show_add_student_page(self):
        self.clear_content()
        page = tk.Frame(self.content_frame, bg="#ECF0F1", padx=20, pady=20)
        page.pack(expand=True, fill="both")
        
        title = tk.Label(page, text="Add Student", font=("Helvetica", 18, "bold"),
                         bg="#ECF0F1", fg="#34495E")
        title.pack(pady=(0,20))
        
        form_frame = tk.Frame(page, bg="#ECF0F1")
        form_frame.pack(pady=10)
        
        # Student Name
        tk.Label(form_frame, text="Student Name:", font=("Helvetica", 12), bg="#ECF0F1")\
          .grid(row=0, column=0, sticky="e", padx=10, pady=5)
        name_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Enrollment ID
        tk.Label(form_frame, text="Enrollment ID:", font=("Helvetica", 12), bg="#ECF0F1")\
          .grid(row=1, column=0, sticky="e", padx=10, pady=5)
        enroll_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
        enroll_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Class Field
        tk.Label(form_frame, text="Class:", font=("Helvetica", 12), bg="#ECF0F1")\
          .grid(row=2, column=0, sticky="e", padx=10, pady=5)
        class_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
        class_entry.grid(row=2, column=1, padx=10, pady=5)
        
        success_label = tk.Label(page, text="", font=("Helvetica", 12, "italic"),
                                 bg="#ECF0F1", fg="#27AE60")
        success_label.pack(pady=10)
        
        def run_enrollment():
            student_name = name_entry.get().strip()
            enrollment_id = enroll_entry.get().strip()
            student_class = class_entry.get().strip()
            if not student_name or not enrollment_id or not student_class:
                page.after(0, lambda: messagebox.showwarning("Input Error",
                                                              "Please enter name, enrollment ID, and class."))
                return
            try:
                # Call your actual enrollment function with the extra parameter.
                enroll.enroll_student(student_name, enrollment_id, student_class)
            except Exception as e:
                page.after(0, lambda: messagebox.showerror("Error", f"Enrollment failed: {e}"))
                return
            page.after(0, on_enrollment_complete)
        
        def on_enrollment_complete():
            success_label.config(text="Student Added Successfully")
            name_entry.delete(0, tk.END)
            enroll_entry.delete(0, tk.END)
            class_entry.delete(0, tk.END)
            page.after(3000, lambda: success_label.config(text=""))
        
        def start_enrollment():
            threading.Thread(target=run_enrollment, daemon=True).start()
        
        tk.Button(page, text="Capture & Enroll", font=("Helvetica", 12, "bold"),
                  command=start_enrollment, bg="#1ABC9C", fg="white", padx=20, pady=10)\
                  .pack(pady=20)
        
        self.current_page = page

    def show_mark_attendance_page(self):
        self.clear_content()
        page = tk.Frame(self.content_frame, bg="#ECF0F1", padx=20, pady=20)
        page.pack(expand=True, fill="both")
        title = tk.Label(page, text="Mark Attendance", font=("Helvetica", 18, "bold"),
                         bg="#ECF0F1", fg="#34495E")
        title.pack(pady=(0,20))
        
        def start_recognition():
            threading.Thread(target=recognize.recognize_students, daemon=True).start()
        
        tk.Button(page, text="Start Recognition", font=("Helvetica", 12, "bold"),
                  command=start_recognition, bg="#1ABC9C", fg="white", padx=20, pady=10)\
                  .pack(pady=20)
        
        self.current_page = page

    def show_view_attendance_page(self):
        self.clear_content()
        page = tk.Frame(self.content_frame, bg="#ECF0F1", padx=20, pady=20)
        page.pack(expand=True, fill="both")
        title = tk.Label(page, text="View Attendance", font=("Helvetica", 18, "bold"),
                         bg="#ECF0F1", fg="#34495E")
        title.pack(pady=(0,20))
        
        def load_and_display():
            df, file_path = view_attendance_file()
            if df is None:
                return
            
            # Define the expected column order.
            expected_columns = ["Enrollment", "Name", "Class", "Time Stamp"]
            # Add missing columns if necessary.
            for col in expected_columns:
                if col not in df.columns:
                    df[col] = "N/A"
            # Reorder the DataFrame columns.
            df = df[expected_columns]
            
            for widget in page.winfo_children():
                if isinstance(widget, ttk.Treeview) or isinstance(widget, tk.Scrollbar):
                    widget.destroy()
            tree = ttk.Treeview(page)
            tree.pack(expand=True, fill='both')
            tree["columns"] = expected_columns
            tree["show"] = "headings"
            for col in expected_columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            for _, row in df.iterrows():
                tree.insert("", "end", values=list(row))
            scrollbar = ttk.Scrollbar(page, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
        
        tk.Button(page, text="Load Attendance File", font=("Helvetica", 12, "bold"),
                  command=load_and_display, bg="#1ABC9C", fg="white", padx=20, pady=10)\
                  .pack(pady=10)
        
        self.current_page = page

    def show_view_students_page(self):
        self.clear_content()
        page = tk.Frame(self.content_frame, bg="#ECF0F1", padx=20, pady=20)
        page.pack(expand=True, fill="both")
        title = tk.Label(page, text="View Students", font=("Helvetica", 18, "bold"),
                         bg="#ECF0F1", fg="#34495E")
        title.pack(pady=(0,20))
        
        tree = ttk.Treeview(page)
        tree.pack(expand=True, fill='both')
        columns = ("Enrollment", "Name", "Class", "Encodings")
        tree["columns"] = columns
        tree["show"] = "headings"
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        student_data = load_student_data()
        if not student_data:
            messagebox.showinfo("No Data", "No student data found.")
        else:
            for student in student_data:
                enrollment_id = student.get("enrollment_id", "N/A")
                name = student.get("name", "N/A")
                student_class = student.get("class", "N/A")
                encodings = len(student.get("encodings", []))
                tree.insert("", "end", values=(enrollment_id, name, student_class, encodings))
        
        def delete_selected_student():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a student to delete.")
                return
            values = tree.item(selected_item, "values")
            enrollment_id, name, student_class, _ = values
            if not messagebox.askyesno("Confirm Deletion", f"Delete student {name} ({enrollment_id})?"):
                return
            file_name = f"{enrollment_id}_{name.replace(' ', '_')}.pkl"
            student_dir = os.path.join("..", "data", "students")
            file_path = os.path.join(student_dir, file_name)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    messagebox.showinfo("Deleted", f"Student {name} deleted successfully.")
                    tree.delete(selected_item)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete student: {e}")
            else:
                messagebox.showwarning("Not Found", "Student file not found. It may have already been deleted.")
        
        tk.Button(page, text="Delete Selected Student", font=("Helvetica", 12, "bold"),
                  command=delete_selected_student, bg="#E74C3C", fg="white", padx=20, pady=10)\
                  .pack(pady=10)
        
        self.current_page = page

if __name__ == '__main__':
    app = Dashboard()
    app.mainloop()
