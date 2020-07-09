from flask import Flask,render_template,request

# set the project root directory as the static folder, you can set others.
#app = Flask(__name__, static_url_path="/static", static_folder='C:\iSmile TEch\covid (1)\covid\static')
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
	
@app.route('/inner')
def inner():
	Fname = request.args.get('Fname')
	Lname = request.args.get('Lname')
	Age = request.args.get('Age')
	City = request.args.get('City')
	print("-------------------------")
	print(Fname)
	print(Lname)
	print(Age)
	print(City)

	import pyodbc

	server = 'virutal.database.windows.net' 
	database = 'COVID19-db' 
	username = 'Ismiledb' 
	password = 'Ismile@123' 
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()

	cursor.execute("INSERT INTO PersonDetails(LastName,FirstName,Age,City) VALUES (?,?,?,?)",(Lname,Fname,Age,City))
	cnxn.commit()

	cursor.execute("SELECT TOP 1 * FROM PersonDetails ORDER BY Personid DESC")
	row=cursor.fetchone()
	print(row[0])

	return render_template('inner.html')

	
@app.route('/results')
def results():
	import pyodbc

	server = 'virutal.database.windows.net' 
	database = 'COVID19-db' 
	username = 'Ismiledb' 
	password = 'Ismile@123' 
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()

	cursor.execute("SELECT TOP 1 * FROM SensorDetails ORDER BY id DESC")
	row=cursor.fetchone()
	print(row[1])

	cursor.execute("SELECT temperature FROM SensorDetails where id="+str(row[1])+"")
	temperature=cursor.fetchone()
	print(temperature[0])

	return render_template('results.html',temperature=temperature[0])
	
if __name__ == "__main__":
    app.run(debug=True)