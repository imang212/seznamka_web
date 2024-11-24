from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify
from sql_db import Vloz_do_db, Vrat_data_z_db
from graph_db import Add_profile_neo, Vrat_pocet_profilu, Vytvor_profil_Node, Pridej_obrazek
from redis import Redis
from bson import json_util
import os, bcrypt, base64

redis = Redis(host="redis", port=6379)
app = Flask(__name__)
app.secret_key = os.urandom(32)


def Vytvor_profil(jmeno,prijmeni,pohlavi,prezdivka,email,telefon,heslo,vek,orientace,konicky,popis):
    node_id = Vrat_pocet_profilu()
    hash_pass = bcrypt.hashpw(heslo.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    #Vytvor_profil_db(node_id,jmeno,prijmeni,email,telefon,uzivatelske_jmeno,hash_pass) #pridam ucet do normalni db
    Add_profile_neo(node_id,jmeno,prijmeni,pohlavi,prezdivka,telefon,email,hash_pass,vek,orientace,konicky,popis) #vytvorim profil v grafove databazi

Vytvor_profil("Patrik","Poklop","m","imang21","pokloppatrik@gmail.com",702742701,"patrik123",23,"H",["sport","posilovani"],"Ahoj já jsem Patrik")
Vytvor_profil("Tomas","Omacka","ž","tomasek123","tomasek@gmail.com",546895962,"tomas123",19,"H",["hrani","pc"],"Ahoj, já jsem tomas.")

@app.route('/')
@app.route('/main')
def main():
    return render_template("main.html")

@app.route("/login",methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['firstname']
        lastname = request.form['lastname']
        nickname = request.form['nickname']
        email = request.form['email']
        heslo = request.form['password']
        heslo_znovu = request.form['password_again']
        datum_narozeni = request.form['datum_narozeni']
        pohlavi=request.form.get("typ_pohlavi")
        orientace=request.form.get("orientace")
        konicky=request.form.getlist("konicky")        
        popis=request.form["popis"]       
        if 'souhlas' in request.form: print("yes")
        else: print("no")
    return render_template("register.html")

@app.route("/browse",methods=['GET'])
def browse():
    return render_template("browse.html")

@app.route("/onas")
def onas():
    return render_template("onas.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
