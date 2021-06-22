import sys, json
import xbmc, xbmcgui
import xbmcplugin
from urllib.parse import unquote_plus
import addonvar
from resources.lib.modules import utils
from resources.lib.modules.params import p
from resources.lib.modules import yt_playlists

handle = int(sys.argv[1])
addDir = utils.addDir
yt_xml = addonvar.yt_xml
xml_folder = addonvar.xml_folder
addon_icon = addonvar.addon_icon
addon_fanart = addonvar.addon_fanart

xbmc.log(str(p.get_params()),xbmc.LOGDEBUG)

def MainMenu(_xml):
	from resources.lib.modules.parser import Parser
	xml = Parser(_xml)
	items = xml.get_list()
	video_ids = []
	for item in json.loads(items)['items']:
		link = item.get('link')
		if 'video/' in link or 'youtu.be/' in link:
			video_ids.append(link.split('/')[-1])
		elif link.endswith('.xml'):
			if link.startswith('http'):
				addDir(item.get('title','Unknown'), item.get('link',''), 4, item.get('icon', addon_icon), item.get('fanart', addon_fanart), 'Playlists from Youtube')
			else:
				addDir(item.get('title','Unknown'),xml_folder+item.get('link',''), 4, item.get('icon', addon_icon), item.get('fanart', addon_fanart), 'Playlists from Youtube')
		else:
			addDir(item.get('title','Unknown'),item.get('link',''), 1, item.get('icon', addon_icon), item.get('fanart', addon_fanart), 'Playlists from Youtube')
	video_list = yt_playlists.get_videos(video_ids)
	for title, video_id, icon, description, duration, date in video_list:
		yt_playlists.addDir(title, 'plugin://plugin.video.youtube/play/?video_id=%s'%video_id,3,icon, icon, description, duration=duration, date='Date Published: '+str(date)+'\n', isFolder=False)

def yt_playlist(link):
	if link.startswith('http'):
		if 'list=' in link:
			link = link.split('list=')[-1]
	elif link.startswith('plugin'):
		link = link.split('playlist/')[-1].replace('/','')
	yt_playlists.get_playlist_items(link)

def yt_channel(_id):
	yt_playlists.ch_playlists(_id)
		
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
	MainMenu(yt_xml)

elif mode==1:
	yt_playlist(url)
	
elif mode==2:
	yt_channel(url)

elif mode==3:
	play_video(name, url, icon)

elif mode==4:
	MainMenu(url)
	
xbmcplugin.endOfDirectory(handle)