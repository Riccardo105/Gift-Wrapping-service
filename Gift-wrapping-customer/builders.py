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

    def set_wrapping_paper(self, w_paper):
        self.new_present.wrapping_paper = w_paper
        return self.new_present.gift_card

    def set_bow(self, bow):
        self.new_present.bow = bow

        return self.new_present.bow

    def set_gift_card(self, gift_card):
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
    def input_validation(self, dict):
        for key, value in dict.items():
            if not value:
                return False
        self.create_credentials(dict)
        self.create_address(dict)
        return True

    def password_validation(self, password):
        pass

    # here we create a Credential object

    def create_credentials(self, dict):
        credentials_keys = ["name", "surname", "DoB", "email", "phone number"]
        user_credentials = user_account.Credentials()
        for key in credentials_keys:
            if key in dict:
                # replace method is used to link 2 word words to the corresponding attribute
                setattr(user_credentials, key.replace(" ", "_"), dict[key])

        self.new_account.credentials = user_credentials
        return self.new_account.credentials

    # here we create an Address object
    def create_address(self, dict):
        address_keys = ["house number", "street", "postcode", "city"]
        user_address = user_account.Address()
        for key in address_keys:
            if key in dict:
                # replace method is used to link 2 word words to the corresponding attribute
                setattr(user_address, key.replace(" ", "_"), dict[key])
        self.new_account.user_address = user_address
        return self.new_account.user_address



