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


import base64
import re
import traceback

from resources.lib.modules import cleantitle, client, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['sharemovies.net']
        self.base_link = 'http://sharemovies.net'
        self.search_link = '/search-movies/%s.html'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            q = cleantitle.geturl(title)
            q2 = q.replace('-', '+')
            url = self.base_link + self.search_link % q2
            r = client.request(url)
            match = re.compile('<div class="title"><a href="(.+?)">'+title+'</a></div>').findall(r)
            for url in match:
                return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('ShareMovies - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('ShareMovies - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            q = url + '-season-' + season
            q2 = url.replace('-', '+')
            url = self.base_link + self.search_link % q2
            r = client.request(url)
            match = re.compile('<div class="title"><a href="(.+?)-'+q+'\.html"').findall(r)
            for url in match:
                url = '%s-%s.html' % (url, q)
                r = client.request(url)
                match = re.compile('<a class="episode episode_series_link" href="(.+?)">' + episode + '</a>').findall(r)
                for url in match:
                    return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('ShareMovies - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = client.request(url)
            try:
                match = re.compile(
                    'themes/movies/img/icon/server/(.+?)\.png" width="16" height="16" /> <a href="(.+?)">Version ').findall(r)
                for host, url in match:
                    if host == 'internet':
                        pass
                    else:
                        sources.append({
                            'source': host,
                            'quality': 'SD',
                            'language': 'en',
                            'url': url,
                            'direct': False,
                            'debridonly': False
                        })
            except Exception:
                failure = traceback.format_exc()
                log_utils.log('ShareMovies - Exception: \n' + str(failure))
                return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('ShareMovies - Exception: \n' + str(failure))
            return
        return sources

    def resolve(self, url):
        r = client.request(url)
        match = re.compile('Base64\.decode\("(.+?)"').findall(r)
        for iframe in match:
            iframe = base64.b64decode(iframe)
            match = re.compile('src="(.+?)"').findall(iframe)
            for url in match:
                return url
