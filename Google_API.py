#Google Requests API
#Get Lat Lon of address of starting run location
from requests import get
import json 
import os 

class GoogleRequests:

	def __init__(self):
		self.GEOCODE_API = os.environ['GOOGLE_API'] + "geocode/json?address="
		self.API_KEY = os.environ['GOOGLE_API_KEY']


	def create_addr_URL(self, starting_address):
		#remove punctutation
		#parse into list
		addr_str = re.sub(r'[^\w]', ' ' , starting_address)
		addr_URL = re.sub(r' ', '+' , starting_address)
		return addr_URL


	def get_geocode(self, starting_address):
		try:
			URL = self.create_addr_URL(starting_address)
			response = get(self.GEOCODE_API + URL + "&Key=" + self.API_KEY)
			payload = json.loads(response.text)
			lat = payload['results'][0]['geometry']['location']['lat']
			lon = payload['results'][0]['geometry']['location']['lng']
			return lat, lon
		except:
			raise RuntimeError


