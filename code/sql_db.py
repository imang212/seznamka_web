from sqlalchemy import create_engine,Table,MetaData,select,Column,Integer,String


def Vrat_profil_z_db():
    db = create_engine('postgresql+psycopg2://dbuser:dbpwd@postgres:5432/postgres')
    metadata_obj=MetaData()
    uzivatele_table = Table('Uzivatel', metadata_obj, autoload_with=db)
    with db.connect() as conn:
        result = conn.execute(uzivatele_table.select()).fetchall()
    return result

def Vytvor_profil_db(id,jmeno,prijmeni,email,telefon,heslo):
    profil = {'id':id,'jmeno': jmeno, 'prijmeni': prijmeni, 'email': email, "telefon": telefon,"heslo": heslo}
    db = create_engine('postgresql+psycopg2://dbuser:dbpwd@postgres:5432/postgres')
    metadata_obj=MetaData()
    uzivatele_table = Table('Uzivatel', metadata_obj, autoload_with=db)
    with db.connect() as conn:
        conn.execute(uzivatele_table.insert(), [profil])
        conn.commit()

