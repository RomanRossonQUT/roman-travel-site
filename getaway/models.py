from . import db
from datetime import datetime
from flask_login import UserMixin

# Define a User class representing user data in the 'users' table
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')  # Establish a one-to-many relationship with comments

    def __repr__(self):
        return f"Name: {self.name}"

# Define a Destination class representing destination data in the 'destinations' table
class Destination(db.Model):
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    currency = db.Column(db.String(3))
    comments = db.relationship('Comment', backref='destination')  # Establish a one-to-many relationship with comments

    def __repr__(self):
        return f"Name: {self.name}"

# Define a Comment class representing comment data in the 'comments' table
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Establish a foreign key relationship with users
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))  # Establish a foreign key relationship with destinations

    def __repr__(self):
        return f"Comment: {self.text}"

# Define a Hotel class representing hotel data in the 'hotels' table
class Hotel(db.Model):
    __tablename__ = 'hotels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    description = db.Column(db.String(500))
    room_avail = db.Column(db.Boolean, default=1)
    rooms = db.relationship('Room', backref='hotel', lazy='dynamic')  # Establish a one-to-many relationship with rooms
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))  # Establish a foreign key relationship with destinations

    def to_dict(self):
        # Convert hotel data to a dictionary
        h_dict = {
            b.name: str(getattr(self, b.name)) for b in self.__table__.columns
        }
        h_rooms = []
        for room in self.rooms:
            room_data = {
                'id': room.id,
                'room_type': room.type,
                'num_rooms': room.num_rooms,
                'room_description': room.description,
                'room_rate': room.rate,
                'hotel_id': room.hotel_id
            }
            h_rooms.append(room_data)
        h_dict['rooms'] = h_rooms
        return h_dict

# Define a Room class representing room data in the 'rooms' table
class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), index=True, nullable=False)
    num_rooms = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500))
    rate = db.Column(db.Float(7))
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))  # Establish a foreign key relationship with hotels
