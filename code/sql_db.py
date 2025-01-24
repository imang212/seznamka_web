from sqlalchemy import create_engine,Table,MetaData
from sqlalchemy.exc import SQLAlchemyError
#pouze přes sqlalchemy bez využití ORM
class Connect:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, user: str, password: str, server_name: str, database_name: str):
        if not hasattr(self,"db"): #aby inisializace proběhla jednou
            self.user = user
            self.password = password
            self.server_name = server_name
            self.database_name = database_name
            try:
                self.db = create_engine(f'postgresql+psycopg2://{user}:{password}@{server_name}:5432/{database_name}')
            except SQLAlchemyError as e:
                raise ConnectionError(f"Připojení selhalo: {e}")

    def Vrat_data_z_db(self, table_name: str):
        metadata_obj=MetaData()
        table = Table(table_name, metadata_obj, autoload_with=self.db)
        with self.db.connect() as conn:
            result = conn.execute(table.select()).fetchall()
        return result

    def Vloz_do_db(self, table_name: str, params: dict):
        #profil = {'id':id,'jmeno': jmeno, 'prijmeni': prijmeni, 'email': email, "telefon": telefon,"heslo": heslo}
        metadata_obj=MetaData()
        table = Table(table_name, metadata_obj, autoload_with=self.db)
        with self.db.connect() as conn:
            conn.execute(table.insert(), [params])
            conn.commit()

    def Vrat_data_z_db_podle_id(self, table_name: str, to_user_id: int):
        metadata_obj=MetaData()
        table = Table(table_name, metadata_obj, autoload_with=self.db)
        with self.db.connect() as conn:
            result = conn.execute(table.select().where(table.c.user_id2 == to_user_id)).fetchall()
        return result#[dict(row) for row in result]


    #Když budu chtím změnit instanci přihlášení
    @classmethod
    def reset_instance(cls, user, password):
        cls._instance = None
        return cls(user, password)

#způsob 2  využitím ORM
#from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker
#from datetime import datetime
#
#db = declarative_base()
#
#class Notification(db):
#    __tablename__ = 'Notification'
#    #__table_args__ = {"schema": "public"}
#    id = Column(Integer, primary_key=True)
#    user_id1 = Column(Integer,nullable=False)
#    user_id2 = Column(Integer,nullable=False)
#    date = Column(DateTime, default=func.now())
#    message = Column(String(255), nullable=False)
#
#
#def Connection(username, password):
#    global engine, session
#    engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/postgres')
#    db.metadata.create_all(engine)
#    Session = sessionmaker(bind=engine)
#    session = Session()
#
#def Insert_notification(user_id1, user_id2, message):
#    try:
#        teleso = Notification(user_id1=user_id1,user_id2=user_id2,date=datetime.now(),message=message)
#        session.add(teleso)
#        session.commit()
#    except Exception as e:
#        session.rollback()
#        print(f"Error: {e}")
#    finally:
#        session.close()
#
#def Return_user_data(user_id):
#    try:
#        notification_data = session.query(Notification).where(user_id2=user_id)
#    finally:
#        return notification_data