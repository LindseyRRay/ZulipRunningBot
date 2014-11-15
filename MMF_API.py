#nformation on parsing json and accessing API from https://www.mapmyapi.com/io-docs
#If this line breaks need to change the json parsing for routes
import os
ONE_MILE_IN_METERS = 1609
from requests import get

 
class MMFRouteAPI:

	def __init__(self):
		self.ROUTE_URL = os.environ['MMF_URL']
		self.MMF_API_KEY = os.environ['MMF_API_KEY']
		self.MMF_SECRET = os.environ['MMF_SECRET']
		self.MMF_BEARER_ACCESS = os.environ['MMF_BEARER_ACCESS']

	def create_req_URL(self, start_lat, start_lon, max_dist, min_dist = 0):
		max_dist_meters = int(max_dist) * ONE_MILE_IN_METERS
		min_dist_meters = int(min_dist) * ONE_MILE_IN_METERS
		print str(start_lon)
		print str(start_lat)
		print max_dist_meters
		print min_dist_meters
		end_URL=self.ROUTE_URL+str(start_lat)+'%2C'+str(start_lon)+'&maximum_distance='+str(int(max_dist_meters))+'&minimum_distance='+str(int(min_dist_meters))
		return end_URL

	def get_routes(self, start_lat, start_lon, max_dist, min_dist = 0):
		start_URL = self.create_req_URL(start_lat, start_lon, max_dist, min_dist = 0)
		resp = get(url = start_URL, verify = False, headers = {'Api-Key': self.MMF_API_KEY,
			'Authorization': self.MMF_BEARER_ACCESS, 'Content-Type': 'application/json'})
		return resp.json()


	def parse_routes(self, json_resonse):
		list_runs = [(route['name'], route['distance'], route['_links']['self'][0]['id']) for route in json_resonse['_embedded']['routes']]
		list_runs.sort(key = itemgetter(1), reverse = True)
		return list_runs

	def list_runs(self, json_resonse):
		return [(tup[0].upper(), str(round(tup[1]/ONE_MILE_IN_METERS, 2)), 'http://www.mapmyrun.com/routes/view/'+str(tup[2])) for tup in self.parse_routes(json_resonse)]


if __name__ == '__main__':

	new_req = MMFRouteAPI()
	json_data = new_req.get_routes(40.719, -73.9915647, 10, 0)
	for l in new_req.list_runs(json_data):
		print(l)



