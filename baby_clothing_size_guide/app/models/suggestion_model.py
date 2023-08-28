from app.config.mysqlconnection import connectToMySQL


class Suggestion:
    db = 'clothing_size_guide'
    def __init__(self, data):
        self.brand = data['brand']
        self.clothing_type = data['clothing_type']
        self.size = data['size']
        self.min_weight = None
        if data['min_weight'] is not None:
            self.min_weight = data['min_weight']
        self.max_weight = None
        if data['max_weight'] is not None:
            self.max_weight = data['max_weight']
        self.min_height = None
        if data['min_height'] is not None:
            self.min_height = data['min_height']
        self.max_height = None
        if data['max_height'] is not None:
            self.max_height = data['max_height']
        self.child_height = data['child_height']
        self.child_weight = data['child_weight']
        self.child_foot_size = data['child_foot_size']
        self.child_id = data['child_id']
    
    @classmethod
    def save_suggestion(cls, data):
        query = '''
                INSERT INTO suggestions (brand, clothing_type, size, min_weight, max_weight, min_height, max_height, child_height, child_weight, child_foot_size, child_id )
                VALUES (%(brand)s, %(clothing_type)s, %(size)s, %(min_weight)s, %(max_weight)s, %(min_height)s, %(max_height)s, %(child_height)s, %(child_weight)s, %(child_foot_size)s, %(child_id)s );
                '''
        return connectToMySQL(cls.db).query_db(query, data)
        
    @classmethod
    def get_search_suggestions(cls, data):
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
        suggestions = []
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
                suggestions.append(cls(info))
        return suggestions
    
    # @classmethod
    # def get_search_suggestions_for_height(cls, data):
    #     query = '''
    #             SELECT * 
    #             FROM size_guides
    #             WHERE height_min < %(height)s
    #             AND height_max > %(height)s;
    #             '''
    #     results = connectToMySQL(cls.db).query_db(query,data)
    #     suggestions = []
    #     for row in results:
    #         if row is not None:
    #             info = {
    #                 'brand': row['brand'],
    #                 'clothing_type': row['clothing_type'],
    #                 'size': row['size'],
    #                 'min_weight': row['weight_min'],
    #                 'max_weight': row['weight_max'],
    #                 'min_height': row['height_min'],
    #                 'max_height': row['height_max'],
    #                 'child_id': data['child_id'],
    #                 'child_height': data['height'],
    #                 'child_weight': data['weight'],
    #                 'child_foot_size': data['foot_size'],
    #                 'match_type': 'height'
    #             }
    #             Suggestion.save_suggestion(info)
    #             suggestions.append(cls(info))
    #     return suggestions
    
    # @classmethod
    # def get_search_suggestions_for_weight(cls, data):
    #     query = '''
    #             SELECT * 
    #             FROM size_guides
    #             WHERE weight_min < %(weight)s
    #             AND weight_max > %(weight)s;
    #             '''
    #     results = connectToMySQL(cls.db).query_db(query,data)
    #     suggestions = []
    #     for row in results:
    #         if row is not None:
    #             info = {
    #                 'brand': row['brand'],
    #                 'clothing_type': row['clothing_type'],
    #                 'size': row['size'],
    #                 'min_weight': row['weight_min'],
    #                 'max_weight': row['weight_max'],
    #                 'min_height': row['height_min'],
    #                 'max_height': row['height_max'],
    #                 'child_id': data['child_id'],
    #                 'child_height': data['height'],
    #                 'child_weight': data['weight'],
    #                 'child_foot_size': data['foot_size'],
    #                 'match_type': 'weight'
    #             }
    #             Suggestion.save_suggestion(info)
    #             suggestions.append(cls(info))
    #     return suggestions

