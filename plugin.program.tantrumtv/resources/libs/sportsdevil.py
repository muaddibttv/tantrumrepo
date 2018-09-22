#######################################################################
#Import Modules Section
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys,xbmcvfs
import shutil
import time
import glo_var
from resources.libs import extract
from resources.libs import downloader
#######################################################################

#######################################################################
# Primary Addon Variables
ADDONTITLE          = glo_var.ADDONTITLE
#######################################################################

def SDFix():

    SPORTS_DEVIL_FOLDER = xbmc.translatePath(os.path.join('special://home/addons','plugin.video.SportsDevil'))
    SPORTS_DEVIL_DATA = xbmc.translatePath('special://userdata/addon_data/plugin.video.SportsDevil')
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))

    choice = xbmcgui.Dialog().yesno(ADDONTITLE,'This option will remove all traces of Sports Devil (If Installed) and install a clean version.','Would you like to continue?',yeslabel='[B][COLOR springgreen]YES[/COLOR][/B]',nolabel='[B][COLOR snow]NO[/COLOR][/B]')
    if choice == 0:
        sys.exit(1)
    dialog = xbmcgui.Dialog()
    if os.path.exists(SPORTS_DEVIL_FOLDER):
        try:
            shutil.rmtree(SPORTS_DEVIL_FOLDER)
        except: pass
    if os.path.exists(SPORTS_DEVIL_DATA):
        try:
            shutil.rmtree(SPORTS_DEVIL_DATA)
        except: pass
    purgePath = xbmc.translatePath('special://home/addons/packages')
    for root, dirs, files in os.walk(purgePath):
        file_count = 0
        file_count += len(files)
    for root, dirs, files in os.walk(purgePath):
        file_count = 0
        file_count += len(files)
        if file_count > 0:
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    if not os.path.exists(path):
        os.makedirs(path)

    url = ('http://repo.tantrumtv.com/dm/patches/plugin.video.SportsDevil.zip')
    dp = xbmcgui.DialogProgress()
    dp.create(ADDONTITLE,"","","Installing Sports Devil")
    lib=os.path.join(path, 'addon.zip')

    try:
        os.remove(lib)
    except:
        pass

    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://home','addons'))
    time.sleep(2)
    dp.update(0,"","Extracting Zip Please Wait","")
    extract.all(lib,addonfolder,dp)
    try:
        os.remove(lib)
    except:
        pass
    xbmc.executebuiltin("ActivateWindow(busydialog)")
    xbmc.executebuiltin("UpdateAddonRepos")
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.executebuiltin("Dialog.Close(busydialog)")

    dialog.ok(ADDONTITLE,"[COLOR snow]The Sports Devil plugin should now be fixed and working correctly. If you have any issues please turn AUTO UPDATE OFF on Sports Devil and run this fix again.[/COLOR]")
    quit()