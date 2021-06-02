import xml.etree.ElementTree as ET
import json

class Parser:
	def __init__(self, url):
		self.url = url
	
	def get_list(self):
		if self.url.endswith('.xml'):
			try:
				xml = ET.fromstring(self.get_page())
			except ET.ParseError:
				xml = ET.fromstringlist(["<root>", self.get_page(), "</root>"])
			item_list = []
			for item in xml:
				item_list.append({child.tag: child.text for child in item})
			return json.dumps({'items': item_list})	
		elif self.url.endswith('.json'):
			return json.dumps(self.get_page())

	def get_page(self):
		if self.url.startswith('http'):
			from .http import http
			d = http(self.url)
			return d.get_session()
		else:
			return open(self.url).read()