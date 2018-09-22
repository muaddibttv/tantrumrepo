#######################################################################
#Import Modules Section
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs
import base64, os, sys, time
import shutil
import glo_var
from resources.libs import extract
#######################################################################

#######################################################################
# Primary Variables
ADDONTITLE          = glo_var.ADDONTITLE
YOUTUBEPATH         = glo_var.YOUTUBE
YOUTUBEDATAPATH     = glo_var.YOUTUBEDATA
#######################################################################

#######################################################################
# YouTube API Settings
DATA_API      = base64.b64decode(b'QUl6YVN5RGI0YTNwME5CdzFwVDI0NkNFeGgwMzRaWmJ1czlvbjQ0')
DATA_CLIENT   = base64.b64decode(b'MTgzMTY1MzQzMjQ0LWtwMjdsc2FhNjgwbnJnazUxYTd1azF1OXNvaWI1b2Jz')
DATA_SECRET   = base64.b64decode(b'dXI4UXNLdHFUTWtRQUN3MkpYYkFwX05Z')
#######################################################################

def YoutubeFix():
    ytDialog = xbmcgui.Dialog()
    if not os.path.exists(YOUTUBEPATH):
        ytDialog(ADDONTITLE,"[COLOR springgreen]The YouTube Addon is not installed. Canceling fix....[/COLOR]")
        quit()
    try:
        __settings__ = xbmcaddon.Addon(id='plugin.video.youtube')
        __settings__.setSetting("youtube.api.enable", 'true')
        __settings__.setSetting("youtube.api.last.switch", 'own')
        __settings__.setSetting("youtube.api.key", DATA_API)
        __settings__.setSetting("youtube.api.id", DATA_CLIENT)
        __settings__.setSetting("youtube.api.secret", DATA_SECRET)
    except:
        ytDialog.ok(ADDONTITLE,"[COLOR red]There was an error patching the YouTube addon data settings[/COLOR]")
        quit()
    ytDialog.ok(ADDONTITLE,"[COLOR snow]The YouTube addon has been patched. Daily Limit error should be resolved.[/COLOR]")