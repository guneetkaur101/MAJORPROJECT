from flask import Flask , render_template , request, redirect, url_for, flash
import sqlite3
import csv
import os
import pandas as pd

app = Flask(__name__)
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
		cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row_c1 integer(10),row_c2 integer(10),row_c3 integer(10),row_c4 integer(10),row_c5 integer(10),row_c6 integer(10),u_row_c1 integer(10),u_row_c2 integer(10),u_row_c3 integer(10),u_row_c4 integer(10),u_row_c5 integer(10),u_row_c6 integer(10),seat integer(10))")
		data = cursor.execute("SELECT * FROM room")
		data = cursor.fetchall()
	return render_template("admin.html",data=data)
@app.route("/addroom",methods=['GET','POST'])

def addroom():
    error = None
    
    if request.method == 'POST':
        room_no = request.form['room_no']

        # Read the rows per column values from the form
        rows_per_columns = [request.form[f'row_c{i}'] for i in range(1, 7)]
        
        # Calculate the total number of seats
        total_seats = sum([int(rows) for rows in rows_per_columns])
        # Copy the same values to u_row_c1, u_row_c2, ..., u_row_c6
        updated_rows_per_columns = rows_per_columns
        
        myconn = sqlite3.connect("room_details.db")

        with myconn:
            cursor = myconn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no INTEGER PRIMARY KEY, col INTEGER, row_c1 INTEGER, row_c2 INTEGER, row_c3 INTEGER, row_c4 INTEGER, row_c5 INTEGER, row_c6 INTEGER,u_row_c1 INTEGER, u_row_c2 INTEGER, u_row_c3 INTEGER, u_row_c4 INTEGER,u_row_c5 INTEGER, u_row_c6 INTEGER, seat INTEGER)")
            temp_no = cursor.execute("SELECT room_no from room where room_no=?", [room_no])
            temp_no = temp_no.fetchone()

        if temp_no is None:
            with myconn:
                cursor = myconn.cursor()
                cursor.execute("INSERT INTO room(room_no, col, row_c1, row_c2, row_c3, row_c4, row_c5, row_c6, u_row_c1, u_row_c2, u_row_c3, u_row_c4, u_row_c5, u_row_c6, seat) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                               [room_no, 6] + rows_per_columns + [total_seats])
                error = f"Room {room_no} is added "
        else:
            error = f"Room {room_no} is already exist."

    return render_template("addroom.html", error=error)  # Pass capacity to the HTML template
    
def show():
	data=None
	filename = None
	myconn = sqlite3.connect("room_details.db")
	with myconn:
		cursor = myconn.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row_c1 integer(10),row_c2 integer(10),row_c3 integer(10),row_c4 integer(10),row_c5 integer(10),row_c6 integer(10),u_row_c1 integer(10),u_row_c2 integer(10),u_row_c3 integer(10),u_row_c4 integer(10),u_row_c5 integer(10),u_row_c6 integer(10),seat integer(10))")
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
		cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row_c1 integer(10),row_c2 integer(10),row_c3 integer(10),row_c4 integer(10),row_c5 integer(10),row_c6 integer(10),u_row_c1 integer(10),u_row_c2 integer(10),u_row_c3 integer(10),u_row_c4 integer(10),u_row_c5 integer(10),u_row_c6 integer(10),seat integer(10))")
		cursor.execute("DELETE FROM room WHERE room_no=?",[id])
	return  redirect(url_for('admin'))

@app.route('/edit/<id>',methods=['GET','POST'])
def edit(id):
    message = None  # Initialize the message variable
    if request.method == 'POST':
        room_no = request.form['room_no']
        col = request.form['col']
        row = request.form['row']
        seat = request.form['seat']
        
        myconn = sqlite3.connect("room_details.db")
        with myconn:
            cursor = myconn.cursor()
            cursor.execute("UPDATE room SET room_no=?, col=?, row=?, seat=? WHERE room_no=?", (room_no, col, row, seat, id))
            myconn.commit()
            message = "Room details have been updated successfully."  # Set the message
            return redirect('/admin')  # Redirect to the admin page

    myconn = sqlite3.connect("room_details.db")
    with myconn:
        cursor = myconn.cursor()
        cursor.execute("SELECT * FROM room WHERE room_no = ?", [id])
        data = cursor.fetchone()
    
    if data:
        room_no = data[0]
        col = data[1]
        row = data[2]
        seat = data[3]
    else:
        room_no = None
        col = None
        row = None
        seat = None

    return render_template("editroom.html", room_no=room_no, col=col, row=row, seat=seat, message=message)
@app.route('/upload_form', methods=['GET', 'POST'])
def upload_form():
    total_strengths = {}  # Initialize as an empty dictionary
    # Define the list of available years
    available_years = ['2nd', '3rd', '4th']
    if request.method == 'POST':
        print("Processing started") 
        # Get the selected years from checkboxes
        selected_years = request.form.getlist('select_year')
        # # Check if at least one year is selected (already alert box)
        # if not selected_years:
        #     error = "Please select at least one year"
        #     return render_template('upload_form.html', total_strengths=total_strengths, error=error)
        upload_errors = []

        for year in available_years:
            if year in selected_years:
                csv_file = request.files.get(f'{year}_year_csv')

                if not csv_file:
                    upload_errors.append(f"Please upload a file for {year} year.")
                    continue  # Skip this year if the file is missing

                filename = f'{year}_year.csv'
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                csv_file.save(file_path)
                print("File saved") 
                # df = pd.read_csv(file_path)

                # # Exclude the top two rows (assuming they are headers)
                # df = df.iloc[1:]
                
                df = pd.read_csv(file_path, skiprows=1)
                # Calculate the number of entries (rows) in the CSV
                num_entries = len(df)
                total_strengths[year] = num_entries

        if upload_errors:
            return render_template('upload_form.html', total_strengths=total_strengths, upload_errors=upload_errors)
        print("Processing completed")
        return render_template('upload_form.html', total_strengths=total_strengths)

    return render_template('upload_form.html', total_strengths=total_strengths)


if __name__ == "__main__":
    app.run()