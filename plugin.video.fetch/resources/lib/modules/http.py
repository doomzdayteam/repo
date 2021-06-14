
import requests
from .utils import Log

class http:
	def __init__(self, url):
		self.url = url
		self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
		self.headers = {"User-Agent":self.user_agent, "Connection":'keep-alive', 'Accept':'audio/webm,audio/ogg,udio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5'}
		
	def get_session(self, decoding=True, stream=False):
		from requests import Session
		session = Session()
		if decoding:
			return session.get(self.url,headers=self.headers, stream=stream,timeout=5).text
		else:
			return session.get(self.url,headers=self.headers, stream=stream)
	
	def get_requests(self, decoding=True, stream=False):
		from requests import get
		if decoding:
			return get(self.url, headers=self.headers, stream=stream).content.decode('utf-8')
		else:
			return get(self.url, headers=self.headers, stream=stream)
	
	def get_urllib(self, decoding=True):
		from urllib.request import Request, urlopen
		req = Request(self.url, headers = self.headers)
		if decoding:
			return urlopen(req).read().decode('utf-8')
		else:
			return urlopen(req)
	
	def get_length(self, response, meth = 'session'):
		if meth in ['session', 'requests']:
			return response.headers['content-length']
		elif meth=='urllib':
			return response.getheader('content-length')


def UrlValidator(url):
	ok=True
	try:
		r = requests.get(url,timeout=5)
		r.raise_for_status()
	except requests.exceptions.HTTPError as errh:
		Log(f"Http Error:{errh}")
		ok=False
	except requests.exceptions.ConnectionError as errc:
		Log(f"Error Connecting:{errc}")
		ok=False
	except requests.exceptions.Timeout as errt:
		Log(f"Timeout Error:{errt}")
		ok=False
	except requests.exceptions.RequestException as err:
		Log(f" Something Else:{err}")
		ok=False
	return ok