import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Progressbar
from datetime import datetime
import subprocess
import sys
import sqlite3
import builders as b
import present as p


# here the installation process of the tkcalendar widget take place
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


install("tkcalendar")

# the import must be executed after the installation
from tkcalendar import Calendar

# here the necessary builders are instantiated
present_builder = b.PresentBuilder()
user_builder = b.AccountBuilder()


class MainWindow(tk.Tk):
    # these class variables are created so that actions can be performed from other frames
    frames = None  # the frames dictionary must be accessed to show the next/previous frame

    def __init__(self):
        super().__init__()

        # main setup
        self.title("Gift Wrapping")
        self.geometry("1000x550")
        self.resizable(False, False)
        self.configure(bg="#EBFFFE")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # this dictionary will contain all the frames, so they are accessible to show_frame()
        MainWindow.frames = {}

        # here all the frames are looped and displayed in the window, and placed inside the dictionary
        for F in (LoginFrame, SignupFrame, ShapeFrame, WrappingPaperFrame, ExtrasFrame, DatesFrame, QuoteFrame):
            frame = F(self)
            MainWindow.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.config(width=1000, height=550, bg="#EBFFFE")

        # show_frame is run once to determine the starting page (otherwise last page in loop would show_up)
        self.show_frame(LoginFrame)

        # run program
        self.mainloop()

    # show frame will be called by the submit buttons, and it will display the frame passed as argument
    @classmethod
    def show_frame(cls, page):
        frame = MainWindow.frames[page]
        frame.tkraise()


# home page implementation
class LoginFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # initial Home page setup

        self.header = tk.Label(self, text=" Welcome to the Gift Wrapping Store!", font=("Helvetica", 20), bg="#EBFFFE")
        self.header.place(relx=0.27, rely=0.1)

        # here the login frame is set up
        self.login_frame = tk.Frame(self, bg="#EBFFFE")
        self.login_frame.place(relx=0.43, rely=0.3)

        self.username_label = tk.Label(self.login_frame, text="Email:", font=("Helvetica", 9), bg="#EBFFFE")
        self.username_label.grid(row=0, column=0, sticky=tk.W)

        self.username_entry = tk.Entry(self.login_frame, bd=2, relief=tk.SUNKEN)
        self.username_entry.grid(row=1, column=0)

        self.password_label = tk.Label(self.login_frame, text="Password:", font=("Helvetica", 9), bg="#EBFFFE")
        self.password_label.grid(row=2, column=0, sticky=tk.W)

        self.password_entry = tk.Entry(self.login_frame, bd=2, relief=tk.SUNKEN)
        self.password_entry.grid(row=3, column=0)

        self.login_button = ttk.Button(self.login_frame, text="login", command=self.process_login_username)
        self.login_button.grid(row=4, column=0, pady=5)

        self.signup_label = tk.Label(self.login_frame, text="Don't have an account yet?", font=("Helvetica", 9),
                                     bg="#EBFFFE")
        self.signup_label.grid(row=5, column=0, sticky=tk.W, pady=5)

        self.signup_button = ttk.Button(self.login_frame, text="Signup", command=lambda:
                                        MainWindow.show_frame(SignupFrame))
        self.signup_button.grid(row=6, column=0, padx=5)

        self.error_message_frame = tk.Frame(self, bg="#EBFFFE")
        self.error_message_frame.place(relx=0.33, rely=0.75)

    def process_login_username(self):
        email = self.username_entry.get()
        if not email:
            error_message = tk.Label(self.error_message_frame, text="Please enter your account's email address.",
                                     font=("Helvetica", 8), bg="#EBFFFE")
            error_message.grid(row=0, column=0, sticky="nsew")
            return False

        conn = sqlite3.connect("../Gift wrapping database.db")
        cur = conn.cursor()
        cur.execute("SELECT username FROM user_account WHERE username=? ",
                    (email,))
        result = cur.fetchone()
        conn.close()
        if not result:
            error_message = tk.Label(self.error_message_frame,
                                     text="We couldn't find an account associated with this email",
                                     font=("Helvetica", 8), bg="#EBFFFE")
            error_message.grid(row=0, column=0, sticky="nsew")
            return False

        is_valid = self.process_password_verification(email)

        if is_valid:
            MainWindow.show_frame(ShapeFrame)

    def process_password_verification(self, username):
        password = self.password_entry.get()

        if not password:
            error_message = tk.Label(self.error_message_frame, text="Please enter your account's password.",
                                     font=("Helvetica", 8), bg="#EBFFFE")
            error_message.grid(row=0, column=0, sticky="nsew")
            return False

        conn = sqlite3.connect("../Gift wrapping database.db")
        cur = conn.cursor()
        cur.execute("SELECT password FROM user_account WHERE username=? ",
                    (username,))
        result = cur.fetchone()
        if not password == result[0]:
            error_message = tk.Label(self.error_message_frame,
                                     text="The password you entered doesn't match our records",
                                     font=("Helvetica", 8), bg="#EBFFFE")
            error_message.grid(row=0, column=0, sticky="nsew")
            return False
        return True







# Signup page implementation
class SignupFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # window controller setup
        self.config(bg="#EBFFFE")

        self.header = tk.Label(self, text="Please enter your details:", font=("Helvetica", 20), bg="#EBFFFE")
        self.header.place(relx=0.35, rely=0.1)

        self.submit_button = ttk.Button(self, text="Create account", command=lambda:
                                        self.process_user_details(self.new_account))
        self.submit_button.place(relx=0.475, rely=0.8)

        self.back_button = ttk.Button(self, text="Back", command=lambda: MainWindow.show_frame(LoginFrame))
        self.back_button.place(relx=0.2, rely=0.2)

        self.error_message_frame = tk.Frame(self, bg="#EBFFFE")
        self.error_message_frame.place(relx=0.43, rely=0.75)
        # credential form set up
        self.credentials_frame = tk.Frame(self, bg="#EBFFFE", width=200, height=300)
        self.credentials_frame.place(relx=0.36, rely=0.2)

        # here the account detail dictionary is initialised,
        # this will store the user details until they're ready to be sent to the database
        self.new_account = {"name": None, "surname": None, "DoB": None, "email": None, "phone number": None,
                            "house number": None, "street": None, "postcode": None, "city": None}

        # this dictionary allows how to access each entry individually, so they can be assigned to new_account
        self.entry_vars = {}

        # the account creation form is created here
        for idx, (key, _) in enumerate(self.new_account.items()):
            self.label = tk.Label(self.credentials_frame, text=key, font=("Helvetica", 9), bg="#EBFFFE")
            self.label.grid(row=idx, column=0, padx=5, pady=5, sticky="w")
            # NOTE: both dictionaries keys will always match as entry_vars{} is created off of new_account{}
            self.entry_vars[key] = tk.StringVar()
            self.entry = tk.Entry(self.credentials_frame, bd=2, textvariable=self.entry_vars[key], relief=tk.SUNKEN)
            self.entry.grid(row=idx, column=1, padx=5, pady=5)

        # password form set up
        self.password_frame = tk.Frame(self, bg="#EBFFFE", width=250, height=300)
        self.password_label = tk.Label(self.password_frame, text="Password", font=("Helvetica", 8), bg="#EBFFFE")
        self.password_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.password = tk.StringVar()
        self.password_entry = tk.Entry(self.password_frame, textvariable=self.password)
        self.password_entry.grid(row=1, column=0, padx=5, pady=5)

        self.confirm_password_label = tk.Label(self.password_frame, text="Confirm password", font=("Helvetica", 8),
                                               bg="#EBFFFE")
        self.confirm_password_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.confirm_password = tk.StringVar()
        self.confirm_password_entry = tk.Entry(self.password_frame, textvariable=self.confirm_password)
        self.confirm_password_entry.grid(row=3, column=0, padx=5, pady=5)

    # this function extract each entry value and assigns it to the correspondent key in the new_account dictionary
    def process_user_details(self, details_dict: dict):
        for key, var in self.entry_vars.items():
            entry_value = var.get()
            details_dict[key] = entry_value

        is_valid, message = user_builder.input_validation(details_dict)
        if is_valid:
            self.password_frame.place(relx=0.36, rely=0.2)
            self.header.config(text="Now choose a password")
            self.submit_button.config(text="save password", command=lambda: self.process_password())
            self.credentials_frame.place_forget()
            self.back_button.config(command=lambda: (self.credentials_frame.place(relx=0.36, rely=0.2),
                                                     self.password_frame.place_forget(),
                                                     self.submit_button.config(text="Create account",
                                                                        command=lambda:
                                                                        self.process_user_details(self.new_account))))
        else:
            error_message = tk.Label(self.error_message_frame, text=message,
                                     font=("Helvetica", 10), bg="#EBFFFE",
                                     fg="red")

            error_message.grid(row=0, column=0)

    def process_password(self):
        password1 = self.password_entry.get()
        password2 = self.confirm_password_entry.get()
        is_valid, message = user_builder.password_validation(password1, password2)
        if is_valid:
            user_builder.account_database_upload()
            MainWindow.show_frame(LoginFrame)

        else:
            error_message = tk.Label(self.error_message_frame, text=message, font=("Helvetica", 8), fg="red",
                                     bg="#EBFFFE")
            error_message.grid(row=0, column=0, sticky="nsew")


# the Parent class contains all the widgets shared by every page of the application
# each frame will configure the button accordingly within the "Window controller setup"
class ParentFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # creation of page layout
        self.top_frame = tk.Frame(self, bg="#EBFFFE")
        self.top_frame.grid(row=0, column=0)
        self.main_frame = tk.Frame(self, width=1000, height=550, bg="#EBFFFE")
        self.main_frame.grid(row=1, column=0, sticky="nsew")

        # window controllers set up
        # the header has no position because it will be determined later on according to text length
        self.header = tk.Label(self.main_frame, font=("Helvetica", 16), bg="#EBFFFE")
        self.back_button = ttk.Button(self.main_frame, text="Back")
        self.back_button.place(relx=0.05, rely=0.05)

        self.submit_button = ttk.Button(self.main_frame, text="Submit")
        self.submit_button.place(relx=.475, rely=.8)

        # Creation of the progress bar inside top_frame
        steps = ["Shape", "Wrapping Paper", "Extras", "Dates"]
        for i in range(len(steps)):
            self.step_label = tk.Label(self.top_frame, text=steps[i], font=("Helvetica", 12), bg="#EBFFFE")
            self.step_label.grid(row=0, column=i)
        self.progress_bar = Progressbar(self.top_frame, mode="determinate", length=1000, orient="horizontal")
        # the progress bar columnspan is equal to the number of steps so all the labels automatically align
        self.progress_bar.grid(row=1, column=0, columnspan=len(steps))

    # update progress bar takes in up or down to determine the state of the progress


# Shape page implementation
class ShapeFrame(ParentFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # window controllers setup
        self.header.config(text="Define the gift's shape:")
        self.header.place(relx=.4, rely=.03)
        self.sub_header = tk.Label(self.main_frame, text="please enter the gift's dimension:", font=("Helvetica", 12),
                                   bg="#EBFFFE")
        self.sub_header.place(relx=.38, rely=.5)

        # back button disabled for shape frame as it is the first step
        self.back_button.config(state="disabled")
        ''' NOTE: within shape frame the submit button is configured inside "entry_frame_setup", 
            as it has different parameters according to user input'''

        self.cube_frame = tk.Frame(self.main_frame, bg="#EBFFFE")
        self.cube_frame.place(relx=.15, rely=.15)
        self.cube_canvas = tk.Canvas(self.cube_frame, width=100, height=130, bg="#EBFFFE", highlightthickness=0)
        self.cube_canvas.grid(row=0, column=0)
        self.cube_canvas.create_rectangle(0, 0, 100, 100, fill="purple", outline="purple")

        # creation of cuboid frame
        self.cuboid_frame = tk.Frame(self.main_frame, bg="#EBFFFE")
        self.cuboid_frame.place(relx=.45, rely=.22)
        self.cuboid_canvas = tk.Canvas(self.cuboid_frame, width=100, height=95, bg="#EBFFFE", highlightthickness=0)
        self.cuboid_canvas.grid(row=0, column=0)
        self.cuboid_canvas.create_rectangle(0, 0, 150, 60, fill="purple", outline="purple")

        # creation of cylinder image
        self.cylinder_frame = tk.Frame(self.main_frame, bg="#EBFFFE")
        self.cylinder_frame.place(relx=.75, rely=0.12)

        self.cylinder_canvas = tk.Canvas(self.cylinder_frame, width=100, height=150, bg="#EBFFFE", highlightthickness=0)
        self.cylinder_canvas.grid(row=0, column=0)

        ''' 25 and 20 represent the starting coordinates of the top oval
            50 and 100 represent the width and height of the cylinder respectively'''
        self.cylinder_canvas.create_oval(25, 20, 25 + 50, 20 + 100 / 2, fill="purple", outline="purple")
        # the second oval is placed right below the first one
        self.cylinder_canvas.create_oval(25, 20 + 100 / 2, 25 + 50, 20 + 100, fill="purple", outline="purple")
        # the rectangle coordinates are worked out so that it is placed to cover half of each oval
        self.cylinder_canvas.create_rectangle(25, 20 + 100 / 4, 25 + 50, 20 + 3*100/4, fill="purple", outline="purple")

        # This is the variable that will store the selected shape
        self.selected_shape = tk.StringVar()
        # the default shape is cube
        self.selected_shape.set("cube")

        # each radio button is bound to selected_shape, and it will call the frame setup function

        self.cube_button = tk.Radiobutton(self.cube_frame, text="cube", variable=self.selected_shape, value="cube",
                                          bg="#EBFFFE", command=lambda: self.entry_frame_setup("cube"))
        self.cube_button.grid(row=1, column=0)
        self.cuboid_button = tk.Radiobutton(self.cuboid_frame, text="cuboid", variable=self.selected_shape,
                                            value="cuboid", bg="#EBFFFE", command=lambda:
                                            self.entry_frame_setup("cuboid"))
        self.cuboid_button.grid(row=1, column=0)
        self.cylinder_button = tk.Radiobutton(self.cylinder_frame, text="cylinder", variable=self.selected_shape,
                                              value="cylinder", bg="#EBFFFE", command=lambda:
                                              self.entry_frame_setup("cylinder"))
        self.cylinder_button.grid(row=1, column=0)

        # this is the frame where the entry frames will be displayed
        self.dimension_frame = tk.Frame(self.main_frame)
        self.dimension_frame.place(relx=.44, rely=.56)
        self.dimension_frame.config(width=200, height=100, bg="#EBFFFE")

        # cube entry frame
        self.cube_entry_frame = tk.Frame(self.dimension_frame)
        cube_length = tk.Label(self.cube_entry_frame, text=" length", bg="#EBFFFE")
        cube_length.grid(row=0, column=0, padx=2, pady=5)
        self.cube_length_entry = tk.Entry(self.cube_entry_frame, width=3, bd=2)
        self.cube_length_entry.grid(row=0, column=1, padx=2, pady=5)
        cube_cm_label = tk.Label(self.cube_entry_frame, text="Cm", bg="#EBFFFE")
        cube_cm_label.grid(row=0, column=2, padx=2, pady=5)

        # cuboid entries frame
        self.cuboid_entry_frame = tk.Frame(self.dimension_frame)
        cuboid_values = ["length", "width", "height"]

        for i in range(len(cuboid_values)):
            label = tk.Label(self.cuboid_entry_frame, text=cuboid_values[i], bg="#EBFFFE")
            label.grid(row=i, column=0, padx=2, pady=2)

        self.cuboid_length_entry = tk.Entry(self.cuboid_entry_frame, width=3, bd=2)
        self.cuboid_length_entry.grid(row=0, column=1, padx=2, pady=2)
        self.cuboid_width_entry = tk.Entry(self.cuboid_entry_frame, width=3, bd=2)
        self.cuboid_width_entry.grid(row=1, column=1, padx=2, pady=2)
        self.cuboid_height_entry = tk.Entry(self.cuboid_entry_frame, width=3, bd=2)
        self.cuboid_height_entry.grid(row=2, column=1, padx=2, pady=2)

        for i in range(3):
            cuboid_cm_label = tk.Label(self.cuboid_entry_frame, text="Cm", bg="#EBFFFE")
            cuboid_cm_label.grid(row=i, column=2, padx=2, pady=2)

        # cylinder entries frame
        self.cylinder_entry_frame = tk.Frame(self.dimension_frame)
        cylinder_values = ["diameter", "height"]

        for i in range(len(cylinder_values)):
            label = tk.Label(self.cylinder_entry_frame, text=cylinder_values[i], bg="#EBFFFE")
            label.grid(row=i, column=0, padx=2, pady=2)

        self.cylinder_diameter_entry = tk.Entry(self.cylinder_entry_frame, width=3, bd=2)
        self.cylinder_diameter_entry.grid(row=0, column=1, padx=2, pady=2)
        self.cylinder_height_entry = tk.Entry(self.cylinder_entry_frame, width=3, bd=2)
        self.cylinder_height_entry.grid(row=1, column=1, padx=2, pady=2)

        for i in range(2):
            label = tk.Label(self.cylinder_entry_frame, text="Cm", bg="#EBFFFE")
            label.grid(row=i, column=2, padx=2, pady=2)

        # this dictionary holds the entry frames
        self.entry_frames = {}

        for i in (self.cube_entry_frame, self.cuboid_entry_frame, self.cylinder_entry_frame):
            frame = i
            self.entry_frames[i] = frame
            # the frames must stick so the cover the bottom frame completely regardless of their size
            frame.grid(row=0, column=0, sticky="nsew")
            frame.config(bg="#EBFFFE")

        # the func is run once to match the default shape (cube)
        self.entry_frame_setup("cube")

    # this func displays the frame correspondent to the selected shape
    def entry_frame_setup(self, value):
        if value == "cube":
            self.entry_frames[self.cube_entry_frame].tkraise()
            self.submit_button.config(command=lambda: self.process_shape_selection("cube"))

        elif value == "cuboid":
            self.entry_frames[self.cuboid_entry_frame].tkraise()
            self.submit_button.config(command=lambda: self.process_shape_selection("cuboid"))

        elif value == "cylinder":
            self.entry_frames[self.cylinder_entry_frame].tkraise()
            self.submit_button.config(command=lambda: self.process_shape_selection("cylinder"))

    # if the user input is valid (is a number) it moves to the next page and call the relative builder function
    def process_shape_selection(self, value):
        try:
            if value == "cube":
                value1 = float(self.cube_length_entry.get())
                MainWindow.show_frame(WrappingPaperFrame)
                # if value is valid it sends it to the area function
                present_builder.set_shape(p.cube, value1)
                return True, value1

            elif value == "cuboid":
                value1 = float(self.cuboid_length_entry.get())
                value2 = float(self.cuboid_width_entry.get())
                value3 = float(self.cuboid_height_entry.get())
                MainWindow.show_frame(WrappingPaperFrame)
                # if value is valid it sends it to the area function
                present_builder.set_shape(p.cuboid, value1, value2, value3)
                return True, value1, value2, value3

            elif value == "cylinder":
                value1 = float(self.cylinder_diameter_entry.get())
                value2 = float(self.cylinder_height_entry.get())
                MainWindow.show_frame(WrappingPaperFrame)
                # if value is valid it sends it to the area function
                present_builder.set_shape(p.cylinder, value1, value2)
                return True, value1, value2
        except ValueError:
            error_label = tk.Label(self.main_frame, text="Invalid input: Enter a number", bg="#EBFFFE", fg="red")
            error_label.place(relx=.43, rely=.75)


# Wrapping paper page implementation
class WrappingPaperFrame(ParentFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # window controllers set up
        self.header.config(text="Choose a Wrapping paper and a colour:")
        self.header.place(relx=.30, rely=.03)
        self.subheader = tk.Label(self.main_frame, text="(NOTE: Standard paper, and purple are selected by default)",
                                  font=("Helvetica", 8),  bg="#EBFFFE")
        self.subheader.place(relx=.36, rely=0.72)
        self.submit_button.config(command=lambda: [MainWindow.show_frame(ExtrasFrame),
                                                   self.process_paper_selection()])
        self.back_button.config(command=lambda: MainWindow.show_frame(ShapeFrame))
        self.progress_bar["value"] = 25

        # standard paper design
        self.standard_paper = tk.Canvas(self.main_frame, width=150, height=150, bg="white", highlightthickness=0)
        self.standard_paper.place(relx=.25, rely=.1)

        x1, y1, x2, y2, x3, y3 = 0, 150, 75, 0, 150, 150
        triangle_colours = ["purple", "white", "purple", "white", "purple"]

        for i in range(5):
            self.standard_paper.create_polygon(x1, y1, x2, y2, x3, y3, fill=triangle_colours[i])
            x1 += 15
            y2 += 30
            x3 -= 15

        # premium paper design
        self.premium_paper = tk.Canvas(self.main_frame, width=150, height=150, bg="white", highlightthickness=0)
        self.premium_paper.place(relx=.55, rely=.1)

        original_points = [(10, 0), (0, 20), (20, 8), (0, 8), (20, 20)]

        x_spacing = 20
        y_spacing = 20

        for row in range(8):
            for col in range(8):
                x_offset = col * x_spacing
                y_offset = row * y_spacing
                shifted_points = [(x + x_offset, y + y_offset) for x, y in original_points]
                self.premium_paper.create_polygon(shifted_points, fill="purple")

        # this variable holds the selected paper
        self.selected_paper = tk.StringVar()
        # the default W-paper is Standard Paper
        self.selected_paper.set("standard paper")

        self.standard_paper_button = tk.Radiobutton(self.main_frame,
                                                    text=f"{p.w_paper1.name}: £ {p.w_paper1.price} cm2",
                                                    variable=self.selected_paper, value=p.w_paper1.name, bg="#EBFFFE")
        self.standard_paper_button.place(relx=.25, rely=.4)

        self.premium_paper_button = tk.Radiobutton(self.main_frame, text=f"{p.w_paper2.name}: £ {p.w_paper2.price} cm2",
                                                   variable=self.selected_paper, value=p.w_paper2.name, bg="#EBFFFE")
        self.premium_paper_button.place(relx=.55, rely=.4)

        # this variable holds the selected colour
        self.selected_colour = tk.StringVar()
        # the default colour is set to purple
        self.selected_colour.set("Purple")

        self.colours_frame = tk.Frame(self.main_frame, bg="#EBFFFE")
        self.colours_frame.place(relx=.20, rely=0.5)

        # here the colour options are set up
        colours = ["purple", "DarkSlateGray4", "DeepSkyBlue", "LightSeaGreen", "VioletRed2", "gold"]
        colours_name = ["Purple", "Dark Slate Grey", "Deep Sky Blue", "Light Sea Green", "Violet Red", "Gold"]

        for i in range(6):
            colours_canvas = tk.Canvas(self.colours_frame, bg=colours[i], width=40, height=40)
            colours_canvas.grid(row=0, column=i, padx=20)

            colours_label = tk.Label(self.colours_frame, text=colours_name[i], font=("Helvetica", 10), bg="#EBFFFE")
            colours_label.grid(row=1, column=i, padx=10)

            selected_colour_button = tk.Radiobutton(self.colours_frame, variable=self.selected_colour,
                                                    value=colours_name[i], bg="#EBFFFE")
            selected_colour_button.grid(row=2, column=i, padx=5)

    # this function sets the colour to the chosen paper then sets the paper to the present (via the builder)
    def process_paper_selection(self):
        if self.selected_paper.get() == "standard paper":
            p.w_paper1.set_colour(self.selected_colour.get())
            present_builder.set_wrapping_paper(p.w_paper1)
        elif self.selected_paper.get() == "premium paper":
            p.w_paper2.set_colour(self.selected_colour.get())
            present_builder.set_wrapping_paper(p.w_paper2)


# Extras page implementation
class ExtrasFrame(ParentFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # window controllers set up
        self.header.config(text="Don't miss out on these extras!")
        self.header.place(relx=.35, rely=.03)
        self.submit_button.config(command=lambda: [self.process_bow_selection(),
                                                   self.process_gift_card_selection()])
        self.back_button.config(command=lambda: MainWindow.show_frame(WrappingPaperFrame))

        self.progress_bar["value"] = 50

        # bow selection implementation
        self.bow_place_holder = tk.Frame(self.main_frame, bg="white")
        self.bow_place_holder.place(relx=.25, rely=.13)
        self.bow_title = tk.Label(self.bow_place_holder, width=20, height=10, text="Bow placeholder",
                                  font=("Helvetica", 8))
        self.bow_title.grid(row=0, column=0)

        # this variable holds the selection of bow
        self.bow_variable = tk.IntVar(value=0)
        self.bow_button = tk.Checkbutton(self.main_frame, variable=self.bow_variable, onvalue=1, text="bow",
                                         bg="#EBFFFE")
        self.bow_button.place(relx=.3, rely=.45)

        # gift card selection implementation
        self.gift_card_place_holder = tk.Frame(self.main_frame, width=150, height=150, bg="white")
        self.gift_card_place_holder .place(relx=.58, rely=.13)
        self.gift_card_title = tk.Label(self.gift_card_place_holder, width=20, height=10, text="GiftCard placeholder",
                                        font=("Helvetica", 8))
        self.gift_card_title.grid(row=0, column=0)

        # this variable holds the selection of gift card
        self.gift_card_variable = tk.IntVar(value=0)
        self.gift_card_button = tk.Checkbutton(self.main_frame, variable=self.gift_card_variable, onvalue=1,
                                               text="Gift Card",
                                               bg="#EBFFFE", command=lambda: self.show_gift_card_entry())
        self.gift_card_button.place(relx=.62, rely=.45)

        # This is the text frame, it will only be displayed if the gift card is selected

        self.gift_card_entry_frame = tk.Frame(self.main_frame, bg="#EBFFFE")
        self.gift_card_entry_prompt = tk.Label(self.gift_card_entry_frame, text="What should we write on the card?",
                                               bg="#EBFFFE", font=("Helvetica", 10))
        self.gift_card_entry_prompt.grid(row=0, column=0, sticky="nw")
        self.gift_card_text = tk.Entry(self.gift_card_entry_frame, bd=2)
        self.gift_card_text.grid(row=1, column=0, sticky="nw", padx=5, pady=5)

    def show_gift_card_entry(self):

        if self.gift_card_variable.get():
            self.gift_card_entry_frame.place(relx=.58, rely=.54)
        else:
            self.gift_card_entry_frame.place_forget()

    def process_bow_selection(self):
        if self.bow_variable.get() == 1:
            present_builder.set_bow(p.bow1)
        else:
            present_builder.set_bow(None)

    def process_gift_card_selection(self):
        try:
            if self.gift_card_variable.get() == 0:
                present_builder.set_gift_card(None)
                MainWindow.show_frame(DatesFrame),
            elif self.gift_card_variable.get() == 1:
                if self.gift_card_text.get() is None or len(self.gift_card_text.get().strip()) == 0:
                    error_label = tk.Label(self.main_frame, text="Please enter a message for the gift card.",
                                           bg="#EBFFFE",
                                           fg="red")
                    error_label.place(relx=.39, rely=.75)
                else:
                    text = str(self.gift_card_text.get())
                    p.gift_card1.set_text(text)
                    present_builder.set_gift_card(p.gift_card1)
                    MainWindow.show_frame(DatesFrame)
        except ValueError:
            pass


class DatesFrame(ParentFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # window controllers setup
        self.header.config(text="Choose a drop off and pick up date:")
        self.header.place(relx=.32, rely=.03)
        self.subheader = tk.Label(self.main_frame, text="Opening hours: Mon-Fri 8am-18:30m", font=("Helvetica", 10),
                                  bg="#EBFFFE")
        self.subheader.place(relx=.39, rely=.08)
        self.sub_subheader = tk.Label(self.main_frame, text="Please allow 24hrs to get your gift wrapped",
                                      font=("Helvetica", 10),
                                      bg="#EBFFFE")
        self.sub_subheader.place(relx=.37, rely=.50)
        self.submit_button.config(command=lambda: self.validate_dates())
        self.back_button.config(command=lambda: [MainWindow.show_frame(ExtrasFrame)])

        self.progress_bar["value"] = 75

        # creation of drop off date calendar
        self.cal1_header = tk.Label(self.main_frame, text="Drop off date:", font=("Helvetica", 12), bg="#EBFFFE")
        self.cal1_header.place(relx=.15, rely=.12)
        self.drop_off_calendar = Calendar(self.main_frame)
        self.drop_off_calendar.place(relx=.15, rely=.16)

        # creation of pick-up date calendar
        self.cal2_header = tk.Label(self.main_frame, text=" Pick up date:", font=("Helvetica", 12), bg="#EBFFFE")
        self.cal2_header.place(relx=.6, rely=.12)
        self.pick_up_calendar = Calendar(self.main_frame)
        self.pick_up_calendar.place(relx=.6, rely=.16)

        # creation of time menu for both dates
        options = []
        for hour in range(8, 19):
            for minute in ['00', '30']:
                options.append(f"{hour}:{minute}")

        # time selection for drop off date
        self.drop_off_time = tk.StringVar()
        self.time1_header = tk.Label(self.main_frame, text="Drop off time:", font=("Helvetica", 12), bg="#EBFFFE")
        self.time1_header.place(relx=.25, rely=.55)
        self.drop_off_time_menu = tk.OptionMenu(self.main_frame, self.drop_off_time, *options)
        self.drop_off_time_menu.place(relx=.25, rely=.59)

        # time selection for pick-up date
        self.pick_up_time = tk.StringVar()
        self.time2_header = tk.Label(self.main_frame, text="Pick up time:", font=("Helvetica", 12), bg="#EBFFFE")
        self.time2_header.place(relx=.7, rely=.55)
        self.pick_up_time_menu = tk.OptionMenu(self.main_frame, self.pick_up_time, *options)
        self.pick_up_time_menu.place(relx=.7, rely=.59)

    # dates are validated to check if there's at least 24 hrs in between
    def validate_dates(self):
        # retrieve dates
        drop_off_date = self.drop_off_calendar.get_date()
        pick_up_date = self.pick_up_calendar.get_date()

        # retrieve times
        drop_off_time = self.drop_off_time.get()
        pick_up_time = self.pick_up_time.get()

        # here it checks if the dates and times were not selected
        if not (drop_off_date and pick_up_date and drop_off_time and pick_up_time):
            error1 = tk.Label(self, text="Please, pick both dates and times", font=("Helvetica", 10), bg="#EBFFFE",
                              fg="red")
            error1.place(relx=.39, rely=.75)
        # if dates where selected they are processed
        else:
            # dates are turned into appropriate format for datetime module
            drop_off_datetime = datetime.strptime(drop_off_date, "%m/%d/%y")
            pick_up_datetime = datetime.strptime(pick_up_date, "%m/%d/%y")

            # hours are turned into appropriate format for datetime module
            start_hour, start_minute = map(int, self.drop_off_time.get().split(":"))
            end_hour, end_minute = map(int, self.pick_up_time.get().split(":"))

            # the time is appended to the date
            drop_off_datetime = drop_off_datetime.replace(hour=start_hour, minute=start_minute)
            pick_up_datetime = pick_up_datetime.replace(hour=end_hour, minute=end_minute)

            # here it checks if the drop-off date is in the future
            if drop_off_datetime <= datetime.now():
                error2 = tk.Label(self.main_frame, text="The dates must be in the future", font=("Helvetica", 10),
                                  bg="#EBFFFE", fg="red")
                error2.place(relx=.39, rely=.75)
            else:
                # here it checks if either of the dates are weekends
                if drop_off_datetime.weekday() in [5, 6] or pick_up_datetime.weekday() in [5, 6]:
                    error3 = tk.Label(self.main_frame, text="The shop is closed on the weekend", font=("Helvetica", 10),
                                      bg="#EBFFFE", fg="red")
                    error3.place(relx=.39, rely=.75)
                else:
                    time_difference = pick_up_datetime - drop_off_datetime
                    # the final validation step is checking if there is at least 24hrs between the days
                    if time_difference.days < 1:
                        error4 = tk.Label(self.main_frame, text="Please, allow 24 hrs before picking up",
                                          font=("Helvetica", 10), bg="#EBFFFE", fg="red")
                        error4.place(relx=.39, rely=.75)
                    else:
                        MainWindow.show_frame(QuoteFrame)
                        present_builder.set_order_dates(drop_off_datetime, pick_up_datetime)
                        present_builder.calculate_price()
                        QuoteFrame.setup_quote()


class QuoteFrame(ParentFrame):
    quote = None
    new_present = None

    def __init__(self, parent):
        super().__init__(parent)

        # Window controllers setup
        self.header.config(text="Here is your quote:")
        self.header.place(relx=.40, rely=.03)
        self.subheader = tk.Label(self.main_frame, text="feel free to download a copy before you go!",
                                  font=("Helvetica", 10), bg="#EBFFFE")
        self.subheader.place(relx=.37, rely=.08)
        self.submit_button.config(text="Download")
        self.back_button.config(command=lambda: MainWindow.show_frame(DatesFrame))

        self.progress_bar["value"] = 100

        # once all the steps have been completed the present is finalised and built
        QuoteFrame.new_present = present_builder.build()

        QuoteFrame.quote = tk.Text(self.main_frame, width=50, height=20, font=("Helvetica", 10))
        QuoteFrame.quote.place(relx=.3, rely=.15)

    @classmethod
    def setup_quote(cls):
        QuoteFrame.quote.insert(1.0, f"Shape: {QuoteFrame.new_present.shape.name} \n"
                                f"Wrapping paper: {QuoteFrame.new_present.wrapping_paper.name} \n"
                                f"Colour: {QuoteFrame.new_present.wrapping_paper.colour} \n")
        if QuoteFrame.new_present.bow is not None:
            QuoteFrame.quote.insert(4.0, f"Bow: {QuoteFrame.new_present.bow.name} \n")
        else:
            QuoteFrame.quote.insert(4.0, f"Bow: None\n")

        if QuoteFrame.new_present.gift_card is not None:
            QuoteFrame.quote.insert(5.0, f"Gift Card: {QuoteFrame.new_present.gift_card.name}\n"
                                         f"Gift Card text: {QuoteFrame.new_present.gift_card.text}\n")
        else:
            QuoteFrame.quote.insert(5.0, f"Gift Card: None\n")
        QuoteFrame.quote.insert(7.0, f"Drop_off_date: {QuoteFrame.new_present.order_dates.drop_off_date}\n"
                                f"Pick_up_date: {QuoteFrame.new_present.order_dates.pick_up_date}\n"
                                f"price: £{QuoteFrame.new_present.price}")


if __name__ == "__main__":
    app = MainWindow()
