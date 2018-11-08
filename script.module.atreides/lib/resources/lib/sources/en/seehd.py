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

from resources.lib.modules import cfscrape, cleantitle, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['seehd.pl']
        self.base_link = 'http://www.seehd.pl'
        self.search_link = '/%s-%s-watch-online/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + self.search_link % (title, year)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('SeeHD - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('SeeHD - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            title = url
            season = '%02d' % int(season)
            episode = '%02d' % int(episode)
            se = 's%se%s' % (season, episode)
            url = self.base_link + self.search_link % (title, se)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('SeeHD - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            scraper = cfscrape.create_scraper()
            r = scraper.get(url).content
            try:
                match = re.compile('<iframe.+?src="(.+?)://(.+?)/(.+?)"').findall(r)
                for http, host, url in match:
                    host = host.replace('www.', '')
                    url = '%s://%s/%s' % (http, host, url)
                    if 'seehd' in host:
                        pass
                    else:
                        sources.append({'source': host, 'quality': 'HD', 'language': 'en',
                                        'url': url, 'direct': False, 'debridonly': False})
            except Exception:
                failure = traceback.format_exc()
                log_utils.log('SeeHD - Exception: \n' + str(failure))
                return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('SeeHD - Exception: \n' + str(failure))
            return sources
        return sources

    def resolve(self, url):
        return url
