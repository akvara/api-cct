from app import db
from .user import User

class Restaurant(db.Model):

    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    menus = db.relationship('Menu', order_by='Menu.id', cascade="all, delete-orphan")
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name):
        """initialize with name."""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Restaurant.query.all()

    def __repr__(self):
        return "<Restaurant: {}>".format(self.name)

class Menu(db.Model):

    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    for_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    restaurant_id = db.Column(db.Integer, db.ForeignKey(Restaurant.id))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    restaurant = db.relationship("Restaurant")

    def __init__(self, restaurant_id, for_date, text):
        self.restaurant_id = restaurant_id
        self.for_date = for_date
        self.text = text

    def save(self):
        db.session.add(self)
        db.session.commit()

    def replace(self):
        db.session.commit()


class Vote(db.Model):

    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    for_menu = db.Column(db.Integer)
    for_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    user = db.relationship("User")

    def __init__(self, user_id, for_date, for_menu):
        self.user_id = user_id
        self.for_date = for_date
        self.for_menu = for_menu

    @staticmethod
    def get_all():
        return Vote.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def replace(self):
        db.session.commit()
