from flask import Flask , render_template , request, redirect, url_for, flash
import sqlite3
import csv
import os

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
		cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row integer(10),seat integer(10))")
		data = cursor.execute("SELECT * FROM room")
		data = cursor.fetchall()
	return render_template("admin.html",data=data)
@app.route("/addroom",methods=['GET','POST'])
def addroom():
	data=None
	error = None
	if request.method == 'POST':
		room_no = request.form['room_no']
		row = request.form['row']
		col = request.form['col']
		seat = request.form['seat']
		myconn = sqlite3.connect("room_details.db")
		if (int(seat) <= int(row) * int(col)):
			with myconn:
				cursor = myconn.cursor()
				cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row integer(10),seat integer(10))")
				temp_no = cursor.execute("SELECT room_no from room where room_no=?",[room_no])
				temp_no = cursor.fetchone()	
			if temp_no is None:
				with myconn:
					cursor = myconn.cursor()
					cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row integer(10),seat integer(10))")
					cursor.execute("INSERT INTO room VALUES(?,?,?,?)",[room_no,col,row,seat]) 
					error = room_no + " is added"
			else:
				error = room_no + " is already exist"
		else:
			error = "Invalid number of seat" 
	return render_template("addroom.html",error = error,data=data)
@app.route("/Upload",methods=['GET','POST'])
def upload():  
    error = None
    uploaded_files = []

    if request.method == 'POST':
        # Handle file uploads for 2nd, 3rd, and 4th years
        for year in ['2nd', '3rd', '4th']:
            csv_file = request.files.get(f'{year}_year_csv')
            if csv_file:
                filename = f'{year}_year.csv'
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                csv_file.save(file_path)
                uploaded_files.append(filename)

         # If no files were uploaded, list all files in the upload directory
        if not uploaded_files:
           uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])

        # Modify the response message
        if uploaded_files:
			
            error = "CSV files uploaded successfully."
        else:
            error = "Please upload CSV files."
	

    return render_template("upload.html", error=error, uploaded_files=uploaded_files)

   


def show():
	data=None
	filename = None
	myconn = sqlite3.connect("room_details.db")
	with myconn:
		cursor = myconn.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row integer(10),seat integer(10))")
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
		cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row integer(10),seat integer(10))")
		cursor.execute("DELETE FROM room WHERE room_no=?",[id])
	return  redirect(url_for('admin'))
@app.route('/edit/<id>',methods=['GET','POST'])
def edit(id):
	if request.method == 'POST':
		room_no = request.form['room_no']
		row = request.form['row']
		col = request.form['col']
		seat = request.form['seat']
		myconn = sqlite3.connect("room_details.db")
		if (int(seat) <= int(row) * int(col)):
			with myconn:
				cursor = myconn.cursor()
				cursor.execute("CREATE TABLE IF NOT EXISTS room(room_no integer(10),col integer(10),row integer(10),seat integer(10))")
				cursor.execute("INSERT INTO room VALUES(?,?,?,?)",[room_no,col,row,seat]) 
				error = room_no + " is added"
		else:
			error = "Invalid number of seat" 
	error = None
	myconn = sqlite3.connect("room_details.db")
	with myconn:
		cursor = myconn.cursor()
		data = cursor.execute("SELECT * FROM room WHERE room_no = ?",[id])
		data = cursor.fetchmany()
	room_no = data[0][0]
	col = 	data[0][1]
	row = data[0][2]
	seat = data[0][3]
	return render_template("addroom.html",error = error,room = room_no,col = col, row = row, seat = seat)





if __name__ == "__main__":
    app.run()