#######################################################################
#Import Modules Section
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys,xbmcvfs
import shutil
import time
import glo_var
import base_info
from resources.libs import extract
from resources.libs import downloader
#######################################################################

#######################################################################
# Primary Addon Variables
AddonID             = glo_var.AddonID
ADDONTITLE          = glo_var.ADDONTITLE
#######################################################################

#######################################################################
# Primary Addon Variables
ADVSETTINGSFILE     = glo_var.ADVSETTINGSFILE
#######################################################################

def ClearAdvanced():
    dialog = xbmcgui.Dialog()
    try:
        os.remove(ADVSETTINGSFILE)
    except:
        dialog.ok(ADDONTITLE, "[B][COLOR red]Sorry, we encountered an error[/COLOR][/B]",'[COLOR red]We were unable to remove the advancedsettings.xml file[/COLOR]')
        sys.exit(0)
        
    dialog.ok(ADDONTITLE, "[B][COLOR snow]Success, we have removed the advancedsettings.xml file.[/COLOR][/B]",'[COLOR white]The advancedsettings.xml has been removed successfully[/COLOR]')
    xbmc.executebuiltin("Container.Refresh")

def PatchAdvanced(name,url,description):
    if base_info.workingURL(url) == False: return False

    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    if not os.path.exists(path):
        os.makedirs(path)
    patchname = name
    dp = xbmcgui.DialogProgress()
    dp.create(ADDONTITLE,"","","[B]Advanced Settings: [/B]" + patchname)
    patchname = "advsettings"
    lib=os.path.join(path, patchname+'.zip')

    try:
        os.remove(lib)
    except:
        pass

    dialog = xbmcgui.Dialog()
    downloader.download(url, lib, dp)

    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"Extracting Zip Please Wait",""," ")
    extract.all(lib,addonfolder,dp)
    time.sleep(1)
    try:
        os.remove(lib)
    except:
        pass
    xbmc.executebuiltin("Container.Refresh")

    dialog.ok(ADDONTITLE, "[COLOR snow]Advanced Settings installed![/COLOR]","[COLOR white]You should now see an imporvment in buffering[/COLOR]")