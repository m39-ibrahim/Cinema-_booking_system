import pymongo
import time
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.horizon_cinema

# insert into cities
cities = [{ "name": "Bristol"}, {"name": "Cardiff"}, {"name": "London" }]
cities_collection = db.cities.insert_many(cities)

#insert into cinemas
cinemas = [{ "city": "Bristol", "location": "Cabot Circus", "morning_price": 11, "afternoon_price": 12, "evening_price": 13 }, { "city": "Cardiff", "location": "Vue Cinema", "morning_price": 11, "afternoon_price": 12, "evening_price": 13 }]
cinemas_collection = db.cinemas.insert_many(cinemas)

# insert into screens
screens = [{"city": "Bristol", "location": "Cabot Circus", "screenNumber": 1, "lowerCapacity": 21, "upperCapacity": 39, "vipCapacity": 10, "totalCapacity": 70 }, {"city": "Cardiff", "location": "Vue Cinema", "screenNumber": 1, "lowerCapacity": 21, "upperCapacity": 39, "vipCapacity": 10, "totalCapacity": 70 }]
screens_collection = db.screens.insert_many(screens)

# insert into films
films = [{"city": "Bristol", "location": "Cabot Circus", "filmName": "Avatar", "actorDetails": "Frank, Grace, Harry, Ida, and John", "filmGenre": "adventure", "age": "13", "rating": "10", "description": "this is a description." }, {"city": "Cardiff", "location": "Vue Cinema", "filmName": "Avengers", "actorDetails": "Charlie, Alice, Bob, David, Eve", "filmGenre": "adventure", "age": "13", "rating": "10", "description": "this is a description." }]
films_collection = db.films.insert_many(films)

# insert into showings
showings = [{"city": "Bristol", "location": "Cabot Circus", "filmName": "Avatar", "screen": 1, "showingTime": int(time.time()), "duration": "2h"}, {"city": "Cardiff", "location": "Vue Cinema", "filmName": "Avatar", "screen": 1, "showingTime": int(time.time()), "duration": "2h" }]
showings_collection = db.showings.insert_many(showings)

# insert into bookings
bookings = [{ "date": 1672935240, "movieName": "captain marvel", "numberOfCustomer": "2", "ticketType": "lowerCapacity", "showingTime": "16:14", "bookingStaffId": "manager", "city": "Bristol", "location": "Cabot Circus", "referenceId": "151d71fd", "price": "10" }]
bookings_collection = db.bookings.insert_many(bookings)

# insert into bookings Staff
bookings_Staff = [
    { "name": "james", "email": "-", "password": "abc", "numberOfBookingsCompleted": 10, "phoneNumber": "-", "id": "uiehew32" },
    { "name": "thomas", "email": "-", "password": "abc", "numberOfBookingsCompleted": 20, "phoneNumber": "-", "id": "uiehew42" },
    { "name": "billy", "email": "-", "password": "abc", "numberOfBookingsCompleted": 30, "phoneNumber": "-", "id": "uiehew52" },
    { "name": "charles", "email": "-", "password": "abc", "numberOfBookingsCompleted": 40, "phoneNumber": "-", "id": "uietew32" },
    { "name": "lisa", "email": "-", "password": "abc", "numberOfBookingsCompleted": 50, "phoneNumber": "-", "id": "uoehew32" },
    { "name": "mary", "email": "-", "password": "abc", "numberOfBookingsCompleted": 1, "phoneNumber": "-", "id": "u3ehew32" }
]
bookings_Staff_collection = db.bookingStaffs.insert_many(bookings_Staff)