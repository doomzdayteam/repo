import json
from typing import Dict, List, Optional, Union
import xbmc
import xbmcgui
from yt_dlp import YoutubeDL
from ..plugin import Plugin


class YtDLP(Plugin):
    name = "YT-Dlp"
    description = "Add support for YT-DLP"
    priority = 121
    
    def get_list(self, url: str) -> Optional[str]:
        if not url.startswith('yt_dlp/'):
            return
        url = url.replace('yt_dlp/', '')
        try:
            ytdlp = YoutubeDL(params = {"quiet": True, "format": "best"})
            results = ytdlp.extract_info(url, download=False, process=False)
            return results["entries"]
        except:
            return

    def parse_list(self, url: str, response: str) -> Optional[List[Dict[str, str]]]:
        if not url.startswith('yt_dlp/'):
            return
        item_list = []
        for entry in response:
            title = entry.get('title', '')
            link = entry.get('url')
            thumbnail = entry.get('thumbnail')
            summary = entry.get('description')
            item_list.append(
                {
                    'type': 'item',
                    'title': title,
                    'link': link,
                    'thumbnail': thumbnail,
                    'summary': summary
                }
            )
        return item_list

    def process_item(
        self, item: Dict[str, str]
    ) -> Optional[Dict[str, Union[str, xbmcgui.ListItem]]]:
        pass

    def get_metadata(
        self, item: Dict[str, Union[str, xbmcgui.ListItem]]
    ) -> Optional[Dict[str, Union[str, xbmcgui.ListItem]]]:
        pass

    def display_list(
        self, jen_list: List[Optional[Dict[str, Union[str, xbmcgui.ListItem]]]]
    ) -> Optional[bool]:
        pass
    
    def pre_play(self, video: str) -> Optional[bool]:
        pass

    def play_video(self, item: str) -> Optional[bool]:
        title = ''
        thumbnail = ''
        summary = ''
        item = json.loads(item)
        link = item.get("link", "")
        if link == "":
            return False
        try:
            ytdlp = YoutubeDL(params = {"quiet": True, "format": "best"})
            results = ytdlp.extract_info(link, download=False)
            title = results.get('title')
            thumbnails_list = results.get('thumbnails')
            thumbnail = thumbnails_list[-1]['url']
            summary = results.get('description', title)
            links_list = results.get('formats', [])
            links = [(link['format_id'], link['url']) for link in links_list]
            links.reverse()
            labels = [link[0] for link in links]
            ret = xbmcgui.Dialog().select("Select stream to play", labels)
            if ret >= 0:
                link = links[ret][1]
        except:
            return
        liz = xbmcgui.ListItem(title)
        if item.get("infolabels"):
            liz.setInfo("video", item["infolabels"])
        else:
            liz.setInfo("video", {"title": title, "plot": summary})
        liz.setArt({"thumb": thumbnail, "icon": thumbnail, "poster": thumbnail})
        
        xbmc.Player().play(link,liz)
        return True
