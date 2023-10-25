from app.config.mysqlconnection import connectToMySQL
from app.models import suggestion_model

class Child:
    db = 'clothing_size_guide'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.date_of_birth = data['date_of_birth']
        self.height = data['height']
        self.weight = data['weight']
        self.foot_size = data['foot_size']
        self.parent = data['user_id']
        self.suggestions = []

    @classmethod
    def create_child(cls, data):
        query = '''
                INSERT INTO children
                (name, date_of_birth, height, weight, foot_size, user_id)
                VALUES
                (%(child_name)s, %(date_of_birth)s, %(child_height)s, %(child_weight)s, %(child_sole_length)s, %(user_id)s);
                '''
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update_child(cls, data):
        query = '''
        UPDATE children 
        SET name = %(name)s, date_of_birth = %(date_of_birth)s, height = %(height)s, weight = %(weight)s, foot_size = %(sole_length)s
        WHERE children.id = %(id)s;
        '''
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_one_by_id(cls, id):
        query = '''
                SELECT *
                FROM children
                LEFT JOIN suggestions on children.id = suggestions.child_id
                WHERE children.id = %(id)s
                '''
        result = (connectToMySQL(cls.db).query_db(query, {'id': id}))
        child = cls(result[0])
        for row in result:
            child.suggestions.append(suggestion_model.Suggestion({
            'id': row['suggestions.id'],
            'brand': row['brand'],
            'clothing_type': row['clothing_type'],
            'size': row['size'],
            'min_weight': row['min_weight'],
            'max_weight': row['max_weight'],
            'min_height': row['min_height'],
            'max_height': row['max_height'],
            'child_height': row['child_height'],
            'child_weight': row['child_weight'],
            'child_foot_size': row['child_foot_size'],
            'created_at': row['suggestions.created_at'],
            'child_id': row['child_id'],
            }))
        return child
    
    @classmethod
    def delete_child(cls, id):
        query = '''
                DELETE
                FROM children
                WHERE id = %(id)s'''
        return (connectToMySQL(cls.db).query_db(query, {'id': id}))



