from flask import Flask
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

from app import views