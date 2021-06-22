#Credits to natko1412, mintsoft, yeahme49,anxdpanic and bromix for code from Youtube Channels and Youtube

import xbmcplugin, xbmcgui, xbmcaddon
import sys, requests, re, json
from urllib.parse import quote_plus

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = xbmcaddon.Addon(addon_id)
addon_icon = addon.getAddonInfo("icon")
addon_fanart = addon.getAddonInfo("fanart")
user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
headers = {'User-Agent': user_agent}
api_key = xbmcaddon.Addon('plugin.video.youtube').getSetting('youtube.api.key')#Requires api key added to Youtube addon. Can be changed to suit your needs.

def get_page(url):
	session = requests.Session()
	return session.get(url, headers=headers).text
	
def get_playlist(pl_id, page_token=None):
	if page_token:
		pl_api = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&fields=items/snippet,nextPageToken&pageToken=%s&maxResults=50&playlistId=%s&key=%s'%(page_token, pl_id, api_key)
	else:
		pl_api = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&fields=items/snippet,nextPageToken&maxResults=%s&playlistId=%s&key=%s'%(str(50),pl_id,api_key)
	page = json.loads(get_page(pl_api))
	items = page['items']
	item_list = []
	video_ids = []
	for item in items:
		video_id = item['snippet']['resourceId']['videoId']
		video_ids.append(video_id)
	video_list = get_videos(video_ids)
	for title, video_id, icon, description, duration, date in video_list:
		item_list.append({'title': title, 'url': 'plugin://plugin.video.youtube/play/?video_id=%s'%video_id, 'icon': icon, 'fanart': icon, 'description': description, 'duration': duration, 'date': date})
	page_token = page.get('nextPageToken')
	if page_token:
		item_list.append(page_token)
	return item_list

def get_playlist_items(pl_id):
	if '|||' in pl_id:
		page_token = pl_id.split('|||')[1]
		pl_id = pl_id.split('|||')[0]
	else:
		page_token = None
		if pl_id.startswith('UU'):
			addDir('Playlists', get_channel_id(pl_id),2, addon_icon, addon_fanart, 'Playlists from this Channel')#mode integer should be one that calls ch_playlists function
		elif pl_id.startswith('UC'):
			addDir('Playlists', pl_id,2, addon_icon, addon_fanart, 'Playlists from this Channel')#mode integer should be one that calls ch_playlists function
			pl_id = get_uploads_id(pl_id)
		elif pl_id.startswith('PL'):
			pl_id = pl_id
		else:
			pl_id = get_ch_id(pl_id)
	items = get_playlist(pl_id, page_token=page_token)
	if type(items[-1]) is dict:
		for item in items:
			if item.get('title')=='Deleted video':
				continue
			addDir(item.get('title'), item.get('url'),3,item.get('icon', addon_icon), item.get('fanart', addon_fanart),item.get('description'), duration=item.get('duration', ''), date='Date Published: '+str(item.get('date','')+'\n'), isFolder=False)#mode integer should be one that calls the player
	else:
		for item in items[:-1]:
			if item.get('title')=='Deleted video':
				continue
			addDir(item.get('title'), item.get('url'),3,item.get('icon', addon_icon), item.get('fanart', addon_fanart),item.get('description'), duration=item.get('duration', ''), date='Date Published: '+str(item.get('date','')+'\n'), isFolder=False)#mode integer should be one that calls the player
		page_token = items[-1]
		addDir('Next Page', pl_id + '|||' + page_token, 1, addon_icon, addon_fanart,'Load the next page.')#mode integer should be one that calls get_playlist_items function

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

def get_channel_playlists(ch_id, page_token=None):
	if ch_id.startswith('UU'):
		ch_id = get_channel_id(ch_id)
	if page_token:
		ch_api ='https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=%s&nextPageToken&pageToken=%s&maxResults=%s&key=%s'%(ch_id, page_token, str(50), api_key)
	else:
		ch_api ='https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=%s&nextPageToken&maxResults=%s&key=%s'%(ch_id, str(50), api_key)
	page = json.loads(get_page(ch_api))
	playlists=[]
	for item in page['items']:
		if item['kind']=='youtube#playlist':
			playlist_id = item['id']
			playlist_name = item['snippet']['title']
			thumbnail = item['snippet']['thumbnails']['high']['url']
			playlists.append([playlist_id,playlist_name,thumbnail])
	page_token = page.get('nextPageToken')
	if page_token:
		playlists.append(page_token)
	return playlists

def ch_playlists(ch_id):
	if '|||' in ch_id:
		pageToken = ch_id.split('|||')[1]
		ch_id = ch_id.split('|||')[0]
		items = get_channel_playlists(ch_id,page_token=pageToken)
	else:
		items = get_channel_playlists(ch_id)
	if isList(items[-1]):
		for _id, name, thumb in items:
			addDir(name, _id, 1, thumb, thumb,name)#mode integer should be one that calls the get_playlist_items function
	else:
		for _id, name, thumb in items[:-1]:
			addDir(name, _id, 1, thumb, thumb,name)#mode integer should be one that calls the get_playlist_items function
		page_token = items[-1]
		addDir('Next Page', ch_id + '|||' + page_token, 2, addon_icon, addon_fanart,'Load the next page.')#mode integer should be one that calls get_ch_playlists function

def get_uploads_id(ch_id):
	return json.loads(get_page('https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id=%s&key=%s'%(ch_id, api_key)))['items'][0]['contentDetails']['relatedPlaylists']['uploads']

def get_channel_id(uploads_id):
	return json.loads(get_page('https://www.googleapis.com/youtube/v3/playlists?part=snippet&id=%s&key=%s'%(uploads_id, api_key)))['items'][0]['snippet']['channelId']

def get_ch_id(username):
	api_url='https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername=%s&key=%s'%(username, api_key)
	uploads_id = json.loads(get_page(api_url))['items'][0]['contentDetails']['relatedPlaylists'].get('uploads', None)
	if uploads_id:
		return uploads_id
	else:
		return False

def get_videos(_ids, item_list = None):
	if item_list==None:
		item_list = []
	video_url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id=%s&key=%s' % (','.join(_ids), api_key)
	items = json.loads(get_page(video_url))['items']
	for item in items:
		title = item['snippet']['title']
		video_id = item['id']
		thumb = item['snippet']['thumbnails']['high']['url']
		description =item['snippet']['description']
		duration = yt_time(item['contentDetails']['duration'])
		date = re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}", item['snippet']['publishedAt'])
		item_list.append([title, video_id, thumb, description, duration, date.group()])
	return item_list

# https://stackoverflow.com/a/49976787
def yt_time(duration="P1W2DT6H21M32S"):
	"""
	Converts YouTube duration (ISO 8061)
	into Seconds

	see http://en.wikipedia.org/wiki/ISO_8601#Durations
	"""
	ISO_8601 = re.compile(
		'P'   # designates a period
		'(?:(?P<years>\d+)Y)?'   # years
		'(?:(?P<months>\d+)M)?'  # months
		'(?:(?P<weeks>\d+)W)?'   # weeks
		'(?:(?P<days>\d+)D)?'    # days
		'(?:T' # time part must begin with a T
		'(?:(?P<hours>\d+)H)?'   # hours
		'(?:(?P<minutes>\d+)M)?' # minutes
		'(?:(?P<seconds>\d+)S)?' # seconds
		')?')   # end of time part
	# Convert regex matches into a short list of time units
	units = list(ISO_8601.match(duration).groups()[-3:])
	# Put list in ascending order & remove 'None' types
	units = list(reversed([int(x) if x != None else 0 for x in units]))
	# Do the maths
	return sum([x*60**units.index(x) for x in units])

def addDir(name,url,mode,icon,fanart,description,duration='',date='',addcontext=False,isFolder=True):
	u=sys.argv[0]+"?name="+quote_plus(name)+"&url="+quote_plus(url)+"&mode="+str(mode)+"&icon="+quote_plus(icon) +"&fanart="+quote_plus(fanart)+"&description="+quote_plus(description)
	liz=xbmcgui.ListItem(name)
	liz.setArt({'fanart':fanart,'icon':'DefaultFolder.png','thumb':icon})
	liz.setInfo(type="Video", infoLabels={ "Title": name, "plot": str(date)+description, 'duration': duration})
	if addcontext:
		contextMenu = []
		liz.addContextMenuItems(contextMenu)
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)

def isList(item):
	if isinstance(item,list):
		return True
	else:
		return False