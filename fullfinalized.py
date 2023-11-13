import sqlite3
import pandas as pd
import os
from collections import deque
import proj
MAX_COLS = 6
MAX_SUBJECTS=3
def load_subject_data():
    
    # Load subject data from Excel filesdf
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    if os.path.exists('uploads/2nd_year.xlsx'):
        df1 = pd.read_excel('uploads/2nd_year.xlsx')
    if os.path.exists('uploads/3rd_year.xlsx'):
        df2 = pd.read_excel('uploads/3rd_year.xlsx')
    if os.path.exists('uploads/4th_year.xlsx'):
        df3 = pd.read_excel('uploads/4th_year.xlsx')
    print('files read')
    return df1, df2, df3
# selected_subjects=proj.selected_subjects
def main(selected_rooms,df1,df2,df3, FILENAME,DATE,TIME,selected_subjects):
    # if os.path.exists(FILENAME):
    #         os.remove(FILENAME)

    # Filter rooms based on user selection
    print("generation started")
    

    # Create a deque with a maximum length of 3 for rotating subjects
    rotating_subjects = deque(selected_subjects[:MAX_SUBJECTS])

    # Create a list to store subjects that are waiting
    waiting_subjects = selected_subjects[MAX_SUBJECTS:]

    # Sort the selected subjects
    # selected_subjects.sort()
    first_check=True
    column_odd_flag= True
    # Create a dictionary to store the subject data and the current roll number position
    subject_data = {subject: df1[subject] if subject in df1.columns else
                df2[subject] if subject in df2.columns else
                df3[subject]
                for subject in selected_subjects}

    subject_positions = {subject: 0 for subject in selected_subjects}
    myconn = sqlite3.connect("room_details.db")
    with myconn:
        cursor = myconn.cursor()
        cursor.execute("SELECT room_no, u_row_c1, u_row_c2, u_row_c3, u_row_c4, u_row_c5, u_row_c6 from room")
        rooms = cursor.fetchall()
    # Create Excel writer
    os.makedirs("generated", exist_ok=True)
    writer = pd.ExcelWriter(os.path.join("generated", FILENAME), engine='xlsxwriter')
    # Open the generated path
    os.startfile("generated")
    workbook = writer.book
    rooms = [room for room in rooms if room[0] in selected_rooms]

    for room in rooms:
        room_no = room[0]
        room_name = str(room_no)
        max_rows = room[1:]  # Extract maximum row counts for each column

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

                if len(rotating_subjects) == 1:

                    if current_col % 2 ==0 and first_check==True:
                        column_odd_flag=False
                        first_check=False

                    if column_odd_flag==True:
                        # Skip one column allocation on even columns
                        first_check=False
                        if current_col%2 == 0:
                            max_rows = list(max_rows)
                            max_rows[current_col] = 0
                            max_rows = tuple(max_rows)
                            current_col +=1
                            break
                        if not subject_heading_added:
                            room_schedule[current_col].append(rotating_subjects[0])
                            subject_heading_added = True

                    if column_odd_flag==False:
                        if current_col%2 != 0:
                            max_rows = list(max_rows)
                            max_rows[current_col] = 0
                            max_rows = tuple(max_rows)
                            current_col +=1
                            break

                        if not subject_heading_added:
                            room_schedule[current_col].append(rotating_subjects[0])
                            subject_heading_added = True

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
                        rotating_subjects.rotate(+1)
                        break

            # Rotate the subjects once a column has finished
            rotating_subjects.rotate(-1)


        # Create a worksheet for the room
        worksheet = workbook.add_worksheet(room_name)
        worksheet.merge_range(1, 0, 1, 1, "Date = " + DATE)
        worksheet.merge_range(1, 4, 1, 5, "Time = " + TIME)
        room_name_format = workbook.add_format({'bold': True, 'font_size': 22, 'align': 'center'})
        worksheet.merge_range(0, 2, 0, 3, room_name, room_name_format)
        worksheet.set_row(0, 30)  # Set the row height to double
        # Write the scheduled students to the worksheet
        for col, students in enumerate(room_schedule):
            for row, student in enumerate(students):
                worksheet.write(row+3, col, student)

    # Save the Excel file
    writer._save()

if __name__ == "__main__":
    main()
