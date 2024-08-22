import present
import order
import user_account
import sqlite3


class OrderBuilder:
    def __init__(self):
        self.new_order = order.Order()

# the current account id is retrieved based on the log-in email to be used as the foreign key later
    def retrieve_account_id(self, username):
        conn = sqlite3.connect('../Gift wrapping database.db')
        cur = conn.cursor()
        cur.execute("SELECT account_id FROM user_account WHERE username = ?", (username,))
        result = cur.fetchone()
        conn.close()
        self.new_order.account_id = result[0]
        return self.new_order.account_id

    def set_order_dates(self, drop_off, pick_up):
        self.new_order.drop_off_date = drop_off
        self.new_order.pick_up = pick_up

        return self.new_order.drop_off_date and self.new_order.pick_up

    def calculate_total_price(self, presents: list):
        for item in presents:
            self.new_order.total_price += item.price
        return self.new_order.total_price

    def build(self):
        return self.new_order


# this is the builder responsible for creating and building the present
class PresentBuilder:
    def __init__(self):
        self.presents = []
        self.new_present = present.Present()

    # it is called by the relevant class and passes the object as the shape
    def set_shape(self, shape, *args):
        shape.calculate_area(*args)
        self.new_present.shape = shape
        return self.new_present.shape

    def set_wrapping_paper(self, w_paper: object):
        self.new_present.wrapping_paper = w_paper
        return self.new_present.gift_card

    def set_bow(self, bow: object):
        self.new_present.bow = bow
        return self.new_present.bow

    def set_gift_card(self, gift_card: object):
        self.new_present.gift_card = gift_card
        return self.new_present.gift_card

    def calculate_price(self):
        # checks for the presence of a bow otherwise the cost is set to 0
        if self.new_present.bow is None:
            bow_price = 0
        else:
            bow_price = self.new_present.bow.price
        # checks for the presence of a gift card otherwise the cost is set to 0
        if self.new_present.gift_card is None:
            gift_card_price = 0
        else:
            gift_card_price = self.new_present.gift_card.price
        # NOTE: paper's price must be converted to pound format before adding bow and gift card and bow price
        total_price = round(self.new_present.shape.area * self.new_present.wrapping_paper.price / 100 + bow_price
                            + gift_card_price, 2)
        self.new_present.price = total_price
        return self.new_present.price

    def build(self):
        return self.new_present


# this is the builder responsible for creating and building a new user account
class AccountBuilder:

    def __init__(self):
        self.new_account = user_account.UserAccount()

    # here we validate the user input, if successful we pass the dictionary over to the next two methods
    def input_validation(self, details_dict: dict):
        for key, value in details_dict.items():
            if not value:
                return False, "please make sure no field is empty"

        conn = sqlite3.connect('../Gift wrapping database.db')
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM user_credentials WHERE email = ?", (details_dict.get("email"),))
        result = cur.fetchone()
        if result:
            return False, "This email is already in use"
        else:

            self.create_credentials(details_dict)
            self.create_address(details_dict)
            return True

    def password_validation(self, password1, password2):
        has_digit = False
        has_upper = False
        has_lower = False
        has_special_char = False
        special_chars = "!£$€@*#%"

        if password1 != password2:
            return False, "Passwords must must match"
        if len(password1) < 8:
            return False, "Password must be at least 8 characters long"

        for char in password1:
            if char.isupper():
                has_upper = True
            elif char.isdigit():
                has_digit = True
            elif char.islower():
                has_lower = True
            elif char in special_chars:
                has_special_char = True

        if not has_upper:
            return False, "Password must have at least one capital letter"
        if not has_lower:
            return False, "Password must have at least one lowercase character"
        if not has_special_char:
            return False, "Password must have at least one special character: !£$€@*#% "
        if not has_digit:
            return False, "Password must have at least one number"

        self.set_password(password1)
        return True, "valid password"

    # called by the validation method if successful
    def set_password(self, password: str):
        self.new_account.password = password
        return self.new_account.password

    # considering each email is unique to an account we decided to use it as the username
    def set_username(self):
        self.new_account.username = self.new_account.credentials.email
        return self.new_account.username

    # here we create a Credential object
    def create_credentials(self, details_dict: dict):
        credentials_keys = ["name", "surname", "DoB", "email", "phone number"]
        user_credentials = user_account.Credentials()
        for key in credentials_keys:
            if key in details_dict:
                # replace method is used to link 2 word words to the corresponding attribute
                setattr(user_credentials, key.replace(" ", "_"), details_dict[key])

        self.new_account.credentials = user_credentials
        self.set_username()
        return self.new_account.credentials

    # here we create an Address object
    def create_address(self, details_dict: dict):
        address_keys = ["house number", "street", "postcode", "city"]
        user_address = user_account.Address()
        for key in address_keys:
            if key in details_dict:
                # replace method is used to link 2 word words to the corresponding attribute
                setattr(user_address, key.replace(" ", "_"), details_dict[key])
        self.new_account.address = user_address
        return self.new_account.address

    # here we build the current account
    def build(self):
        return self.new_account

    '''here we handle the upload of the account to the database, the calls are places in the correct sequence to 
    update the foreign key fields first'''
    def account_database_upload(self):
        new_account = self.build()
        new_account.address.upload_address()
        new_account.credentials.retrieve_address_id(new_account.address)
        new_account.credentials.upload_credentials()
        new_account.retrieve_credentials_id()
        new_account.retrieve_username()
        new_account.upload_account()
