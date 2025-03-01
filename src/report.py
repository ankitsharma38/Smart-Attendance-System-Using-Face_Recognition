import pandas as pd
import os
from datetime import datetime

def generate_monthly_report(subject, month_year, attendance_dir='../data'):
    """
    Generate a monthly attendance report for a given subject and month.

    Args:
        subject (str): The subject name (e.g., "Data Visualization").
        month_year (str): Month and year in format "YYYY-MM" (e.g., "2025-02").
        attendance_dir (str): Directory where attendance files are stored.

    Returns:
        pd.DataFrame or None: A DataFrame containing aggregated attendance data,
                              including total attendance and percentage,
                              or None if no matching data is found.
    """
    all_data = []
    session_dates = set()

    # Iterate over files in the attendance directory
    for file in os.listdir(attendance_dir):
        # Expected file format: attendance_{subject}_{YYYY-MM-DD}.xlsx
        if file.startswith(f"attendance_{subject}_") and file.endswith(".xlsx"):
            try:
                # Extract the date part from the filename
                date_str = file.split('_')[-1].replace('.xlsx', '')
                # Check if the date matches the requested month (YYYY-MM)
                if date_str.startswith(month_year):
                    session_dates.add(date_str)
                    file_path = os.path.join(attendance_dir, file)
                    df = pd.read_excel(file_path)
                    
                    # Normalize key columns to ensure consistency:
                    if 'Enrollment' in df.columns:
                        df['Enrollment'] = df['Enrollment'].astype(str).str.strip().str.lower()
                    if 'Name' in df.columns:
                        df['Name'] = df['Name'].astype(str).str.strip().str.title()
                    if 'Class' in df.columns:
                        df['Class'] = df['Class'].astype(str).str.strip()

                    df['Date'] = date_str  # add Date column for reference
                    all_data.append(df)
            except Exception as e:
                print(f"Error processing file {file}: {e}")

    if not all_data:
        return None

    # Total unique sessions in the month (based on the dates extracted from filenames)
    total_sessions = len(session_dates)
    if total_sessions == 0:
        return None

    monthly_df = pd.concat(all_data, ignore_index=True)

    # Remove duplicate attendance entries for a student for the same session
    unique_attendance = monthly_df.drop_duplicates(subset=['Enrollment', 'Date'])

    # Group by Enrollment, Name, and Class, counting unique sessions attended
    report_df = unique_attendance.groupby(['Enrollment', 'Name', 'Class'], as_index=False)['Date'].nunique()
    report_df.rename(columns={'Date': 'Total Attendance'}, inplace=True)

    # Calculate attendance percentage: (sessions attended / total sessions) * 100
    report_df['Attendance Percentage'] = (report_df['Total Attendance'] / total_sessions) * 100
    report_df['Attendance Percentage'] = report_df['Attendance Percentage'].round(2)

    return report_df

def save_report(report_df, subject, month_year, attendance_dir='../data'):
    """
    Save the generated report to an Excel file.

    Args:
        report_df (pd.DataFrame): The DataFrame containing the report.
        subject (str): The subject name.
        month_year (str): Month and year in format "YYYY-MM".
        attendance_dir (str): Directory where attendance files are stored.

    Returns:
        str: The path to the saved report.
    """
    report_filename = f"monthly_report_{subject}_{month_year}.xlsx"
    report_file = os.path.join(attendance_dir, report_filename)
    report_df.to_excel(report_file, index=False)
    return report_file

# For standalone testing
if __name__ == '__main__':
    subject = input("Enter subject: ").strip()
    month_year = input("Enter month and year (YYYY-MM): ").strip()
    report_df = generate_monthly_report(subject, month_year)
    if report_df is not None:
        report_file = save_report(report_df, subject, month_year)
        print(f"Monthly report saved to: {report_file}")
    else:
        print("No attendance data found for the given month and subject.")
