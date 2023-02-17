from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__, template_folder='templates')
app.secret_key ='thisisnotasecretkey'
bcrypt = Bcrypt(app) 
