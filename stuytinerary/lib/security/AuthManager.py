import flask
import passlib
import pymongo

import security_utils

class AuthManager:

    def __init__(self):
        client = pymongo.MongoClient()
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
                'passhash': security_utils.secure_hash_password(password)
            })

            print('Registered ' + username + ' with password ' + password)

            return True, 'Successfully registered!'

    def login(self, username, password):
        result = self.db.users.find_one({
            'username': username
        })
        if not result:
            return False, 'User does not exist.'

        hashed_password = result.get('passhash')
        if result and passlib.hash.argon2.verify(password, hashed_password):
            return True, 'Successfully logged in!'
        else:
            return False, 'Invalid username or password.'

    # TO DO: REWRITE REQUIRED
    def change_password(self, username, old_password, new_password, confirm_new_password):
        if new_password != confirmation_new_password:
            flask.flash('Sorry, your passwords do not match.')
            return False, 'Passwords do not match.'

        result = self.db.users.find_one({
            'username': username,
            'passhash': security_utils.secure_hash_password(old_password)
        })
        if not result:
            flask.flash('Password not correct.')
            return False, 'Incorrect password.'

        self.db.users.update_one({'username': username}, {
            '$set': {'passhash': security_utils.secure_hash_password(new_password)}
        })
        flask.flash('Password successfully changed!')
        return True, 'Password successfully updated!'


    def drop_user(self, username, force=False):
        if not self.is_registered(username) and not force:
            return False, 'User does not exist.'
        else:
            self.db.users.remove({
                'username': username
            })

            self.drop_admin(username, True)
            self.drop_developer(username, True)

            return True, 'User dropped!'

    def make_admin(self, username, force=False):
        if not self.is_registered(username) and not force:
            return False, 'User does not exist.'
        elif self.is_admin(username):
            return False, 'User is already an admin.'
        else:
            self.db.admins.insert_one({
                'username': username
            })

            return True, 'User is now an admin!'

    def drop_admin(self, username, force=False):
        if not self.is_registered(username) and not force:
            return False, 'User does not exist.'
        elif not self.is_admin(username):
            return False, 'User is not an admin.'
        else:
            result = self.db.admins.remove({
                'username': username
            })

            return True, 'Admin dropped!'

    def make_developer(self, username, force=False):
        if not self.is_registered(username) and not force:
            return False, 'User does not exist.'
        elif self.is_developer(username):
            return False, 'User is already a developer.'
        else:
            self.db.developers.insert_one({
                'username': username,
            })

            self.make_admin(username, force)
            return True, 'User is now a developer!'

    def drop_developer(self, username, force=False):
        if not self.is_registered(username) and not force:
            return False, 'User does not exist.'
        elif not self.is_developer(username):
            return False, 'User is not a developer.'
        else:
            self.db.developers.remove({
                'username': username
            })

            return True, 'Developer dropped!'
