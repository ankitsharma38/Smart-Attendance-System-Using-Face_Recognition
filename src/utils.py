import os
import pickle

def load_student_data(directory='../data/students'):
    """
    Load all student data from the specified directory.

    Args:
        directory (str): Path to the directory containing student .pkl files.

    Returns:
        list: A list of dictionaries with student information and encodings.
    """
    student_data = []
    if not os.path.exists(directory):
        os.makedirs(directory)
    for filename in os.listdir(directory):
        if filename.endswith('.pkl'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'rb') as file:
                data = pickle.load(file)
                student_data.append(data)
    return student_data
