
# This is the present the user will build, the user inputs are firstly processed by the present builder
# and then appended to the created object
class Present:
    def __init__(self):
        # all parameters are set to be None initially (to allow creation of empty object)
        # measures have put in place within the Gui to make sure all the required fields are filled
        self.shape = None
        self.wrapping_paper = None
        self.bow = None
        self.gift_card = None
        self.price = None
        self.order_dates = None


# this is the parent class for the available shapes, in this instance the controller will be only one, the builder
class Shape:
    def __init__(self, name):
        self.name = name
        self.area = 0


class Cube(Shape):
    def __init__(self):
        super().__init__("cube")

    def calculate_area(self, side):
        offset = 3
        length = (int(side) * 4) + (offset * 2)
        width = (int(side) * 3) + (offset * 2)
        self.area = length * width
        # once the shapes area is calculated it is set to the present (via the builder)
        return self.area


class Cuboid(Shape):
    def __init__(self):
        super().__init__("cuboid")

    def calculate_area(self, length, width, height):
        length = int(length)
        width = int(width)
        height = int(height)
        offset = 3
        total_length = (width * 2) + (height * 2) + (offset * 2)
        total_width = (height * 2) + length + (offset * 2)
        self.area = total_length * total_width
        # once the shapes area is calculated it is set to the present (via the builder)
        return self.area


class Cylinder(Shape):
    def __init__(self):
        super().__init__("cylinder")

    def calculate_area(self, diameter, height):
        diameter = int(diameter)
        height = int(height)
        offset = 3
        total_diameter = diameter + (offset * 2)
        total_height = height + diameter + (offset * 2)
        self.area = total_diameter * total_height
        # once the shapes area is calculated it is set to the present (via the builder)
        return self.area


# wrapping paper class
class WrappingPaper:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.colour = None

    def set_colour(self, colour):
        self.colour = colour
        return self.colour


# bow class
class Bow:
    def __init__(self, name, price):
        self.name = name
        self.price = price


# Gift card class
class GiftCard:
    def __init__(self, name, flat_rate, character_price):
        self.name = name
        self.flat_rate = flat_rate
        self.character_price = character_price
        self.text = None
        self.price = 0

    def set_text(self, text):
        self.text = text
        self.calculate_price()
        return self.text

    def calculate_price(self):
        self.price = len(self.text) * self.character_price + self.flat_rate
        return self.price


# order dates class
class OrderDates:
    def __init__(self, drop_off_date, pick_up_date):
        self.drop_off_date = drop_off_date
        self.pick_up_date = pick_up_date


# here all the available components are created

cube = Cube()
cuboid = Cuboid()
cylinder = Cylinder()

w_paper1 = WrappingPaper("standard paper", 0.40)
w_paper2 = WrappingPaper("premium paper", 0.75)

bow1 = Bow("standard bow", 1.50)

gift_card1 = GiftCard("standard gift_card", 0.50, 0.02)