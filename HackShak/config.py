import os

class HackShakConfig():
	SECRET_KEY = '3db99dd7894026ef33ecc5043d58019c5bb4e04274bc1f7ecb572026702bd392'

	DB_USERNAME = 'root' # set as environment variable at some stage
	DB_PASSWORD = 'mma2d&nqa'
	DB_DATABASE = 'hackshakdata'

	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+DB_USERNAME+':'+DB_PASSWORD+'@localhost:3306/'+DB_DATABASE


