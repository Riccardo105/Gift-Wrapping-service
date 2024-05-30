import sqlite3


#  The UserAccount is responsible for writing itself on the database
class UserAccount:
    def __init__(self):
        self.username = None
        self.password = None
        self.foreign_key_user_id = None

    # current user_id is retrieved to be used as the foreign key
    def retrieve_credentials_id(self, credential_object):
        conn = sqlite3.connect('Gift wrapping database.db')
        cur = conn.cursor()
        # it takes in the current credentials being set by the user to assign the correct id to the foreign key
        cur.execute("SELECT user_id FROM user_credentials WHERE email= ? ",
                    credential_object.email)
        user_id = cur.fetchone()
        self.foreign_key_user_id = user_id
        conn.close()
        return self.foreign_key_user_id

    def upload_account(self):
        pass




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
        conn = sqlite3.connect('Gift wrapping database.db')
        cur = conn.cursor()

        # it takes in the current address being set by the user to assign the correct id to the foreign key
        cur.execute("SELECT address_id FROM user_address WHERE postcode = ?, house_number = ?, street = ?, city = ? ",
                    (address_object.postcode, address_object.house_number, address_object.street, address_object))
        address_id = cur.fetchone()
        self.foreign_key_address_id = address_id
        conn.close()
        return self.foreign_key_address_id

    def upload_credentials(self):
        conn = sqlite3.connect("Gift wrapping database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO user_credentials (name, surname, dob, email, phone_number) VALUES (?,?,?,?)",
                    (self.name, self.surname, self.DoB, self.email, self.phone_number))
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
        conn = sqlite3.connect("Gift wrapping database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO user_address (postcode, house_number, street, city) VALUES (?,?,?,?)",
                    (self.house_number, self.street, self.postcode, self.city))
        conn.commit()
        conn.close()
