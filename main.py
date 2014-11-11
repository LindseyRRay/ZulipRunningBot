from Google_API import GoogleRequests


if __name__ == '__main__':
	get_coords = GoogleRequests()
	lat, lon = get_coords.get_geocode('47 Delancey Street New York NY 10002')
	print(lat)
	print(lon)