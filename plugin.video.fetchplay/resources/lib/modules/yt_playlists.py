#Credits to natko1412, mintsoft, yeahme49,anxdpanic and bromix for code from Youtube Channels and Youtube

import xbmcplugin, xbmcgui, xbmcaddon
import sys, requests, json
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
		items = get_playlist(pl_id,page_token=pageToken)
	else:
		if pl_id.startswith('UU'):
			addDir('Playlists', get_channel_id(pl_id),2, addon_icon, addon_fanart, 'Playlists from this Channel')#mode integer should be one that calls ch_playlists function
		elif pl_id.startswith('UC'):
			addDir('Playlists', pl_id,2, addon_icon, addon_fanart, 'Playlists from this Channel')#mode integer should be one that calls ch_playlists function
			pl_id = get_uploads_id(pl_id)
		elif pl_id.startswith('PL'):
			pl_id = pl_id
		else:
			pl_id = get_ch_id(pl_id)
			if pl_id:
				addDir('Playlists', get_channel_id(pl_id),2, addon_icon, addon_fanart, 'Playlists from this Channel')#mode integer should be one that calls ch_playlists function
		items = get_playlist(pl_id)
	for item in items[:-1]:
		if item.get('title')=='Deleted video':
			continue
		addDir(item.get('title'), item.get('url'),3,item.get('icon', addon_icon), item.get('fanart', addon_fanart),item.get('description'), isFolder=False)#mode integer should be one that calls the player
	page_token = items[-1]
	if page_token:
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

def get_channel_playlists(ch_id):
	if ch_id.startswith('UU'):
		ch_id = get_channel_id(ch_id)
	ch_api ='https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=%s&maxResults=500&key=%s'%(ch_id, api_key)
	page = json.loads(get_page(ch_api))
	playlists=[]
	for item in page['items']:
		if item['kind']=='youtube#playlist':
			playlist_id = item['id']
			playlist_name = item['snippet']['title']
			thumbnail = item['snippet']['thumbnails']['high']['url']
			playlists.append([playlist_id,playlist_name,thumbnail])
	return playlists

def ch_playlists(ch_id):
	for _id, name, thumb in get_channel_playlists(ch_id):
		addDir(name, _id, 1, thumb, thumb,name)#mode integer should be one that calls the get_playlist_items function

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

def addDir(name,url,mode,icon,fanart,description,addcontext=False,isFolder=True):
	u=sys.argv[0]+"?name="+quote_plus(name)+"&url="+quote_plus(url)+"&mode="+str(mode)+"&icon="+quote_plus(icon) +"&fanart="+quote_plus(fanart)+"&description="+quote_plus(description)
	liz=xbmcgui.ListItem(name)
	liz.setArt({'fanart':fanart,'icon':'DefaultFolder.png','thumb':icon})
	liz.setInfo(type="Video", infoLabels={ "Title": name, "plot": description})
	if addcontext:
		contextMenu = []
		liz.addContextMenuItems(contextMenu)
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)