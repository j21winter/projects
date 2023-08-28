import re
from app.config.mysqlconnection import connectToMySQL
from app import app
from flask import flash 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

from app.models import child_model

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
        query = '''
                SELECT * FROM users
                LEFT JOIN children on users.id = children.user_id
                WHERE users.id = %(id)s;
                '''
        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        user = cls(results[0])
        for row in results:
            if 'children.id' in row and row['children.id'] is not None:
                user.children.append(child_model.Child( {
                    'id': row['children.id'],
                    'name': row['children.name'],
                    'height': row['height'],
                    'weight': row['weight'],
                    'foot_size': row['foot_size'],
                    'created_at': row['children.created_at'],
                    'updated_at': row['children.updated_at'],
                    'user_id': row['user_id'],
                }))
        print(user.children)
        print(f'GETTING USERS with children sending back {user}')
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

    # @classmethod
    # def data_upload(cls):
    #     # data = .....
    #     query = '''
    #             INSERT INTO size_guides (brand, clothing_type, size, weight_min, weight_max, height_min, height_max)
    #             VALUES (%(brand)s, %(clothing_type)s, %(size)s, %(weight_min)s, %(weight_max)s, %(height_min)s, %(height_max)s);
    #             '''
    #     data = {}
    #     for clothes_type in guide:
    #         data['brand'] = 'gerber'
    #         data['clothing_type'] = clothes_type
    #         for size in guide[clothes_type]:
    #             data['size'] = size
    #             weight = guide[clothes_type][size]['weight']
    #             height = guide[clothes_type][size]['height']
    #             if 'min' in weight:
    #                 data['weight_min'] = weight['min']
    #             else:
    #                 data['weight_min'] = 0
    #             if 'max' in weight:
    #                 data['weight_max'] = weight['max']
    #             # else:
    #             #     data['weight_max'] = 'none'
    #             if 'min' in height:
    #                 data['height_min'] = height['min']
    #             else:
    #                 data['height_min'] = 0
    #             if 'max' in height:
    #                 data['height_max'] = height['max']
    #             # else:
    #             #     data['height_max'] = 'none'
    #             connectToMySQL(cls.db).query_db(query, data)
    #     return guide

