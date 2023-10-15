import sqlite3
import pandas as pd
import os

df1 = pd.read_excel('2ND YEAR.xlsx')
df2 = pd.read_excel('3RD YEAR.xlsx')
roll_no_list1 = df1['URN'].tolist()
roll_no_list2 = df2['URN'].tolist()

max_cols = 6
date= input("enter the date")
time = input("enter the time of exam")
filename = f'{date}.xlsx' 
if os.path.exists(filename):     
    os.remove(filename)
myconn = sqlite3.connect("room_details.db")
with myconn:
    cursor = myconn.cursor()
    cursor.execute("SELECT room_no, u_row_c1, u_row_c2, u_row_c3, u_row_c4, u_row_c5, u_row_c6 from room")
    rows = cursor.fetchall()
    writer = pd.ExcelWriter(f'{filename}', engine='xlsxwriter')
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
        row = 4
        col = 0
        room = []
        worksheet.write(1, 1, date)
        worksheet.write(1, 5, time)
        worksheet.write(0, 3, room_no)
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
                worksheet.write(i+4, j, roll_no)
    writer._save()

