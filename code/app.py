from flask import Flask, render_template, request, redirect, url_for, flash, session
from graph_db import Add_profile_neo, Vrat_pocet_profilu, Kontrola_existence_profilu, Vrat_uzivatele_podle_id, Vrat_prihlasovaci_udaje, Pridej_fotku_data, Pridej_popis, Zmen_konicky, Vrat_vsechny_profily, Like_profile, get_user_likes, delete_like
from redis import Redis
import os, bcrypt, datetime
from flask_login import LoginManager, login_user, logout_user,current_user
import user_model
from image_decoder import Image_decoder
from like_notifier import Like_notifier, User_Notification
from sql_db import Connect

redis = Redis(host="redis", port=6379)
app = Flask(__name__)
app.secret_key = os.urandom(32)

app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=1)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

def Vytvor_profil(jmeno,prijmeni,pohlavi,email,heslo,vek,orientace,konicky,popis):
    node_id = Vrat_pocet_profilu()+1
    #Vytvor_profil_db(node_id,jmeno,prijmeni,email,telefon,uzivatelske_jmeno,hash_pass) #pridam ucet do normalni db
    Add_profile_neo(node_id,jmeno,prijmeni,pohlavi,email,bcrypt.hashpw(heslo.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),vek,orientace,konicky,popis) #vytvorim profil v grafove databazi
#Vytvor_profil("Patrik","Poklop","m","pokloppatrik@gmail.com","patrik123",23,"H",["sport","posilovani"],"Ahoj já jsem Patrik")
#Vytvor_profil("Tomas","Omacka","m","tomasek@gmail.com","tomas123",19,"H",["hrani","pc"],"Ahoj, já jsem tomas.")


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
            if 'remember' in request.form: app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=3) 
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

@app.route("/profil",methods=['GET'])
def profil():
    #photos = []
    #for file in user.files:
    #    base64_photo = base64.b64encode(file.file_data).decode('utf-8')
    #    mimetype = "jpeg" if file.file_name.lower().endswith('.jpg') else "png"
    #    photos.append({'base64_photo': base64_photo, 'mimetype': mimetype})
    return render_template("profil.html")
# setter který patří k stránce profil
@app.route('/update_konicky', methods=['POST'])
def update_konicky(): 
    error,success = None,None
    konicky = request.form.getlist("konicky")
    if len(konicky)<3 not in request.files: error="Musíte vybrat minimálně 3 koníčky"; return render_template("profil.html",error=error)
    result = Zmen_konicky(session['user_id'],konicky)
    if result: success="Vaše koníčky byli změněny."
    else: error="Chyba při změně koníčků"
    return render_template("profil.html",error=error,success=success)

@app.route('/update_popis', methods=['POST'])
def update_popis(): 
    error,success = None,None
    popis = request.form['popis']
    result = Pridej_popis(session['user_id'],popis)
    if result: success="Popis byl změněn."
    else: error="Chyba při změně popisu"
    return render_template("profil.html",error=error,success=success)

@app.route('/update_image', methods=['POST'])
def update_image(): 
    error,success = None,None
    if 'photo' not in request.files: error="No file uploaded" 
    photo = request.files['photo']; datafile = photo.read() #fotku si uložím jenom do databáze
    if photo.filename == '': error="No selected file"
    if photo.mimetype not in ['image/png', 'image/jpeg', 'image/jpg']: error="Invalid file type"
    result = Pridej_fotku_data(session['user_id'],image_file=datafile)
    if result: success="Fotka byla úspěšně nahraná."
    else: error="Chyba při nahrání fotky"
    return render_template("profil.html",error=error,success=success)

@app.route("/profiles",methods=['GET'])
def profiles():
    users = Vrat_vsechny_profily() 
    if users: return render_template("profiles.html",users=users,image_format=Image_decoder(None).commit_format,age_formater=user_model.Account_info_format.age_formater,get_user_likes=get_user_likes)

@app.route('/like/<int:user_node_id>/<int:node_id>/<name>/<liker_name>', methods=['GET'])
def like_profile(user_node_id,node_id,name,liker_name):
    session.pop('_flashes', None)
    if not user_node_id: render_template("profil.html")
    likers = get_user_likes(user_node_id)
    if node_id not in likers: 
        olajkuj = Like_profile(user_node_id,node_id)
        if olajkuj:
            #informuji o tom uživatele pomocí Notifikace
            like_notifier = Like_notifier()
            like_notifier.like(User_Notification)
            like_notifier.set_user_state(1)
            like_notifier.notify(user_node_id, node_id, f"{liker_name} liked your profile!")
            flash(f"Dal jsi like profilu {name}","success")
        else: flash(f"Chyba při komunikaci se serverem","danger")
    else: flash("Profilu jste již dal like","danger")
    return redirect(url_for('profiles')) 
     

@app.route("/likes",methods=['GET'])
def likes():
    users = Vrat_vsechny_profily() 
    if users: return render_template("likes.html",users=users,image_format=Image_decoder(None).commit_format,age_formater=user_model.Account_info_format.age_formater,get_user_likes=get_user_likes)

@app.route('/remove_like/<int:user_node_id>/<int:node_id>/<name>', methods=['GET'])
def remove_like(user_node_id,node_id,name):
    session.pop('_flashes', None)
    if not user_node_id: render_template("profil.html")
    result = delete_like(user_node_id,node_id)
    if result: 
        flash(f"Profil {name} byl odebraný z liků","success")
        return redirect(url_for('likes'))
    else: flash(f"Profil {name} jste nedal like","success")
    return redirect(url_for('likes')) 

@app.route("/notifications",methods=['GET'])
def notifications():
    db = Connect("dbuser","dbpwd","postgres","postgres")
    if session.get('user_id') is not None:
        notifikace = db.Vrat_data_z_db_podle_id('Notification', session['user_id'])
        print(notifikace)
        if db: return render_template("notifications.html",notifications=notifikace)
    else:
        return render_template("notifications.html")


@app.route("/onas")
def onas():
    return render_template("onas.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
