from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash
# create a regular expression object that we'll use later   

from flask import flash

class User:
    db = "arbortrary_schema"
    def __init__(self, data):
        self.id_user=data['id_user']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW());"
        print(query)
        return connectToMySQL("arbortrary_schema").query_db(query,data)   

    @classmethod                                    
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("arbortrary_schema").query_db(query)
        users = []
        for u in results:
            users.append (cls (u))
        return users
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("arbortrary_schema").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id_user = %(id_user)s;"
        print(query)
        results = connectToMySQL("arbortrary_schema").query_db(query,data)
        return cls(results[0])
        


    @classmethod
    def get_one (cls, data):
        query="SELECT * FROM users WHERE id_user = %(id_user)s";
        result = connectToMySQL("arbortrary_schema").query_db(query,data)
        return cls(result[0])

    @classmethod
    def full_name (cls, data):
        query= "select distinct u.id_user, u.first_name, u.last_name, u.email, u.password, u.created_at, u.updated_at from users u left join  users_visited_trees uvt on u.id_user = uvt.users_id_visited where uvt.trees_id_planted = %(id)s;"
        result = connectToMySQL("arbortrary_schema").query_db(query,data)
        print(query)
        users = []
        for u in result:
            users.append (cls (u))
        return users
    

    #PROCESO DE VALIDACION

    @staticmethod
    def validate_register(data):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("arbortrary_schema").query_db(query,data)
        
        
        
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(data['first_name']) < 2:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if data['password'] != data['confirm']:
            flash("Passwords don't match","register")
            is_valid=False
        return is_valid