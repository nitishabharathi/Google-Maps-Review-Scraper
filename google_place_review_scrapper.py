from tkinter import *
from googlegeocoder import GoogleGeocoder
import requests
import json
import time




class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey

    def search_places_by_coordinate(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        results =  json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            places.extend(results['results'])
            time.sleep(2)
        return places

    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        place_details =  json.loads(res.content)
        return place_details
root = Tk()
root.geometry('500x500')
root.title("Google Review Scraper")

OPTIONS = [
'accounting',
'airport',
'amusement_park',
'aquarium',
'art_gallery',
'atm',
'bakery',
'bank',
'bar',
'beauty_salon',
'bicycle_store',
'book_store',
'bowling_alley',
'bus_station',
'cafe',
'campground',
'car_dealer',
'car_rental',
'car_repair',
'car_wash',
'casino',
'cemetery',
'church',
'city_hall',
'clothing_store',
'convenience_store',
'courthouse',
'dentist',
'department_store',
'doctor',
'electrician',
'electronics_store',
'embassy',
'fire_station',
'florist',
'funeral_home',
'furniture_store',
'gas_station',
'gym',
'hair_care',
'hardware_store',
'hindu_temple',
'home_goods_store',
'hospital',
'insurance_agency',
'jewelry_store',
'laundry',
'lawyer',
'library',
'liquor_store',
'local_government_office',
'locksmith',
'lodging',
'meal_delivery',
'meal_takeaway',
'mosque',
'movie_rental',
'movie_theater',
'moving_company',
'museum',
'night_club',
'painter',
'park',
'parking',
'pet_store',
'pharmacy',
'physiotherapist',
'plumber',
'police',
'post_office',
'real_estate_agency',
'restaurant',
'roofing_contractor',
'rv_park',
'school',
'shoe_store',
'shopping_mall',
'spa',
'stadium',
'storage',
'store',
'subway_station',
'supermarket',
'synagogue',
'taxi_stand',
'train_station',
'transit_station',
'travel_agency',
'veterinary_care',
'zoo'

] #etc




label_0 = Label(root, text="Review Scrapper",width=20,font=("bold", 20))
label_0.place(x=90,y=53)

label_1 = Label(root, text="Place Name",width=20,font=("bold", 10))
label_1.place(x=80,y=130)

entry_1 = Entry(root)
entry_1.place(x=240,y=130)

label_2 = Label(root, text="Choose type of place",width=20,font=("bold", 10))
label_2.place(x=68,y=180)


variable = StringVar(root)
variable.set(OPTIONS[0]) # default value

w = OptionMenu(root, variable, *OPTIONS)
w.place(x=240,y=180)


label_3 = Label(root, text="Type of Output",width=20,font=("bold", 10))
label_3.place(x=70,y=230)
var = IntVar()
Radiobutton(root, text="CSV",padx = 5, variable=var, value=1).place(x=235,y=230)
Radiobutton(root, text="Raw Text",padx = 20, variable=var, value=2).place(x=290,y=230)




# This function is executed by the submit button
# it retrieves the outputs of both entry boxes
def submit():
    print('I am inside')
    api = GooglePlaces("YOUR API")
    apii = "YOUR API"
    place = entry_1.get()
    print(place)
    geocoder = GoogleGeocoder(apii)
    search = geocoder.get(place)
    coord = str(search[0].geometry.location.lat)+','+str(search[0].geometry.location.lng)
    places = api.search_places_by_coordinate(coord, "100", variable.get())
    print('I am here')
    fields = ['name', 'formatted_address', 'international_phone_number', 'website', 'rating', 'review']
    for place in places:
        details = api.get_place_details(place['place_id'], fields)
        try:
            website = details['result']['website']
        except KeyError:
            website = ""

        try:
            name = details['result']['name']
        except KeyError:
            name = ""

        try:
            address = details['result']['formatted_address']
        except KeyError:
            address = ""

        try:
            phone_number = details['result']['international_phone_number']
        except KeyError:
            phone_number = ""

        try:
            reviews = details['result']['reviews']
        except KeyError:
            reviews = []
        print("===================PLACE===================")
        print("Name:", name)
        print("Website:", website)
        print("Address:", address)
        print("Phone Number", phone_number)
        print("==================REWIEVS==================")
        for review in reviews:
            author_name = review['author_name']
            rating = review['rating']
            text = review['text']
            time = review['relative_time_description']
            profile_photo = review['profile_photo_url']
            print("Author Name:", author_name)
            print("Rating:", rating)
            print("Text:", text)
            print("Time:", time)
           


Button(root, text='Submit',command=submit,width=20,bg='brown',fg='white').place(x=180,y=280)

#button.pack()
root.mainloop()


