import re
from app.config.mysqlconnection import connectToMySQL
from app import app
from flask import flash 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

from app.models import child_model
from app.models import suggestion_model

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# PASSWORD_REGEX = re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$")


class User:
    db = 'clothing_size_guide'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.children = []

    @classmethod
    def get_user_by_id(cls, id):
        print('GETTING USER WITH ID')
        # Query to get user by ID with all children and subsequent child suggestions.
        query = '''
                SELECT * FROM users
                LEFT JOIN children on users.id = children.user_id
                LEFT JOIN suggestions on children.id = suggestions.child_id
                WHERE users.id = %(id)s;     
                '''
        results = connectToMySQL(cls.db).query_db(query, {'id': id})

        # Instantiate the user. 
        user = cls(results[0])

        # Loop through results for children and suggestions
        for row in results:

            # Check that their is child data and that the child has not already been added to user.children[].
            if row['children.id'] is not None and row['children.id'] not in [child.id for child in user.children] :

                # Instantiate the child with the available data
                child = child_model.Child({
                    'id': row['children.id'],
                    'name': row['children.name'],
                    'date_of_birth': row['date_of_birth'],
                    'height': row['height'],
                    'weight': row['weight'],
                    'foot_size': row['foot_size'],
                    'user_id': row['user_id'],
                })

                # Append the child to the user.children list. 
                user.children.append(child)
            
            # Check that their is suggestion data and that the suggestions has not already been added to child.suggestions[].
            if row['suggestions.id'] is not None and row['suggestions.id'] not in [suggestion.id for suggestion in child.suggestions] :

                # Instantiate the suggestion with the available data
                suggestion = suggestion_model.Suggestion({
                    'id': row['suggestions.id'],
                    'brand': row['brand'],
                    'clothing_type': row['clothing_type'],
                    'size': row['size'],
                    'child_height': row['child_height'],
                    'child_weight': row['child_weight'],
                    'child_foot_size': row['child_foot_size'],
                    'child_id': row['child_id'],
                    'min_weight': row['min_weight'],
                    'max_weight': row['max_weight'],
                    'min_height': row['min_height'],
                    'max_height': row['max_height'],
                })

                # Find the child object in the user.children list that matches the relationship
                child = next(child for child in user.children if child.id == row['child_id'])
                # Attach the child to the found object 
                child.suggestions.append(suggestion)
        
        print(f'GETTING USERS with children sending back {user}')
        # return the user with children and suggestions attached
        return user
    
    @classmethod
    def create_user(cls, data):
        data['password'] =  bcrypt.generate_password_hash(data['password'])
        query = '''
                INSERT INTO users
                (name, email, password)
                VALUES
                (%(name)s, %(email)s, %(password)s);
                '''
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_user_with_email(cls, email):
        print('GETTING USER WITH EMAIL')
        query = '''
                SELECT * FROM users
                WHERE email = %(email)s;
                '''
        results = connectToMySQL(cls.db).query_db(query, {'email': email})
        if len(results) < 1:
            return False
        else:
            user = cls(results[0])
            print(f'GETTING USERS sending back {user}')
        return user
    
        #validate registration form information
    
    @staticmethod
    def validate_user(data):
        # Set is_valid to true as default
        is_valid = True

        #validate name
        #length
        print('VALIDATING')
        if len(data['name'])<2:
            if len(data['name'])<1:
                flash('Name field must be filled', 'registration')
                is_valid = False
            else:
                flash('Name field must be more than 2 characters', 'registration')
                is_valid = False
        
        #validate email
        #length
        if len(data['email'])<1:
            flash('email field must be filled', 'registration')
            is_valid = False
        
        #format
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email format', 'registration')
            print('\n EMAIL FORMAT FAILED\n')
            is_valid = False
        
        #unique
        if User.get_user_with_email(data['email']):
            flash('Email not unique, please provide another', 'registration')
            is_valid = False

        #validate password
        #length
        if len(data['password'])<8:
            if len(data['password'])<1:
                flash('Password name field must be filled', 'registration')
                is_valid = False
            else:
                flash('Password name field must be more than 8 characters', 'registration')
                is_valid = False
        #FORMAT
        # if not PASSWORD_REGEX.match(data['password']):
        #     flash('Invalid Password format', 'registration')
        #password match
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match', 'registration')
            is_valid = False
        
        print(is_valid)
        return is_valid

