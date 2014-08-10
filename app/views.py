from flask import render_template, flash, redirect
from app import app
from forms import LoginForm

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
	return render_template('index.html', title=title, user=user, posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
	title = 'Sign In'
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
		return redirect('/index')
	return render_template('login.html', title=title, form=form, providers=app.config['OPENID_PROVIDERS'])
