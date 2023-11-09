import sqlite3
import pandas as pd
import os
from collections import deque

MAX_COLS = 6
DATE = "26-10-2023"
TIME = "10:00 AM"
FILENAME = f'{DATE}.xlsx'

def load_subject_data():
    # Load subject data from Excel files
    df1 = pd.read_excel('2ND YEAR.xlsx')
    df2 = pd.read_excel('3RD YEAR.xlsx')
    df3 = pd.read_excel('4TH YEAR.xlsx')
    return df1, df2, df3

def get_selected_subjects(subject_headings):
    print("Select the subjects you want to include:")
    for i, heading in enumerate(subject_headings):
        print(f"{i + 1}. {heading}")

    selected_subjects = []
    while True:
        subject_choice = int(input("Enter the number of the subject (0 to finish): "))
        if subject_choice == 0:
            break
        elif 1 <= subject_choice <= len(subject_headings):
            selected_subjects.append(subject_headings[subject_choice - 1])
        else:
            print("Invalid choice. Please enter a valid number.")
    return selected_subjects

# Load subject data
df1, df2, df3 = load_subject_data()
subject_headings = list(df1.columns) + list(df2.columns) + list(df3.columns)

# Get selected subjects from the user
selected_subjects = get_selected_subjects(subject_headings)

# Create a deque with a maximum length of 3 for rotating subjects
rotating_subjects = deque(selected_subjects[:3])

# Create a list to store subjects that are waiting
waiting_subjects = selected_subjects[3:]

# Sort the selected subjects
selected_subjects.sort()

# Create a dictionary to store the subject data and the current roll number position
subject_data = {subject: df1[subject] if subject in df1.columns else
               df2[subject] if subject in df2.columns else
               df3[subject]
               for subject in selected_subjects}

subject_positions = {subject: 0 for subject in selected_subjects}

# Connect to SQLite database with room details
myconn = sqlite3.connect("room_details.db")
with myconn:
    cursor = myconn.cursor()
    cursor.execute("SELECT room_no, u_row_c1, u_row_c2, u_row_c3, u_row_c4, u_row_c5, u_row_c6 from room")
    rows = cursor.fetchall()

    # Create Excel writer
    writer = pd.ExcelWriter(FILENAME, engine='xlsxwriter')
    workbook = writer.book

    for row in rows:
        room_no = row[0]
        room_name = str(room_no)
        max_rows = row[1:]  # Extract maximum row counts for each column

        # Initialize a schedule list for the room
        room_schedule = [[] for _ in range(MAX_COLS)]

        for current_col in range(MAX_COLS):
            # Check if rotating_subjects is empty, terminate the program
            subject_heading_added = False
            if not rotating_subjects:
                break
            if len(rotating_subjects) != 1: 
                    room_schedule[current_col].append(rotating_subjects[0]) 
                    
            for _ in range(max_rows[current_col]):
                current_subject = rotating_subjects[0]
                 # Get the current subject from the rotating queue

                # Inside the loop where you handle column allocation
                if len(rotating_subjects) == 1:
                    

                    if (current_col - 1) % 2 == 0:
                        # Skip one column allocation on even columns
                        current_col += 1
                        break
                    elif current_col % 2 == 0:
                        if not subject_heading_added:
                            room_schedule[current_col].append(rotating_subjects[0])
                            subject_heading_added = True

                        max_rows = list(max_rows)
                        max_rows[current_col] = 0
                        max_rows = tuple(max_rows)

# Continue with the rest of the loop...

                     

                if subject_positions[current_subject] < len(subject_data[current_subject]):
                    student = subject_data[current_subject].iloc[subject_positions[current_subject]]
                    room_schedule[current_col].append(student)
                    subject_positions[current_subject] += 1

                # Check if the subject is exhausted and replace it
                if subject_positions[current_subject] >= len(subject_data[current_subject]):
                    rotating_subjects.popleft()
                    if waiting_subjects:
                        rotating_subjects.append(waiting_subjects.pop(0))
                        rotating_subjects.rotate(+1)
                        
                    elif not waiting_subjects:
                        # rotating_subjects.append(current_subject)
                        rotating_subjects.rotate(+1)# Treat the column as filled
                        break

            # Rotate the subjects once a column has finished
            rotating_subjects.rotate(-1)
            

        # Create a worksheet for the room
        worksheet = workbook.add_worksheet(room_name)

        # Write the scheduled students to the worksheet
        for col, students in enumerate(room_schedule):
            for row, student in enumerate(students):
                worksheet.write(row, col, student)

# Save the Excel file
writer._save()
