# -*- coding: UTF-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# @tantrumdev wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: 69 Death Squad


import re
import traceback

from resources.lib.modules import cleantitle, client, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['iwatchflix.xyz']
        self.base_link = 'https://iwatchflix.xyz'
        self.movie_link = '/%s'
        self.tv_link = '/episode/%s-season-%s-episode-%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + self.movie_link % title
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('iwatchflixxyz - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('iwatchflixxyz - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            title = url
            url = self.base_link + self.tv_link % (title, season, episode)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('iwatchflixxyz - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = client.request(url)
            try:
                match = re.compile('vidoza(.+?)"').findall(r)
                for url in match:
                    url = 'https://vidoza%s' % url
                    sources.append({'source': 'Vidoza', 'quality': 'HD', 'language': 'en',
                                    'url': url, 'direct': False, 'debridonly': False})
            except Exception:
                failure = traceback.format_exc()
                log_utils.log('iwatchflixxyz - Exception: \n' + str(failure))
                return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('iwatchflixxyz - Exception: \n' + str(failure))
            return sources
        return sources

    def resolve(self, url):
        return url
