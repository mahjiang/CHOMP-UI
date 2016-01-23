from flask import Flask,render_template
#from app import app
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object('config')
db_params = {
	'user' : 'chompdb',
	'passwd' : 'pennapps2016s',
	'host' : 'chompdb.cdslabnytkw3.us-east-1.rds.amazonaws.com',
	'db' : 'chompdb'
}
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = db_params['user']
app.config['MYSQL_DATABASE_PASSWORD'] = db_params['passwd']
app.config['MYSQL_DATABASE_DB'] = db_params['db']
app.config['MYSQL_DATABASE_HOST'] = db_params['host']
mysql.init_app(app)

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)

from flask import Flask, render_template, flash, redirect, request, json
from app import app
from .forms import LoginForm

# index view function suppressed for brevity

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _phone = request.form['inputPhone']
    _handle = request.form['inputHandle']
    _location = request.form['inputLocation']
    _password = request.form['inputPassword']
    # validate the received values
    if _name and _phone and _handle and _location and _password:
        
		conn = mysql.connect()
		cursor = conn.cursor()
		_hashed_password = generate_password_hash(_password)
		cursor.callproc('sp_createUser',(_phone,_name,_location,_handle,_hashed_password))
		data = cursor.fetchall()
		if len(data) is 0:
			conn.commit()
			return json.dumps({'message':'User created successfully !'})
		else:
			return json.dumps({'error':str(data[0])})
    else:
		return json.dumps({'html':'<span>Enter the required fields</span>'})

