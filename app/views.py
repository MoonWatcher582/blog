from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
	user = { 'nickname': 'Eric' }
	title = 'Home'
	posts = [
		{
			'author': { 'nickname': 'Robert' },
			'body': 'When I am king, you will be first against the wall.'
		},
		{
			'author': { 'nickname': 'Jason' },
			'body': 'With your opinion which is of no consequence at all.'
		}
	]
	return render_template("index.html", title=title, user=user, posts=posts)
