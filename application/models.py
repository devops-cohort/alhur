from application import db, login_manager
from flask_login import UserMixin
from flask_wtf import FlaskForm
from datetime import datetime

team_maker= db.Table('actualteams',
    db.Column('pokedex_number', db.Integer, db.ForeignKey('pokedex.pokedex_number')),
    db.Column('id', db.Integer, db.ForeignKey('team.id'))
        )


class Pokedex(db.Model):
    pokedex_number = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    type1 = db.Column(db.String(8), nullable=False)
    type2 = db.Column(db.String(8))
    hp = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    sp_attack = db.Column(db.Integer, nullable=False)
    sp_defense = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer,nullable=False)
    base_stat_total = db.Column(db.Integer,nullable=False)
    abilities = db.Column(db.String(89), nullable=False)
    base_happiness = db.Column(db.Integer,nullable=False)
    experience_growth = db.Column(db.Integer, nullable=False)
    egg_steps = db.Column(db.Integer, nullable=False)
    capture_rate = db.Column(db.String(24), nullable=False)
    height_m = db.Column(db.Integer)
    classfication = db.Column(db.String(21))
    gender_ratio = db.Column(db.Integer) 
    generation = db.Column(db.Integer, nullable=False)
    is_legendary = db.Column(db.Integer,nullable=False)
    teams = db.relationship('Team',secondary = team_maker, backref=db.backref('pokemon_info'), lazy= 'dynamic')

    def __repr__(self):
        return f"[Pokedex Number: {self.pokedex_number} \r\nName: {self.name}]"

class Team(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    team_name = db.Column(db.String(20))
    Pokedex1_id = db.Column(db.Integer, db.ForeignKey('pokedex.pokedex_number'), nullable=False)
    Pokedex2_id = db.Column(db.Integer, db.ForeignKey('pokedex.pokedex_number'))
    Pokedex3_id = db.Column(db.Integer, db.ForeignKey('pokedex.pokedex_number'))
    Pokedex4_id = db.Column(db.Integer, db.ForeignKey('pokedex.pokedex_number'))
    Pokedex5_id = db.Column(db.Integer, db.ForeignKey('pokedex.pokedex_number'))
    Pokedex6_id = db.Column(db.Integer, db.ForeignKey('pokedex.pokedex_number'))
    def __repr__(self):
        return f"[Pokemon1: {self.Pokedex1_id} \r\nPokemon2: {self.Pokedex3_id} \r\nPokemon3: {self.Pokedex3_id} \r\nPokemon: {self.Pokedex4_id} \r\nPokemon5: {self.Pokedex5_id} \r\nPokemon6: {self.Pokedex6_id}]"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)

    def __repr__(self):
        return ''.join(['User: ', self.user_id, '\r\n', 'Title: ', self.title, '\r\n',self.content])

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name=db.Column(db.String(30), nullable=False)
    posts = db.relationship('Posts', backref='author',lazy=True)
    
    def __repr__(self):
        return ''.join([
            'User ID: ', str(self.id), '\r\n', 
            'Email: ', self.email, '\r\n', 
            'Name: ',self.first_name, '\r\n', ' ', self.last_name
        ])

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
