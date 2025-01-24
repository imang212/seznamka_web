from sql_db import Connect
from datetime import datetime

#publisher
class Like_notifier:
    def __init__(self):
        self.observers = []
        self.state = 1
            
    def like(self, observer):
        self.observers.append(observer)
    
    def delike(self, observer):
        self.observers.remove(observer)
    
    def set_user_state(self, _state):
        self.state = _state

    def notify(self, user1: int, user2: int, message: str):
        state = self.state
        if state == 1:
            for observer in self.observers:
                observer.Update(self, user1, user2, message, state)

#observer (subscriber)
class User_Notification:
    def Update(self, user1, user2, message, state):
        #zápis do databáze
        db = Connect("dbuser","dbpwd","postgres","postgres")
        #Connect.reset_instance("fdsfsd","dsfaS")
        db = Connect("fwefwe","zwqdw","frefwe","dfeoeo") #instance se špatných uživatelem a heslem
        #uzivatel by mel dostat informaci
        if state == 1:
            db.Vloz_do_db(table_name='Notification',params={'user_id1': user1,'user_id2': user2, 'date': datetime.now(),'message': message})
            return db

#testing
#if __name__ == "__main__":
#    #udělám si proměnnou pro třídu (publisher)
#    like_notifier = Like_notifier()
#    #přidám třídu notifikace d publishera k dané operaci like/delike 
#    like_notifier.like(User_Notification())
#    #informuji o tom uživatele
#    like_notifier.notify(1,2) #sem vložím id liker a id uživatele kterému dal like
#    like_notifier.delike(User_Notification())