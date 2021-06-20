#Based on Playlist Loader by Avigdor
import requests, re
import addonvar
from .http import http

addon_icon = addonvar.addon_icon

class m3u():
    def __init__(self, url):
    	self.url = url
    
    def get_page(self):
    	h = http(self.url)
    	return h.get_session()
    
    def get_list(self):
    	page = self.get_page()
    	matches=re.compile('^#EXTINF:-?[0-9]*(.*?),(.*?)\n(.*?)$', re.M).findall(page)
    	li = []
    	for params, display_name, url in matches:
    		item_data = {"params": params, "display_name": display_name.strip(), "url": url.strip()}
    		li.append(item_data)
    	chList = []
    	for channel in li:
    		item_data = {"display_name": channel["display_name"], "url": channel["url"]}
    		matches=re.compile(' (.+?)="(.+?)"').findall(channel["params"])
    		for field, value in matches:
    			item_data[field.strip().lower().replace('-', '_')] = value.strip()
    		chList.append(item_data)
    	return chList
    
    def get_categories(self):
    	cats = []
    	for x in self.get_list():
    		cat = x.get('group_title', None)
    		if cat:
    			if cat not in cats:
    				cats.append(cat)
    	return sorted(cats)
    
    def get_catlist(self, category):
    	cat_list = []
    	for channel in self.get_list():
    		_cat = channel.get('group_title',None)
    		if _cat:
    			if category == _cat:
    				cat_list.append({'name': channel.get('display_name', 'Unknown'), 'url': channel.get('url', ''), 'icon': channel.get('tvg_logo', addon_icon)})
    	return cat_list