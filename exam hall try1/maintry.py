import sqlite3
import pandas as pd
import os

df1 = pd.read_excel('2ND YEAR.xlsx')
df2 = pd.read_excel('3RD YEAR.xlsx')
df3 = pd.read_excel('4TH YEAR.xlsx')
subject_headings = []
subject_headings.extend([f"D2CSE_{heading}" for heading in list(df1.columns)])
subject_headings.extend([f"D3CSE_{heading}" for heading in list(df2.columns)])
subject_headings.extend([f"D4CSE_{heading}" for heading in list(df3.columns)])

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

        row = 4
        col = 0
        room = []

        worksheet.write(1, 1, date)
        worksheet.write(1, 5, time)
        worksheet.write(0, 3, room_no)
    
    
    writer._save()