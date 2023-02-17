from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
db = 'project'


class Bands:
    def __init__(self,data):
        self.id = data['id']
        self.band_name = data['band_name']
        self.founding_member = data['founding_member']
        self.genre = data['genre']
        self.home_city = data['home_city']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.founding_member = ''




    @classmethod
    def create_band(cls,data):
        query = """
        INSERT INTO bands(band_name,genre,home_city,users_id)
        VALUES(%(band_name)s,%(genre)s,%(home_city)s,%(users_id)s)
        """
        return connectToMySQL(db).query_db(query,data)


    @classmethod    
    def get_one_band(cls,data):
        query="""
        SELECT * FROM bands
        WHERE id = %(id)s
        """
        results = connectToMySQL(db).query_db(query,data)
        if results:
            return cls(results[0])

    @classmethod
    def show_all_bands(cls): #use join
        query="""
        SELECT * FROM bands
        JOIN users
        ON bands.users_id = users.id
        """
        results = connectToMySQL(db).query_db(query)

        band = []
        if results:
            for row in results:
                this_band = cls(row)
                this_band.founding_member = f"{row['first_name']} {row['last_name']}"
                band.append(this_band)
            return band
        return []

    @classmethod
    def delete_band(cls,data):
        query="""
        DELETE FROM bands
        WHERE id = %(id)s
        """
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def edit_band(cls,data):
        query="""
        UPDATE bands
        SET band_name = %(band_name)s, genre = %(genre)s, home_city = %(home_city)s
        WHERE id = %(id)s
        """
        return connectToMySQL(db).query_db(query,data)
    


    @classmethod
    def my_bands(cls,data):
        query="""
        SELECT * FROM bands
        JOIN users
        ON bands.users_id = users.id
        WHERE users_id = %(id)s
        """
        results = connectToMySQL(db).query_db(query,data)
        band = []
        if results:
            for row in results:
                this_band = cls(row)
                this_band.founding_member = f"{row['first_name']} {row['last_name']}"
                band.append(this_band)
            return band
        return []
        
        







    @staticmethod
    def validate_create(create_band):
        is_valid = True
        if len(create_band['band_name']) <  3:
            flash("Band Name must be atleast 3 characters long!")
            is_valid = False
        if len(create_band['genre']) < 3:
            flash("Genre must be atleast 3 characters long!")
            is_valid = False
        if len(create_band['home_city']) < 3:
            flash("Home City must be atleast 3 characters long!")
            is_valid = False
        return is_valid

