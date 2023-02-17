from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
# we are creating an object called bcrypt, 
# which is made by invoking the function Bcrypt with our app as an argument

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*\d).{8,}$')
db = 'project'

class Users:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls,data):
        query="""
        INSERT INTO users(first_name,last_name,email,password)
        VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)
        """
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def login_user(cls,data):
        query="""
        SELECT email,password
        FROM users
        WHERE email == %(email)s
        """
        results = connectToMySQL(db).query_db(query,data)
        if results:
            if data['password'] == results[0]['password']:
                return True
            else:
                return False
        else:return False

    @classmethod
    def dashboard_page(cls,data):
        query = """
        SELECT * FROM users 
        WHERE email = %(email)s
        """
        results = connectToMySQL(db).query_db(query,data)
        return results[0]


    @classmethod
    def get_by_email(cls,data):
        query="""
        SELECT * FROM users WHERE email = %(email)s
        """
        results = connectToMySQL(db).query_db(query,data)
        if results and len(results) > 0:
            found_user = cls(results[0])
            return found_user
        return False
        

        
    @staticmethod
    def validate_create(create_user):
        is_valid = True
        if len(create_user['first_name']) <  2:
            flash("First name must be at least 2 characters long!")
            is_valid = False
        if len(create_user['last_name']) < 2:
            flash("Last name must be at least 2 characters long!")
            is_valid = False
        if not EMAIL_REGEX.match(create_user['email']):
            flash("Invalid email address!")
            is_valid = False
        if not PASSWORD_REGEX.match(create_user['password']):
            flash("invalid password! Must be atleast 8 characters long and contain a number!")
            is_valid = False
        if (create_user['confirm_password']) != create_user['password']:
            flash("passwords dont match! Try again")
            is_valid = False
        return is_valid


    @staticmethod
    def validate_login(login_user):
        is_valid = True
        if len(login_user['email']) == 0:
            flash('Email field left blank, please enter information!')
            is_valid = False
        if len(login_user['password']) < 3:
            flash('Password field left blank, please enter information!')
            is_valid = False
        return is_valid