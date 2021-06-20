import sys, json
import xbmc, xbmcgui
import xbmcplugin
from urllib.parse import unquote_plus
import addonvar
from resources.lib.modules import utils
from resources.lib.modules.params import p

handle = int(sys.argv[1])
addDir = utils.addDir
yt_xml = addonvar.yt_xml
addon_icon = addonvar.addon_icon
addon_fanart = addonvar.addon_fanart

xbmc.log(str(p.get_params()),xbmc.LOGDEBUG)

def MainMenu():
	from resources.lib.modules.parser import Parser
	xml = Parser(yt_xml)
	items = xml.get_list()
	for item in json.loads(items)['items']:
		addDir(item.get('title','Unknown'),item.get('link',''), 1, item.get('icon', addon_icon), item.get('fanart', addon_fanart), 'Playlists from Youtube')

def yt_playlist(link):
	from resources.lib.modules.yt_playlists import get_playlist_items
	if link.startswith('http'):
		if 'list=' in link:
			link = link.split('list=')[-1]
		
	elif link.startswith('plugin'):
		link = link.split('playlist/')[-1].replace('/','')
	
	get_playlist_items(link)

def yt_channel(_id):
	from resources.lib.modules.yt_playlists import ch_playlists
	ch_playlists(_id)
		
def play_video(title, link, iconimage):
    video = unquote_plus(link)
    liz = xbmcgui.ListItem(title)
    liz.setInfo('video', {'Title': title})
    liz.setArt({'thumb': iconimage, 'icon': iconimage})
    xbmc.Player().play(video,liz)

name = p.get_name()
url = p.get_url()
mode = p.get_mode()
icon = p.get_icon()
fanart = p.get_fanart()
description = p.get_description()

xbmcplugin.setContent(handle, 'movies')

if mode==None:
	MainMenu()

elif mode==1:
	yt_playlist(url)
	
elif mode==2:
	yt_channel(url)

elif mode==3:
	play_video(name, url, icon)

xbmcplugin.endOfDirectory(handle)