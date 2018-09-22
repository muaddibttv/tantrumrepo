#######################################################################
#Import Modules Section
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs
import os
import sys 
import glob
import shutil
import urllib2,urllib
import re
import backuprestore
import glo_var
import base_info
from resources.libs import skinSwitch
from resources.libs import downloader
from resources.libs import extract
from resources.libs import notify
from datetime import date, datetime, timedelta
#######################################################################

#######################################################################
#Global Variables
#Do Not Edit These Variables or any others in this wizard!
HOMEPATH       = glo_var.HOMEPATH
ADDONS         = glo_var.ADDONS
ADDON_ID       = glo_var.ADDON_ID
ADDONTITLE     = glo_var.ADDONTITLE
AUTOUPDATE     = glo_var.AUTOUPDATE
BUILDCHECK     = base_info.getS('lastbuildcheck')
BUILDNAME      = base_info.getS('buildname')
BUILDVERSION   = base_info.getS('buildversion')
my_addon       = xbmcaddon.Addon()
checkver       = my_addon.getSetting('checkupdates')
USERDATAPATH   = glo_var.USERDATAPATH
CHECKVERSION   = os.path.join(USERDATAPATH,'version.txt')
COLOR1         = glo_var.COLOR1
COLOR2         = glo_var.COLOR2
cr             = glo_var.COLOR
cr1            = glo_var.COLOR1
cr2            = glo_var.COLOR2
DEFAULTIGNORE  = base_info.getS('defaultskinignore')
DEFAULTNAME    = base_info.getS('defaultskinname')
DEFAULTSKIN    = base_info.getS('defaultskin')
DIALOG         = xbmcgui.Dialog()
dp             = glo_var.dp
ENABLE         = glo_var.ENABLE
EXTRACT        = base_info.getS('extract')
EXTERROR       = base_info.getS('errors')
FAILED         = False
gn             = glo_var.GROUP_NAME
INSTALLED      = base_info.getS('installed')
NOTIFICATION   = glo_var.NOTIFICATION
NOTIFY         = base_info.getS('notify')
NOTEDISMISS    = base_info.getS('notedismiss')
NOTEID         = base_info.getS('noteid') 
NOTEID         = 0 if NOTEID == "" else int(NOTEID)
PLUGIN         = os.path.join(ADDONS,   ADDON_ID)
SKIN           = xbmc.getSkinDir()
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
ONEWEEK        = TODAY + timedelta(days=7)
UPDATECHECK    = glo_var.UPDATECHECK if str(glo_var.UPDATECHECK).isdigit() else 1
NEXTCHECK      = TODAY + timedelta(days=UPDATECHECK)
WIZARDFILE     = glo_var.WIZARDFILE
WORKING        = True if base_info.workingURL(WIZARDFILE) == True else False
VERSION        = base_info.addonInfo(ADDON_ID,'version')
VER            = glo_var.VERSION
#######################################################################

#######################################################################
def checkSkin():
    base_info.loga("[Build Check] Invalid Skin Check Start")
    DEFAULTSKIN   = base_info.getS('defaultskin')
    DEFAULTNAME   = base_info.getS('defaultskinname')
    DEFAULTIGNORE = base_info.getS('defaultskinignore')
    gotoskin = False
    if not DEFAULTSKIN == '':
        if os.path.exists(os.path.join(ADDONS, DEFAULTSKIN)):
            if DIALOG.yesno(ADDONTITLE, "[COLOR %s]It seems that the skin has been set back to [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, SKIN[5:].title()), "Would you like to set the skin back to:[/COLOR]", '[COLOR %s]%s[/COLOR]' % (COLOR1, DEFAULTNAME)):
                gotoskin = DEFAULTSKIN
                gotoname = DEFAULTNAME
            else: base_info.loga("Skin was not reset"); base_info.setS('defaultskinignore', 'true'); gotoskin = False
        else: base_info.setS('defaultskin', ''); base_info.setS('defaultskinname', ''); DEFAULTSKIN = ''; DEFAULTNAME = ''
    if DEFAULTSKIN == '':
        skinname = []
        skinlist = []
        for folder in glob.glob(os.path.join(ADDONS, 'skin.*/')):
            xml = "%s/addon.xml" % folder
            if os.path.exists(xml):
                f  = open(xml,mode='r'); g = f.read().replace('\n','').replace('\r','').replace('\t',''); f.close();
                match = re.compile('<addon.+?id="(.+?)".+?>').findall(g)
                match2 = re.compile('<addon.+?name="(.+?)".+?>').findall(g)
                base_info.loga("%s: %s" % (folder, str(match[0])))
                if len(match) > 0: skinlist.append(str(match[0])); skinname.append(str(match2[0]))
                else: base_info.loga("ID not found for %s" % folder)
            else: base_info.loga("ID not found for %s" % folder)
        if len(skinlist) > 0:
            if len(skinlist) > 1:
                if DIALOG.yesno(ADDONTITLE, "[COLOR %s]It seems that the skin has been set back to [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, SKIN[5:].title()), "Would you like to view a list of avaliable skins?[/COLOR]"):
                    choice = DIALOG.select("Select skin to switch to!", skinname)
                    if choice == -1: base_info.loga("Skin was not reset"); base_info.setS('defaultskinignore', 'true')
                    else: 
                        gotoskin = skinlist[choice]
                        gotoname = skinname[choice]
                else: base_info.loga("Skin was not reset"); base_info.setS('defaultskinignore', 'true')
            else:
                if DIALOG.yesno(ADDONTITLE, "[COLOR %s]It seems that the skin has been set back to [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, SKIN[5:].title()), "Would you like to set the skin back to:[/COLOR]", '[COLOR %s]%s[/COLOR]' % (COLOR1, skinname[0])):
                    gotoskin = skinlist[0]
                    gotoname = skinname[0]
                else: base_info.loga("Skin was not reset"); base_info.setS('defaultskinignore', 'true')
        else: base_info.loga("No skins found in addons folder."); base_info.setS('defaultskinignore', 'true'); gotoskin = False
    if gotoskin:
        skinSwitch.swapSkins(gotoskin)
        x = 0
        xbmc.sleep(1000)
        while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 150:
            x += 1
            xbmc.sleep(200)

        if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
            xbmc.executebuiltin('SendClick(11)')
            base_info.lookandFeelData('restore')
        else: base_info.LogNotify(ADDONTITLE,'[COLOR red]Skin Swap Timed Out![/COLOR]')
    base_info.loga("[Build Check] Invalid Skin Check End")

while xbmc.Player().isPlayingVideo():
    xbmc.sleep(1000)

base_info.loga("[Auto Update Wizard] Started")
if AUTOUPDATE == 'Yes':
    base_info.wizardUpdate('startup')
else: base_info.loga("[Auto Update Wizard] Not Enabled")

base_info.loga("[Notifications] Started")
if ENABLE == 'Yes':
    if not NOTIFY == 'true':
        url = base_info.workingURL(NOTIFICATION)
        if url == True:
            link  = base_info.OPEN_URL(NOTIFICATION).replace('\r','').replace('\t','')
            id, msg = link.split('|||')
            if int(id) == int(NOTEID):
                if NOTEDISMISS == 'false':
                    notify.notification(msg=msg)
                else: base_info.loga("[Notifications] id[%s] Dismissed" % int(id))
            elif int(id) > int(NOTEID):
                base_info.loga("[Notifications] id: %s" % str(int(id)))
                base_info.setS('noteid', str(int(id)))
                base_info.setS('notedismiss', 'false')
                if BUILDCHECK == '' and BUILDNAME == '':
                    base_info.loga("[Notifications] First Run, skipping base notify window")
                else:
                    notify.notification(msg=msg)
                base_info.loga("[Notifications] Complete")
        else: base_info.loga("[Notifications] URL(%s): %s" % (NOTIFICATION, url))
    else: base_info.loga("[Notifications] Turned Off")
else: base_info.loga("[Notifications] Not Enabled")

base_info.loga("[Version Check] Version Check Start")
if not os.path.exists(CHECKVERSION):
        file = open(CHECKVERSION,'w') 
        file.write("<version>0</version>")
        file.close()
checkurl = (VER)
vers = open(CHECKVERSION, "r")
regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
for line in vers:
    if checkver!='false':
        currversion = regex.findall(line)
        for build,vernumber in currversion:
            if vernumber > 0:
                req = urllib2.Request(checkurl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match = re.compile('<build>'+build+'</build><version>(.+?)</version>').findall(link)
                for newversion in match:
                    if vernumber > 0:
                        req = urllib2.Request(checkurl)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response = urllib2.urlopen(req)
                        link=response.read()
                        response.close()
                        match = re.compile('<build>'+build+'</build><version>(.+?)</version>').findall(link)
                        for newversion in match:
                            if newversion > vernumber:
                                yes_pressed = xbmcgui.Dialog().yesno(cr+gn+" Wizard"+cr2, cr+'A NEW version of this build has been released!'+cr2, cr1+'Would you like to install the new version now?'+cr2, '', yeslabel=cr+'YES'+cr2,nolabel=cr1+'LATER'+cr2)
                                if yes_pressed:
                                    if 'Adult' in build:
                                        url = 'plugin://%s/?mode=adult' % ADDON_ID
                                    else:
                                        url = 'plugin://%s/?mode=builds' % ADDON_ID
                                    xbmc.executebuiltin('ActivateWindow(10025, "%s", return)' % url)
                                else: DIALOG.ok(cr+gn+' Wizard'+cr2,cr1+'No Problem, you can always run the update from the wizard when its convenient for you.'+cr2,'','')
                                sys.exit(0)            
else: base_info.loga("[Version Check] Version Check Check End")

base_info.loga("[Installed Check] Started")
if INSTALLED == 'true':
    if KODIV >= 17:
        base_info.kodi17Fix()
        if SKIN in ['skin.confluence', 'skin.estuary']:
            checkSkin()
        FAILED = True
    elif not EXTRACT == '100':
        base_info.loga("[Installed Check] Build was extracted %s/100 with [ERRORS: %s]" % (EXTRACT, EXTERROR))
        yes=DIALOG.yesno(ADDONTITLE, '[COLOR %s]%s[/COLOR] [COLOR %s]was not installed correctly!' % (COLOR1, COLOR2, BUILDNAME), 'Installed: [COLOR %s]%s[/COLOR] / Error Count: [COLOR %s]%s[/COLOR]' % (COLOR1, EXTRACT, COLOR1, EXTERROR), 'Would you like to try again?[/COLOR]', nolabel='[B]No Thanks![/B]', yeslabel='[B]Retry Install[/B]')
        base_info.clearS('build')
        FAILED = True
        if yes: 
            xbmc.executebuiltin("PlayMedia(plugin://%s/?mode=install&name=%s&url=fresh)" % (ADDON_ID, urllib.quote_plus(BUILDNAME)))
            base_info.loga("[Installed Check] Fresh Install Re-activated")
        else: base_info.loga("[Installed Check] Reinstall Ignored")
    elif SKIN in ['skin.confluence', 'skin.estuary']:
        base_info.loga("[Installed Check] Incorrect skin: %s" % SKIN)
        gui = base_info.checkBuild(BUILDNAME, 'gui')
        FAILED = True
        if gui == 'http://':
            base_info.loga("[Installed Check] Guifix was set to http://")
            DIALOG.ok(ADDONTITLE, "[COLOR %s]It looks like the skin settings was not applied to the build." % COLOR2, "Sadly no gui fix was attatched to the build", "You will need to reinstall the build and make sure to do a force close[/COLOR]")
        elif base_info.workingURL(gui):
            yes=DIALOG.yesno(ADDONTITLE, '%s was not installed correctly!' % BUILDNAME, 'It looks like the skin settings was not applied to the build.', 'Would you like to apply the GuiFix?', nolabel='[B]No, Cancel[/B]', yeslabel='[B]Apply Fix[/B]')
            if yes: xbmc.executebuiltin("PlayMedia(plugin://%s/?mode=install&name=%s&url=gui)" % (ADDON_ID, urllib.quote_plus(BUILDNAME))); base_info.loga("[Installed Check] Guifix attempting to install")
            else: base_info.loga('[Installed Check] Guifix url working but cancelled: %s' % gui)
        else:
            DIALOG.ok(ADDONTITLE, "[COLOR %s]It looks like the skin settings was not applied to the build." % COLOR2, "Sadly no gui fix was attatched to the build", "You will need to reinstall the build and make sure to do a force close[/COLOR]")
            base_info.loga('[Installed Check] Guifix url not working: %s' % gui)
    else:
        base_info.loga('[Installed Check] Install seems to be completed correctly')
    if KEEPTRAKT == 'true': traktit.traktIt('restore', 'all'); base_info.loga('[Installed Check] Restoring Trakt Data')
    if KEEPREAL  == 'true': debridit.debridIt('restore', 'all'); base_info.loga('[Installed Check] Restoring Real Debrid Data')
    if KEEPLOGIN == 'true': loginit.loginIt('restore', 'all'); base_info.loga('[Installed Check] Restoring Login Data')
    base_info.clearS('install')
else: base_info.loga("[Installed Check] Not Enabled")

if FAILED == False:
    base_info.loga("[Build Check] Started")
    if not WORKING:
        base_info.loga("[Build Check] Not a valid URL for Build File: %s" % WIZARDFILE)
    elif BUILDCHECK == '' and BUILDNAME == '':
        base_info.loga("[Build Check] First Run")
        notify.firstRun()
        base_info.setS('lastbuildcheck', str(NEXTCHECK))
    elif not BUILDNAME == '':
        base_info.loga("[Build Check] Build Installed")
        if SKIN in ['skin.confluence', 'skin.estuary'] and not DEFAULTIGNORE == 'true':
            checkSkin()
            base_info.loga("[Build Check] Build Installed: Checking Updates")
            base_info.setS('lastbuildcheck', str(NEXTCHECK))
            checkUpdate()
        elif BUILDCHECK <= str(TODAY):
            base_info.loga("[Build Check] Build Installed: Checking Updates")
            base_info.setS('lastbuildcheck', str(NEXTCHECK))
            checkUpdate()
        else: 
            base_info.loga("[Build Check] Build Installed: Next check isnt until: %s / TODAY is: %s" % (BUILDCHECK, str(TODAY)))
#######################################################################         