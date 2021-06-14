import re
from requests import Session
import json
import csv

# url ='https://bitbucket.org/!api/2.0/snippets/fluxustv/expnoX/5e2627cda2a19eea8adf521c70a9e678a85e6955/files/IPTV_032321'
url='https://doomzdayteam.github.io/iptv/languages/eng.m3u'

def re_me(data, re_patten):
	match = ''
	m = re.search(re_patten, data)
	if m != None:
		match = m.group(1)
	else:
		match = ''
	return match

def EpgRegex():
	m3udata = {}
	chId = 0
	s = Session()
	content = s.get(url).content
	match = re.compile(rb'#EXTINF:(.+?),(.*?)[\n\r]+([^\n]+)').findall(content)
	for other,channel_name,stream_url in match:
		channel_name = channel_name.decode('utf-8')
		stream_url = stream_url.decode('utf-8')
		tvg_id='';tvg_name='';tvg_country='';tvg_language='';tvg_logo='';group_title=''
		if b'tvg-id' in other:
			tvg_id = re_me(other,b'tvg-id=[\'"](.*?)[\'"]').decode('utf-8')
		if b'tvg-name' in other:
			tvg_name = re_me(other,b'tvg-name=[\'"](.*?)[\'"]').decode('utf-8')
		if b'tvg-country' in other:
			tvg_country = re_me(other,b'tvg-country=[\'"](.*?)[\'"]').decode('utf-8')
		if b'tvg-language' in other:
			tvg_language = re_me(other,b'tvg-language=[\'"](.*?)[\'"]').decode('utf-8')
		if b'tvg-logo' in other:
			tvg_logo = re_me(other,b'tvg-logo=[\'"](.*?)[\'"]').decode('utf-8')
		if b'group-title' in other:
			group_title = re_me(other,b'group-title=[\'"](.*?)[\'"]').decode('utf-8')
		if group_title == '':
			if tvg_country != '':
				group_title = tvg_country
			else:
				group_title = 'noGroup'
		chId += 1
		m3udata.update({chId:{"tvg_id":tvg_id,"tvg_name":tvg_name,"tvg_country":tvg_country,"tvg_language":tvg_language,"tvg_logo":tvg_logo,"group_title":group_title,"channel_name":channel_name,"stream_url":stream_url}})
	m3udata = json.dumps(m3udata, indent=4)
	print(sorted(list(set(v.get('group_title') for k,v in json.loads(m3udata).items()))))
	print(dict((k,v) for k,v in json.loads(m3udata).items() if v.get('group_title')=='Movies'))
	# print(list(filter(lambda x: x['group_title'] == 'noGroup', json.loads(m3udata).items())))

# EpgRegex()


		
def CSVreader():
	iso_date={}
	with open('iso-country-codes.csv') as iso_file:
		reader = csv.DictReader(iso_file,fieldnames=['name','alpha2','alpha3','int','iso_3166-2'])
		for row in reader:
			iso_date.update({"_".join(row['name'].lower().split() ):row})
	print(json.dumps(iso_date,indent=4))

		


# CSVreader()
def files():
	file = {"json_files":{"user_data": [{"file": "customiser.json", "headers": {"hidden_category": {}, "hidden_channel": {}},"req_start":True,"temp":True},{"file": "recent_played.json", "headers": {"recent_played": {}},"req_start":True,"temp":True},{"file": "search.json", "headers": {"search_history": {}},"req_start":True,"temp":True},{"file": "user_fav.json", "headers": {"channels":{}},"req_start":True,"temp":True}],"temp_data":[{"file":"m3udata.json","headers":{},"req_start":False,"temp":True}]}}
	print(json.dumps(file,indent=4))
	# print(file.replace("'",'"'))

# files()

print(len(list()))