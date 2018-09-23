#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Fitness Zone
# Addon id: plugin.video.fitnesszone
# Addon Provider: MuadDib

#######################################################################
#Import Modules Section
import xbmc
import xbmcgui
import xbmcaddon
import base64
from glo_var import *
#######################################################################

#######################################################################
# YouTube API Settings
DATA_API      = base64.b64decode(b'QUl6YVN5QmRURXFVOXNhUDcwRHRvUTcxQ0VKbHRDYkMzSWV1UmM0')
DATA_CLIENT   = base64.b64decode(b'MTgzMTY1MzQzMjQ0LTlhOW1nMDFkNHBhNTEwc2djajNidm42c2Q1djVlNnNmLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29t')
DATA_SECRET   = base64.b64decode(b'enFfV1hvQzBUUTVoSDVyNFFvSVZjMjZq')
#######################################################################

def Apply_API():
    __settings__ = xbmcaddon.Addon(id='plugin.video.youtube')
    __settings__.setSetting("youtube.api.enable", 'true')
    __settings__.setSetting("youtube.api.last.switch", 'own')
    __settings__.setSetting("youtube.api.key", DATA_API)
    __settings__.setSetting("youtube.api.id", DATA_CLIENT)
    __settings__.setSetting("youtube.api.secret", DATA_SECRET)
    ytDialog = xbmcgui.Dialog()
    ytDialog.ok(ADDONTITLE, '[COLOR springgreen]YouTube API Keys Set To ' + ADDONTITLE + '[/COLOR]')