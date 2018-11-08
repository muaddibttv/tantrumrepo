# -*- coding: UTF-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# @tantrumdev wrote this file.  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: 69 Death Squad

import os
import re
import requests
import sys
import urllib
import xbmc

from resources.lib.modules import client, control, log_utils

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
control.moderator()
artPath = control.artPath()
addonFanart = control.addonFanart()


class documentary:
    def __init__(self):
        self.list = []

        self.docu_link = 'https://topdocumentaryfilms.com/'
        self.docu_cat_list = 'https://topdocumentaryfilms.com/watch-online/'

    def root(self):
        try:
            html = client.request(self.docu_cat_list)

            cat_list = client.parseDOM(html, 'div', attrs={'class': 'sitemap-wraper clear'})
            for content in cat_list:
                cat_info = client.parseDOM(content, 'h2')[0]
                cat_url = client.parseDOM(cat_info, 'a', ret='href')[0]
                cat_title = client.parseDOM(cat_info, 'a')[0].encode('utf-8', 'ignore').decode('utf-8').replace("&amp;", "&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'").replace('&#8211;',' - ').replace('&#8217;',"'").replace('&#8216;',"'").replace('&#038;','&').replace('&acirc;','')
                try:
                    cat_icon = client.parseDOM(content, 'img', ret='data-src')[0]
                except Exception:
                    cat_icon = client.parseDOM(content, 'img', ret='src')[0]
                cat_action = 'docuHeaven&docuCat=%s' % cat_url
                self.list.append({'name': cat_title, 'url': cat_url, 'image': cat_icon, 'action': cat_action})
        except Exception as e:
            log_utils.log('documentary root : Exception - ' + str(e))
            pass

        self.list = self.list[::-1]
        self.addDirectory(self.list)
        return self.list

    def docu_list(self, url):
        try:
            html = client.request(url)

            cat_list = client.parseDOM(html, 'article', attrs={'class': 'module'})
            for content in cat_list:
                docu_info = client.parseDOM(content, 'h2')[0]
                docu_url = client.parseDOM(docu_info, 'a', ret='href')[0]
                docu_title = client.parseDOM(docu_info, 'a')[0].replace("&amp;", "&").replace('&#39;', "'").replace('&quot;', '"').replace('&#39;', "'").replace('&#8211;', ' - ').replace('&#8217;', "'").replace('&#8216;', "'").replace('&#038;', '&').replace('&acirc;', '')
                try:
                    docu_icon = client.parseDOM(content, 'img', ret='data-src')[0]
                except Exception:
                    docu_icon = client.parseDOM(content, 'img', ret='src')[0]
                docu_action = 'docuHeaven&docuPlay=%s' % docu_url
                self.list.append({'name': docu_title, 'url': docu_url, 'image': docu_icon, 'action': docu_action})

            try:
                navi_content = client.parseDOM(html, 'div', attrs={'class': 'pagination module'})[0]
                links = client.parseDOM(navi_content, 'a', ret='href')
                link = links[(len(links)-1)]
                docu_action = 'docuHeaven&docuCat=%s' % link
                self.list.append({'name': control.lang(32053).encode('utf-8'), 'url': link, 'image': control.addonNext(), 'action': docu_action})
            except Exception:
                pass
        except Exception as e:
            log_utils.log('documentary docu_list : Exception - ' + str(e))
            pass

        self.addDirectory(self.list)
        return self.list

    def docu_play(self, url):
        control.moderator()
        try:
            docu_page = client.request(url)
            docu_item = client.parseDOM(docu_page, 'meta', attrs={'itemprop': 'embedUrl'}, ret='content')[0]
            if 'http:' not in docu_item and 'https:' not in docu_item:
                docu_item = 'https:' + docu_item
            url = docu_item

            if 'youtube' in url:
                if 'videoseries' not in url:
                    video_id = client.parseDOM(docu_page, 'div', attrs={'class': 'youtube-player'}, ret='data-id')[0]
                    url = 'plugin://plugin.video.youtube/play/?video_id=%s' % video_id
                else:
                    pass
            elif 'dailymotion' in url:
                video_id = client.parseDOM(docu_page, 'div', attrs={'class': 'youtube-player'}, ret='data-id')[0]
                url = self.getDailyMotionStream(video_id)
            else:
                log_utils.log('Play Documentary: Unknown Host: ' + str(url))
                control.infoDialog('Unknown Host - Report To Developer: ' + str(url), sound=True, icon='INFO')

            control.execute('PlayMedia(%s)' % url)
        except Exception as e:
            log_utils.log('docu_play: Exception - ' + str(e))
            pass

    def sort_key(self, elem):
        if elem[0] == "auto":
            return 1
        else:
            return int(elem[0].split("@")[0])

    # Code originally written by gujal, as part of the DailyMotion Addon in the official Kodi Repo. Modified to fit the needs here.
    def getDailyMotionStream(self, id):
        headers = {'User-Agent': 'Android'}
        cookie = {'Cookie': "lang=en_US; ff=off"}
        r = requests.get("http://www.dailymotion.com/player/metadata/video/"+id, headers=headers, cookies=cookie)
        content = r.json()
        if content.get('error') is not None:
            Error = (content['error']['title'])
            xbmc.executebuiltin('XBMC.Notification(Info:,' + Error + ' ,5000)')
            return
        else:
            cc = content['qualities']

            cc = cc.items()

            cc = sorted(cc, key=self.sort_key, reverse=True)
            m_url = ''
            other_playable_url = []

            for source, json_source in cc:
                source = source.split("@")[0]
                for item in json_source:

                    m_url = item.get('url', None)

                    if m_url:
                        if source == "auto":
                            continue

                        elif int(source) <= 2:
                            if 'video' in item.get('type', None):
                                return m_url

                        elif '.mnft' in m_url:
                            continue
                        other_playable_url.append(m_url)

            if len(other_playable_url) > 0:  # probably not needed, only for last resort
                for m_url in other_playable_url:

                    if '.m3u8?auth' in m_url:
                        rr = requests.get(m_url, cookies=r.cookies.get_dict(), headers=headers)
                        if rr.headers.get('set-cookie'):
                            print 'adding cookie to url'
                            strurl = re.findall('(http.+)', rr.text)[0].split('#cell')[0]+'|Cookie='+rr.headers['set-cookie']
                        else:
                            strurl = re.findall('(http.+)', rr.text)[0].split('#cell')[0]
                        return strurl

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try:
            name = control.lang(name).encode('utf-8')
        except Exception:
            pass
        url = '%s?action=%s' % (sysaddon, query) if isAction is True else query
        thumb = os.path.join(artPath, thumb) if artPath is not None else icon
        cm = []

        queueMenu = control.lang(32065).encode('utf-8')

        if queue is True:
            cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if context is not None:
            cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if addonFanart is not None:
            item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)

    def addDirectory(self, items, queue=False, isFolder=True):
        if items is None or len(items) is 0:
            control.idle()
            sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        for i in items:
            try:
                name = i['name']

                if i['image'].startswith('http'):
                    thumb = i['image']
                elif artPath is not None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb

                item = control.item(label=name)

                if isFolder:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % urllib.quote_plus(i['url'])
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'false')
                else:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % i['url']
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'true')
                    item.setInfo("mediatype", "video")
                    item.setInfo("audio", '')

                item.setArt({'icon': thumb, 'thumb': thumb})
                if addonFanart is not None:
                    item.setProperty('Fanart_Image', addonFanart)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
            except Exception:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
