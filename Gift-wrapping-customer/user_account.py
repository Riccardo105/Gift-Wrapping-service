import sqlite3

#  The UserAccount is responsible for writing itself on the database
class UserAccount:
    def __init__(self):

        self.username = None
        self.password = None
        self.user_credentials = None
        self.user_address = None


# a credential class is created to reflect the database structure
class Credentials:
    def __init__(self):
        self.name = None
        self.surname = None
        self.DoB = None
        self.email = None
        self.phone_number = None

    def upload_credentials(self):
        con = sqlite3.connect(r"C:\Users\User\PycharmProjects\Gift-Wrapping-service\Gift wrapping database.db")
        cur = con.cursor()


# an address class is created to reflect the database structure
class Address:
    def __init__(self):
        self.house_number = None
        self.street = None
        self.postcode = None
        self.city = None

    def upload_address(self):
        conn = sqlite3.connect("Gift wrapping database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO user_address ( postcode, house_number, street, city) VALUES (?,?,?,?)",
                    (self.house_number, self.street, self.postcode, self.city))
