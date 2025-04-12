import cv2
import face_recognition
import numpy as np
import pickle
import os
from datetime import datetime
import pandas as pd
import threading
import tkinter as tk
from utils import load_student_data

# Global subject variable.
SUBJECT = "Data Visualization"

def show_popup(message="Attendance Marked Successfully", duration=5000):
    """
    Display a popup window with the given message for the specified duration (in milliseconds).
    """
    def popup():
        root = tk.Tk()
        root.title("Notification")
        window_width = 300
        window_height = 100
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        label = tk.Label(root, text=message, font=("Arial", 12))
        label.pack(expand=True, fill="both")
        root.after(duration, root.destroy)
        root.mainloop()
    threading.Thread(target=popup, daemon=True).start()

def mark_attendance(student_name, enrollment_id, student_class, subject, attendance_dir='../data'):
    """
    Mark the attendance of a student in an Excel file.
    The file is named with the current date and subject (e.g. attendance_Machine Learning_YYYY-MM-DD.xlsx)
    and has columns: Enrollment, Name, Class, Subject, Time Stamp.
    
    Args:
        student_name (str): Name of the student.
        enrollment_id (str): Unique enrollment ID.
        student_class (str): The class of the student.
        subject (str): Subject for which attendance is being marked.
        attendance_dir (str): Directory where attendance files are stored.
    """
    if not os.path.exists(attendance_dir):
        os.makedirs(attendance_dir)
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_path = os.path.join(attendance_dir, f"attendance_{subject}_{current_date}.xlsx")
    timestamp = datetime.now().strftime('%I:%M:%S %p')
    new_row = {
        'Enrollment': enrollment_id,
        'Name': student_name,
        'Class': student_class,
        'Subject': subject,
        'Time Stamp': timestamp
    }
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            print("Error reading the existing attendance file:", e)
            df = pd.DataFrame(columns=['Enrollment', 'Name', 'Class', 'Subject', 'Time Stamp'])
    else:
        df = pd.DataFrame(columns=['Enrollment', 'Name', 'Class', 'Subject', 'Time Stamp'])
    if enrollment_id in df['Enrollment'].values:
        print(f"Attendance already marked for {student_name}.")
    else:
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(file_path, index=False)
        print(f"Attendance marked for {student_name} at {timestamp} for subject: {subject}")
        show_popup()  # Display popup message

def recognize_students(video_source=0, subject="Data Visualization"):
    """
    Recognize students from the video feed and mark their attendance.
    If a face is not recognized, a red rectangle is drawn and "Unknown" is displayed.
    
    Args:
        video_source (int or str): Video source (default is 0 for webcam).
        subject (str): The subject name to use when marking attendance.
    """
    student_data = load_student_data()
    known_encodings = []
    student_info = []
    
    # Prepare known encodings and student info (including class)
    for data in student_data:
        known_encodings.extend(data['encodings'])
        student_info.extend([
            {
                'name': data['name'],
                'enrollment_id': data['enrollment_id'],
                'class': data.get('class', 'N/A')
            }
        ] * len(data['encodings']))
    
    video_capture = cv2.VideoCapture(video_source)
    recognized_students = set()
    print("Starting video stream for subject:", subject, ". Press 'q' to quit.")
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame from webcam. Exiting...")
            break

        # Resize frame for faster processing and convert from BGR to RGB.
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        rgb_small_frame = np.ascontiguousarray(rgb_small_frame)

        # Detect faces and compute encodings.
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                student = student_info[best_match_index]
                name = student['name']
                enrollment_id = student['enrollment_id']
                student_class = student.get('class', 'N/A')
                if enrollment_id not in recognized_students:
                    mark_attendance(name, enrollment_id, student_class, subject)
                    recognized_students.add(enrollment_id)
                rect_color = (0, 255, 0)  # Green for recognized
            else:
                name = "Unknown"
                rect_color = (0, 0, 255)  # Red for unknown

            # Scale back up face location coordinates.
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw rectangle and label on the frame.
            cv2.rectangle(frame, (left, top), (right, bottom), rect_color, 2)
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, rect_color, 2)

        cv2.imshow('Attendance Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    recognize_students()
