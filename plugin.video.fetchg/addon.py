import sys, json
import xbmc, xbmcgui
import xbmcplugin
from urllib.parse import unquote_plus
import addonvar
from resources.lib.modules import utils
from resources.lib.modules.params import p
from resources.lib.modules.m3u_parser import m3u

handle = int(sys.argv[1])
addDir = utils.addDir
base_url = addonvar.base_url
addon_icon = addonvar.addon_icon
addon_fanart = addonvar.addon_fanart

xbmc.log(str(p.get_params()),xbmc.LOGDEBUG)

def MainMenu():
	addDir('Playlists','',3, addon_icon, addon_fanart, 'Playlists from Youtube')
	m = m3u(base_url)
	for cat in m.get_categories():
		addDir(cat,base_url,1, addon_icon, addon_fanart, 'Categories')

def SubMenu(cname):
	m = m3u(url)
	for channel in m.get_catlist(cname):
		addDir(channel.get('name','Unknown'), channel.get('url',''), 2, channel.get('icon', addon_icon), addon_fanart, 'Channels',isFolder=False)

def yt_playlists_menu():
	from resources.lib.modules.parser import Parser
	xml = Parser(addonvar.yt_xml)
	items = xml.get_list()
	for item in json.loads(items)['items']:
		addDir(item.get('title','Unknown'),item.get('link',''), 4, addon_icon, addon_fanart, 'Playlists from Youtube')

def yt_playlists(link):
	from resources.lib.modules.yt_playlists import get_playlist_items
	if link.startswith('http'):
		link = link.split('list=')[-1]
	elif link.startswith('plugin'):
		link = link.split('playlist/')[-1].replace('/','')
	get_playlist_items(link)
		

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
	SubMenu(name)
elif mode==2:
	play_video(name, url, icon)
elif mode==3:
	yt_playlists_menu()
elif mode==4:
	yt_playlists(url)

xbmcplugin.endOfDirectory(handle)