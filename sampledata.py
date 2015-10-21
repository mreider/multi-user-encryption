# -*- coding: utf-8 -*-
from dbmanager import Database,User
from crypto import generate_key,Encrypter

def load_sample_data():
    """
    This will load sample data. The following users are created:
    Root / password
    Jim / bunny
    Bill / gopher

    :return:
    """
    db = Database()
    db.start_engine()

    content_key = generate_key()
    user1_key = generate_key()
    content_key_encrypted = Encrypter(user1_key).encrypt(content_key)
    user1 = User(username='Root',password='password',content_key=content_key_encrypted,encrypt_key=user1_key)

    db.session.add(user1)
    user2_key = generate_key()
    content_key_encrypted = Encrypter(user2_key).encrypt(content_key)
    user2 = User(username='Jim',password='bunny',content_key=content_key_encrypted,encrypt_key=user2_key)
    db.session.add(user2)
    user3_key = generate_key()
    content_key_encrypted = Encrypter(user3_key).encrypt(content_key)
    user3 = User(username='Bill',password='gopher',content_key=content_key_encrypted,encrypt_key=user3_key)
    db.session.add(user3)
    db.session.commit()

if __name__ == '__main__':
    load_sample_data()