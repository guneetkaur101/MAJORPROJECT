import sqlite3
import pandas as pd
import os

df1 = pd.read_excel('2ND YEAR.xlsx')
df2 = pd.read_excel('3RD YEAR.xlsx')
df3 = pd.read_excel('4TH YEAR.xlsx')
# roll_no_list1 = df1['URN'].tolist()
# roll_no_list2 = df2['URN'].tolist()



max_cols = 6
date = "26-10-2023"
time = "10:00"
filename = f'{date}.xlsx'
if os.path.exists(filename):
    os.remove(filename)

myconn = sqlite3.connect("room_details.db")
with myconn:
    cursor = myconn.cursor()
    cursor.execute("SELECT room_no, u_row_c1, u_row_c2, u_row_c3, u_row_c4, u_row_c5, u_row_c6 from room")
    rows = cursor.fetchall()
    writer = pd.ExcelWriter(f'{date}.xlsx', engine='xlsxwriter')
    workbook = writer.book
    for row in rows:
        room_no = row[0]
        room_name =str(room_no)
        u_row_c1 = row[1]
        u_row_c2 = row[2]
        u_row_c3 = row[3]
        u_row_c4 = row[4]
        u_row_c5 = row[5]
        u_row_c6 = row[6]
        max_rows = [u_row_c1, u_row_c2, u_row_c3, u_row_c4, u_row_c5, u_row_c6]

        worksheet = workbook.add_worksheet(room_name)
        row = 0
        col = 0
        room = []
        for j in range(max_cols):
            for i in range(max_rows[j]):
                if len(room) == i:
                    room.append([])
                if j % 2 == 0:
                    if roll_no_list1:
                        roll_no = roll_no_list1.pop(0)
                    else:
                        break
                else:
                    if roll_no_list2:
                        roll_no = roll_no_list2.pop(0)
                    else:
                       break
                room[j].append(roll_no)
                worksheet.write(i, j, roll_no)
    writer._save()

# writer = pd.ExcelWriter(f'{filename}', engine='xlsxwriter')
# workbook = writer.book

# for row in rows:
#     room_no = row[0]
#     room_name = str(room_no)
#     u_row_c1 = row[1]
#     u_row_c2 = row[2]
#     u_row_c3 = row[3]
#     u_row_c4 = row[4]
#     u_row_c5 = row[5]
#     u_row_c6 = row[6]
#     max_rows = [u_row_c1, u_row_c2, u_row_c3, u_row_c4, u_row_c5, u_row_c6]

#     worksheet = workbook.add_worksheet(room_name)
#     row = 4
#     col = 0
#     room = []

#     worksheet.write(1, 1, date)
#     worksheet.write(1, 5, time)
#     worksheet.write(0, 3, room_no)


# Get the list of subject headings from the CSV file (use the actual column name)
subject_headings = list(df3.columns)

print("Select the subjects you want to include:")
for i, heading in enumerate(subject_headings):
    print(f"{i + 1}. {heading}")

# Ask the user to select subjects
selected_subjects = []
while True:
    subject_choice = int(input("Enter the number of the subject (0 to finish): "))
    if subject_choice == 0:
        break
    elif 1 <= subject_choice <= len(subject_headings):
        selected_subjects.append(subject_headings[subject_choice - 1])
    else:
        print("Invalid choice. Please enter a valid number.")

# Now, you have the list of selected subjects in selected_subjects
print("Selected subjects:", selected_subjects)

# Create a dictionary to store data for each selected subject
subject_data = {subject: [] for subject in selected_subjects}

# ...

for j in range(max_cols):
    for i in range(max_rows[j]):
        if len(room) == i:
            room.append([])
        if j % 2 == 0:
            if roll_no_list1:
                roll_no = roll_no_list1.pop(0)
            else:
                break
        else:
            if roll_no_list2:
                roll_no = roll_no_list2.pop(0)
            else:
                break
        # Check if the student's subject is in the selected subjects
        # Use the actual column name from your DataFrame
        student_subject = df3.loc[i, selected_subjects[0]]  # Modify this to select the right subject column
        if student_subject in selected_subjects:
            subject_data[student_subject].append(roll_no)


    # Now, you have data under selected subjects stored in respective lists
    for subject, data in subject_data.items():
        print(f"Data for {subject}: {data}")

writer._save()
