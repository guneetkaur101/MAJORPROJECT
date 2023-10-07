import pandas as pd

df1 = pd.read_excel('2ND YEAR.xlsx')
df2 = pd.read_excel('3RD YEAR.xlsx')
df3 = pd.read_excel('4TH YEAR.xlsx')
roll_no_list1 = df1['URN'].tolist()
roll_no_list2 = df2['URN'].tolist()
roll_no_list3 = df3['URN'].tolist()

max_row = int(input("Enter the maximum number of columns: "))
max_col = int(input("Enter the maximum number of rows: "))
max_capacity = max_row * max_col

room = []
room_count = 0
room_no = 1

while roll_no_list3:
    filename = f'room_{room_no}.xlsx'
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0

    for i in range(max_row):
        for j in range(max_col):
            if room_count == max_capacity:
                room_count = 0
                room_no += 1
                filename = f'room_{room_no}.xlsx'
                writer = pd.ExcelWriter(filename, engine='xlsxwriter')
                workbook = writer.book
                worksheet = workbook.add_worksheet()
                row = 0
                col = 0
            if len(room) == j:
                room.append([])
            if i % 3 == 0:
                if roll_no_list1:
                    roll_no = roll_no_list1.pop(0)
                else:
                    if roll_no_list2:
                        roll_no = roll_no_list2.pop(0)
                    else:
                        break
            else:
                if roll_no_list2:
                    roll_no = roll_no_list2.pop(0)
                else:
                    if roll_no_list1:
                        roll_no = roll_no_list1.pop(0)
                    else:
                        break
            room[j].append(roll_no)
            room_count += 1
            worksheet.write(j, i, roll_no)

    writer._save()
    room_no += 1
    room_count = 0
    room = []