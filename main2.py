import tkinter as tk
import datetime
from tkcalendar import DateEntry
import database
import tkinter.simpledialog as simpledialog
import functools
import secrets
import random

LARGE_FONT = ('Verdana', 12)
MEDIAN_FONT = ('Verdana', 10)
SMALL_FONT = ('Verdana', 8)

class User():
    def __init__(self):
        self.userName = None
        self.bookingStaff = None

class LoginPage(tk.Tk):
    def __init__(self, **kwargs):
        self.db = database.HorizonCinemaSystem()
        tk.Tk.__init__(self, **kwargs)
        self.geometry('{}x{}'.format(820, 400))
        self.wm_title('Horizon Cinemas Booking System')
        tk.Label(self).grid(row=0, column=2, padx=5, pady=5)
        tk.Label(self, text='Username').grid(row=1, column=3, sticky='E', padx=5)
        tk.Label(self, text='Password').grid(row=2, column=3, sticky='E', padx=5)
        self.entry2 = tk.Entry(self)
        self.entry3 = tk.Entry(self, show="*")
        self.entry2.grid(row=1, column=4, sticky='W')
        self.entry3.grid(row=2, column=4, sticky='W')
        tk.Button(self, text="Register", command = self.clickRegister, bg="#d5f7e2").grid(row=3, column=4, sticky='W')
        tk.Button(self, text="Login", command = self.clickEmployee, bg="#d5f7e2").grid(row=3, column=4, sticky='E')

    def clickEmployee(self):
        enteredEmployeeUserName = self.entry2.get()
        enteredEmployeePassword = self.entry3.get()
        global userE
        userE = User()

        if enteredEmployeeUserName == 'staff' and enteredEmployeePassword == 'staff':
            userE.userName = 'staff'
            userE.role = 'staff'
        elif enteredEmployeeUserName == 'admin' and enteredEmployeePassword == 'admin':
            userE.userName = 'admin'
            userE.role = 'admin'
        elif enteredEmployeeUserName == 'manager' and enteredEmployeePassword == 'manager':
            userE.userName = 'manager'
            userE.role = 'manager'
        else:
            result = database.BookingStaff.login(self.db.getdb() ,enteredEmployeeUserName, enteredEmployeePassword)
            if result['register'] == False:
                return tk.messagebox.showerror('Error', 'You have not registered yet.')
            elif result['register'] == True and result['password'] == False:
                return tk.messagebox.showerror('error', 'Invalid password.')
            elif result['register'] == True and result['password'] == True:
                userE.username = enteredEmployeeUserName
                userE.role = 'Staff'
                userE.bookingStaff = database.BookingStaff(result['id'], enteredEmployeeUserName, '-', '-', self.db.getdb())

        userE.cinema = 'Cabot Circus'
        userE.city = 'Bristol'
        userE.currentCinema = None
        userE.currentCity = None
        self.destroy()
        app = EmployeeHomePage()
        app.mainloop()

    def clickRegister(self):

        self.window = tk.Toplevel(self)
        self.window.wm_title('Create Account')

        frame = tk.Frame(self.window)
        frame.pack(side='top', fill='both', expand=True)

        username_frame = tk.Frame(frame)
        username_frame.pack(side='top', fill='x')
        tk.Label(username_frame, text='Username:').pack(side='left', padx=5)
        self.entry_username = tk.Entry(username_frame)
        self.entry_username.pack(side='left', fill='x', expand=True, padx=5)

        email_frame = tk.Frame(frame)
        email_frame.pack(side='top', fill='x')
        tk.Label(email_frame, text='Email:').pack(side='left', padx=5)
        self.entry_email = tk.Entry(email_frame)
        self.entry_email.pack(side='left', fill='x', expand=True, padx=5)

        phone_frame = tk.Frame(frame)
        phone_frame.pack(side='top', fill='x')
        tk.Label(phone_frame, text='Phone Number:').pack(side='left', padx=5)
        self.entry_phone = tk.Entry(phone_frame)
        self.entry_phone.pack(side='left', fill='x', expand=True, padx=5)

        password_frame = tk.Frame(frame)
        password_frame.pack(side='top', fill='x')
        tk.Label(password_frame, text='Password:').pack(side='left', padx=5)
        self.entry_password = tk.Entry(password_frame, show="*")
        self.entry_password.pack(side='left', fill='x', expand=True, padx=5)

        button_frame = tk.Frame(self.window, bd=5)
        button_frame.pack(side='bottom', fill='x')

        tk.Button(button_frame, text='Create Account', command=self.createAccount).pack(side="right")

    def createAccount(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()

        if(len(username) <= 0 or len(password) <= 0) or len(email) <= 0 or len(phone) <= 0:
            tk.messagebox.showerror('Error', 'Please complete the form!')
        else:
            result = database.BookingStaff(secrets.token_hex(5), username, email, phone, self.db.getdb()).createAccount(password)
            if result == True:
                tk.messagebox.showinfo('Success', 'Your account has been created successfully.')
                self.window.destroy()
            else:
                tk.messagebox.showerror('Error', 'Your account already exist.')

class EmployeeWindows(tk.Tk):

    def __init__(self, **kwargs):
        self.db = database.HorizonCinemaSystem()
        tk.Tk.__init__(self, **kwargs)
        self.geometry('{}x{}'.format(820, 500))
        self.wm_title(f'{userE.cinema} ({userE.city}) Booking System')

        frame = tk.Frame(self)
        frame.pack(side='left')

        tk.Button(frame, text='Main Menu', command=self.returnToHome, width=20, bg="#958ce6").pack(padx=10, pady=15)
        tk.Button(frame, text='Listings', command=self.Listings, width=20, bg="#958ce6").pack(padx=10, pady=15)
        tk.Button(frame, text='New Booking', command=self.NewBooking, width=20, bg="#958ce6").pack(padx=10, pady=15)
        tk.Button(frame, text='Cancel Booking', command=self.CancelBooking, width=20, bg="#958ce6").pack(padx=10, pady=15)

        if userE.role == 'admin' or userE.role == 'manager':
            tk.Button(frame, text='Manage Films', command=self.ManageFilms, width=20, bg="#958ce6").pack(padx=10, pady=15)
            tk.Button(frame, text='Generate Reports', command=self.GenerateReports, width=20, bg="#958ce6").pack(padx=10, pady=15)

        if userE.role == 'manager':
            tk.Button(frame, text='Manage Cinemas', command=self.ManageCinemas, width=20, bg="#958ce6").pack(padx=10, pady=15)

        tk.Button(frame, text='Log out', command =self.logoutEmployee, width=20, bg="#f08db0").pack(padx=10, pady=15)

    def returnToHome(self):
        try: 
            if self.name == 'home' :
                return
            else:
                self.destroy()
                app = EmployeeHomePage()
                return app.mainloop()
        except Exception as e:
            self.destroy()
            app = EmployeeHomePage()
            return app.mainloop()

    def Listings(self):
        try: 
            if self.name == 'listings' :
                return
            else:
                self.destroy()
                app = Listings()
                return app.mainloop()
        except Exception as e:
            self.destroy()
            app = Listings()
            return app.mainloop()

    def NewBooking(self):
        try: 
            if self.name == 'newbooking' :
                return
            else:
                self.destroy()
                app = NewBooking()
                return app.mainloop()
        except Exception as e:
            self.destroy()
            app = NewBooking()
            return app.mainloop()

    def CancelBooking(self):
        try: 
            if self.name == 'cancelbooking' :
                return
            else:
                self.destroy()
                app = CancelBooking()
                return app.mainloop()
        except Exception as e:
            self.destroy()
            app = CancelBooking()
            return app.mainloop()

    def ManageFilms(self):
        try: 
            if self.name == 'managefilms' :
                return
            else:
                self.destroy()
                app = ManageFilms()
                return app.mainloop()
        except Exception as e:
            self.destroy()
            app = ManageFilms()
            return app.mainloop()

    def GenerateReports(self):
        try: 
            if self.name == 'generatereports' :
                return
            else:
                self.destroy()
                app = GenerateReports()
                return app.mainloop()
        except Exception as e:
            self.destroy()
            app = GenerateReports()
            return app.mainloop()

    def ManageCinemas(self):
        try: 
            if self.name == 'managecinemas' :
                return
            else:
                self.destroy()
                app = ManageCinemas()
                return app.mainloop()
        except Exception as e:
            self.destroy()
            app = ManageCinemas()
            return app.mainloop()

    def logoutEmployee(self):
        self.destroy()
        app = LoginPage()
        return app.mainloop()

class EmployeeHomePage(EmployeeWindows):
    def __init__(self, **kwargs):
        self.name = 'home'
        EmployeeWindows.__init__(self, **kwargs)
        city = None
        cinema = None

        cities = self.db.getCities()
        cinemas = []

        citiesNames =[]
        cinemaNames = []

        selectCinema = tk.StringVar(self)
        selectCity = tk.StringVar(self)

        for i in cities:
            citiesNames.append(i.getCity())

        for i in citiesNames:
            if i == userE.city:
                selectCity.set(i)

        if selectCity.get() is None:
            userE.city = citiesNames[0]
            selectCity.set(citiesNames[0])

        for i in cities:
            if i.getCity() == userE.city:
                city = i

        cinemas = city.getCinemas()

        for i in cinemas:
            cinemaNames.append(i.getLocation())

        for i in cinemaNames:
            if i == userE.cinema:
                selectCinema.set(i)

        if selectCinema.get() is None:
            userE.cinema = cinemaNames[0]
            selectCinema.set(cinemaNames[0])

        for i in cinemas:
            if i.getLocation() == userE.cinema:
                cinema = i

        city_menu = tk.OptionMenu(self, selectCity, *citiesNames)
        cinema_menu = tk.OptionMenu(self, selectCinema, *cinemaNames)

        userE.currentCinema = cinema
        userE.currentCity = city

        self.wm_title(f'{userE.cinema} ({userE.city}) Booking System')

        def option_selected(*args):
            userE.cinema = selectCinema.get()
            userE.city = selectCity.get()
            for i in cities:
                if i.getCity() == userE.city:
                    city = i
            for i in cinemas:
                if i.getLocation() == userE.cinema:
                    cinema = i
            userE.currentCinema = cinema
            userE.currentCity = city
            self.wm_title(f'{userE.cinema} ({userE.city}) Booking System')

        selectCinema.trace("w", option_selected)
        selectCity.trace("w", option_selected)

        if userE.userName == 'manager':
            city_menu.pack()
            cinema_menu.pack()

class Listings(EmployeeWindows):
    def __init__(self, **kwargs):
        self.name = 'listings'
        EmployeeWindows.__init__(self, **kwargs)
        calendar_test = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2)
        movies = userE.currentCinema.getListings(calendar_test.get())

        global current_page
        global num_movies_per_page
        def go_to_prev_page():
            global current_page
            if current_page > 0:
                current_page -= 1
                update_movies_box(movies, True)

        def go_to_next_page():
            global current_page
            if current_page < total_num_pages - 1:
                current_page += 1
                update_movies_box(movies, True)

        def update_movies_box(movies, yes = False):
            global movies_frame
            if yes == False:
                global movies_box
                global framess
                framess = []
                movies_box = None

            if yes == True:
                for movie_frame in framess:
                    for widget in movie_frame.winfo_children():
                        widget.destroy()

                    movie_frame.destroy()
                framess = []
                movies_box.pack_forget()
                movies_box.destroy()
                movies_frame.destroy()

            movies_frame = tk.Frame(self)
            movies_frame.pack(side="top")

            movies_box = tk.Frame(movies_frame)
            movies_box.pack()

            start_index = current_page * num_movies_per_page
            end_index = start_index + num_movies_per_page

            if end_index > len(movies):
                end_index = len(movies)

            for i in range(start_index, end_index):
                movie_frame = tk.Frame(movies_box, bd=1, relief="solid")
                movie_frame.pack(side="left", padx=5, pady=5)

                movie_title_label = tk.Label(movie_frame, text=f"Movie Title: {movies[i]['title']}")
                movie_title_label.pack()
                movie_rating_label = tk.Label(movie_frame, text=f"Rating: {movies[i]['rating']}/5")
                movie_rating_label.pack()
                movie_description_label = tk.Label(movie_frame, text=f"Movie Description : {movies[i]['description']}")
                movie_description_label.pack()
                movie_actors_label = tk.Label(movie_frame, text=f"Actors: {movies[i]['actors']} ")
                movie_actors_label.pack()
                movie_genre_label = tk.Label(movie_frame, text=f"Genre: {movies[i]['genre']}")
                movie_genre_label.pack()
                movie_age_label = tk.Label(movie_frame, text=f"Age: {movies[i]['age']}")
                movie_age_label.pack()

                showtimes_frame = tk.Frame(movie_frame)
                showtimes_frame.pack()

                showtimes_box = tk.Frame(showtimes_frame)
                showtimes_box.pack()

                for ii in range(len(movies[i]['showings'])):
                    showtime1_button = tk.Button(showtimes_box, text=f"{movies[i]['showings'][ii]['time']} ({movies[i]['showings'][ii]['seats']} seats left)")
                    showtime1_button.pack(side="left")
                    if (ii+1) % 2 == 0:
                        showtimes_box.pack()
                        showtimes_box = tk.Frame(showtimes_frame)
                        showtimes_box.pack()

                if (i+1) % 2 == 0:
                    movies_box.pack()
                    movies_box = tk.Frame(movies_frame)
                    movies_box.pack()

                framess.append(movie_frame)

        def on_date_change(movies, date):
            movies = userE.currentCinema.getListings(calendar.get())
            update_movies_box(movies, True)

        top_frame = tk.Frame(self)
        top_frame.pack(side="top", fill="x")

        middle_label = tk.Label(top_frame, text="Horizon Cinemas")
        middle_label.pack(side="left")

        right_frame = tk.Frame(top_frame)
        right_frame.pack(side="right")

        right_label = tk.Label(right_frame, text=f"{userE.currentCinema.getCity()} {userE.currentCinema.getLocation()}")
        right_label.pack(side="top")

        name_label = tk.Label(right_frame, text=f"{userE.userName}")
        name_label.pack(side="top")

        second_frame = tk.Frame(self) 
        second_frame.pack(side="top", fill="x")

        calendar_frame = tk.Frame(second_frame)
        calendar_frame.pack()
        calendar_label = tk.Label(calendar_frame, text="Select a date : ")
        calendar_label.pack(side="left")
        calendar = DateEntry(calendar_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        calendar.pack(side="left")

        movies_frame = tk.Frame(self)
        movies_frame.pack(side="top")

        current_page = 0
        num_movies_per_page = 4
        total_num_pages = (len(movies) + num_movies_per_page - 1) // num_movies_per_page

        nav_frame = tk.Frame(self)
        nav_frame.pack(side="top")

        prev_button = tk.Button(nav_frame, text="Previous", command=go_to_prev_page)
        prev_button.pack(side="left")

        next_button = tk.Button(nav_frame, text="Next", command=go_to_next_page)
        next_button.pack(side="left")

        update_movies_box(movies)
        calendar.bind("<<DateEntrySelected>>", lambda event: on_date_change(movies, calendar))


class NewBooking(EmployeeWindows):
    def __init__(self, **kwargs):
        self.name = 'newbooking'
        EmployeeWindows.__init__(self, **kwargs)
        self.geometry('{}x{}'.format(760, 500))
        userE.available_ticket = False
        refrenceId = secrets.token_hex(4)

        labels_frame = tk.Frame(self)
        labels_frame.pack(side="top")

        label_cinema = tk.Label(labels_frame, text="Horizon Cinema")
        label_cinema.pack()

        label_location = tk.Label(labels_frame, text=f"{userE.city} {userE.cinema}")
        label_location.pack()

        label_staff = tk.Label(labels_frame, text=f"{userE.userName} [{userE.role}]")
        label_staff.pack()

        inputCategory = tk.Frame(self)
        inputCategory.pack(side="left")

        frame_category1 = tk.Frame(inputCategory)
        frame_category1.pack(side="top")

        calendar_frame = tk.Frame(frame_category1)
        calendar_frame.pack()
        calendar_label = tk.Label(calendar_frame, text="Select a date : ")
        calendar_label.pack(side="left")
        calendar = DateEntry(calendar_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        calendar.pack(side="right")

        film_frame = tk.Frame(frame_category1)
        film_frame.pack()
        calendar_label = tk.Label(film_frame, text="Select a film : ")
        calendar_label.pack(side="left")
        film_options = []
        films = userE.currentCinema.getFilms()
        for i in films:
            film_options.append(i.getFilmName())
        film_var = tk.StringVar(film_frame)
        film_menu = tk.OptionMenu(film_frame, film_var, 'Select a film', *film_options)
        film_menu.pack(side="right")

        def getShowings():
            filmName = film_var.get()
            showings = []
            showingList = []
            for i in films:
                if i.getFilmName() == filmName:
                    showings = i.getShowings()
            for i in showings:
                date = calendar.get()
                time = datetime.datetime.fromtimestamp(i.getShowingTime())
                timestamp_date = datetime.datetime.fromtimestamp(i.getShowingTime()).date()
                date = datetime.datetime.strptime(date, '%d/%m/%y').date()
                if timestamp_date == date:
                    showingList.append(time.strftime("%H:%M"))
            return showingList

        showing_frame = tk.Frame(frame_category1)
        showing_frame.pack()
        showing_label = tk.Label(showing_frame, text="Select a Showing : ")
        showing_label.pack(side="left")
        showing_options = getShowings()
        showing_var = tk.StringVar(showing_frame)
        if len(showing_options) >= 1:
            showing_var.set(showing_options[0])
            showing_menu = tk.OptionMenu(showing_frame, showing_var, *showing_options)
        else: 
            showing_menu = tk.OptionMenu(showing_frame, showing_var, ())
        showing_menu.pack(side="right")

        customer_frame = tk.Frame(frame_category1)
        customer_frame.pack()
        customer_label = tk.Label(customer_frame, text="Select # of tickets")
        customer_label.pack(side="left")
        customer_input = tk.Entry(customer_frame)
        customer_input.pack(side="left")

        def on_value_change(*args):
            showing_options = getShowings()
            update_options(showing_menu, showing_var, showing_options)

        def on_date_change():
            showing_options = getShowings()
            update_options(showing_menu, showing_var, showing_options)
            update_receipt()

        film_var.trace('w', on_value_change)

        ticket_frame = tk.Frame(frame_category1)
        ticket_frame.pack()
        ticketLabel = tk.Label(ticket_frame, text="Select Ticket Type :")
        ticketLabel.pack(side="left")
        ticket_type = tk.IntVar(ticket_frame, value=2)
        vip_button = tk.Radiobutton(ticket_frame, text="VIP", variable=ticket_type, value=1)
        vip_button.pack(side="right")
        lower_button = tk.Radiobutton(ticket_frame, text="Lower", variable=ticket_type, value=2)
        lower_button.pack(side="right")
        upper_button = tk.Radiobutton(ticket_frame, text="Upper", variable=ticket_type, value=3)
        upper_button.pack(side="right")

        check_button = tk.Button(frame_category1, text="Check Availability", command= lambda: check_availability())
        check_button.pack(side="right",pady=10)

        frame_category2 = tk.Frame(inputCategory)
        frame_category2.pack(pady=(0, 10), side="bottom")

        availability_label_frame = tk.Frame(frame_category2)
        availability_label_frame.pack()
        availability_label = tk.Label(availability_label_frame, text="Availablility:")
        availability_label.pack()
        price = tk.Label(availability_label_frame, text="Price:")
        price.pack()

        def check_availability():
            showings = []
            showing = None
            filmName = film_var.get()
            showingTime = showing_var.get()
            noOfCustomer = customer_input.get()
            ticketType = ticket_type.get()

            if (noOfCustomer.isdigit() == True and int(noOfCustomer) in range(1, 41)) == False:
                return tk.messagebox.showwarning("Warning",f"Please enter a number between 1 to 40 for the # of tickets.")

            if ticketType == '0':
                return tk.messagebox.showwarning("Warning",f"Please select a ticket type.")

            ticketType = str(ticketType).replace('1', "vipCapacity").replace('2', "lowerCapacity").replace('3', "upperCapacity")

            for i in films:
                if i.getFilmName() == filmName:
                    showings = i.getShowings()

            for i in showings:
                time = datetime.datetime.fromtimestamp(i.getShowingTime())
                if time.strftime("%H:%M") == showingTime:
                    showing = i

            try:
                result = showing.checkAvailability(noOfCustomer, ticketType, userE.currentCinema)
            except Exception as e:
                userE.available_ticket = False
                availability_label.config(text=f"Availablility: ")
                price.config(text=f"Price:")
                return tk.messagebox.showwarning("Warning",f"Film unavailable!")

            if result['result'] == False:
                userE.available_ticket = False
                availability_label.config(text=f"Availablility: ")
                price.config(text=f"Price:")
                return tk.messagebox.showwarning("Warning",f"Film unavailable!")
            else:
                userE.available_ticket = True
                availability_label.config(text=f"Availablility: ✅")
                price.config(text=f"Price: £{result['price']}")

        def update_options(option_menu, selected_value, options):

            option_menu['menu'].delete(0, 'end')

            for option in options:
                option_menu['menu'].add_command(label=option, command=lambda value=option: selected_value.set(value))

            if len(options) <= 0:
                userE.available_ticket = False
                availability_label.config(text=f"Availablility: ")
                price.config(text=f"Price:")
                showing_var.set('No Showings')

        name_frame = tk.Frame(frame_category2)
        name_frame.pack()
        name_label = tk.Label(name_frame, text="Name : ")
        name_label.pack(side="left")
        name_entry = tk.Entry(name_frame)
        name_entry.pack(side="right")

        phone_frame = tk.Frame(frame_category2)
        phone_frame.pack()
        phone_label = tk.Label(phone_frame, text="Phone : ")
        phone_label.pack(side="left")
        phone_entry = tk.Entry(phone_frame)
        phone_entry.pack(side="right")

        email_frame = tk.Frame(frame_category2)
        email_frame.pack()
        email_label = tk.Label(email_frame, text="Email : ")
        email_label.pack(side="left")
        email_entry = tk.Entry(email_frame)
        email_entry.pack(side="right")

        card_frame = tk.Frame(frame_category2)
        card_frame.pack()
        card_label = tk.Label(card_frame, text="Card # : ")
        card_label.pack(side="left")
        card_entry = tk.Entry(card_frame)
        card_entry.pack(side="right")

        cvv_frame = tk.Frame(frame_category2)
        cvv_frame.pack()
        cvv_label = tk.Label(cvv_frame, text="CVV : ")
        cvv_label.pack(side="left")
        cvv_entry = tk.Entry(cvv_frame)
        cvv_entry.pack(side="right")

        expiry_frame = tk.Frame(frame_category2)
        expiry_frame.pack()
        expiry_label = tk.Label(expiry_frame, text="Expiry : ")
        expiry_label.pack(side="left")
        expiry_month_entry = tk.Entry(expiry_frame, width=3)
        expiry_month_entry.pack(side="left")
        expiry_label = tk.Label(expiry_frame, text=" : ")
        expiry_label.pack(side="left")
        expiry_year_entry = tk.Entry(expiry_frame, width=5)
        expiry_year_entry.pack(side="left")

        book_now_button = tk.Button(frame_category2, text="Book Now", command=lambda: book_now_command())
        book_now_button.pack(side="right")

        frame_category3 = tk.Frame(self)
        frame_category3.pack()

        receipt_text = tk.Text(frame_category3, width=30, height=15, font=("Arial", 12))
        receipt_text.config(state='disabled')
        receipt_text.pack(side="right")

        def update_receipt():
            ticket_str = ""

            date = calendar.get_date()
            film = film_var.get()
            showing = showing_var.get()
            ticket = ticket_type.get()
            if ticket == 1:
                ticket_str = "VIP"
            elif ticket == 2:
                ticket_str = "Lower"
            elif ticket == 3:
                ticket_str = "Upper"
            name = name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            card = card_entry.get()
            cvv = cvv_entry.get()
            expiry_month = expiry_month_entry.get()
            expiry_year = expiry_year_entry.get()
            numOfTickets = customer_input.get()

            receipt_text.config(state='normal')
            receipt_text.delete("1.0", "end")
            receipt_text.insert("1.0", f"Date: {date}\n")
            receipt_text.insert("end", f"Film: {film}\n")
            receipt_text.insert("end", f"Showing: {showing}\n")
            receipt_text.insert("end", f"Ticket: {ticket_str}\n")
            receipt_text.insert("end", f"Number of tickets: {numOfTickets}\n\n")
            receipt_text.insert("end", f"Name: {name}\n")
            receipt_text.insert("end", f"Phone: {phone}\n")
            receipt_text.insert("end", f"Email: {email}\n")
            receipt_text.insert("end", f"Card #: {card}\n")
            receipt_text.insert("end", f"CVV: {cvv}\n")
            receipt_text.insert("end", f"Expiry: {expiry_month}/{expiry_year}\n\n")
            receipt_text.insert("end", f"Reference Id: {refrenceId}\n")
            receipt_text.config(state='disabled')

        def book_now_command():
            update_receipt()
            if userE.available_ticket == False:
                return  tk.messagebox.showwarning("Warning",f"Please click check availability and proceed when it is available.")

            date = calendar.get_date()
            film = film_var.get()
            showing = showing_var.get()
            ticket = ticket_type.get()
            name = name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            card = card_entry.get()
            cvv = cvv_entry.get()
            expiry_month = expiry_month_entry.get()
            expiry_year = expiry_year_entry.get()
            if not(card.isdigit()):
                tk.messagebox.showerror("Error","card # must be a number")
                return
            else: 
                pass
            cvv = cvv_entry.get()
            if not(cvv.isdigit()):
                tk.messagebox.showerror("Error","cvv must be a number")
                return
            else: 
                pass
            expiry_month = expiry_month_entry.get()
            if not(expiry_month.isdigit()):
                tk.messagebox.showerror("Error","month must be a number")
                return
            elif int(expiry_month)<1 or int(expiry_month)>12:
                tk.messagebox.showerror("Error","month must be between 1 and 12")
                return
            else: 
                pass
            expiry_year = expiry_year_entry.get()
            if not(expiry_year.isdigit()):
                tk.messagebox.showerror("Error","year must be a number")
                return
            else: 
                pass
            ques = { "date": date, "film": film, "showing": showing, "ticket type": ticket, "name": name, "phone": phone, "email": email, "card": card, "cvv": cvv, "expiry month": expiry_month, "expiry year": expiry_year }

            for i in ques:
                if len(str(ques.get(i))) < 1 or ques.get(i) == '0':
                    return  tk.messagebox.showwarning("Warning",f"Please enter {i}.")

            if (customer_input.get().isdigit() == True and int(customer_input.get()) in range(1, 41)) == False:
                return  tk.messagebox.showwarning("Warning",f"Please enter a number between 1 to 40 for the # of tickets.")

            showings = None
            showing = None
            filmName = film_var.get()
            showingTime = showing_var.get()
            noOfCustomer = customer_input.get()
            ticketType = ticket_type.get()
            date = calendar.get()
            ticketType = str(ticketType).replace('1', "vipCapacity").replace('2', "lowerCapacity").replace('3', "upperCapacity")
            for i in films:
                if i.getFilmName() == filmName:
                    showings = i.getShowings()

            for i in showings:
                time = datetime.datetime.fromtimestamp(i.getShowingTime())
                if time.strftime("%H:%M") == showingTime:
                    showing = i

            staffId = userE.userName
            if userE.bookingStaff is not None:
                staffId = userE.bookingStaff.getID()

            result = showing.addBooking(create_timestamp(date, showingTime), noOfCustomer, ticketType, showingTime, staffId, refrenceId, price.cget('text'))

            if result == True:
                if userE.bookingStaff is not None:
                    staffId = userE.bookingStaff.increaseBookings()
                tk.messagebox.showinfo("Success",f"Your booking has been completed.")
            else:
                tk.messagebox.showerror("Error",f"An error occured. Please try again!")

        def create_timestamp(date_str, time_str):

            date = datetime.datetime.strptime(date_str, '%d/%m/%y')
            time = datetime.datetime.strptime(time_str, '%H:%M')

            time = datetime.time(time.hour, time.minute)

            dt = datetime.datetime.combine(date, time)

            timestamp = dt.timestamp()

            return timestamp

        calendar.bind("<<DateEntrySelected>>", lambda event: on_date_change())
        film_var.trace("w", lambda *args: update_receipt())
        showing_var.trace("w", lambda *args: update_receipt())
        ticket_type.trace("w", lambda *args: update_receipt())

        name_entry.bind("<<Modified>>", update_receipt)
        phone_entry.bind("<<Modified>>", update_receipt)
        email_entry.bind("<<Modified>>", update_receipt)
        card_entry.bind("<<Modified>>", update_receipt)
        cvv_entry.bind("<<Modified>>", update_receipt)
        expiry_month_entry.bind("<<Modified>>", update_receipt)
        expiry_year_entry.bind("<<Modified>>", update_receipt)
        customer_input.bind("<<Modified>>", update_receipt)


class CancelBooking(EmployeeWindows):
    def __init__(self, **kwargs):
        self.name = 'cancelbooking'
        EmployeeWindows.__init__(self, **kwargs)

        label = tk.Label(self, text="Enter the reference ID of the booking you want to cancel:")
        label.pack()

        entry = tk.Entry(self)
        entry.pack()

        def submit():

            ref_id = entry.get()

            if(len(ref_id) == 0):
                return  tk.messagebox.showwarning("Warning","Please enter a reference ID.")

            result = tk.messagebox.askyesno("Confirm Cancellation", f"Are you sure you want to cancel the booking with reference ID : {ref_id} ?")

            if result:
                bookings = userE.currentCinema.getBookings()
                booking = None

                for i in bookings:
                    if i.getReferenceId() == ref_id:
                        booking = i

                if booking is not None:
                    deleteBooking = booking.deleteBooking()

                if booking is not None and deleteBooking == True:
                    tk.messagebox.showinfo("Confirmation", "The item with reference ID " + ref_id + " has been cancelled.")
                else:
                    tk.messagebox.showerror("Error", "Invalid reference id.")

        button = tk.Button(self, text="Submit", command=submit)
        button.pack()

class ManageFilms(EmployeeWindows):
    def __init__(self, **kwargs):
        self.name = 'managefilms'
        EmployeeWindows.__init__(self, **kwargs)

        cinema = userE.currentCinema
        films = cinema.getFilms()

        search_frame = tk.Frame(self)
        search_frame.pack(side="top", fill="x")

        def new_film():

            new_window = tk.Toplevel(self)
            new_window.title("New Film")

            film_name_label = tk.Label(new_window, text="Film Name:")
            film_description_label = tk.Label(new_window, text="Film Description:")
            film_genre_label = tk.Label(new_window, text="Film Genre:")
            film_rating_label = tk.Label(new_window, text="Film Rating:")
            actorDetails_label = tk.Label(new_window, text="Actor Details:")
            age_label = tk.Label(new_window, text="Age:")

            film_name_entry = tk.Entry(new_window)
            film_description_entry = tk.Entry(new_window)
            film_genre_entry = tk.Entry(new_window)
            film_rating_entry = tk.Entry(new_window)
            actorDetails_entry = tk.Entry(new_window)
            age_label_entry = tk.Entry(new_window)

            confirm_button = tk.Button(new_window, text="Confirm", command=lambda: confirm(new_window, film_name_entry, film_description_entry, film_genre_entry, film_rating_entry, actorDetails_entry, age_label_entry))
            cancel_button = tk.Button(new_window, text="Cancel", command=new_window.destroy)

            film_name_label.pack()
            film_name_entry.pack()
            film_description_label.pack()
            film_description_entry.pack()
            film_genre_label.pack()
            film_genre_entry.pack()
            film_rating_label.pack()
            film_rating_entry.pack()
            actorDetails_label.pack()
            actorDetails_entry.pack()
            age_label.pack()
            age_label_entry.pack()
            confirm_button.pack(side="left")
            cancel_button.pack(side="right")

        def confirm(new_window, film_name_entry, film_description_entry, film_genre_entry, film_rating_entry, actorDetails_entry, age_label_entry):

            film_name = film_name_entry.get()
            film_description = film_description_entry.get()
            film_genre = film_genre_entry.get()
            film_rating = film_rating_entry.get()
            actor_details = actorDetails_entry.get()
            age = age_label_entry.get()

            film = database.Film(cinema.getCity(), cinema.getLocation(), film_name, film_description, actor_details, film_genre, age, film_rating, self.db.getdb())

            film_details = tk.Frame(film_frame, relief="solid", borderwidth=1)
            film_details.pack(side="top", fill="both", expand=True)

            film_details.columnconfigure(0, weight=1)
            film_details.rowconfigure(0, weight=1)
            film_details.rowconfigure(1, weight=1)
            film_details.rowconfigure(2, weight=1)
            film_details.rowconfigure(3, weight=1)
            film_details.rowconfigure(4, weight=1)

            filmCategory = tk.Frame(film_details)
            frameCategory1 = tk.Frame(filmCategory)

            film_name_label = tk.Label(frameCategory1, text=f"Film Name: {film_name}")
            film_name_label.pack()
            film_description_label = tk.Label(frameCategory1, text=f"Film Description: {film_description}")
            film_description_label.pack()
            film_genre_label = tk.Label(frameCategory1, text=f"Film Genre: {film_genre}")
            film_genre_label.pack()
            film_rating_label = tk.Label(frameCategory1, text=f"Film Rating: {film_rating}")
            film_rating_label.pack()

            frameCategory2 = tk.Frame(filmCategory)

            edit_button = tk.Button(frameCategory2, text="Edit", command=lambda film_details=film_details, film_name_label=film_name_label, film_description_label=film_description_label, film_genre_label=film_genre_label, film_rating_label=film_rating_label: edit(film_details, film_name_label, film_description_label, film_genre_label, film_rating_label, film))
            edit_button.pack()
            delete_button = tk.Button(frameCategory2, text="Delete", command=lambda film_details=film_details: delete(film_details, film))
            delete_button.pack()

            filmCategory.pack(side="top")
            frameCategory1.pack(side="left")
            frameCategory2.pack(side="right")

            showingsCategory = tk.Frame(film_details)
            showtimes_frame = tk.Frame(showingsCategory)
            showtimes_frame.pack(side="left")

            showtimes_box = tk.Frame(showtimes_frame)
            showtimes_box.pack()

            if not(film_rating.isdigit()):
                tk.messagebox.showerror("Error","Rating must be a NUMBER between 0 and 5")
                return
            elif int(film_rating) <0 or int(film_rating)>5:
                tk.messagebox.showerror("Error","Rating must be a NUMBER between 0 and 5")
                return

            film.saveFilm()

            showingsCategory.pack(side="bottom")
            newShowingButton = tk.Button(showingsCategory, text=f"New Showtime", command=functools.partial(new_showing, cinema.getScreens(), film)).pack(side="left", padx=4)

            new_window.destroy()

        new_button = tk.Button(search_frame, text="New Film", command= new_film)
        new_button.pack(side="right")

        details_frame = tk.Frame(self)
        details_frame.pack(side="top", fill="both", expand=True)

        scrollbar = tk.Scrollbar(details_frame)
        scrollbar.pack(side="right", fill="y")

        canvas = tk.Canvas(details_frame, yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=canvas.yview)

        film_frame = tk.Frame(canvas)

        canvas.create_window((0,0), window=film_frame, anchor="nw")

        film_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        def edit(film_details, film_name_label, film_description_label, film_genre_label, film_rating_label, film):

            edit_window = tk.Toplevel(self)
            edit_window.title("Edit Film")

            film_name = film_name_label.cget("text")
            film_description = film_description_label.cget("text")
            film_genre = film_genre_label.cget("text")
            film_rating = film_rating_label.cget("text")

            film_name_label2 = tk.Label(edit_window, text="Film Name:")
            film_description_label2 = tk.Label(edit_window, text="Film Description:")
            film_genre_label2 = tk.Label(edit_window, text="Film Genre:")
            film_rating_label2 = tk.Label(edit_window, text="Film Rating:")

            film_name_entry = tk.Entry(edit_window)
            film_name_entry.insert(0, film_name)
            film_description_entry = tk.Entry(edit_window)
            film_description_entry.insert(0, film_description)
            film_genre_entry = tk.Entry(edit_window)
            film_genre_entry.insert(0, film_genre)
            film_rating_entry = tk.Entry(edit_window)
            film_rating_entry.insert(0, film_rating)

            confirm_button = tk.Button(edit_window, text="Confirm", command=lambda: confirm_edit(edit_window, film_details, film_name_label, film_description_label, film_genre_label, film_rating_label, film_name_entry, film_description_entry, film_genre_entry, film_rating_entry, film))
            cancel_button = tk.Button(edit_window, text="Cancel", command=edit_window.destroy)

            film_name_label2.pack()
            film_name_entry.pack()
            film_description_label2.pack()
            film_description_entry.pack()
            film_genre_label2.pack()
            film_genre_entry.pack()
            film_rating_label2.pack()
            film_rating_entry.pack()
            confirm_button.pack(side="left")
            cancel_button.pack(side="right")

        def confirm_edit(edit_window, film_details, film_name_label, film_description_label, film_genre_label, film_rating_label, film_name_entry, film_description_entry, film_genre_entry, film_rating_entry, film):

            film_name = film_name_entry.get()
            film_description = film_description_entry.get()
            film_genre = film_genre_entry.get()
            film_rating = film_rating_entry.get()

            film_name_label.config(text=film_name)
            film_description_label.config(text=film_description)
            film_genre_label.config(text=film_genre)
            film_rating_label.config(text=film_rating)

            cinema.editFilms(film, film_name, film_description, film_genre, film_rating)

            edit_window.destroy()

        def delete(film_details, film):
            cinema.removeFilm(film)                

            film_details.pack_forget()
            film_details.destroy()

        def show_modal(showtime, seats, screen_number, button, time, film, showing):

            modal = tk.Toplevel(self)
            modal.title("Showtime Details")

            showtime_label = tk.Label(modal, text=f"Showtime: {showtime}")
            seats_label = tk.Label(modal, text=f"Seats: {seats}")
            screen_label = tk.Label(modal, text=f"Screen: {screen_number}")

            time_label = tk.Label(modal, text=f"Date: {time}")

            delete_button = tk.Button(modal, text="Delete", command=lambda: delete_showtime(modal, button, film, showing))

            showtime_label.pack()
            seats_label.pack()
            screen_label.pack()

            time_label.pack()

            time_label.pack()
            delete_button.pack(side="right")

        def delete_showtime(modal, showtime, film, showing):

            cinema.removeShowing(film, showing)

            showtime.pack_forget()
            showtime.destroy()

            modal.destroy()

        def confirm_new_showtime(modal, screen_var, time_var, calendar_var, film, showings):
            screen = screen_var.get()
            time = time_var.get()
            calendar_var = calendar_var.get()
            Screen = None

            combined_string = f"{time} {calendar_var}"

            datetime_object = datetime.datetime.strptime(combined_string, "%H:%M %d/%m/%y")

            unix_timestamp = datetime_object.timestamp()

            for i in showings:
                if (f"Screen {i.getScreenNumber()}" == screen):
                    Screen = i

            if not screen or not time or not calendar_var:
                return tk.messagebox.showerror('Error', "Please complete the form!")
            elif Screen is None:
                return tk.messagebox.showerror('Error', "Select another screen!")

            cinema.addShowing(film, unix_timestamp, Screen)
            modal.destroy()
            self.name = '0'
            self.ManageFilms()

        def new_showing(showings, film):
            screens = []
            for i in showings:
                screens.append(f"Screen {i.getScreenNumber()}")

            modal = tk.Toplevel(self)
            modal.title("Add New Showing")

            screen_var = tk.StringVar(modal)
            screen_label = tk.Label(modal, text="Select Screen:")
            screen_menu = tk.OptionMenu(modal, screen_var, 'Select a screen', *screens)
            screen_label.pack()
            screen_menu.pack()

            time_options = []
            for hour in range(8, 24):
                for minute in ["00", "30"]:
                    time = f"{hour:02}:{minute}"
                    time_options.append(time)

            time_var = tk.StringVar(modal)
            time_var.set("08:00")
            time_label = tk.Label(modal, text="Select Time:")
            time_menu = tk.OptionMenu(modal, time_var, *time_options)
            time_label.pack()
            time_menu.pack()

            calendar_label = tk.Label(modal, text="Select a date : ")
            calendar_label.pack()
            calendar = DateEntry(modal, width=12, background='darkblue', foreground='white', borderwidth=2)
            calendar.pack()

            button_frame = tk.Frame(modal)
            button_frame.pack(pady=5)
            ok_button = tk.Button(button_frame, text="Confirm", command= lambda: confirm_new_showtime(modal, screen_var, time_var, calendar, film, showings))
            ok_button.pack(side="right")

        for i, film in enumerate(films):

            film_details = tk.Frame(film_frame, relief="solid", borderwidth=1)
            film_details.pack(side="top", fill="both", expand=True)

            film_details.columnconfigure(0, weight=1)
            film_details.rowconfigure(0, weight=1)
            film_details.rowconfigure(1, weight=1)
            film_details.rowconfigure(2, weight=1)
            film_details.rowconfigure(3, weight=1)
            film_details.rowconfigure(4, weight=1)

            filmCategory = tk.Frame(film_details)
            frameCategory1 = tk.Frame(filmCategory)

            film_name_label = tk.Label(frameCategory1, text=f"Film Name: {film.getFilmName()}")
            film_name_label.pack()
            film_description_label = tk.Label(frameCategory1, text=f"Film Description: {film.getDescription()}")
            film_description_label.pack()
            film_genre_label = tk.Label(frameCategory1, text=f"Film Genre: {film.getFilmGenre()}")
            film_genre_label.pack()
            film_rating_label = tk.Label(frameCategory1, text=f"Film Rating: {film.getRating()}")
            film_rating_label.pack()

            frameCategory2 = tk.Frame(filmCategory)

            edit_button = tk.Button(frameCategory2, text="Edit", command=lambda film_details=film_details, film_name_label=film_name_label, film_description_label=film_description_label, film_genre_label=film_genre_label, film_rating_label=film_rating_label: edit(film_details, film_name_label, film_description_label, film_genre_label, film_rating_label, film))
            edit_button.pack()
            delete_button = tk.Button(frameCategory2, text="Delete", command=lambda film_details=film_details: delete(film_details, film))
            delete_button.pack()

            filmCategory.pack(side="top")
            frameCategory1.pack(side="left")
            frameCategory2.pack(side="right")

            showingsCategory = tk.Frame(film_details)
            showtimes_frame = tk.Frame(showingsCategory)
            showtimes_frame.pack(side="left")

            showtimes_box = tk.Frame(showtimes_frame)
            showtimes_box.pack()

            for ii, showing in enumerate(film.getShowings()):
                dt = datetime.datetime.fromtimestamp(showing.getShowingTime())
                hour = dt.strftime("%H:%M")
                date = dt.strftime('%Y-%m-%d')
                seating = showing.getSeatsLeft()
                seat = 0
                for i in seating:
                    seat = int(seat) + int(seating.get(i))
                showtime1_button = tk.Button(showtimes_box, text=f"{hour} ({seat} seats left)")
                showtime1_button.pack(side="left")
                showtime1_button.config( command=functools.partial(show_modal, f"{hour}", seat, showing.getScreenNumber(), showtime1_button, date, film, showing))

                if (ii+1) % 2 == 0:
                    showtimes_box.pack()
                    showtimes_box = tk.Frame(showtimes_frame)
                    showtimes_box.pack()

            showingsCategory.pack(side="bottom")
            newShowingButton = tk.Button(showingsCategory, text=f"New Showtime", command=functools.partial(new_showing, cinema.getScreens(), film)).pack(side="left", padx=4)

class GenerateReports(EmployeeWindows):
    def __init__(self, **kwargs):
        self.name = 'generatereports'
        EmployeeWindows.__init__(self, **kwargs)

        label = tk.Label(text="Select an option below to generate a report:")
        label.pack()

        button_frame = tk.Frame(self)
        button_frame.pack(side="top", fill="x", padx=5)

        bookings_by_listings_button = tk.Button(button_frame, text="Number of Bookings by Listings", command= lambda: show_modal(self.db.numOfBookings(), "Number of Bookings by Listings"))
        bookings_by_listings_button.pack(side="top", fill="x")

        revenue_button = tk.Button(button_frame, text="Revenue", command= lambda: show_modal(self.db.revenue(), "Revenue"))
        revenue_button.pack(side="top", fill="x")

        bookings_by_staff_button = tk.Button(button_frame, text="Number of Bookings by Staff", command= lambda: show_modal(self.db.staffBookings(), "Number of Bookings by Staff"))
        bookings_by_staff_button.pack(side="top", fill="x")

        def show_modal(info, title):
            window = tk.Toplevel(self)

            report_text = tk.Text(window, width=30, height=len(info)+6, font=("Arial", 12))
            report_text.pack()

            report_text.config(state='normal')
            report_text.insert('end', f"{title}\n\n")
            for i in info:
                report_text.insert("end", f"{i}\n")

            report_text.config(state='disabled')

class ManageCinemas(EmployeeWindows):
    def __init__(self, **kwargs):
        self.name = 'managecinemas'
        EmployeeWindows.__init__(self, **kwargs)

        search_frame = tk.Frame(self)
        search_frame.pack(side="top", fill="x")

        new_button = tk.Button(search_frame, text="New City")
        new_button.pack(side="right")

        details_frame = tk.Frame(self)
        details_frame.pack(side="top", fill="both", expand=True)

        scrollbar = tk.Scrollbar(details_frame)
        scrollbar.pack(side="right", fill="y")

        canvas = tk.Canvas(details_frame, yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=canvas.yview)

        film_frame = tk.Frame(canvas)

        new_button.config(command=lambda: newCity(film_frame))

        canvas.create_window((0,0), window=film_frame, anchor="nw")

        film_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        list_of_city = {}
        list_of_city_frames = {}
        list_of_cinema = {}

        def delete_city(index, cityName):
            city = list_of_city_frames[index]
            result = tk.messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the city : {cityName} ?")
            if result:
                self.db.removeCity(cityName)
                city.pack_forget()
                city.destroy()

        cities = self.db.getJSONcities()

        def delete_cinema(screens, showtime1_button, city, location, morning_price, afternoon_price, evening_price):
            window = tk.Toplevel(self)

            screens_frames = []

            morning_label = tk.Label(window, text="Morning Price")
            morning_label.pack()
            morning_entry = tk.Entry(window)
            morning_entry.insert('end', morning_price)
            morning_entry.pack()

            afternoon_label = tk.Label(window, text="Afternoon Price")
            afternoon_label.pack()
            afternoon_price_entry = tk.Entry(window)
            afternoon_price_entry.insert('end', afternoon_price)
            afternoon_price_entry.pack()

            evening_label = tk.Label(window, text="Evening Price")
            evening_label.pack()
            evening_entry = tk.Entry(window)
            evening_entry.insert('end', evening_price)
            evening_entry.pack()

            screens_frame = tk.Frame(window)
            screens_frame.pack(side="top", fill="x")

            def on_edit(screens, index, seat_count, a, b, c):
                screens[index] = { 'seats': seat_count.get(), 'screen': screens[index]['screen']}

            def delete_screen(screen_index, screen_frame):

                if screens_frames:

                    screens.pop(screen_index)
                    screens_frames.pop(screen_index)

                    screen_frame.destroy()

                i = len(screens) - 1
                while i >= 0:

                    screen = screens[i]
                    screen_frame = screens_frames[i]

                    delete_button = screen_frame.winfo_children()[0]
                    delete_button.config(command=functools.partial(delete_screen, i, screen_frame))

                    screen_label = screen_frame.winfo_children()[1]
                    screen_label.config(text=f"Screen {screen['screen']}:")

                    seat_count = screen_frame.winfo_children()[2]

                    i -= 1

            def new_screen():

                screen_number = random.randint(1, len(screens) + 1)
                while any(screen['screen'] == screen_number for screen in screens):
                    screen_number = random.randint(1, len(screens) + 1)

                new_screen = {'screen': screen_number, 'seats': 50}

                screens.append(new_screen)

                screen_frame = tk.Frame(screens_frame)
                screen_frame.pack()

                delete_button = tk.Button(screen_frame, text="🗑️", command=functools.partial(delete_screen, len(screens) - 1, screen_frame))
                delete_button.pack(side="left")

                screen_label = tk.Label(screen_frame, text=f"Screen {new_screen['screen']}:")
                screen_label.pack(side="left")

                seat_count = tk.StringVar(screen_frame)
                seat_count.set(new_screen['seats'])
                seat_count_menu = tk.OptionMenu(screen_frame, seat_count, *range(50, 121, 10))
                seat_count_menu.pack(side="left")
                seat_count.trace("w", functools.partial(on_edit, screens, len(screens)-1, seat_count))

                screens_frames.append(screen_frame)

            for i, screen in enumerate(screens):
                screen_frame = tk.Frame(screens_frame)
                screen_frame.pack()

                delete_button = tk.Button(screen_frame, text="🗑️", command=functools.partial(delete_screen, i, screen_frame))
                delete_button.pack(side="left")

                screen_label = tk.Label(screen_frame, text=f"Screen {screen['screen']}:")
                screen_label.pack(side="left")

                seat_count = tk.StringVar(screen_frame)
                seat_count.set(screen['seats'])
                seat_count_menu = tk.OptionMenu(screen_frame, seat_count, *range(50, 121, 10))
                seat_count_menu.pack(side="left")
                seat_count.trace("w", functools.partial(on_edit, screens, i, seat_count))

                screens_frames.append(screen_frame)

            new_screen_frame = tk.Frame(window)
            new_screen_frame.pack(side="top", fill="x")

            new_screen_button = tk.Button(screens_frame, text="New Screen", command=new_screen)
            new_screen_button.pack(side="bottom")

            save_delete_frame = tk.Frame(window)
            save_delete_frame.pack(side="bottom", fill="x")

            save_changes_button = tk.Button(save_delete_frame, text="Save Changes", command=lambda: save_changes_cinema(screens))
            save_changes_button.pack(side="left")

            delete_cinema_button = tk.Button(save_delete_frame, text="Delete Cinema", command=lambda: confirm_delete_cinema(showtime1_button))
            delete_cinema_button.pack(side="right")

            def save_changes_cinema(screens):
                for i in userE.currentCity.getCinemas():
                    if i.getLocation() == location:
                        i.saveChanges(screens, morning_entry.get(),afternoon_price_entry.get(), evening_entry.get())
                        window.destroy()

            def confirm_delete_cinema(showtime1_button):
                result = tk.messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the Cinema : {showtime1_button.cget('text')} ?")
                if result:
                    self.db.deleteCinema(city, location)
                    showtime1_button.pack_forget()
                    showtime1_button.destroy()
                    window.destroy()

        def newCinema(city):
            def numOnly(string):
                if string.isdigit() == False:
                    tk.messagebox.showerror('Error', 'You must enter a digit !')
                    return False
                else:
                    return True
            name = simpledialog.askstring("New Cinema", "Enter the new cinema name:")
            if name:
                morning_price = simpledialog.askstring("Price", "Enter the morning price:")
                if morning_price and numOnly(morning_price):
                    afternoon_price = simpledialog.askstring("Price", "Enter the afternoon price:")
                    if afternoon_price and numOnly(afternoon_price):
                        evening_price = simpledialog.askstring("Price", "Enter the evening price:")
                        if evening_price and numOnly(evening_price):
                            self.db.addNewCinema(city, name, morning_price, afternoon_price, evening_price)
                            self.name = '0'
                            self.ManageCinemas()

        def newCity(film_frame):
            result = simpledialog.askstring("New Cinema", "Enter the new cinema name:")
            if result:
                self.db.addCity(result)
                film_details = tk.Frame(film_frame, relief="solid", borderwidth=1)
                film_details.pack(side="top", fill="both", expand=True)
                list_of_city_frames[len(list_of_city_frames)] = film_details

                filmCategory = tk.Frame(film_details)
                frameCategory1 = tk.Frame(filmCategory)

                film_name_label = tk.Label(frameCategory1, text=f"City Name: {result}")
                list_of_city[len(list_of_city_frames)] = film_name_label
                film_name_label.pack()

                frameCategory2 = tk.Frame(filmCategory)

                delete_button = tk.Button(frameCategory2, text="Delete", command=functools.partial(delete_city, len(list_of_city_frames)-1, result))
                delete_button.pack()

                filmCategory.pack(side="top")
                frameCategory1.pack(side="left")
                frameCategory2.pack(side="right")

                showingsCategory = tk.Frame(film_details)
                showtimes_frame = tk.Frame(showingsCategory)
                showtimes_frame.pack(side="right")

                showtimes_box = tk.Frame(showtimes_frame)
                showtimes_box.pack()

                showingsCategory.pack(side="bottom", pady=5)
                newShowingButton = tk.Button(showingsCategory, text=f"New Cinema", command=functools.partial(newCinema, result)).pack(side="left", padx=4)

        for i, city in enumerate(cities):

            film_details = tk.Frame(film_frame, relief="solid", borderwidth=1)
            film_details.pack(side="top", fill="both", expand=True)
            list_of_city_frames[i] = film_details

            film_details.columnconfigure(0, weight=1)
            film_details.rowconfigure(0, weight=1)
            film_details.rowconfigure(1, weight=1)
            film_details.rowconfigure(2, weight=1)
            film_details.rowconfigure(3, weight=1)
            film_details.rowconfigure(4, weight=1)

            filmCategory = tk.Frame(film_details)
            frameCategory1 = tk.Frame(filmCategory)

            film_name_label = tk.Label(frameCategory1, text=f"City Name: {city['city']}")
            list_of_city[i] = film_name_label
            film_name_label.pack()

            frameCategory2 = tk.Frame(filmCategory)

            delete_button = tk.Button(frameCategory2, text="Delete", command=functools.partial(delete_city, i, city['city']))
            delete_button.pack()

            filmCategory.pack(side="top")
            frameCategory1.pack(side="left")
            frameCategory2.pack(side="right")

            showingsCategory = tk.Frame(film_details)
            showtimes_frame = tk.Frame(showingsCategory)
            showtimes_frame.pack(side="right")

            showtimes_box = tk.Frame(showtimes_frame)
            showtimes_box.pack()

            showingsCategory.pack(side="bottom", pady=5)
            newShowingButton = tk.Button(showingsCategory, text=f"New Cinema", command=functools.partial(newCinema, city['city'])).pack(side="left", padx=4)

            for ii, cinema in enumerate(city['cinemas']):
                showtime1_button = tk.Button(showtimes_box, text=f"Cinema {cinema['location']}")
                showtime1_button.config(command=functools.partial(delete_cinema, cinema['screens'], showtime1_button, city['city'], cinema['location'], cinema['morning_price'], cinema['afternoon_price'] ,cinema['evening_price']))
                showtime1_button.pack(side="left")

                if (ii+1) % 2 == 0:
                    showtimes_box.pack()
                    showtimes_box = tk.Frame(showtimes_frame)
                    showtimes_box.pack()

app = LoginPage()
app.mainloop()