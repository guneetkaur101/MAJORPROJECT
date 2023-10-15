import pandas as pd

df1 = pd.read_excel('2ND YEAR.xlsx')
df2 = pd.read_excel('3RD YEAR.xlsx')
roll_no_list1 = df1['URN'].tolist()
roll_no_list2 = df2['URN'].tolist()

room = input("Enter the room name")
max_rows = [int(input(f"Enter the maximum number of rows in column{i+1}: ")) for i in range(6)]
max_cols = 6
max_capacity = sum(max_rows)

room = []
room_count = 0
room_no = 1

while roll_no_list1 or roll_no_list2:
    filename = f'room_{room_no}.xlsx'
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0

    for j in range(max_cols):
        for i in range(max_rows[j]):
            if room_count == max_capacity:
                room_count = 0
                room_no += 1
                filename = f'room_{room_no}.xlsx'
                writer = pd.ExcelWriter(filename, engine='xlsxwriter')
                workbook = writer.book
                worksheet = workbook.add_worksheet()
                row = 0
                col = 0
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
            room_count += 1
            worksheet.write(i, j, roll_no)

    writer._save()
    room_no += 1
    room_count = 0
    room = []