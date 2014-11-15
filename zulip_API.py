#Zulip API
 
from Google_API import GoogleRequests
from MMF_API import MMFRouteAPI
from requests import get 
from zulip import Client
import os



class ZulipBot:

	def __init__(self):
		self.client = Client(email = os.environ['ZULIP_USERNAME'], api_key = os.environ['ZULIP_API_KEY'])
		self.subscribe_streams()


	def subscribe_streams(self):
		response = get('https://api.zulip.com/v1/streams', auth=(os.environ['ZULIP_USERNAME'], os.environ['ZULIP_API_KEY']))
		
		if response.status_code == 200:
			streams = [{'name': stream['name']} for stream in response.json()['streams']]
			self.client.add_subscriptions(streams)

		else:
			raise RuntimeError(response)


	##Function to check for any messages

	def read_message(self, msg):
		content = msg['content'].split(',')
		sender_email = msg['sender_email']

		if sender_email == os.environ['ZULIP_USERNAME']:
			return
		if content[0].upper() in ['RUNNING', 'RUNNINGBOT', '@**RUNNING**']:
			return_info = self.find_runs(content)
			if return_info is None:
				self.send_message("No results", msg)
			else:
				[self.send_message(run, msg) for run in return_info]
		else:
			return 


	def find_runs(self, content):
		run_info = sorted(content[1:])
		
		if len(run_info) == 2:
			run_info.append('min=1')
		elif len(run_info) == 1:
			run_info.extend(['max=5.5', 'min=1'])

		run_params = [r.split("=")[-1] for r in run_info]

		get_coords = GoogleRequests()
		lat, lon = get_coords.get_geocode(run_params[0])

		new_req = MMFRouteAPI()
		json_data = new_req.get_routes(lat, lon, run_params[1], run_params[2])
		list_runs = new_req.list_runs(json_data)
		
		if len(list_runs) < 1:
			return None

		return list_runs



	def send_message(self, return_content, msg):
		links = ["Run Name: ", return_content[0], "Distance (miles): ", return_content[1], "Link:", return_content[-1]]
		return_str = " ".join(links)
		if msg['type'] == 'stream':
			self.client.send_message({
                'type': 'stream',
                'subject': 'RUNNINGBOT',
                'to': msg['display_recipient'],
                'content': return_str})
            
		elif msg['type'] == 'private':
			self.client.send_message({
                    'type': 'private',
                    'to': msg['sender_email'],
                    'content': return_str })      


def main():
	bot = ZulipBot()
	bot.client.call_on_each_message(bot.read_message)

if __name__ == '__main__':
	main()




