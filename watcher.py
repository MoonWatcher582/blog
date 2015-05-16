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

if __name__ == '__main__':
	app.run()
