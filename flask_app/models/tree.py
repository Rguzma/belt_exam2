from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
# create a regular expression object that we'll use later   

from flask import flash

class Tree:
    db = "arbortrary_schema"
    def __init__(self, data):
        self.id_tree=data['id_tree']
        self.specie = data['specie']
        self.location=data['location']
        self.reason = data['reason']
        self.date_planted=data['date_planted']
        self.created_at = data['created_at']
        self.updated_at=data['updated_at']
        self.who_planted=data['who_planted']
        try:
            self.first_name=data['first_name']
            self.last_name=data['last_name']
            self.counter=data['counter']
        except:
            self.first_name= ''
            self.last_name=''
            self.counter=0


    
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO trees (specie,location,reason,date_planted,created_at,who_planted) VALUES(%(specie)s,%(location)s,%(reason)s,NOW(), NOW(), %(who_planted)s);"
        return connectToMySQL("arbortrary_schema").query_db(query, data)

    @classmethod
    def get_all(cls, data):
        query = "select u.first_name, u.last_name, t.*, count(trees_id_planted) as 'counter' from trees t left join users u on t.who_planted = u.id_user left join users_visited_trees uvt on t.id_tree = uvt.trees_id_planted group by t.id_tree;"
        results =  connectToMySQL("arbortrary_schema").query_db(query, data)
        all_trees = []
        for row in results:
            all_trees.append( cls(row) )
        return all_trees

    @classmethod
    def get_car_and_seller(cls,data):
        query ="select c.*,u.first_name as 'seller_first_name', u.last_name as 'seller_last_name' from trees c join users u on u.id_user = c.seller where t.id_tree= %(id)s;"
        results = connectToMySQL("arbortrary_schema").query_db(query,data)
        print(78, query)
        return cls( results[0] )

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT t.*, u.first_name, u.last_name, 'counter'  FROM trees t inner join users u on t.who_planted = u.id_user WHERE id_tree = %(id)s;"
        print(query)
        results = connectToMySQL("arbortrary_schema").query_db(query,data)
        all_trees = []
        for row in results:
            all_trees.append( cls(row) )
        return all_trees

    @staticmethod
    def validate_tree(data_tree):
        is_valid = True
        if data_tree['specie'] == "" or data_tree['location']== "" or data_tree['reason']== "" or data_tree['date_planted']== "":
            is_valid = False
            flash("All spaces required","add_car")
        if len(data_tree['specie']) < 5:
            is_valid=False
            flash("Species must have min 5 characters","add_car")
        if len(data_tree['location']) < 2:
            is_valid=False
            flash("Species must have min 2 characters","add_car")
        if len(data_tree['specie']) < 5:
            is_valid=False
            flash("Species must have min 5 characters","add_car")
        if len(data_tree['reason']) > 50:
            is_valid=False
            flash("Reason must have max 50 characters","add_car")
        return is_valid

    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM trees WHERE id = %(id)s;"
        return connectToMySQL("arbortrary_schema").query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE trees SET price=%(price)s,model=%(model)s,make=%(make)s,year=%(year)s,updated_at=NOW(), description=%(description)s WHERE id_tree = %(id)s;"
        return connectToMySQL("arbortrary_schema").query_db(query,data)

