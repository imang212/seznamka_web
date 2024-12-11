from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify, session
from sql_db import Connect
from graph_db import Add_profile_neo, Vrat_pocet_profilu, Vytvor_profil_Node, Kontrola_existence_profilu, Vrat_uzivatele_podle_id, Vrat_prihlasovaci_udaje, Pridej_fotku_data, Pridej_fotku
from redis import Redis
from bson import json_util
import os, bcrypt, datetime
from flask_login import LoginManager, login_user, logout_user,current_user
import user_model
from werkzeug.utils import secure_filename

redis = Redis(host="redis", port=6379)
app = Flask(__name__)
app.secret_key = os.urandom(32)

login_manager = LoginManager()
login_manager.init_app(app)

def Vytvor_profil(jmeno,prijmeni,pohlavi,email,heslo,vek,orientace,konicky,popis):
    node_id = Vrat_pocet_profilu()
    #Vytvor_profil_db(node_id,jmeno,prijmeni,email,telefon,uzivatelske_jmeno,hash_pass) #pridam ucet do normalni db
    Add_profile_neo(node_id,jmeno,prijmeni,pohlavi,email,bcrypt.hashpw(heslo.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),vek,orientace,konicky,popis) #vytvorim profil v grafove databazi
#Vytvor_profil("Patrik","Poklop","m","pokloppatrik@gmail.com","patrik123",23,"H",["sport","posilovani"],"Ahoj já jsem Patrik")
#Vytvor_profil("Tomas","Omacka","ž","tomasek@gmail.com","tomas123",19,"H",["hrani","pc"],"Ahoj, já jsem tomas.")


@login_manager.user_loader
def loader_user(email):
    if email is not None:
        user_data = Vrat_uzivatele_podle_id(email) #komunikace s db
        return user_model.User(email=user_data['email'],node_id=user_data['node_id'],name=user_data['name'],surname=user_data['surname'],pohlavi=user_data['pohlavi'],vek=user_data['age'],orientace=user_data['orientace']) #uložím do třídy
    return None

@app.route('/')
@app.route('/main')
def main():
    return render_template("main.html")

@app.route("/login",methods=['GET', 'POST'])
def login(): 
    error = None
    if request.method == 'POST':
        email = request.form['email']; heslo = request.form['password']
        user_data = Vrat_prihlasovaci_udaje(email)
        if not user_data: error = "Zadaná emailová adresa neexistuje nebo není zaregistrovaná"
        elif not bcrypt.checkpw(heslo.encode('utf-8'), user_data['heslo'].encode('utf-8')): error = "Vaše heslo je špatný."
        else:
            session['user_id'] = user_data['node_id'] #vytvořím session
            login_user(user_model.User(email=user_data['email'],node_id=user_data['node_id'],name=user_data['name'],surname=user_data['surname'],pohlavi=user_data['pohlavi'],vek=user_data['age'],orientace=user_data['orientace']))
            return redirect(url_for("home"))
    return render_template("login.html",error=error)
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
@app.route('/debug')
def debug():
    return f"Authenticated: {current_user.is_authenticated}, User: {current_user.get_id()}"
@app.route("/register", methods=['GET','POST'])
def register():
    error, success = None, None
    if request.method == 'POST':        
            name = request.form['firstname']; lastname = request.form['lastname']; email = request.form['email']
            heslo = request.form['password']; heslo_znovu = request.form['password_again']
            datum_narozeni = request.form['datum_narozeni']; year,month,day = map(int, datum_narozeni.split("-")); today = datetime.date.today(); age = today.year - year - ((today.month, today.day) < (month, day))
            pohlavi=request.form.get("typ_pohlavi"); orientace=request.form.get("orientace")
            konicky=request.form.getlist("konicky"); popis=request.form["popis"]
            if Kontrola_existence_profilu(email): error = "Účet s tímto emailem již existuje."; return render_template("register.html",error=error)       
            elif len(konicky)<3: error = "Musíte mít vybrené minimálně 3 koníčky."; return render_template("register.html",error=error)
            elif age < 18: error = "Musíte být straší 18 let"; return render_template("register.html",error=error)
            elif heslo != heslo_znovu: error = "Vaše hesla se neshodují"; return render_template("register.html",error=error)
            elif 'souhlas' not in request.form: error = "Musíte souhlasit s podmínkami"; return render_template("register.html",error=error)
            else: 
                error,success = None, "Úspěšně jste se zaregistroval!"
                Vytvor_profil(name,lastname,pohlavi,email,heslo,datum_narozeni,orientace,konicky,popis)
                return render_template("register.html",success=success)
    return render_template("register.html")
def success():
    ...
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/browse",methods=['GET'])
def browse():
    return render_template("browse.html")
@app.route("/profil",methods=['GET'])
def profil():
    #photos = []
    #for file in user.files:
    #    base64_photo = base64.b64encode(file.file_data).decode('utf-8')
    #    mimetype = "jpeg" if file.file_name.lower().endswith('.jpg') else "png"
    #    photos.append({'base64_photo': base64_photo, 'mimetype': mimetype})
    return render_template("profil.html")
# setter který patří k stránce profil
@app.route('/update_image', methods=['POST'])
def update_image(): #načte data z jsonu
    photo_error,photo_success = None,None
    if 'photo' not in request.files: photo_error="No file uploaded" 
    photo = request.files['photo']; datafile = photo.read() #fotku si uložím jenom do databáze
    if photo.filename == '': photo_error="No selected file"
    if photo.mimetype not in ['image/png', 'image/jpeg', 'image/jpg']: photo_error="Invalid file type"
    result = Pridej_fotku_data(session['user_id'],image_file=datafile)
    if result: photo_success="Fotka byla úspěšně nahraná."
    else: photo_error="Chyba při nahrání fotky"
    return render_template("profil.html",photo_error=photo_error,photo_success=photo_success)

@app.route("/profiles",methods=['GET'])
def profiles():
    return render_template("profiles.html")
@app.route("/likes",methods=['GET'])
def likes():
    return render_template("likes.html")


@app.route("/onas")
def onas():
    return render_template("onas.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
