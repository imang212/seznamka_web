from flask_login import UserMixin
from py2neo.ogm import GraphObject, Property


class User(UserMixin,GraphObject):
    __primarykey__ = "email"
    __primarylabel__ = "name"
    email = Property()
    name = Property()
    
    def __init__(self, name, email):
        self.email = email
        self.name = name
        
    def get_id(self):
        return self.email
    
    