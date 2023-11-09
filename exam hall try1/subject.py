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
date = "26-10-2023"
time = "10:00"
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

# Create lists for each selected subject
subject_lists = []
for subject in selected_subjects:
    subject_list = []
    if subject.startswith("D2CSE_"):
        subject_column = subject.replace("D2CSE_", "")
        subject_list = list(df1[subject_column])
    elif subject.startswith("D3CSE_"):
        subject_column = subject.replace("D3CSE_", "")
        subject_list = list(df2[subject_column])
    elif subject.startswith("D4CSE_"):
        subject_column = subject.replace("D4CSE_", "")
        subject_list = list(df3[subject_column])
    subject_lists.append(subject_list)
# Sort the selected subjects
selected_subjects.sort()

subject_list_mapping = {}
for subject, subject_list in zip(selected_subjects, subject_lists):
    subject_list_mapping[subject] = subject_list
print("Selected subjects:", selected_subjects)
for subject in selected_subjects:
    print(f"List for {subject}: {subject_list_mapping[subject]}")

