import present
import user_account


# this is the builder responsible for creating and building the present
class PresentBuilder:
    def __init__(self):
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

    def set_order_dates(self, drop_off, pick_up):
        order_dates = present.OrderDates(drop_off, pick_up)
        self.new_present.order_dates = order_dates
        return self.new_present.order_dates

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
                return False
        self.create_credentials(details_dict)
        self.create_address(details_dict)
        return True

    def password_validation(self, password: list):
        has_digit = False
        has_upper = False
        has_lower = False
        has_special_char = False
        special_chars = "!£$€@*#%"

        if password[0] != password[1]:
            return False, "Passwords must must match"

        if len(password[0]) < 8:
            return False, "Password must be at least 8 characters long"

        for char in password:
            if char.isdigit():
                has_digit = True
            elif char.isupper():
                has_upper = True
            elif char.islower():
                has_lower = True
            elif char in special_chars:
                has_special_char = True

        if not has_digit:
            return False, "Password must have at least one number"
        if not has_upper:
            return False, "Password must have at least one capital letter"
        if not has_lower:
            return False, "Password must have at least one lowercase character"
        if not has_special_char:
            return False, "Password must have at least one special character: !£$€@*#% "

        self.set_password(password[0])
        return True, password

    # here we create a Credential object
    def create_credentials(self, details_dict: dict):
        credentials_keys = ["name", "surname", "DoB", "email", "phone number"]
        user_credentials = user_account.Credentials()
        for key in credentials_keys:
            if key in details_dict:
                # replace method is used to link 2 word words to the corresponding attribute
                setattr(user_credentials, key.replace(" ", "_"), details_dict[key])

        self.new_account.credentials = user_credentials
        return self.new_account.credentials

    # here we create an Address object
    def create_address(self, details_dict: dict):
        address_keys = ["house number", "street", "postcode", "city"]
        user_address = user_account.Address()
        for key in address_keys:
            if key in details_dict:
                # replace method is used to link 2 word words to the corresponding attribute
                setattr(user_address, key.replace(" ", "_"), details_dict[key])
        self.new_account.user_address = user_address
        return self.new_account.user_address

    def set_password(self, password: str):
        self.new_account.password = password
        return self.new_account.password

    def set_account_number(self):
        pass

    def build(self):
        return self.new_account


