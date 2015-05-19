from flask import Flask, request, session, g, redirect, url_for, \
		abort, render_template, flash
from contextlib import closing
from config import *
import sqlite3

app = Flask(__name__)
#set up config
app.config.from_object(__name__)

def connect_db():
	'''handy function to connect to the database watcher.db'''
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	'''initialize the database watcher.db'''
	#closing keeps connection open for the with block
	with closing(connect_db()) as db:
		#open file for reading
		with app.open_resource('schema.sql', mode='r') as f:
			#db is a connection object
			#cursor() allows us to execute a script
			db.cursor().executescript(f.read())
		#commit changes
		db.commit()

#these functions will be called before a request
@app.before_request
def before_request():
	#g stores information for one request only
	g.db = connect_db()

#these functions will be called after a request
@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

@app.route('/')
def show_entries():
	cur = g.db.execute('select title, text from entries order by id desc')
	entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into entries (title, text) values (?,?)', 
			[request.form['title'], request.form['text']])
	g.db.commit()
	flash('New entry was successfully posted!')
	return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were successfully logged in!')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were successfully logged out!')
	return redirect(url_for('show_entries'))

if __name__ == '__main__':
	app.run()
