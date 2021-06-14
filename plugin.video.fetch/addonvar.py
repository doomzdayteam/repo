import xbmc, xbmcvfs, xbmcaddon, xbmcgui
import os

translatePath = xbmcvfs.translatePath
addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = xbmcaddon.Addon(addon_id)
addoninfo = addon.getAddonInfo
addon_version = addoninfo('version')
addon_name = addoninfo('name')
addon_icon = addoninfo("icon")
addon_fanart = addoninfo("fanart")
addon_profile = translatePath(addoninfo('profile'))
addon_path = translatePath(addoninfo('path'))	
setting = addon.getSetting
setting_set = addon.setSetting
local_string = addon.getLocalizedString
home = translatePath('special://home/')
dialog = xbmcgui.Dialog()
dp = xbmcgui.DialogProgress()
addons_path = os.path.join(home, 'addons/')
user_path = os.path.join(home, 'userdata/')
data_path = os.path.join(user_path, 'addon_data/')
packages = os.path.join(addons_path, 'packages/')
resources = os.path.join(addon_path, 'resources/')
data = os.path.join(resources,'data')
user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
headers = {'User-Agent': user_agent}
iso_country_codes = 'http://geohack.net/gis/wikipedia-iso-country-codes.csv'
icons = os.path.join(resources,'icons')

search_json       = os.path.join(addon_profile,'search.json')
customiser_json   = os.path.join(addon_profile,'customiser.json')
fav_json          = os.path.join(addon_profile,'user_fav.json')
recentplayed_json = os.path.join(addon_profile,'recent_played.json')
icon_search       = os.path.join(icons,'search.png')
icon_fav          = os.path.join(icons,'favorites.png')
icon_recent       = os.path.join(icons,'recent.png')
icon_settings     = os.path.join(icons,'settings.png')
