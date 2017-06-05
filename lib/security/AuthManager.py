from passlib.hash import argon2
from pymongo import MongoClient
from flask import flash

from security_utils import secure_hash_password

class AuthManager:

    def __init__(self):
        client = MongoClient()
        self.db = client['schedule_login']

    def is_registered(self, username):
        result = self.db.users.find_one({
            'username': username
        })

        return bool(result)

    def is_admin(self, username):
        result = self.db.admins.find_one({
            'username': username
        })

        return bool(result)

    def is_developer(self, username):
        result = self.db.developers.find_one({
            'username': username
        })

        return bool(result)

    def register(self, username, password, confirm_password):
        if password != confirm_password:
            return False, 'Passwords do not match.'
        elif self.is_registered(username):
            return False, 'User already exists.'
        else:
            self.db.users.insert_one({
                'username': username,
                'passhash': secure_hash_password(password)
            })

            print("Registered " + username + " with password " + password)

            return True, 'Successfully registered!'

    def login(self, username, password):
        result = self.db.users.find_one({
            'username': username
        })

        if not result:
            return False, 'User does not exist.'

        hashed_password = result.get('passhash')

        if result and argon2.verify(password, hashed_password):
            return True, 'Successfully logged in!'
        else:
            return False, 'Invalid username or password.'

    def change_pass(self, username, old_pass, new_pass, conf_new_pass):

        if new_pass != conf_new_pass:
            return False, 'Passwords do not match.'

        result = self.db.users.find_one({
            'username': username,
        })

        if not result:
            return False, 'Incorrect password.'

        self.db.users.update_one({'username': username}, {
            '$set': {'passhash': secure_hash_password(new_pass)}
        })

        flash("Password successfully changed!")

        return True, 'Password successfully updated!'


    def drop_user(self, username):
        if not self.is_registered(username):
            return False, 'User does not exist.'
        else:
            self.db.users.remove({
                'username': username
            })

            self.drop_admin(username)
            self.drop_developer(username)

            return True, 'User dropped!'

    def make_admin(self, username):
        if not self.is_registered(username):
            return False, 'User does not exist.'
        elif self.is_admin(username):
            return False, 'User is already an admin.'
        else:
            self.db.admins.insert_one({
                'username': username
            })

            return True, 'User is now an admin!'

    def drop_admin(self, username):
        if not self.is_registered(username):
            return False, 'User does not exist.'
        elif not self.is_admin(username):
            return False, 'User is not an admin.'
        else:
            result = self.db.admins.remove({
                'username': username
            })

            return True, 'Admin dropped!'

    def make_developer(self, username):
        if not self.is_registered(username):
            return False, 'User does not exist.'
        elif self.is_developer(username):
            return False, 'User is already a developer.'
        else:
            self.db.developers.insert_one({
                'username': username,
            })

            self.make_admin(username)
            return True, 'User is now a developer!'

    def drop_developer(self, username):
        if not self.is_registered(username):
            return False, 'User does not exist.'
        elif not self.is_developer(username):
            return False, 'User is not a developer.'
        else:
            self.db.developers.remove({
                'username': username
            })

            return True, 'Developer dropped!'

db_manager = AuthManager()
