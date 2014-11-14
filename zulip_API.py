#Zulip API
from config import ZULIP_USERNAME, ZULIP_API_KEY, ZULIP_STREAMS 
from Google_API import GoogleRequests
from MMF_API import MMFRouteAPI

from requests import get 
from zulip import Client



class ZulipBot:

	def __init__(self):
		self.client = Client(email = ZULIP_USERNAME, api_key = ZULIP_API_KEY)
		self.subscribe_streams()


	def subscribe_streams(self):
		reponse = get(ZULIP_STREAMS, auth=(ZULIP_USERNAME, ZULIP_API_KEY))
		
		if response.status_code == 200:
			streams = [{'name': stream['name']} for stream in response.json()['streams']
			 self.client.add_subscriptions(streams)

		else:
			raise RuntimeError(response)


	##Function to check for any messages

	def read_message(self, msg):
		content = msg['content'].split(',')
		sender_email = msg['sender_email']

		if sender == ZULIP_USERNAME:
			return

		if content[0].upper() in ['RUNNING', 'RUNNNINGBOT', '@**RUNNING**']:
			return_info = self.find_runs(content)
			#if no runs found, return custom message
			#put this is funciton send message

            if msg['type'] == 'stream':
                self.client.send_message({
                    'type': 'stream',
                    'subject': msg['subject'],
                    'to': msg['display_recipient'],
                    'content': return_info
                })
            elif msg['type'] == 'private':
                self.client.send_message({
                    'type': 'private',
                    'to': msg['sender_email'],
                    'content': return_info
                })
            else:
                return











	def find_runs(self, content):

			run_info = sorted(content[1:])
			
			if len(run_info) == 2:
				run_info.append[min=1]
			elif len(run_info) == 1:
				run_info.extend[[max = 5.5, min =1 ]]

			#order should be address, max distance, min distance
			get_coords = GoogleRequests()
			lat, lon = get_coords.get_geocode(run_info[0])

			print lat
			print lon

			new_req = MMFRouteAPI()
			json_data = new_req.get_routes(lat, lon, run_info[1], run_info[2])
					for c in content:
				print c

	##Function to send messages back




# Send a private message