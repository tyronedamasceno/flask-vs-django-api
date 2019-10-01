from random import choice, random, randint

from time import sleep

from flaskapi.flaskapi.models import User, Transaction


def populate():
    user1 = User(email='chico@mail.com', password='pass', doc_number='123456')
    user2 = User(email='zezin@mail.com', password='pass', doc_number='765432')
    user1.save_to_db()
    user2.save_to_db()
    ids = (user1.id, user2.id)
    for _ in range(30):
        tx = Transaction(user_id=choice(ids), value=random()*randint(1, 1000))
        tx.save_to_db()
        sleep(0.3)
