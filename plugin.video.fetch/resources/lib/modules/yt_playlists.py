#Credits to natko1412, mintsoft, yeahme49,anxdpanic and bromix for code from Youtube Channels and Youtube

import urllib.request, json
import addonvar
from .utils import addDir

addon_icon = addonvar.addon_icon
addon_fanart = addonvar.addon_fanart

api_key = addonvar.api_key

def get_page(url):
	req = urllib.request.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0')
	response = urllib.request.urlopen(req)
	link=response.read()
	response.close()
	return link.decode('utf-8')

def get_playlist(pl_id, apiKey, page_token=None):
	if page_token:
		pl_api = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&fields=items/snippet,nextPageToken&pageToken=%s&maxResults=%s&playlistId=%s&key='%(page_token,str(50),pl_id)+apiKey
	else:
		pl_api = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&fields=items/snippet,nextPageToken&maxResults=%s&playlistId=%s&key='%(str(50),pl_id)+apiKey
	page = json.loads(get_page(pl_api))
	items = page['items']
	item_list = []
	for item in items:
		title = item['snippet']['title']
		video_id = item['snippet']['resourceId']['videoId']
		icon = get_thumbnail('high',item['snippet']['thumbnails'])
		fanart = icon
		description = item['snippet']['description']
		item_list.append({'title': title, 'url': 'plugin://plugin.video.youtube/play/?video_id=%s'%video_id, 'icon': icon, 'fanart': fanart, 'description': description})
	page_token = page.get('nextPageToken')
	item_list.append(page_token)
	return item_list

def get_playlist_items(pl_id):
	if '|||' in pl_id:
		pageToken = pl_id.split('|||')[1]
		pl_id = pl_id.split('|||')[0]
		items = get_playlist(pl_id, api_key,page_token=pageToken)
	else:
		items = get_playlist(pl_id, api_key)
	for item in items[:-1]:
		addDir(item.get('title'), item.get('url'),2,item.get('icon', addon_icon), item.get('fanart', addon_fanart),item.get('description'), isFolder=False)
	page_token = items[-1]
	if page_token and len(page_token)>1:
		addDir('Next Page', pl_id + '|||' + page_token, 4, addon_icon, addon_fanart,'Load the next page.')

def get_thumbnail(thumb_size, thumbnails):
    if thumb_size == 'high':
        thumbnail_sizes = ['high', 'medium', 'default']
    else:
        thumbnail_sizes = ['medium', 'high', 'default']
    image = ''
    for thumbnail_size in thumbnail_sizes:
        try:
            image = thumbnails.get(thumbnail_size, {}).get('url', '')
        except AttributeError:
            image = thumbnails.get(thumbnail_size, '')
        if image:
            break
    return image