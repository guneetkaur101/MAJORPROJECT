import pandas as pd

# Read data from Excel files
df1 = pd.read_excel('2ND YEAR.xlsx')
df2 = pd.read_excel('3RD YEAR.xlsx')
df3 = pd.read_excel('4TH YEAR.xlsx')

# Extract lists of roll numbers from DataFrames
roll_no_list1 = df1['URN'].tolist()
roll_no_list2 = df2['URN'].tolist()
roll_no_list3 = df3['URN'].tolist()

# Determine the sizes of the lists
size1 = len(roll_no_list1)
size2 = len(roll_no_list2)
size3 = len(roll_no_list3)
print(size1,size2,size3)
# Combine the two smallest lists and keep the largest list as it is
if size1 <= size2 and size2 <= size3:
    combined_list = roll_no_list1 + roll_no_list2
    largest_list = roll_no_list3
elif size2 <= size1 and size3 <= size1:
    combined_list = roll_no_list2 + roll_no_list3
    largest_list = roll_no_list1
else:
    combined_list = roll_no_list1 + roll_no_list3
    largest_list = roll_no_list2

# Prompt the user to input the maximum number of rows and columns for each room
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
