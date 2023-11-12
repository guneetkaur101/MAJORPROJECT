from flask import Flask , render_template , request, redirect, url_for, flash, session,send_file
from flask import request, Response
import json
import sqlite3
import csv
import os
import pandas as pd
from collections import deque
import datetime
import fullfinalized as ff
from flask import jsonify
app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route("/")
def home():
    return render_template("home.html" )
@app.route("/About")
def about():
    return render_template("aboutus.html")
@app.route("/login",methods=['GET','POST'])
def login():
	error = None
	if request.method=='POST':
		email = request.form['email']
		password = request.form['psw']
		if email =="admin" and password == "admin":
			return  redirect(url_for('admin'))
		else:
			error = "INVALID DETAILS"
	return render_template("login.html",error=error)
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/admin")
def admin():
	myconn = sqlite3.connect("room_details.db")
	with myconn:
		cursor = myconn.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row_c1 integer(10),row_c2 integer(10),row_c3 integer(10),row_c4 integer(10),row_c5 integer(10),row_c6 integer(10),u_row_c1 integer(10),u_row_c2 integer(10),u_row_c3 integer(10),u_row_c4 integer(10),u_row_c5 integer(10),u_row_c6 integer(10),seat integer(10),usable_seats integer(10))")
		data = cursor.execute("SELECT * FROM room")
		data = cursor.fetchall()
	return render_template("admin.html",data=data)
@app.route("/addroom",methods=['GET','POST'])

def addroom():
    error = None
    
    if request.method == 'POST':
        room_no = request.form['room_no']
        print(request.form)
        # Read the rows per column values from the form
        rows_per_columns = [request.form[f'row_c{i}'] for i in range(1, 7)]
        print(rows_per_columns)
        # Copy the values to u_row_c1, u_row_c2, ..., u_row_c6
        updated_rows_per_columns = rows_per_columns
        print(updated_rows_per_columns)
        # Calculate the total number of seats
        total_seats = sum([int(rows) for rows in rows_per_columns])
        print(total_seats)
        room_usable_seats=sum([int(rows) for rows in updated_rows_per_columns])
        print(room_usable_seats)

        myconn = sqlite3.connect("room_details.db")

        with myconn:
            cursor = myconn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no INTEGER PRIMARY KEY, col INTEGER, row_c1 INTEGER, row_c2 INTEGER, row_c3 INTEGER, row_c4 INTEGER, row_c5 INTEGER, row_c6 INTEGER,u_row_c1 INTEGER, u_row_c2 INTEGER, u_row_c3 INTEGER, u_row_c4 INTEGER,u_row_c5 INTEGER, u_row_c6 INTEGER, seat INTEGER, usable_seats INTEGER)")
            temp_no = cursor.execute("SELECT room_no from room where room_no=?", [room_no])
            temp_no = temp_no.fetchone()

        if temp_no is None:
            with myconn:
                cursor = myconn.cursor()
                cursor.execute("INSERT INTO room(room_no, col, row_c1, row_c2, row_c3, row_c4, row_c5, row_c6, u_row_c1, u_row_c2, u_row_c3, u_row_c4, u_row_c5, u_row_c6,seat,usable_seats) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                               [room_no, 6] + rows_per_columns + updated_rows_per_columns + [total_seats,room_usable_seats])
                error = f"Room {room_no} is added "
        else:
            error = f"Room {room_no} is already exist."
        # Commit the changes to the database
        myconn.commit()
    return render_template("addroom.html", error=error)  # Pass capacity to the HTML template
    
def show():
	data=None
	filename = None
	myconn = sqlite3.connect("room_details.db")
	with myconn:
		cursor = myconn.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row_c1 integer(10),row_c2 integer(10),row_c3 integer(10),row_c4 integer(10),row_c5 integer(10),row_c6 integer(10),u_row_c1 integer(10),u_row_c2 integer(10),u_row_c3 integer(10),u_row_c4 integer(10),u_row_c5 integer(10),u_row_c6 integer(10),seat integer(10),usable_seats integer(10))")
		temp_no = cursor.execute("SELECT room_no from room ")
		temp_no = cursor.fetchall()
	if request.method == 'POST':
		room_no = request.form['room']
		data =  read(room_no)
		data= data.to_html()
		filename = '/static/execl/'+room_no+'.xlsx'
	return render_template("show_result.html",data=data,room_no=temp_no,filename=filename)

@app.route('/delete/<id>')
def delete(id):
	myconn = sqlite3.connect("room_details.db")
	with myconn:
		cursor = myconn.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row_c1 integer(10),row_c2 integer(10),row_c3 integer(10),row_c4 integer(10),row_c5 integer(10),row_c6 integer(10),u_row_c1 integer(10),u_row_c2 integer(10),u_row_c3 integer(10),u_row_c4 integer(10),u_row_c5 integer(10),u_row_c6 integer(10),seat integer(10),usable_seats integer(10))")
		cursor.execute("DELETE FROM room WHERE room_no=?",[id])
	return  redirect(url_for('admin'))

@app.route('/edit/<room_no>', methods=['GET', 'POST'])
def edit(room_no):
    error = None
    if request.method == 'POST':
        # Retrieve the updated details from the form
        col = request.form['columns']
        rows_per_columns = [request.form[f'row_c{i}'] for i in range(1, 7)]
        print(rows_per_columns)
        # Calculate the total number of seats
        total_seats = sum([int(rows) for rows in rows_per_columns])
        updated_rows_per_columns = rows_per_columns
        print(updated_rows_per_columns)
        print(total_seats)
        room_usable_seats=sum([int(rows) for rows in updated_rows_per_columns])
        print(room_usable_seats)
        room_usable_seats=total_seats
        myconn = sqlite3.connect("room_details.db")
        with myconn:
           cursor = myconn.cursor()
        # # Update the room details in the database
        #    cursor.execute("UPDATE room SET col=?, row_c1=?, row_c2=?, row_c3=?, row_c4=?, row_c5=?, row_c6=?, u_row_c1=?, u_row_c2=?, u_row_c3=?, u_row_c4=?, u_row_c5=?, u_row_c6=?, seat=?,usable_seats=? WHERE room_no=?", 
        #                [col] + rows_per_columns + updated_rows_per_columns + [total_seats, room_no],[room_usable_seats,room_no])
        # Update the room details in the database
           cursor.execute("UPDATE room SET col=?, row_c1=?, row_c2=?, row_c3=?, row_c4=?, row_c5=?, row_c6=?, u_row_c1=?, u_row_c2=?, u_row_c3=?, u_row_c4=?, u_row_c5=?, u_row_c6=?, seat=?, usable_seats=? WHERE room_no=?", 
               (col, *rows_per_columns, *updated_rows_per_columns, total_seats, room_usable_seats, room_no))

           myconn.commit()
           error = "Room details have been updated successfully."
           return redirect('/admin')  # Redirect to the admin page
    
    myconn = sqlite3.connect("room_details.db")
    with myconn:
        cursor = myconn.cursor()
    # Fetch the current room details for rendering the edit page
        cursor.execute("SELECT * FROM room WHERE room_no = ?", [room_no])
        room_details = cursor.fetchone()

    if room_details:
        col = room_details[1]
        row_details = room_details[2:15]
    else:
        col = None
        row_details = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    return render_template("editroom.html", room_no=room_no, col=col, row_details=row_details, error=error)

# @app.route('/edit/<id>',methods=['GET','POST'])
# def edit(id):
#     message = None  # Initialize the message variable
#     if request.method == 'POST':
#         room_no = request.form['room_no']
#         col = request.form['col']
#         row = request.form['row']
#         seat = request.form['seat']
        
#         myconn = sqlite3.connect("room_details.db")
#         with myconn:
#             cursor = myconn.cursor()
#             cursor.execute("UPDATE room SET room_no=?, col=?, row=?, seat=? WHERE room_no=?", (room_no, col, row, seat, id))
#             myconn.commit()
#             message = "Room details have been updated successfully."  # Set the message
#             return redirect('/admin')  # Redirect to the admin page

#     myconn = sqlite3.connect("room_details.db")
#     with myconn:
#         cursor = myconn.cursor()
#         cursor.execute("SELECT * FROM room WHERE room_no = ?", [id])
#         data = cursor.fetchone()
    
#     if data:
#         room_no = data[0]
#         col = data[1]
#         row = data[2]
#         seat = data[3]
#     else:
#         room_no = None
#         col = None
#         row = None
#         seat = None

#     return render_template("editroom.html", room_no=room_no, col=col, row=row, seat=seat, message=message)
@app.route('/upload_form', methods=['GET', 'POST'])
def upload_form():
    total_strengths = {}  # Initialize as an empty dictionary
    # Define the list of available years
    # available_subjects = [list(df1.columns) + list(df2.columns) + list(df3.columns)]
    global selected_subjects
    selected_subjects = []
    df1, df2, df3 = ff.load_subject_data()
    available_years = ['2nd', '3rd', '4th']

    # Check if the upload folder already contains excel files for respective inputs
    uploaded_files = []
    for year in available_years:
        filename = f'{year}_year.xlsx'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            timestamp = os.path.getmtime(file_path)
            formatted_timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%d:%m:%Y %H:%M')
            uploaded_files.append((filename, formatted_timestamp))


    if request.method == 'POST':
        upload_errors = []
        for year in available_years:
            xlsx_file = request.files.get(f'{year}_year_xlsx')

            if not xlsx_file:
                upload_errors.append(f"Please upload a file for {year} year.")
                continue  # Skip this year if the file is missing

            filename = f'{year}_year.xlsx'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            xlsx_file.save(file_path)
            print("File saved") 

    return render_template('upload_form.html', total_strengths=total_strengths, df1=df1, df2=df2, df3=df3, selected_subjects=selected_subjects, uploaded_files=uploaded_files)


@app.route("/generate", methods=['GET', 'POST'])
def generate():
    myconn = sqlite3.connect("room_details.db")
    with myconn:
        cursor = myconn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row_c1 integer(10),row_c2 integer(10),row_c3 integer(10),row_c4 integer(10),row_c5 integer(10),row_c6 integer(10),u_row_c1 integer(10),u_row_c2 integer(10),u_row_c3 integer(10),u_row_c4 integer(10),u_row_c5 integer(10),u_row_c6 integer(10),seat integer(10),usable_seats integer(10))")

    total_strengths = {}  # Initialize as an empty dictionary
    global selected_subjects
    selected_subjects = []

    df1, df2, df3 = ff.load_subject_data()
    subject_headings = list(df1.columns) + list(df2.columns) + list(df3.columns)

    if request.method == 'POST':
        print("Processing started")
        
        # Check if the request is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            selected_subjects = request.form.getlist('select_subject')
            session['selected_subjects'] = selected_subjects  # Store in session
            subject_lengths = {}
            file_strength_df1 = 0
            file_strength_df2 = 0
            file_strength_df3 = 0

            for subject in selected_subjects:
                subject_length = 0

                for csv_file in [df1, df2, df3]:
                    if subject in csv_file.columns:
                        roll_numbers = csv_file[subject].dropna().tolist()
                        subject_length += len(roll_numbers) - 1

                        if subject in df1:
                            file_strength_df1 += subject_length
                        if subject in df2:
                            file_strength_df2 += subject_length
                        if subject in df3:
                            file_strength_df3 += subject_length

                subject_lengths[subject] = subject_length

            total_strength = sum(subject_lengths.values())
            total_strengths.update(subject_lengths)
            total_strengths['2nd Year students'] = file_strength_df1
            total_strengths['3rd Year students'] = file_strength_df2
            total_strengths['4th Year students'] = file_strength_df3
            total_strengths['ALL Years total'] = total_strength

            selected_strengths = {subject: total_strengths.get(subject, 0) for subject in selected_subjects}
            selected_strengths['ALL Years total'] = total_strength
            response_data = json.dumps(selected_strengths)

            return Response(response_data, content_type='application/json')

        else:
            selected_rooms = request.form.getlist('selected_rooms')
            selected_subjects = session.get('selected_subjects', [])
            # This block will handle non-AJAX form submissions
            selected_rooms = request.form.getlist('selected_rooms')
            print(selected_rooms)
            MAX_COLS = 6
            DATE = datetime.datetime.now().strftime('%d-%m-%Y')
            TIME = datetime.datetime.now().strftime('%H-%M %p')
            FILENAME = f'{DATE}_{TIME}.xlsx'

            df1, df2, df3 = ff.load_subject_data()
            subject_headings = list(df1.columns) + list(df2.columns) + list(df3.columns)
            print(selected_subjects)
            print(subject_headings)

            ff.main(selected_rooms, df1, df2, df3, FILENAME, DATE, TIME, selected_subjects)
            return send_file(FILENAME,as_attachment=True)
    cursor.execute("SELECT * FROM room")
    data = cursor.fetchall()
    # # Clear the 'selected_subjects' session variable on page refresh
    # session.pop('selected_subjects', None)
    # Clear all session variables on page refresh
    session.clear()
    return render_template("generate.html", data=data, total_strengths=total_strengths, df1=df1, df2=df2, df3=df3, selected_subjects=selected_subjects)

def get_room_data(room_no):
    # This function retrieves the data for the specified room from the database.
    myconn = sqlite3.connect("room_details.db")
    cursor = myconn.cursor()
    cursor.execute("SELECT * FROM room WHERE room_no=?", (room_no,))
    room_data = cursor.fetchone()
    myconn.close()
    return room_data
@app.route("/edit-usable-rows/<room_no>", methods=['GET', 'POST'])
def edit_usable_rows(room_no):
    if request.method == 'POST':
        # Get the submitted form data and update the database
        usable_row_c1 = request.form.get('usable_row_c1')
        usable_row_c2 = request.form.get('usable_row_c2')
        usable_row_c3 = request.form.get('usable_row_c3')
        usable_row_c4 = request.form.get('usable_row_c4')
        usable_row_c5 = request.form.get('usable_row_c5')
        usable_row_c6 = request.form.get('usable_row_c6')
        usable_rows_per_columns = [request.form[f'usable_row_c{i}'] for i in range(1, 7)]
        # Calculate the total number of seats
        room_usable_seats = sum([int(rows) for rows in usable_rows_per_columns])
        print(room_usable_seats)
        
        myconn = sqlite3.connect("room_details.db")
        cursor = myconn.cursor()

        # Update the database with the new usable rows data
        cursor.execute(
            "UPDATE room SET u_row_c1=?, u_row_c2=?, u_row_c3=?, u_row_c4=?, u_row_c5=?, u_row_c6=?,usable_seats=? WHERE room_no=?",
            (usable_row_c1, usable_row_c2, usable_row_c3, usable_row_c4, usable_row_c5, usable_row_c6,room_usable_seats, room_no)
        )
        myconn.commit()
        myconn.close()

        # Redirect back to the "generate" page after the update
        return redirect("/generate")

    # In the GET request, you can fetch the room data to display in the form
    room_data = get_room_data(room_no)

    return render_template("edit_usable_rows.html", room_data=room_data)
if __name__ == "__main__":
    app.run(debug=True)