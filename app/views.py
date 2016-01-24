from flask import Flask
#from app import app
from flask.ext.mysql import MySQL

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

from flask import render_template, flash, redirect, request, json, session
from app import app
from .forms import LoginForm
from werkzeug import generate_password_hash, check_password_hash


@app.route('/')
@app.route('/index')
def main():
    return render_template("index.html")

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
		cursor.callproc('sp_createUser',(_phone,_name,_location,_handle,_password))
		data = cursor.fetchall()
		if len(data) is 0:
			conn.commit()
			#return json.dumps({'message':'User created successfully !'})
			return redirect('/userHome')
		else:
			return json.dumps({'error':str(data[0])})
    else:
		return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _phone = request.form['inputPhone']
        _password = request.form['inputPassword']


        # connect to mysql
 
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_phone,))
        data = cursor.fetchall()

        if len(data) > 0:
            if str(data[0][5]) == str(_password):
                session['user'] = data[0][2]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Phone Number or Password.')
        else:
            return render_template('error.html',error = 'Wrong Phone Number or Password.')
 
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/myMenu')
def menu():
    if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()
        thisId = session['user']
        query = ("SELECT * FROM food WHERE vendor_id=1")
        cursor.execute(query)
        fields=cursor.fetchall()
        return render_template('menu.html',fields=fields)
    else:
        return render_template('error.html',error = 'Unauthorized Access')



