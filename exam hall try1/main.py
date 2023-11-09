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

def create_subject_data(df1, df2, df3, selected_subjects):
    # Create a dictionary to store the subject data and the current roll number position
    subject_data = {subject: df1[subject] if subject in df1.columns else
                   df2[subject] if subject in df2.columns else
                   df3[subject]
                   for subject in selected_subjects}
    return subject_data

def create_subject_positions(selected_subjects):
    subject_positions = {subject: 0 for subject in selected_subjects}
    return subject_positions

def connect_to_database():
    # Connect to SQLite database with room details
    myconn = sqlite3.connect("room_details.db")
    return myconn

def get_room_details(myconn):
    with myconn:
        cursor = myconn.cursor()
        cursor.execute("SELECT room_no, u_row_c1, u_row_c2, u_row_c3, u_row_c4, u_row_c5, u_row_c6 from room")
        rows = cursor.fetchall()
    return rows

def create_excel_writer():
    # Create Excel writer
    writer = pd.ExcelWriter(FILENAME, engine='xlsxwriter')
    return writer

def create_workbook(writer):
    workbook = writer.book
    return workbook

def create_room_schedule():
    # Initialize a schedule list for the room
    room_schedule = [[] for _ in range(MAX_COLS)]
    return room_schedule

def check_rotating_subjects(rotating_subjects):
    # Check if rotating_subjects is empty, terminate the program
    if not rotating_subjects:
        return False
    return True

def add_subject_to_schedule(rotating_subjects, room_schedule, current_col):
    if len(rotating_subjects) != 1: 
        room_schedule[current_col].append(rotating_subjects[0]) 
    return room_schedule

def allocate_students_to_room(rotating_subjects, room_schedule, current_col, max_rows, subject_positions, subject_data, waiting_subjects):
    for _ in range(max_rows[current_col]):
        current_subject = rotating_subjects[0]
        # Get the current subject from the rotating queue
        if len(rotating_subjects) == 1:
            if (current_col - 1) % 2 == 0:
                # Skip one column allocation on even columns
                current_col += 1
                break
            elif current_col % 2 == 0:
                max_rows = list(max_rows)
                max_rows[current_col] = 0
                max_rows = tuple(max_rows)

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
                rotating_subjects.rotate(+1)# Treat the column as filled
                break
    return room_schedule, rotating_subjects, subject_positions

def rotate_subjects(rotating_subjects):
    # Rotate the subjects once a column has finished
    rotating_subjects.rotate(-1)
    return rotating_subjects

def create_worksheet(workbook, room_name):
    # Create a worksheet for the room
    worksheet = workbook.add_worksheet(room_name)
    return worksheet

def write_to_worksheet(worksheet, room_name, room_schedule):
    worksheet.write(1, 1, "Date = " + DATE)
    worksheet.write(1, 5, "Time = " + TIME)
    room_name_format = workbook.add_format({'bold': True, 'font_size': 22})
    worksheet.write(0, 3, room_name, room_name_format)
    worksheet.set_row(0, 30)  # Set the row height to double
    # Write the scheduled students to the worksheet
    for col, students in enumerate(room_schedule):
        for row, student in enumerate(students):
            worksheet.write(row+3, col, student)
    return worksheet

def save_excel_file(writer):
    # Save the Excel file
    writer._save()

