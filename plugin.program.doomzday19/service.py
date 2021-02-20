#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, glob, sqlite3, json, base64
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from urllib.request import Request
from addonvar import *
from datetime import datetime
from xml.dom.minidom import parse
	
def check_updates():
    if current_build != 'No Build Installed':
    	req = Request(buildfile, headers = headers)
    	response = urlopen(req).read()
    	version = 0.0
    	try:
    		builds = json.loads(response)['builds']
    		for build in builds:
    			if build.get('name') == current_build:
    				version = float(build.get('version'))
    	except:
    		builds = ET.fromstring(response)
    		for tag in builds.findall('build'):
    			if tag.get('name') == current_build:
    				version = float(tag.find('version').text)
    	if version > current_version:
    		xbmcgui.Dialog().ok(addon_name, 'A new version of ' + current_build +' is available.' + '\n' + 'Installed Version: ' + str(current_version) + '\n' + 'New Version: ' + str(version) + '\n' + 'You can update from the Build Menu in ' + addon_name + '.')
    	else:
    		return
    else:
    	return
    	
def save_menu():
	save_items = []
	choices = ["Favourites", "Sources", "Debrid - Resolve URL", "Advanced Settings"]
	dialog = xbmcgui.Dialog()
	save_select = dialog.multiselect(addon_name + " - Select items to keep during a build install.",choices, preselect=[])
	
	if save_select == None:
		return
	else:
		for index in save_select:
			save_items.append(choices[index])
	if 'Favourites' in save_items:
		setting_set('savefavs','true')
	else:
		setting_set('savefavs','false')
	if 'Sources' in save_items:
		setting_set('savesources', 'true')
	else:
		setting_set('savesources', 'false')
	if 'Debrid - Resolve URL' in save_items:
		setting_set('savedebrid','true')
	else:
		setting_set('savedebrid','false')
	if 'Advanced Settings' in save_items:
		setting_set('saveadvanced','true')
	else:
		setting_set('saveadvanced','false')
	
	setting_set('firstrunSave', 'true')
	return
	
if __name__ == '__main__':
	try:
		if isBase64(buildfile):
			buildfile = base64.b64decode(buildfile).decode('utf8')
	except:
		pass
	
	current_build = setting('buildname')
	try:
		current_version = float(setting('buildversion')) 
	except:
		current_version = 0.0
	
	if not setting('firstrunSave')=='true':
		save_menu()
		
	from resources.lib.GUIcontrol.notify import get_notifyversion
	notify_version = get_notifyversion()	
	if not setting('firstrunNotify')=='true' or notify_version > int(setting('notifyversion')):
		from resources.lib.GUIcontrol import notify
		d=notify.notify()
		d.doModal()
		del d
		setting_set('firstrunNotify', 'true')
		setting_set('notifyversion', str(notify_version))
		
	check_updates()
	
	if setting('firstrun') == 'true':
		from resources.lib.modules import addonsEnable
		addonsEnable.enable_addons()
		xbmc.executebuiltin('UpdateLocalAddons')
		xbmc.executebuiltin('UpdateAddonRepos')