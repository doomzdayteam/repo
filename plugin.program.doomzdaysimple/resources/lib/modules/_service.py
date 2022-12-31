import xbmc
import xbmcgui
import xbmcaddon
import json
import base64
import xml.etree.ElementTree as ET
from .maintenance import clear_packages
from uservar import buildfile, notify_url
from .addonvar import setting, setting_set, addon_name, isBase64, headers, dialog, local_string, addon_id
from .build_install import restore_binary, binaries_path

current_build = setting('buildname')
try:
    current_version = float(setting('buildversion')) 
except:
    current_version = 0.0

class Startup:
    
    def check_updates(self):
           if current_build == 'No Build Installed':
               nobuild = dialog.yesnocustom(addon_name, 'There is currently no build installed.\nWould you like to install one now?', 'Remind Later')
               if nobuild == 1:
                   xbmc.executebuiltin(f'ActivateWindow(10001, "plugin://{addon_id}/?mode=1",return)')
               elif nobuild == 0:
                   setting_set('buildname', 'No Build')
               else:
                   return
           try:
               response = self.get_page(buildfile)
           except:
               return
           version = 0.0
           try:
               builds = json.loads(response)['builds']
               for build in builds:
                       if build.get('name') == current_build:
                           version = float(build.get('version'))
                           break
           except:
               builds = ET.fromstring(response)
               for tag in builds.findall('build'):
                       if tag.find('name').text == current_build:
                           version = float(tag.find('version').text)
                           break
           if version > current_version and setting('update_passed') != 'true':
               update_available = xbmcgui.Dialog().yesnocustom(addon_name, local_string(30047) + ' ' + current_build +' ' + local_string(30048) + '\n' + local_string(30049) + ' ' + str(current_version) + '\n' + local_string(30050) + ' ' + str(version) + '\n' + local_string(30051), 'Remind Later')
               if update_available == 1:
                   xbmc.executebuiltin(f'ActivateWindow(10001, "plugin://{addon_id}/?mode=1",return)')
               elif update_available == 0:
                   setting_set('update_passed', 'true')
               else:
                   return
           else:
               return

    def file_check(self, bfile):
        if isBase64(bfile):
            return base64.b64decode(bfile).decode('utf8')
        else:
            return bfile
            
    def get_page(self, url):
           from urllib.request import Request,urlopen
           req = Request(self.file_check(url), headers = headers)
           return urlopen(req).read()
        
    def save_menu(self):
        save_items = []
        choices = ["Favourites", "Sources", "Debrid - Resolve URL", "Advanced Settings"]
        save_select = dialog.multiselect(addon_name + ' - ' + local_string(30052),choices, preselect=[])  # Select Save Items
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

    def notify_check(self):
        notify_version = self.get_notifyversion()    
        if not setting('firstrunNotify')=='true' or notify_version > int(setting('notifyversion')):
            self.notification()
            
    def notification(self):
        from resources.lib.GUIcontrol import notify
        d=notify.notify('notify.xml', xbmcaddon.Addon().getAddonInfo('path'), 'Default', '720p')
        d.doModal()
        del d
        setting_set('firstrunNotify', 'true')
        setting_set('notifyversion', str(self.get_notifyversion()))
    
    def get_notifyversion(self):
        try:
            response = self.get_page(notify_url).decode('utf-8')
        except:
            return
        try:
            split_response = response.split('|||')
            return int(split_response[0])    
        except:
            return False    

    def run_startup(self):
        if binaries_path.exists():
            restore_binary()
        if setting('autoclearpackages')=='true':
            xbmc.sleep(2000)
            clear_packages()
        
        if not setting('firstrunSave')=='true':
            xbmc.sleep(2000)
            self.save_menu()
        
        self.notify_check()
        self.check_updates()
        
        if setting('firstrun') == 'true':
            from resources.lib.modules import addons_enable
            addons_enable.enable_addons()
        setting_set('firstrun', 'false')