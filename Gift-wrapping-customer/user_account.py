
class UserAccount:
    def __init__(self, credentials, address):
        self.account_number = None
        self.username = None
        self.password = None
        self.user_credentials = credentials
        self.user_address = address


class Credentials:
    def __init__(self, name, surname, email):
        self.name = name
        self.surname = surname
        self.email = email


class Address:
    def __init__(self, house_number, street, postcode, city):
        self.house_number = house_number
        self.street = street
        self.postcode = postcode
        self.city = city
