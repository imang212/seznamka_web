from flask_login import UserMixin
from py2neo.ogm import GraphObject, Property
from graph_db import Vrat_fotku, Pridej_fotku_data, Vrat_konicky, Vrat_popis
from base64 import b64decode
import datetime

class User(UserMixin,GraphObject):
    __primarylabel__ = "User"
    __primarykey__ = "email"

    email = Property() #email je reprezentovaný jako key
    node_id = Property() #?name je také reprezentovaný jako key? 
    name = Property() 
    surname = Property() 
    heslo = Property()
    pohlavi = Property() #tohle se už volá jako normální property atribut s malým p, tak musím nadefinovat ještě setter před property(fset=set_name), kam bude vstupovat funkce
    vek = Property()
    orientace = Property()
    konicky = Property()
    popis = Property()
    fotka = Property()
    
    def __init__(self, email, node_id, name, surname,pohlavi,vek,orientace): #sestavím uzivatele User podle predanych informací v init, dávám jenom pevně dané informace
        self.email = email
        self.node_id = node_id
        self.name = name
        self.surname = surname
        self.pohlavi = pohlavi
        year,month,day = map(int, vek.split("-")); today = datetime.date.today(); age = today.year - year - ((today.month, today.day) < (month, day))
        self.vek = age
        self.orientace = orientace

    #settery
    def set_name(self,name): self.name = name 
    def set_surname(self,surname): self.surname = surname
    def set_vek(self,vek): self.vek = vek
    def set_pohlavi(self,pohlavi): self.pohlavi = pohlavi
    def set_popis(self,popis): self.popis = popis
    def set_orientace(self,orientace): self.orientace = orientace
    
    def set_fotka(self,new_fotka_file): 
        result = Pridej_fotku_data(self.node_id,new_fotka_file)
        if result: self.fotka = Vrat_fotku(self.node_id); return result
        return None
    
    def get_id(self): return self.email #nejsřív si ověřuji podle emailu v user_loader()
    def get_node_id(self): return self.node_id
    
    #vytvorim gettery ke kazde vlastnosti
    def get_name(self): return self.name
    def get_surname(self): return self.surname
    def get_pohlavi(self): return self.pohlavi
    def get_vek(self):  
        return self.vek
    def get_orientace(self): return self.orientace
    
    def get_konicky(self):
        konicky = Vrat_konicky(self.node_id)
        if konicky: self.konicky = konicky; return self.konicky
        return None
    
    def get_popis(self): 
        popis = Vrat_popis(self.node_id)
        if popis: self.popis = popis; return self.popis
        return None
    
    def get_fotka(self):  #!důležité! fotku si nechám dekodovovanou html img element si umí sám fotku dekodovat 
        fotka = Vrat_fotku(self.node_id) #načte fotku z databáze
        # nejdžív musím rozpoznat formát fotky abych jí mohl otevřít
        fotka_bin_format = b64decode(fotka) #dekoduji abych to mohl oznat
        if fotka_bin_format.startswith(b'\xFF\xD8\xFF'): image_format = 'image/jpeg'
        elif fotka_bin_format.startswith(b'\x89PNG\r\n\x1A\n'): image_format = 'image/png'
        elif fotka_bin_format.startswith(b'GIF8'): image_format = 'image/gif'
        else: return None
        if fotka: return {"image_format": image_format,"image_data": fotka}#vrátím dekodovana data fotky podle zkratky a binárních dat, abych je poté mohl uložit do html image
        return None
    
    


    
