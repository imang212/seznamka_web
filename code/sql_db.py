from sqlalchemy import create_engine,Table,MetaData,select,Column,Integer,String

def Vrat_data_z_db(table_name: String):
    db = create_engine('postgresql+psycopg2://dbuser:dbpwd@postgres:5432/postgres')
    metadata_obj=MetaData()
    table = Table(table_name, metadata_obj, autoload_with=db)
    with db.connect() as conn:
        result = conn.execute(table.select()).fetchall()
    return result

def Vloz_do_db(table_name: String, params: dict):
    #profil = {'id':id,'jmeno': jmeno, 'prijmeni': prijmeni, 'email': email, "telefon": telefon,"heslo": heslo}
    db = create_engine('postgresql+psycopg2://dbuser:dbpwd@postgres:5432/postgres')
    metadata_obj=MetaData()
    table = Table('Uzivatel', metadata_obj, autoload_with=db)
    with db.connect() as conn:
        conn.execute(table.insert(), [params])
        conn.commit()

