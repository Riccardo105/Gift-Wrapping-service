import sqlite3
import uuid

#  The UserAccount is responsible for writing itself on the database
class UserAccount:
    def __init__(self):
        self.account_number = None
        self.username = None
        self.password = None
        self.user_credentials = None
        self.user_address = None

    def upload_credentials(self):
        self.account_number = uuid.uuid4()
        pass

    def upload_address(self):
        pass


# a credential class is created to reflect the database structure
class Credentials:
    def __init__(self):
        self.name = None
        self.surname = None
        self.DoB = None
        self.email = None
        self.phone_number = None


# an address class is created to reflect the database structure
class Address:
    def __init__(self):
        self.house_number = None
        self.street = None
        self.postcode = None
        self.city = None
