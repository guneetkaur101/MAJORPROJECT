import pandas as pd

year1 = ['subject1', 'subject2', 'subject3', 'none']
year2 = ['subject4', 'subject5', 'subject6', 'none']
year3 = ['subject7', 'subject8', 'subject9', 'none']

year1_file = None
year2_file = None
year3_file = None

while year1_file is None:
    print('Select a subject from year 1:')
    for i, subject in enumerate(year1):
        print(f'{i+1}. {subject}')
    choice = int(input())
    if choice == 4:
        break
    year1_file = pd.read_excel(f'2ND YEAR.xlsx')

while year2_file is None:
    print('Select a subject from year 2:')
    for i, subject in enumerate(year2):
        print(f'{i+1}. {subject}')
    choice = int(input())
    if choice == 4:
        break
    year2_file = pd.read_excel(f'3RD YEAR.xlsx')

while year3_file is None:
    print('Select a subject from year 3:')
    for i, subject in enumerate(year3):
        print(f'{i+1}. {subject}')
    choice = int(input())
    if choice == 4:
        break
    year3_file = pd.read_excel(f'4TH YEAR.xlsx')

roll_no_list1 = year1_file['URN'].tolist() if year1_file is not None else []
roll_no_list2 = year2_file['URN'].tolist() if year2_file is not None else []
roll_no_list3 = year3_file['URN'].tolist() if year3_file is not None else []

size1 = len(roll_no_list1)
size2 = len(roll_no_list2)
size3 = len(roll_no_list3)
print(size1,size2,size3)

if size1 <= size2 and size2 <= size3:
    combined_list = roll_no_list1 + roll_no_list2
    largest_list = roll_no_list3
elif size2 <= size1 and size3 <= size1:
    combined_list = roll_no_list2 + roll_no_list3
    largest_list = roll_no_list1
else:
    combined_list = roll_no_list1 + roll_no_list3
    largest_list = roll_no_list2

max_row = int(input("Enter the maximum number of columns: "))
max_col = int(input("Enter the maximum number of rows: "))
max_capacity = max_row * max_col

room = []
room_count = 0
room_no = 1

while combined_list or largest_list:
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
            if i % 2 == 0:
                if combined_list:
                    roll_no = combined_list.pop(0)
                else:
                    break
            else:
                if largest_list:
                    roll_no = largest_list.pop(0)
                else:
                    break
            room[j].append(roll_no)
            room_count += 1
            worksheet.write(j, i, roll_no)

    writer._save()
    room_no += 1
    room_count = 0
    room = []
