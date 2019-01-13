from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "E2NEWMIO3Z3ZKR5AT1YQ1MI0YPKCR0AP0LF5ZP0KKYI0MIJ1"
foursquare_client_secret = "H34UQEYSJXUXXI4X3P13AZVMOOU35P0F3NFFE4FPEEZU3FR2"


def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	latitude, longitude = getGeocodeLocation(location)
	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s' % (foursquare_client_id, foursquare_client_secret,latitude,longitude,mealType))
	h = httplib2.Http()
	result = json.loads(h.request(url,'GET')[1])
	
	if result['response']['venues']:
		#3.  Grab the first restaurant
		restaurant = result['response']['venues'][0]
		venue_id = restaurant['id'] 
		restaurant_name = restaurant['name']
		restaurant_address = restaurant['location']['formattedAddress']
		address = ""
		for i in restaurant_address:
			address += i + " "
		restaurant_address = address
	
		#7.  return a dictionary containing the restaurant name, address, and image url
		restaurantInfo = {'name':restaurant_name, 'address':restaurant_address}
		print "Restaurant Name: %s" % restaurantInfo['name']
		print "Restaurant Address: %s" % restaurantInfo['address']
		#print "Image: %s \n" % restaurantInfo['image']
		return restaurantInfo
	else:
		print "No Restaurants Found for %s" % location
		return "No Restaurants Found"


if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney, Australia")