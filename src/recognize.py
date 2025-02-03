import cv2
import face_recognition
import numpy as np
from datetime import datetime
import os
import pandas as pd
import threading
import tkinter as tk
from utils import load_student_data

def show_popup(message="Attendance Marked Successfully", duration=2000):
    """
    Display a popup window with the given message for the specified duration (in milliseconds).
    """
    def popup():
        root = tk.Tk()
        root.title("Notification")
        # Set the window size and position it at the center of the screen
        window_width = 300
        window_height = 100
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create and pack the label
        label = tk.Label(root, text=message, font=("Arial", 12))
        label.pack(expand=True, fill="both")

        # Schedule the popup window to close after the specified duration
        root.after(duration, root.destroy)
        root.mainloop()

    # Run the popup in a separate thread so as not to block the main thread
    threading.Thread(target=popup, daemon=True).start()

def mark_attendance(student_name, enrollment_id, attendance_dir='../data'):
    """
    Mark the attendance of a student in an Excel file.
    The file is named with the current date (attendance_YYYY-MM-DD.xlsx) and has columns:
    Enrollment, Name, Time Stamp (12-hr format).

    Args:
        student_name (str): Name of the student.
        enrollment_id (str): Unique enrollment ID.
        attendance_dir (str): Directory where attendance files are stored.
    """
    # Create attendance directory if it doesn't exist
    if not os.path.exists(attendance_dir):
        os.makedirs(attendance_dir)

    # Construct file name with current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_path = os.path.join(attendance_dir, f"attendance_{current_date}.xlsx")

    # Time stamp in 12-hour format with AM/PM
    timestamp = datetime.now().strftime('%I:%M:%S %p')
    new_row = {'Enrollment': enrollment_id, 'Name': student_name, 'Time Stamp': timestamp}

    # If the file exists, load and append; otherwise, create a new DataFrame
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            print("Error reading the existing attendance file:", e)
            df = pd.DataFrame(columns=['Enrollment', 'Name', 'Time Stamp'])
    else:
        df = pd.DataFrame(columns=['Enrollment', 'Name', 'Time Stamp'])

    # Optional: Prevent marking attendance twice by checking if enrollment ID is already present.
    if enrollment_id in df['Enrollment'].values:
        print(f"Attendance already marked for {student_name}.")
    else:
        # Append new row and save to Excel
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(file_path, index=False)
        print(f"Attendance marked for {student_name} at {timestamp}")
        show_popup()  # Display popup message

def recognize_students(video_source=0):
    """
    Recognize students from the video feed and mark their attendance in an Excel file.

    Args:
        video_source (int or str): Video source (default is 0 for webcam).
    """
    student_data = load_student_data()
    known_encodings = []
    student_info = []

    # Prepare the known face encodings and corresponding student info
    for data in student_data:
        known_encodings.extend(data['encodings'])
        student_info.extend([{'name': data['name'], 'enrollment_id': data['enrollment_id']}] * len(data['encodings']))

    video_capture = cv2.VideoCapture(video_source)
    recognized_students = set()

    print("Starting video stream. Press 'q' to quit.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame from webcam. Exiting...")
            break

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        rgb_small_frame = np.ascontiguousarray(rgb_small_frame)

        # Detect faces and compute encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                student = student_info[best_match_index]
                name = student['name']
                enrollment_id = student['enrollment_id']

                if enrollment_id not in recognized_students:
                    mark_attendance(name, enrollment_id)
                    recognized_students.add(enrollment_id)

                # Display the name on the frame
                for (top, right, bottom, left) in face_locations:
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Attendance Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    recognize_students()
