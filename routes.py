from flask import *
from functools import wraps
#from torndb import Connection
#from flaskext.mysql import MySQL
#mysql = MySQL()
app = Flask(__name__)

#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
#app.config['MYSQL_DATABASE_DB'] = 'demo'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'

#mysql.init_app(app)

app.secret_key = 'Anup'

#g.db = Connection('localhost','demo', user='root', password='root')

@app.route('/')
def home():
	cursor = mysql.connect().cursor()
	#cursor.execute('select * from flask')
#	cursor.execute("SELECT * from flask where username='Ashish' and pass='anup'")
	data = cursor.fetchone()
	if data is None:
		return "Username or Password is wrong"
	else:
		#return "Logged in successfully"
		return render_template('home.html')
	
	#entries = cursor.fetchall()
	#rows = g.iter("select * from flask")
	
	
@app.route('/welcome')
def welcome():
	return render_template('welcome.html')
	
def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You Need to Logged in first')
			return redirect(url_for('login'))
	return wrap
		
@app.route('/hello')
@login_required 
def hello():
	return render_template('hello.html')
	
@app.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid username or Password please try again.'
		else:
			session['logged_in'] = True
			return redirect( url_for('hello') )	
	return render_template('login.html', error=error )

@app.route('/logout')
def logout():
	session.pop('loggged_in', None)
	flash('you are Logged out')
	return redirect( url_for('login'))
if __name__ == '__main__':
	app.run(debug = True)

