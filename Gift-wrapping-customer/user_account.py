import sqlite3


#  The UserAccount is responsible for writing itself on the database
class UserAccount:
    def __init__(self):
        self.username = None
        self.password = None
        self.credentials = None
        self.address = None
        self.foreign_key_user_id = None

    # current user_id is retrieved to be used as the foreign key
    def retrieve_credentials_id(self):
        conn = sqlite3.connect('../Gift wrapping database.db')
        cur = conn.cursor()
        # it takes in the current credentials being set by the user to assign the correct id to the foreign key
        cur.execute("SELECT user_id FROM user_credentials WHERE email= ? ",
                    (self.credentials.email,))
        result = cur.fetchone()
        self.foreign_key_user_id = result[0]
        conn.close()
        return self.foreign_key_user_id

    # the email is being used as username
    def retrieve_username(self):
        conn = sqlite3.connect('../Gift wrapping database.db')
        cur = conn.cursor()
        # it takes in the current credentials being set by the user to assign the correct username
        cur.execute("SELECT email FROM user_credentials WHERE user_id= ? ",
                    (self.foreign_key_user_id,))
        result = cur.fetchone()
        self.username = result[0]
        conn.close()
        return self.foreign_key_user_id

    def upload_account(self):
        conn = sqlite3.connect('../Gift wrapping database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO user_account (user_id, username, password) VALUES (?, ?, ?)",
                    (self.foreign_key_user_id, self.username, self.password))
        conn.commit()
        conn.close()


# a credential class is created to reflect the database structure
class Credentials:
    def __init__(self):
        self.name = None
        self.surname = None
        self.DoB = None
        self.email = None
        self.phone_number = None
        self.foreign_key_address_id = None

    # current address_id is retrieved to be used as the foreign key
    def retrieve_address_id(self, address_object):
        conn = sqlite3.connect('../Gift wrapping database.db')
        cur = conn.cursor()

        # it takes in the current address being set by the user to assign the correct id to the foreign key
        cur.execute("SELECT address_id FROM user_address WHERE postcode = ? AND house_number = ? "
                    "AND street = ? AND city = ? ",
                    (address_object.postcode, address_object.house_number, address_object.street, address_object.city))
        result = cur.fetchone()
        self.foreign_key_address_id = result[0]
        conn.close()
        return self.foreign_key_address_id

    def upload_credentials(self):
        conn = sqlite3.connect("../Gift wrapping database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO user_credentials (name, surname, dob, email, phone_number, address_id) "
                    "VALUES (?,?,?,?,?,?)",
                    (self.name, self.surname, self.DoB, self.email, self.phone_number, self.foreign_key_address_id))
        conn.commit()
        conn.close()


# an address class is created to reflect the database structure
class Address:
    def __init__(self):
        self.house_number = None
        self.street = None
        self.postcode = None
        self.city = None

    def upload_address(self):
        conn = sqlite3.connect("../Gift wrapping database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO user_address (postcode, house_number, street, city) VALUES (?,?,?,?)",
                    (self.postcode, self.house_number, self.street, self.city))
        conn.commit()
        conn.close()
