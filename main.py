from Google_API import GoogleRequests
from MMF_API import MMFRouteAPI


if __name__ == '__main__':
	get_coords = GoogleRequests()
	lat, lon = get_coords.get_geocode('47 Delancey Street New York NY 10002')
	print(lat)
	print(lon)

	new_req = MMFRouteAPI()
	json_data = new_req.get_routes(lat, lon, 10, 0)
	for l in new_req.list_runs(json_data):
		print(l)
