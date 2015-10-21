# -*- coding: utf-8 -*-
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.ext.declarative.api import declarative_base

from crypto import Encrypter,generate_key



class Database:
    """
    Database connection manager. SQL Alchemy ORM.
    If the tables don't exist, it will generate them.
    """

    def __init__(self, database_path='db.sqlite3'):
        self.database = database_path
        self.start_engine()

    #         self.clear_all_tables()

    def start_engine(self):
        """
        Starts the DB session.
        :return:
        """
        # CONNECT
        self.engine = create_engine('sqlite:///' + self.database, echo=False)
        self.connection = self.engine.connect()

        # Create Session for sqlalchemy ...
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    def clear_all_tables(self):

        for table in reversed(self.meta.sorted_tables):
            self.connection.execute(table.delete())
        self.session.commit()

    def connection_close(self):
        self.connection.close()

    def define_tables(self):

        """ Create tables if they do not exist. """
        self.meta.create_all(self.engine)

    def save_data(self, data, username, password):
        """
         Saves the data encrypted.
         Encryption key is common but decrypted by user key
        :param data:
        :param username:
        :param password:
        :return:
        """
        user = self.session.query(User).filter(User.username == username, User.password == password).first()
        if user:
            print 'Before decryption %s' % user.content_key
            content_key = Encrypter(user.encrypt_key).decrypt(user.content_key)
            print 'Content Key = %s' % content_key
            encrypted_text = Encrypter(content_key).encrypt(data)
            content = self.session.query(Data).first()
            if content:
                content.data = encrypted_text
            else:
                d = Data(data=encrypted_text)
                self.session.add(d)
            self.session.commit()
        else:
            return "Erro:No user found"

    def get_data(self, username, password):
        """
        Based on the user passed , user key is retrived
        Using the userkey content key is decrypted and used to decrypt the content.
        :param username:
        :param password:
        :return:
        """
        content = self.session.query(Data).first()
        if content:
            user = self.session.query(User).filter(User.username == username, User.password == password).first()
            if user:
                content_key = Encrypter(user.encrypt_key).decrypt(user.content_key)
                decrypted_text = Encrypter(content_key).decrypt(content.data)
                return decrypted_text
            else:
                return "Error : No user found"
        else:
            return "Error : Not content found"

    def rotate_data(self,username,password):
        """
        This will clear all existing user key and content keys. Will generate new keys and
        encrypt data based on the new keys.
        :param username:
        :param password:
        :return:
        """
        content = self.session.query(Data).first()
        user = self.session.query(User).filter(User.username == 'Root', User.password == password).first()
        if user:
            content_key = Encrypter(user.encrypt_key).decrypt(user.content_key)
            decrypted_text = Encrypter(content_key).decrypt(content.data)
            new_content_key = generate_key()
            content.data = Encrypter(new_content_key).encrypt(decrypted_text)
            for user in self.session.query(User).all():
                new_key = generate_key()
                content_key_enc = Encrypter(new_key).encrypt(new_content_key)
                user.content_key = content_key_enc
                user.encrypt_key = new_key

            self.session.commit()
            return 'Success : Keys and data is rotated successfully.'
        else:
            return 'Error : Root user password not match.'


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    username = Column(String, primary_key=True)
    password = Column(String)
    content_key = Column(String)
    encrypt_key = Column(String)


class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    data = Column(String)
