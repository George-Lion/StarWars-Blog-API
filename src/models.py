from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False, unique=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    favorites = db.relationship("Favorites", backref="user")

    def __repr__(self):
        return "user: " + self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "favorites": list(map(lambda favo: favo.serialize(), self.favorites))
    }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    character = db.relationship("Characters")
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet = db.relationship("Planets")
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    vehicle = db.relationship("Vehicles")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id     
    }
    
class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False )
    height = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(120), nullable=False)
 
    def __repr__(self):
        return "character: " + self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "gender": self.gender 
            
    }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    
    def __repr__(self):
        return "planet: " + self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "climate": self.climate
    }

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    model = db.Column(db.String(250), nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return "vehicle: " + self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "passengers": self.passengers,
            
    }
    