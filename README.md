# Smart Attendance System Using Face Recognition

## Overview
The Smart Attendance System Using Face Recognition is an innovative solution that leverages artificial intelligence and computer vision to automate the process of attendance tracking. This system uses face recognition technology to identify and verify individuals, making attendance recording accurate, efficient, and secure.

## Features
- **Student Enrollment**: Capture student face images along with details such as Name, Enrollment ID, and Class. Face encodings are stored for later recognition.
- **Face Recognition for Attendance**: Recognize students in real-time using a webcam. The system marks attendance in a subject-specific Excel file and displays a popup notification.
- **Subject-wise Attendance**: Choose a subject (e.g., Data Visualization, Machine Learning, App Development) from the GUI. Attendance is recorded in a file named like `attendance_Machine Learning_YYYY-MM-DD.xlsx`.
- **Dashboard GUI**: A multi-page Tkinter-based dashboard that includes:
  - Welcome/Home Page
  - Add Student Page
  - Mark Attendance Page (with subject selection)
  - View Attendance Page
  - View Students Page (with deletion capability)
- **Optional MongoDB Integration (Future Enhancement)**: Replace file-based storage with MongoDB using PyMongo for scalable data management.

## Technologies & Libraries
- **Python 3.x**: The project is developed in Python.
- **OpenCV (cv2)**: For capturing video from the webcam and processing image frames.
- **face_recognition**: For detecting faces and computing face encodings.
- **NumPy**: For numerical operations and handling image data as arrays.
- **Pandas**: For reading/writing Excel files to store attendance records.
- **Pickle**: For serializing student data (e.g., face encodings) into files.
- **Tkinter**: For building the GUI dashboard.
- **Threading**: To run resource-intensive operations in the background while keeping the GUI responsive.
- **Optional – MongoDB & PyMongo**: (For future expansion) To store student records and attendance data in a NoSQL database.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.x
- OpenCV
- dlib
- face_recognition
- NumPy
- pandas
- streamlit
- openpyxl
- Flask

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ankitsharma38/Smart-Attendance-System-Using-Face_Recognition.git
   cd Smart-Attendance-System-Using-Face_Recognition
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   env\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the face recognition script to start the attendance system:
   ```bash
   python attendance_system.py
   ```

2. Run the dashboard script to view the attendance dashboard:
   ```bash
   python Dashboard.py
   ```

3. Follow the on-screen instructions to register new users, recognize faces for attendance, or view attendance data on the dashboard.

## Project Structure
- `attendance_system.py`: Main script to run the attendance system.
- `Dashboard.py`: Script to run the face recognition dashboard built with Tkinter.
- `face_recognition.py`: Module for face recognition functionality.
- `database.py`: Module for database operations.
- `ui.py`: Module for the user interface.
- `requirements.txt`: List of required Python packages.

## How It Works
1. **Face Detection**: The system detects faces in the video feed using OpenCV and dlib.
2. **Face Recognition**: Recognizes and matches detected faces with the registered faces in the database.
3. **Attendance Logging**: Logs the attendance of recognized individuals in the database.
4. **Dashboard**: Displays attendance data in a user-friendly interface using Tkinter.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
Created by [Ankit Sharma](https://github.com/ankitsharma38) - feel free to contact me!

## Acknowledgements
- [OpenCV](https://opencv.org/)
- [dlib](http://dlib.net/)
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Streamlit](https://streamlit.io/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
