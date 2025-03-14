import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import random

# Define project tasks and their durations
tasks = [
    ("Project Discussion", "2025-01-08", "2025-01-14"),
    ("Project Structure Setup", "2025-01-15", "2025-01-21"),
    ("Face Recognition Implementation", "2025-01-22", "2025-02-04"),
    ("GUI Development (Tkinter)", "2025-02-05", "2025-02-18"),
    ("Attendance Management System", "2025-02-19", "2025-03-05"),
    ("Testing and Debugging", "2025-03-06", "2025-03-20"),
    ("Final Report Preparation", "2025-03-21", "2025-03-31"),
]

# Convert date strings to datetime objects
task_names, start_dates, end_dates = zip(*tasks)
start_dates = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in start_dates]
end_dates = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in end_dates]

# Calculate durations
durations = [(end - start).days for start, end in zip(start_dates, end_dates)]

# Define a color palette for tasks
colors = [
    "#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0", "#ffb3e6", "#ff6666"
]
random.shuffle(colors)  # Shuffle colors for variety

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 6))

# Plot each task as a horizontal bar
for i, (task, start, duration, color) in enumerate(zip(task_names, start_dates, durations, colors)):
    ax.barh(task, duration, left=start, color=color, edgecolor="black", alpha=0.8)

# Format x-axis with dates
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))  # Show every 2 weeks
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))  # Format dates as "Jan 08"
plt.xticks(rotation=45, fontsize=10)

# Add labels and title
plt.xlabel("Timeline", fontsize=12, fontweight="bold")
plt.ylabel("Tasks", fontsize=12, fontweight="bold")
plt.title("Gantt Chart for Smart Attendance System", fontsize=14, fontweight="bold")

# Enable grid for better readability
plt.grid(axis="x", linestyle="--", alpha=0.7)

# Adjust layout and show chart
plt.tight_layout()
plt.show()
