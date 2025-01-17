from sql_db import Connect
from datetime import datetime

#publisher
class Like_notifier:
    def __init__(self):
        self.observers = []
            
    def like(self, observer):
        self.observers.append(observer)
    
    def delike(self, observer):
        self.observers.remove(observer)
    
    def notify(self, user1, user2, message):
        for observer in self.observers:
            observer.Update(self, user1, user2, message)

#observer (subscriber)
class User_Notification:
    def Update(self, user1, user2, message):
        #zápis do databáze
        db = Connect("dbuser","dbpwd")
        #Connect.reset_instance("fdsfsd","dsfaS")
        db = Connect("fwefwe","zwqdw") #instance se špatných uživatelem a heslem

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