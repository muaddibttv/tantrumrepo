#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

#######################################################################
#Import Modules Section
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys,xbmcvfs
import shutil
import glo_var
import time
from resources.libs import extract
#######################################################################

#######################################################################
# Primary Addon Variables
AddonID             = glo_var.AddonID
ADDONTITLE          = glo_var.ADDONTITLE
#######################################################################

#######################################################################
# Path Variables
COVENANTPATH         = glo_var.COVENANT
COVENANTDATAPATH     = glo_var.COVENANTDATA
#######################################################################

def AddonFix():

    ytDialog = xbmcgui.Dialog()
    if not os.path.exists(COVENANTPATH):
        ytDialog(ADDONTITLE,"[COLOR springgreen]The Covenant Addon is not installed. Canceling fix....[/COLOR]")
        quit()
    if os.path.exists(COVENANTDATAPATH):
        try:
            shutil.rmtree(COVENANTDATAPATH)
        except:
            ytDialog.ok(ADDONTITLE,"[COLOR red]There was an error removing the Covenant addon data folder[/COLOR]")
            quit()
    try:
        COVENANT_FOLDER = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.covenant')
        os.makedirs(COVENANT_FOLDER)
        PATCH_FILE = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'resources/files/covenant_settings.xml'))
        FILE_TO_PATCH = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.covenant/settings.xml')
        shutil.copyfile(PATCH_FILE, FILE_TO_PATCH)
    except:
        ytDialog.ok(ADDONTITLE,"[COLOR red]There was an error patching the Covenant addon data settings[/COLOR]")
        quit()
    ytDialog.ok(ADDONTITLE,"[COLOR snow]The Covenant addon has been patched. Addon has been reset.[/COLOR]")