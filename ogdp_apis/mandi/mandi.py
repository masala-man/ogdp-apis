import json
import requests

class mandiData():

	def __init__(self, apiKey, *args):
		self.apiPath = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
		self.session = requests.Session()
		self.session.params = {
			"api-key": apiKey,
			"format": "json",
			"limit": 10000,
			"fields": ""
		}
		self.states = {
			"AP": "Andhra Pradesh",
			"AS": "Assam",
			"BR": "Bihar",
			"CH": "Chandigarh",
			"CT": "Chattisgarh",
			"DL": "Delhi",
			"GA": "Goa",
			"GJ": "Gujarat",
			"HR": "Haryana",
			"HP": "Himachal Pradesh",
			"JK": "Jammu and Kashmir",
			"JH": "Jharkhand",
			"KA": "Karnataka",
			"KL": "Kerala",
			"LK": "Lakshadweep",
			"MP": "Madhya Pradesh",
			"MH": "Maharashtra",
			"MN": "Manipur",
			"ML": "Meghalaya",
			"MZ": "Mizoram",
			"OR": "Odisha",
			"PY": "Puducherry",
			"PB": "Punjab",
			"RJ": "Rajasthan",
			"SK": "Sikkim",
			"TN": "Tamil Nadu",
			"TG": "Telangana",
			"TP": "Tripura",
			"UP": "Uttar Pradesh",
			"UK": "Uttarakhand",
			"WB": "West Bengal"
		}


	def get_data(self, fields=['state','district','market','arrival_date','commodity','min_price','max_price','modal_price', 'variety']):
		"""
		Query API for data in raw form
		"""
		self.session.params["fields"] = ','.join(fields)
		request = self.session.get(self.apiPath)
		return json.loads(request.content)


	def filter_data(self, data, filter={}):
		"""
		Fetch data that matches the values specified in the dict 'filter'
		filter={'district': 'Mulakalacheruvu', 'commodity': 'Tpmato'}
		"""
		data = data['records']
		filteredData = []
		for x in range(len(data)):
			for key in filter:
				if data[x][key] == filter[key]:
					filteredData.append(data[x])
		return filteredData


	def format_data(self, data):
		"""
		Condense data for each market into one list item in the
		following format:

 		{"arrival_date": "31/07/2020",
  		"commodities": {
				"Jowar(Sorghum)": {
				"max": "2560",
				"min": "2450",
				"modal": "2500",
				"variety": "Jowar ( White)"
				},
            	"Paddy(Dhan)(Common)": {	
				"max": "2100",
				"min": "1760",
				"modal": "1900",
				"variety": "Sona"
			}
		}
		"""
		# Create list of markets and organize commodity values
		market_list = []
		commodity_list = []
		for x in range(len(data)):
			data[x][data[x]["commodity"]] = {
				"min": data[x].pop('min_price'),
				"max": data[x].pop('max_price'),
				"modal": data[x].pop('modal_price'),
				"variety": data[x].pop('variety')
			}	
			if market_list.count(data[x]['market']) == 0:
				market_list.append(data[x]['market'])
			if data[x]['commodity'] not in commodity_list:
				commodity_list.append(data[x]['commodity'])
		# Count number of commodities listed under each market
		market_map = {}
		for x in range(len(market_list)):
			market_map[market_list[x]] = 0
		for x in range(len(data)):
			if data[x]['market'] in market_list:
				market_map[data[x]['market']] += 1
		# Format to final form
		formatted_data = []
		commodities = {}
		for key in market_map:
			for x in range(market_map[key]):
				for commodity in data[x]:
					if commodity in commodity_list:
						commodities[commodity] = data[x][commodity]
			data[0]['commodities'] = commodities
			commodities = {}
			formatted_data.append(data[0])
			for x in range(market_map[key]):
				data.pop(0)
		for x in range(len(market_list)):
			formatted_data[x].pop(formatted_data[x]['commodity'])
			formatted_data[x].pop('commodity')
		# Return formatted data
		return formatted_data


	def state(self, state):
		"""
		Fetch a formatted list of data from markets in the specified state
		"""
		data = self.get_data()
		data = self.filter_data(data, filter={'state': self.states[state]})
		data = self.format_data(data)
		return data


	def district(self, district):
		"""
		Fetch a formatted list of data from markets in the specified district  
		"""
		data = self.get_data()
		data = self.filter_data(data, filter={'district': district})
		data = self.format_data(data)
		return data
	
	def market(self, market):
		"""
		Fetch a formatted list of data from markets in the specified district  
		"""
		data = self.get_data()
		data = self.filter_data(data, filter={'market': market})
		data = self.format_data(data)
		return data