import pymongo
import datetime

class City:
    def __init__(self, city, db):
        self.__city = city
        self.__db = db
        self.__cinemas = self.getCinemas()

    def getCity(self):
        return self.__city

    def getCinemas(self):
        cursor = self.__db.cinemas.find({ "city": self.__city })
        cinemas = []

        for doc in cursor:
            city = doc["city"]
            location = doc["location"]
            morning_price = doc["morning_price"]
            afternoon_price = doc["afternoon_price"]
            evening_price = doc["evening_price"]
            cinema = Cinema(city, location, morning_price, afternoon_price, evening_price, self.__db)
            cinemas.append(cinema)

        return cinemas

    def addNewCinema(self, location, morning_price, afternoon_price, evening_price):
        cinema = Cinema(self.__city, location, morning_price, afternoon_price, evening_price, self.__db)
        result = cinema.saveCinema()

        if result == True:
            self.__cinemas.append(cinema)
        else:
            raise ValueError("Failed to add item to list in object")

        return cinema

    def addcinema(self, cinema):
        self.__cinemas.append(cinema)

    def removeCinema(self, cinema):
        result = cinema.deleteCinema()

        if result == True:
            for i, cinemaa in enumerate(self.__cinemas):
                if cinemaa.getLocation() == cinema.getLocation():
                    self.__cinemas.pop(i)
        else:
            raise ValueError("Failed to remove item from the list in object")

        return cinema

    def findCinema(self, location, morning_price, afternoon_price, evening_price):
        for cinema in self.__cinemas:
            if cinema.getLocation() == location:
                if cinema.getMorningPrice() == morning_price:
                    if cinema.getAfternoonPrice() == afternoon_price:
                        if cinema.getEveningPrice() == evening_price:
                            return cinema

        return None

    def saveCity(self):
        result = self.__db.cities.insert_one({ "name": self.__city })
        if result.acknowledged:
            return True
        else:
            return False

    def removeCity(self):
        result = self.__db.cities.delete_one({ "name": self.__city })

        if result.deleted_count == 1:
            return True

class Cinema:
    def __init__(self, city, location, morning_price, afternoon_price, evening_price, db):
        self.__db = db
        self.__city = city
        self.__location = location        
        self.__morning_price = morning_price
        self.__afternoon_price = afternoon_price
        self.__evening_price = evening_price
        self.__films = self.getFilms()
        self.__bookings = self.getBookings()
        self.__screens = self.getScreens()

    def getListings(self, date):
        films = self.getFilms()
        showings_dict = {}

        date1 = datetime.datetime.strptime(date, '%d/%m/%y')

        for film in films:
            for showing in film.getShowings():
                date2 = datetime.datetime.fromtimestamp(showing.getShowingTime())
                if date1.date() == date2.date():
                    seating = showing.getSeatsLeft()
                    seat = 0
                    for i in seating:
                        seat = int(seat) + int(seating.get(i))
                    foundFilm = showings_dict.get(film.getFilmName())
                    if foundFilm:
                        shows = foundFilm['showings'] + [{"time" : datetime.datetime.fromtimestamp(showing.getShowingTime()).strftime("%H:%M"), "seats": seat}]
                        showings_dict.update({film.getFilmName() : {
                            "title": film.getFilmName(),
                            "rating": film.getRating(),
                            "description": film.getDescription(),
                            "actors": film.getActorDetails(),
                            "genre": film.getFilmGenre(),
                            "age": film.getAge(),
                            "showings": shows
                        }})
                    else:
                        seating = showing.getSeatsLeft()
                        seat = 0
                        for i in seating:
                            seat = int(seat) + int(seating.get(i))
                        shows = [{"time" : datetime.datetime.fromtimestamp(showing.getShowingTime()).strftime("%H:%M"), "seats": seat }]
                        showings_dict.update({film.getFilmName() : {
                            "title": film.getFilmName(),
                            "rating": film.getRating(),
                            "description": film.getDescription(),
                            "actors": film.getActorDetails(),
                            "genre": film.getFilmGenre(),
                            "age": film.getAge(),
                            "showings": shows
                        }})

        keys = []

        for i in showings_dict:
            keys.append(showings_dict.get(i))

        return keys

    def getBookings(self):
        cursor = self.__db.bookings.find({ "city": self.__city, "location": self.__location })
        bookings = []
        for doc in cursor:
            booking = Booking(self.__db, doc['date'], doc['movieName'], doc['numberOfCustomer'], doc['ticketType'], doc['showingTime'], doc['bookingStaffId'], doc['city'], doc['location'], doc['referenceId'], doc['price'])
            bookings.append(booking)

        return bookings

    def getCity(self):
        return self.__city

    def getLocation(self):
        return self.__location

    def getMorningPrice(self):
        return self.__morning_price

    def getAfternoonPrice(self):
        return self.__afternoon_price

    def getEveningPrice(self):
        return self.__evening_price

    def getFilms(self):
        films = []
        cursor = self.__db.films.find({ "city": self.__city, "location": self.__location })

        for doc in cursor:
            city = doc["city"]
            location = doc["location"]
            filmName = doc["filmName"]
            description = doc["description"]
            actorDetails = doc["actorDetails"]
            filmGenre = doc["filmGenre"]
            age = doc["age"]
            ratings = doc["rating"]
            film = Film(city, location, filmName, description, actorDetails, filmGenre, age, ratings, self.__db)

            films.append(film)

        return films

    def addFilm(self, filmName, description, actorDetails, filmGenre, age, rating):
        film = Film(self.__city, self.__location, filmName, description, actorDetails, filmGenre, age, rating, self.__db)
        result = film.saveFilm()

        if result == True:
            self.__films.append(film)
        else:
            raise ValueError("Failed to add item to list in object")

        return film

    def saveCinema(self):
        result = self.__db.cinemas.insert_one({ "city": self.__city, "location": self.__location, "morning_price": self.__morning_price, "afternoon_price": self.__afternoon_price, "evening_price": self.__evening_price })

        if result.acknowledged:
            return True
        else:
            return False

    def deleteCinema(self):
        result = self.__db.cinemas.delete_one({ "city": self.__city, "location": self.__location, "morning_price": self.__morning_price, "afternoon_price": self.__afternoon_price, "evening_price": self.__evening_price })

        if result.deleted_count == 1:
            return True

    def addScreen(self, screenNumber, totalCapacity):
        if len(self.__screens) < 6:

            result = Screen.saveScreen(self.__db, screenNumber, totalCapacity, self.__location, self.__city)

            if result['result'] == True:
                self.__screens.append(result['screen'])
            else:
                raise ValueError("Failed to add item to list in object")

    def getScreens(self):    
        cursor = self.__db.screens.find({ "city": self.__city, "location": self.__location })
        screens = []
        for doc in cursor:
            screen = Screen(doc['screenNumber'], self.__db, self.__location, self.__city)
            screens.append(screen)

        return screens

    def saveChanges(self, screens, morning_price, afternoon_price, evening_price):
        new_values = {
            'morning_price': int(morning_price),
            'afternoon_price': int(afternoon_price),
            'evening_price': int(evening_price)
        }

        self.__db.cinemas.update_many({ "location": self.__location, "city": self.__city }, {'$set': new_values})
        self.__db.screens.delete_many({ "city": self.__city, "location": self.__location })

        for i in screens:
            screen = Screen.saveScreen(self.__db, i['screen'], i['seats'], self.__location, self.__city)

    def editFilms(self, Film, name, desc, genre, rating):
        newFilm = Film.editFilm(name, desc, genre, rating)
        for i, film in enumerate(self.__films):
            if film.getFilmName() == name:
                self.__films.pop(i)

        self.__films.append(newFilm)

    def removeFilm(self, Film):
        for i, film in enumerate(self.__films):
            if film.getFilmName() == Film.getFilmName():
                self.__films.pop(i)

        Film.deleteFilm()

    def removeShowing(self, film, showing):
        film.removeShowing(showing)

        for i, film in enumerate(self.__films):
            if film.getFilmName() == film.getFilmName():
                self.__films.pop(i)

    def addShowing(self, Film, showingTime, Screen):
        Film.addShowing(showingTime, Screen)
        for i, film in enumerate(self.__films):
            if film.getFilmName() == Film.getFilmName():
                self.__films.pop(i)

        self.__films.append(Film)

class Film:
    def __init__(self, city, location, filmName, description, actorDetails, filmGenre, age, rating, db):
        self.__db = db
        self.__filmName = filmName
        self.__description = description
        self.__actorDetails = actorDetails
        self.__filmGenre = filmGenre
        self.__age = age
        self.__rating = rating
        self.__city = city
        self.__location = location
        self.__showings = self.getShowings()

    def getFilmName(self):
        return self.__filmName

    def getDescription(self):
        return self.__description

    def getActorDetails(self):
        return self.__actorDetails

    def getFilmGenre(self):
        return self.__filmGenre

    def getAge(self):
        return self.__age

    def getRating(self):
        return self.__rating

    def getCity(self):
        return self.__city

    def getLocation(self):
        return self.__location

    def saveFilm(self):
        result = self.__db.films.insert_one({ "city": self.__city, "location": self.__location, "filmName": self.__filmName, "description": self.__description, "actorDetails": self.__actorDetails, "filmGenre" : self.__filmGenre, "age": self.__age, "rating": self.__rating })

        if result.acknowledged:
            return True
        else:
            return False

    def addShowing(self, showingTime, Screen):
        shows = Showing(self.__db, showingTime, '2h', self.__location, self.__city, self.__filmName, Screen)
        result = shows.saveShows()

        if result == True:
            self.__showings.append(shows)
        else:
            raise ValueError("Failed to add item to list in object")

    def getShowings(self):
        cursor = self.__db.showings.find({ "city": self.__city, "location": self.__location, "filmName": self.__filmName })
        shows = []

        for film in cursor:
            screen = Screen(film["screen"], self.__db, self.__location, self.__city)
            shows.append(Showing(self.__db, film["showingTime"], film["duration"], film["location"], film["city"], film["filmName"], screen))

        return shows

    def editFilm(self, name, desc, genre, rating):
        filter = {"city": self.__city, "location": self.__location, "filmName": self.__filmName }
        update = {"$set": {"filmName": name, "description": desc, "filmGenre": genre, "rating": rating}}
        self.__db.films.update_one(filter, update)
        self.__filmName = name
        self.__description = desc
        self.__rating = rating
        self.__filmGenre = genre

        return self

    def deleteFilm(self):
        self.__db.films.delete_one({ "filmName": self.__filmName, "city": self.__city, "location": self.__location })

    def removeShowing(self, showing):
        showing.deleteShowing()

        for i, shows in enumerate(self.__showings):
            if shows.getShowingTime() == showing.getShowingTime():
                self.__showings.pop(i)

class Showing:
    def __init__(self, db, showingTime, duration, location, city, filmName, Screen):
        self.__db = db
        self.__showingTime = showingTime
        self.__duration = duration
        self.__location = location
        self.__city = city
        self.__filmName = filmName
        self.__Screen = Screen
        self.__bookings = self.getBookings()

    def deleteShowing(self):
        self.__db.showings.delete_one({"city": self.__city, "showingTime": self.__showingTime, "location": self.__location })

    def getScreenNumber(self):
        return self.__Screen.getScreenNumber()

    def getBookings(self):

        cursor = self.__db.bookings.find({ "city": self.__city, "location": self.__location, "movieName": self.__filmName, "date": self.__showingTime })
        bookings = []
        for doc in cursor:
            booking = Booking(self.__db, doc['date'], doc['movieName'], doc['numberOfCustomer'], doc['ticketType'], doc['showingTime'], doc['bookingStaffId'], self.__city, self.__location, doc['referenceId'], doc['price'])
            bookings.append(booking)

        return bookings

    def getSeatsLeft(self):

        lowerCapacity = 0
        upperCapacity = 0
        vipCapacity = 0

        for booking in self.__bookings:
            if booking.getTicketType() == "lowerCapacity":
                lowerCapacity = lowerCapacity + int(booking.getNumberOfCustomer())
            elif booking.getTicketType() == "upperCapacity":
                upperCapacity = upperCapacity + int(booking.getNumberOfCustomer())
            elif booking.getTicketType() == "vipCapacity":
                vipCapacity = vipCapacity + int(booking.getNumberOfCustomer())

        self.__Screen.loadData()

        lowerCapacity = int(self.__Screen.getLowerCapacity()) - lowerCapacity
        upperCapacity = int(self.__Screen.getUpperCapacity()) - upperCapacity
        vipCapacity = int(self.__Screen.getVipCapacity()) - vipCapacity

        return {
            "lowerCapacity": lowerCapacity,
            "upperCapacity": upperCapacity,
            "vipCapacity": vipCapacity
        }

    def getShowingTime(self):
        return self.__showingTime

    def getDuration(self):
        return self.__duration

    def getLocation(self):
        return self.__location

    def getCity(self):
        return self.__city

    def getFilmName(self):
        return self.__filmName

    def checkAvailability(self, noOfCustomers, ticketType, cinema):
        lowerCapacity = 0
        upperCapacity = 0
        vipCapacity = 0

        noOfCustomers= int(noOfCustomers)

        for booking in self.__bookings:
            if booking.getTicketType() == "lowerCapacity":
                lowerCapacity = lowerCapacity + int(booking.getNumberOfCustomer())
            elif booking.getTicketType() == "upperCapacity":
                upperCapacity = upperCapacity + int(booking.getNumberOfCustomer())
            elif booking.getTicketType() == "vipCapacity":
                vipCapacity = vipCapacity + int(booking.getNumberOfCustomer())

        self.__Screen.loadData()

        if ticketType == "lowerCapacity":
            if noOfCustomers <= (int(self.__Screen.getLowerCapacity()) - lowerCapacity):
                return { 'result': True, 'price': self.getPrice(self.checkTime(), noOfCustomers, ticketType,cinema) }
        elif ticketType == "upperCapacity":
            if noOfCustomers <= (int(self.__Screen.getUpperCapacity()) - upperCapacity):
                return { 'result': True, 'price': self.getPrice(self.checkTime(), noOfCustomers, ticketType,cinema) }
        elif ticketType == "vipCapacity":
            if noOfCustomers <= (int(self.__Screen.getVipCapacity()) - vipCapacity):
                return { 'result': True, 'price': self.getPrice(self.checkTime(), noOfCustomers, ticketType,cinema) }

        return { 'result' : False}

    def checkTime(self):
        dt = datetime.datetime.fromtimestamp(self.__showingTime)

        time_str = dt.strftime('%H:%M')

        time1 = datetime.datetime.strptime('08:00', '%H:%M')
        time2 = datetime.datetime.strptime('12:00', '%H:%M')
        time3 = datetime.datetime.strptime(time_str, '%H:%M')

        time4 = datetime.datetime.strptime('12:00', '%H:%M')
        time5 = datetime.datetime.strptime('17:00', '%H:%M')

        if time1 <= time3 <= time2:
            return 'morning'
        elif time4 <= time3 <= time5:
            return 'afternoon'
        else:
            return 'night'

    def getPrice(self, time, people, type,cinema):
        amount = 0
        if time == 'morning':
            amount = cinema.getMorningPrice() * people
        elif time == 'afternoon':
            amount = cinema.getAfternoonPrice() * people
        else:
            amount = cinema.getEveningPrice() * people

        if type == 'vipCapacity':
            amount = amount + ((amount + (amount * 0.2)) * 0.2) + ((amount * 0.2))
        elif type == 'upperCapacity':
            amount = amount + amount * 0.2
        else:
            amount = amount

        return amount

    def saveShows(self):
        result = self.__db.showings.insert_one({ "city": self.__city, "location": self.__location, "filmName": self.__filmName, "screen": self.__Screen.getScreenNumber(), "showingTime": self.__showingTime, "duration": self.__duration })

        if result.acknowledged:
            return True
        else:
            return False

    def addBooking(self, date, numberOfCustomers, ticketType, showingTime, bookingStaffId, referenceId, price):
        booking = Booking(self.__db, date, self.__filmName, numberOfCustomers, ticketType, showingTime, bookingStaffId, self.__city, self.__location, referenceId, price)
        result = booking.saveBooking()

        if result == True:
            self.__bookings.append(booking)
            return True
        else:
            return False

class Screen:
    def __init__(self, screenNumber, db, location, city):
        self.__db = db
        self.__screenNumber = screenNumber
        self.__location = location
        self.__city = city
        self.loadData()
        self.__lowerCapacity = None
        self.__upperCapacity = None
        self.__vipCapacity = None
        self.__totalCapacity = None

    def loadData(self):
        cursor = self.__db.screens.find({ "screenNumber": self.__screenNumber, "city": self.__city, "location": self.__location })
        for doc in cursor:
            self.__totalCapacity = doc["totalCapacity"]

        lowerCapacity = int(self.__totalCapacity) * 0.3
        vipCapacity = 10
        upperCapacity = int(self.__totalCapacity) - lowerCapacity - vipCapacity

        self.__vipCapacity = vipCapacity
        self.__upperCapacity = upperCapacity
        self.__lowerCapacity = lowerCapacity

        return 

    def getTotalCapacity(self):
        return self.__totalCapacity

    def getScreenNumber(self):
        return self.__screenNumber

    def getLowerCapacity(self):
        return self.__lowerCapacity

    def getUpperCapacity(self):
        return self.__upperCapacity

    def getVipCapacity(self):
        return self.__vipCapacity

    @staticmethod
    def saveScreen(db, screenNumber, totalCapacity, location, city):
        lowerCapacity = int(totalCapacity) * 0.3
        vipCapacity = 10
        upperCapacity = int(totalCapacity) - lowerCapacity - vipCapacity

        result = db.screens.insert_one({ "city": city, "location": location, "screenNumber": screenNumber, "lowerCapacity": lowerCapacity, "upperCapacity": upperCapacity, "vipCapacity": vipCapacity, "totalCapacity": totalCapacity })

        if result.acknowledged:
            return {'result': True, 'screen': Screen(screenNumber, db, location, city)}
        else:
            return {'result': False, 'screen': None}

class Booking:
    def __init__(self, db, date, movieName, numberOfCustomer, ticketType, showingTime, bookingStaffId, city, location, referenceId, price):
        self.__db = db
        self.__date = date
        self.__movieName = movieName
        self.__numberOfCustomer = numberOfCustomer
        self.__ticketType = ticketType
        self.__showingTime = showingTime
        self.__bookingStaffId = bookingStaffId
        self.__city = city
        self.__location = location
        self.__referenceId = referenceId
        self.__price = price

    def getPrice(self):
        return self.__price

    def getReferenceId(self):
        return self.__referenceId

    def getDate(self):
        return self.__date

    def getMovieName(self):
        return self.__movieName

    def getNumberOfCustomer(self):
        return self.__numberOfCustomer

    def getTicketType(self):
        return self.__ticketType

    def getShowingTime(self):
        return self.__showingTime

    def getBookingStaffId(self):
        return self.__bookingStaffId

    def getLocation(self):
        return self.__location

    def saveBooking(self):
        string = self.__price
        start = string.index("£") + 1
        end = len(string)
        result = self.__db.bookings.insert_one({ "date": self.__date, "movieName": self.__movieName, "numberOfCustomer": self.__numberOfCustomer, "ticketType": self.__ticketType, "showingTime": self.__showingTime, "bookingStaffId": self.__bookingStaffId, "city": self.__city, "location": self.__location, "referenceId": self.__referenceId, "price": string[start:end] })

        if result.acknowledged:
            return True
        else:
            return False

    def deleteBooking(self):
        result = self.__db.bookings.delete_one({ "date": self.__date, "movieName": self.__movieName, "numberOfCustomer": self.__numberOfCustomer, "ticketType": self.__ticketType, "showingTime": self.__showingTime, "bookingStaffId": self.__bookingStaffId, "city": self.__city, "location": self.__location })

        if result.deleted_count == 1:
            return True
        else:
            return False

class Payment:
    def __init__(self, cardNumber, cardExpiryDate, cardCvv, email, phone, name):
        self.__cardNumber = cardNumber
        self.__cardExpiryDate = cardExpiryDate
        self.__cardCvv = cardCvv
        self.__email = email
        self.__phone = phone
        self.__name = name

    def getCardNumber(self):
        return self.__cardNumber

    def getCardExpiryDate(self):
        return self.__cardExpiryDate

    def getCardCvv(self):
        return self.__cardCvv

    def getEmail(self):
        return self.__email

    def getPhone(self):
        return self.__phone

    def getName(self):
        return self.__name

class BookingReceipt:
    def __init__(self, db, bookingReference, filmName, filmDate, showingTime, screenNumber, numberOfTickets, seatNumber, totalBookingCost, bookingDate):
        self.__bookingReference = bookingReference
        self.__filmName = filmName
        self.__filmDate = filmDate
        self.__showingTime = showingTime
        self.__screenNumber = screenNumber
        self.__numberOfTickets = numberOfTickets
        self.__seatNumber = seatNumber
        self.__totalBookingCost = totalBookingCost
        self.__bookingDate = bookingDate
        self.__db = db

    def getBookingReference(self):
        return self.__bookingReference

    def getFilmName(self):
        return self.__filmName

    def getFilmDate(self):
        return self.__filmDate

    def getShowingTime(self):
        return self.__showingTime

    def getScreenNumber(self):
        return self.__screenNumber

    def getNumberOfTickets(self):
        return self.__numberOfTickets

    def getSeatNumber(self):
        return self.__seatNumber

    def getTotalBookingCost(self):
        return self.__totalBookingCost

    def getBookingDate(self):
        return self.__bookingDate

    def saveBookingReceipt(self):
        result = self.__db.bookings.insert_one({ "bookingReference": self.__bookingReference, "filmName": self.__filmName, "filmDate": self.__filmDate, "showingTime": self.__showingTime, "screenNumber": self.__screenNumber, "numberOfTickets": self.__numberOfTickets, "seatNumber": self.__seatNumber, "totalBookingCost": self.__totalBookingCost, "bookingDate": self.__bookingDate })

        if result.acknowledged:
            return True
        else:
            return False

class BookingStaff:
    def __init__(self, ID, name, email, phoneNumber, db):
        self.__ID = ID
        self.__name = name
        self.__email = email
        self.__phoneNumber = phoneNumber
        self.__db = db
        self.__numberOfBookingsCompleted = self.getNumberOfBookingsCompleted()

    def getID(self):
        return self.__ID

    def getName(self):
        return self.__name

    def getEmail(self):
        return self.__email

    def getPhoneNumber(self):
        return self.__phoneNumber

    def getNumberOfBookingsCompleted(self):
        account = self.__db.bookingStaffs.find_one({ "name" : self.__name, "id": self.__ID })
        if account is None:
            return None
        else:
            return account['numberOfBookingsCompleted']

    def increaseBookings(self):
        result = self.__db.bookingStaffs.update_one({ "id": self.__ID }, { "$inc": { "numberOfBookingsCompleted": 1 } })

        self.__numberOfBookingsCompleted += 1

        return result

    def createAccount(self, password):
        account = self.__db.bookingStaffs.find_one({ "name" : self.__name, "password" : password })
        if account is None:
            result = self.__db.bookingStaffs.insert_one({ "id": self.__ID, "name": self.__name, "email": self.__email, "password": password, "numberOfBookingsCompleted": self.__numberOfBookingsCompleted, "phoneNumber": self.__phoneNumber })
            if result.acknowledged:
                return True
            else:
                return False
        else :
            return False

    @staticmethod
    def login(db, username, password):
        account = db.bookingStaffs.find_one({ "name" : username })

        if account is None:
            return { "register": False }
        elif account['password'] != password:
            return { "register": True, "password": False }
        else :
            id = account['id']
            return { "register": True, "password": True, "id": id }

class Admin(BookingStaff):
    pass

class Manager(BookingStaff):
    pass

class HorizonCinemaSystem:
    def __init__(self):
        self.__client = pymongo.MongoClient("mongodb://localhost:27017")
        self.__db = self.__client.horizon_cinema
        self.__cities = self.getCities()

    def getdb(self):
        return self.__db

    def getCities(self):
        cursor = self.__db.cities.find()
        cities = []

        for doc in cursor:
            city = doc['name']
            cities.append(City(city, self.__db))       

        return cities

    def addCity(self, name):
        city = City(name, self.__db)
        result = city.saveCity()
        if(result == True):
            self.__cities.append(city)
        else:
            raise ValueError("Failed to add city")

        return city

    def removeCity(self, name):
        city = City(name, self.__db)
        result = city.removeCity()
        if result == True:
            for i, city in enumerate(self.__cities):
                if city.getCity() == name:
                    self.__cities.pop(i)
        else:
            return False

    def getJSONcities(self):
        cities = []
        for city in self.__cities:
            name = city.getCity()
            cinemas = []
            for cinema in city.getCinemas():
                cinema_name = cinema.getLocation()
                morning_price = cinema.getMorningPrice()
                afternoon_price = cinema.getAfternoonPrice()
                evening_price = cinema.getEveningPrice()
                screens = []
                for screen in cinema.getScreens():
                    screen.loadData()
                    seating = screen.getTotalCapacity()
                    screenNumber = screen.getScreenNumber()
                    screens.append({"seats": seating, "screen": screenNumber})
                cinemas.append({ "location": cinema_name, "screens": screens, "morning_price": morning_price, "afternoon_price": afternoon_price, "evening_price": evening_price })
            cities.append({ "city": name, "cinemas": cinemas })
        return cities

    def addNewCinema(self, city, location, morning_price, afternoon_price, evening_price):
        cinema = Cinema(city, location, morning_price, afternoon_price, evening_price, self.__db)
        result = cinema.saveCinema()

        if result == True:
            for i in self.__cities:
                if i.getCity() == city:
                    i.addcinema(cinema)
        else:
            raise ValueError("Failed to add item to list in object")

        return cinema

    def deleteCinema(self, city, location):
        for i in self.__cities:
            if i.getCity() == city:
                for ii in i.getCinemas():
                    if ii.getLocation() == location:
                        i.removeCinema(ii)

    def numOfBookings(self):
        cursor = self.__db.bookings.find({})
        bookings = {}
        for doc in cursor:
            city = doc['location']

            if bookings.get(city) is None:
                bookings[city] = 1
            else:
                bookings[city] += 1

        list = []

        for i in bookings:
            list.append(f"{i} : {bookings.get(i)}")

        return list

    def revenue(self):
        cursor = self.__db.bookings.find({})
        bookings = []
        prices = {}
        film = {}

        for i in cursor:
            bookings.append(Booking(self.__db, i['date'], i['movieName'], i['numberOfCustomer'], i['ticketType'], i['showingTime'], i['bookingStaffId'], i['city'], i['location'], i['referenceId'], i['price']))

        list = []
        total = 0

        for i in bookings:
            total += int(i.getPrice())

        for i in bookings:
            location = film.get(i.getMovieName())
            if location is None:
                film[i.getMovieName()] = int(i.getPrice())
            else:
                film[i.getMovieName()] = (int(int(i.getPrice()) + int(location)))

        highest_key = None
        highest_value = None

        for key, value in film.items():
            if highest_value is None or value > highest_value:
                highest_key = key
                highest_value = value

        list.append(f"Top revenue generating film: {highest_key} - £{highest_value}")
        list.append(f"Total Revenue: £{total}\n")
        list.append(f"Revenue for each Listings:")

        for i in bookings:
            location = prices.get(i.getLocation())
            if location is None:
                prices[i.getLocation()] = int(i.getPrice())
            else:
                prices[i.getLocation()] = (int(int(i.getPrice()) + int(location)))

        for (i, booking) in enumerate(prices):
            list.append(f"{i+1}. {booking} - £{prices.get(booking)}")

        return list

    def staffBookings(self):
        cursor = self.__db.bookingStaffs.find({})
        bookings = {}  

        for i in cursor:
            bookings[i['name']] = i['numberOfBookingsCompleted']

        sorted_items = sorted(bookings.items(), key=lambda item: item[1], reverse=True)

        dict_list = [{key: value} for key, value in sorted_items]

        list = []

        for i, item in enumerate(dict_list):
            for key, value in item.items():
                list.append(f'{i+1}. {key} - {value}')

        return list

