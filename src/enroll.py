import cv2
import face_recognition
import numpy as np
import pickle
import os

def enroll_student(student_name, enrollment_id, student_class, save_dir='../data/students', num_images=5):
    """
    Enroll a student by capturing their face encodings.

    Args:
        student_name (str): Name of the student.
        enrollment_id (str): Unique enrollment ID.
        student_class (str): Class of the student.
        save_dir (str): Directory where the student data will be saved.
        num_images (int): Number of face samples to capture.
    """
    # Ensure the save directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    video_capture = cv2.VideoCapture(0)
    collected_encodings = []

    print(f"Enrolling student: {student_name} | Enrollment ID: {enrollment_id} | Class: {student_class}")
    print("Press 'c' to capture a frame when your face is clearly visible.")
    print("Press 'q' to quit early if needed.")

    count = 0
    while count < num_images:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame from webcam. Exiting...")
            break

        # Resize frame for faster processing (scale factor 0.25)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert BGR (OpenCV default) to RGB (face_recognition uses RGB)
        rgb_small_frame = small_frame[:, :, ::-1]
        rgb_small_frame = np.ascontiguousarray(rgb_small_frame)

        # Detect face locations in the frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        if len(face_locations) == 0:
            cv2.putText(frame, "No face detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Face detected! Press 'c' to capture", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            # Draw rectangles around detected faces (optional)
            for (top, right, bottom, left) in face_locations:
                # Scale back up since we resized earlier
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow('Enrollment', frame)
        key = cv2.waitKey(1) & 0xFF

        # Capture the face encoding when 'c' is pressed
        if key == ord('c'):
            if face_locations:
                # Use the first detected face (assumes one face per frame)
                face_encoding = face_recognition.face_encodings(rgb_small_frame, face_locations)[0]
                collected_encodings.append(face_encoding)
                count += 1
                print(f"Captured image {count}/{num_images}")
            else:
                print("No face detected! Please try again.")
        elif key == ord('q'):
            print("Enrollment aborted by user.")
            break

    video_capture.release()
    cv2.destroyAllWindows()

    # Save the data if any encodings were captured
    if collected_encodings:
        student_data = {
            "name": student_name,
            "enrollment_id": enrollment_id,
            "class": student_class,
            "encodings": collected_encodings
        }
        # The file name can be structured as enrollmentID_name.pkl
        file_name = f"{enrollment_id}_{student_name.replace(' ', '_')}.pkl"
        file_path = os.path.join(save_dir, file_name)
        with open(file_path, "wb") as f:
            pickle.dump(student_data, f)
        print(f"Student data saved to {file_path}")
    else:
        print("No face data captured. Enrollment unsuccessful.")

if __name__ == '__main__':
    # Collect student details from the user
    student_name = input("Enter student name: ").strip()
    enrollment_id = input("Enter enrollment ID: ").strip()
    student_class = input("Enter student class: ").strip()
    enroll_student(student_name, enrollment_id, student_class)
