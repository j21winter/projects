from app.config.mysqlconnection import connectToMySQL


class Suggestion:
    # DATA BASE NAME
    db = 'clothing_size_guide'

    #CONSTRUCTOR
    def __init__(self, data):

        self.id = data['id']

        self.brand = data['brand']

        self.clothing_type = data['clothing_type']

        self.size = data['size']

        self.child_height = data['child_height']

        self.child_weight = data['child_weight']

        self.child_foot_size = data['child_foot_size']
        
        self.child_id = data['child_id']

        # OPTIONAL ATTRIBUTES
        # TODO WORK OUT WHY WE NEED THESE IN THE CONSTRUCTOR
        #? IS IT BECAUSE OF THE RELATIONSHIP TO SUGGESTIONS AND WHAT WE ARE DISPLAYING ON THE VIEW
        self.min_weight = None
        if 'min_weight' in data:
            self.min_weight = data['min_weight']

        self.max_weight = None
        if 'max_weight' in data:
            self.max_weight = data['max_weight']

        self.min_height = None
        if 'min_height' in data:
            self.min_height = data['min_height']

        self.max_height = None
        if 'max_height' in data:
            self.max_height = data['max_height']

    
    #* SAVE A NEW SUGGESTION
    #? Added a unique index into the suggestions table to prevent duplicate rows being added.
    #? Also changed the INSERT statement to an INSERT IGNORE statement to handle duplicates gracefully.
    
    @classmethod
    def save_suggestion(cls, data):
        query = '''
                INSERT IGNORE INTO suggestions (brand, clothing_type, size, min_weight, max_weight, min_height, max_height, child_height, child_weight, child_foot_size, child_id )
                VALUES (%(brand)s, %(clothing_type)s, %(size)s, %(min_weight)s, %(max_weight)s, %(min_height)s, %(max_height)s, %(child_height)s, %(child_weight)s, %(child_foot_size)s, %(child_id)s );
                '''
        return connectToMySQL(cls.db).query_db(query, data)
    
    #* SEARCH SUGGESTIONS
    @classmethod
    def get_search_suggestions(cls, data):
        # SUB QUERIES SHOULD PREVENT DUPLICATE SUGGESTIONS
        query = '''
                SELECT * 
                FROM size_guides
                WHERE 
                (weight_min < %(weight)s AND weight_max > %(weight)s)
                OR
                (height_min < %(height)s AND height_max > %(height)s)
                OR
                (weight_min < %(weight)s AND weight_max > %(weight)s AND height_min < %(height)s AND height_max > %(height)s);
                '''
        results = connectToMySQL(cls.db).query_db(query,data)

        # SENDING BACK A LIST OF SUGGESTION OBJECTS
        suggestions = []

        # BUILDING OBJECTS AND ADDING TO LIST
        for row in results:
            if row is not None:
                info = {
                    'brand': row['brand'],
                    'clothing_type': row['clothing_type'],
                    'size': row['size'],
                    'min_weight': row['weight_min'],
                    'max_weight': row['weight_max'],
                    'min_height': row['height_min'],
                    'max_height': row['height_max'],
                    'child_id': data['child_id'],
                    'child_height': data['height'],
                    'child_weight': data['weight'],
                    'child_foot_size': data['foot_size'],
                }

                Suggestion.save_suggestion(info)

                #ADD CREATE OBJECT AND ADD TO THE LIST
                suggestions.append(cls(info))
        return suggestions



