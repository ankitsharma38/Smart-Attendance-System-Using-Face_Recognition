# Smart Attendance System

The **Smart Attendance System** is a Python-based project that automates attendance management using face recognition technology. It captures student data via a webcam, stores face encodings along with student details, and marks attendance by recognizing faces in real-time. A user-friendly GUI dashboard built with Tkinter is provided for enrolling students, marking attendance subject-wise, and viewing records.

---

## Features

- **Student Enrollment:**  
  Capture student face images along with details such as Name, Enrollment ID, and Class. Face encodings are stored for later recognition.

- **Face Recognition for Attendance:**  
  Recognize students in real-time using a webcam. The system marks attendance in a subject-specific Excel file (or later in a database) and displays a popup notification.

- **Subject-wise Attendance:**  
  Choose a subject (e.g., Data Visualization, Machine Learning, App Development) from the GUI. Attendance is recorded in a file named like `attendance_Machine Learning_YYYY-MM-DD.xlsx`.

- **Dashboard GUI:**  
  A multi-page Tkinter-based dashboard that includes:
  - Welcome/Home Page
  - Add Student Page
  - Mark Attendance Page (with subject selection)
  - View Attendance Page
  - View Students Page (with deletion capability)

- **Optional MongoDB Integration (Future Enhancement):**  
  Replace file-based storage with MongoDB using PyMongo for scalable data management.

---

## Technologies & Libraries

- **Python 3.x**  
  The project is developed in Python.

- **OpenCV (cv2):**  
  For capturing video from the webcam and processing image frames.

- **face_recognition:**  
  For detecting faces and computing face encodings.

- **NumPy:**  
  For numerical operations and handling image data as arrays.

- **Pandas:**  
  For reading/writing Excel files to store attendance records.

- **Pickle:**  
  For serializing student data (e.g., face encodings) into files.

- **Tkinter:**  
  For building the GUI dashboard.

- **Threading:**  
  To run resource-intensive operations in the background while keeping the GUI responsive.

- **Optional – MongoDB & PyMongo:**  
  (For future expansion) To store student records and attendance data in a NoSQL database.

---

## Project Structure

## 🚀Installation And setup

### 📋 Prerequisites
```bash
Python >= 3.11 (for AI server)
```
# Setup environment variables
```bash
python -m venv env
env\Scripts\activate
```
