# -*- coding: utf-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # As long as you retain this notice you can do whatever you want with this
 # stuff. If we meet some day, and you think this stuff is worth it, you can
 # buy me a beer in return.
 # ----------------------------------------------------------------------------
#######################################################################

# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Thanks to the Authors of the base code
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# modified by: MuadDib
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.tantrumtvchannel'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "PLCFu4DdaZx0nQx2gMlOKKFobU5-5xH8sG"     # Tantrum.TV Playlist
YOUTUBE_CHANNEL_ID_2 = "PLCFu4DdaZx0kH7jrjvwhM8DkdpPPqdGd7"     # Kodi (IN)Sanity Playlist
YOUTUBE_CHANNEL_ID_3 = "PLCFu4DdaZx0lOLkA2LOrNqAHBGlMMTeVw"     # Tutorials and How-To
YOUTUBE_CHANNEL_ID_4 = "PLCFu4DdaZx0lBgVtEqrEMWYsYlNrhkA-h"     # Streaming to a Desktop

# Entry point
def run():
    plugintools.log("docu.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("docu.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title="Tantrum.TV Videos",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="special://home/addons/plugin.video.tantrumtvchannel/icon.png",
        fanart="special://home/addons/plugin.video.tantrumtvchannel/fanart.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Kodi (IN)Sanity Vidoes",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="special://home/addons/plugin.video.tantrumtvchannel/icon.png",
        fanart="special://home/addons/plugin.video.tantrumtvchannel/fanart.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Streaming on a Desktop PC",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="special://home/addons/plugin.video.tantrumtvchannel/icon.png",
        fanart="special://home/addons/plugin.video.tantrumtvchannel/fanart.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Tutorials and How-To",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="special://home/addons/plugin.video.tantrumtvchannel/icon.png",
        fanart="special://home/addons/plugin.video.tantrumtvchannel/fanart.jpg",
        folder=True )
        
run()