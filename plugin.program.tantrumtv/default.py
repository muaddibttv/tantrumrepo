#######################################################################
#Import Modules Section
import xbmcplugin, xbmcaddon
import sys
import urllib
import re
import glo_var
import base_info
import backuprestore
from resources.libs import advanced
from resources.libs import contact
from resources.libs import covenant
from resources.libs import notify
from resources.libs import sportsdevil
from resources.libs import wizard as wiz
from resources.libs import theme_functions as themehelper
from resources.libs import youtube
global parse
#######################################################################


#######################################################################
# Global Variables
AddonID        = glo_var.AddonID
THISADDON      = glo_var.THISADDON
ARTA           = glo_var.ADULT_ICON
ARTK           = glo_var.KRYPTON_ICON
ARTB           = glo_var.BACKUP_ICON
ARTBL          = glo_var.BACKUPLOGIN_ICON
ARTBU          = glo_var.BUILDS_ICON
ARTCI          = glo_var.CACHE_ICON
ARTCP          = glo_var.CONVERTPATH_ICON
ARTCR          = glo_var.CHKREPO_ICON
ARTCS          = glo_var.CHKSOURCE_ICON
ARTC           = glo_var.CREDIT_ICON
ARTDA          = glo_var.DELETEALL_ICON
ARTDB          = glo_var.DELETEBACKUP_ICON
ARTD           = glo_var.DEV_ICON
ARTF           = glo_var.FRESHSTART_ICON
ARTM           = glo_var.MAINT_ICON
ARTP           = glo_var.PACKAGES_ICON
ARTR           = glo_var.REST_ICON
ARTRB          = glo_var.RESTOREBACKUP_ICON
ARTRL          = glo_var.RESTORELOGIN_ICON
ICON_SAVE      = glo_var.SAVE_ICON
ARTS           = glo_var.SUPPORT_ICON
ARTTH          = glo_var.THUMBNAILS_ICON
ARTFC          = glo_var.FORCECLOSE_ICON
ARTCCL         = glo_var.CLEARCRASH_ICON
ICON_THEMES    = glo_var.THEME_ICON
ARTV           = glo_var.VIEWLOG_ICON
CONT_NOT       = contact.CONT_NOT
CREDITSFILE    = glo_var.CREDITSFILE
DEVELOPER      = base_info.getS('developer')
FANART         = glo_var.FANART
gn             = glo_var.GROUP_NAME
ICON           = glo_var.ICON
ICONMAINT      = glo_var.ICONMAINT if not glo_var.ICONMAINT == 'http://' else ICON
ICONSAVE       = glo_var.ICONSAVE if not glo_var.ICONSAVE == 'http://' else ICON
ICON_FIXES     = glo_var.ICON_FIXES
ICON_TWEAKS    = glo_var.ICON_TWEAKS
ICON_FIXESMENU = glo_var.ICON_FIXESMENU
KEEPFAVS       = base_info.getS('keepfavourites')
KEEPSOURCES    = base_info.getS('keepsources')
KEEPPROFILES   = base_info.getS('keepprofiles')
KEEPADVANCED   = base_info.getS('keepadvanced')
THEME          = base_info.getS('theme')
THEME1         = glo_var.THEME1
VERSION        = THISADDON.getAddonInfo('version')
ADDF           = base_info.addFile
ANDROID        = base_info.getS('android')
####################################################################################


#######################################################################
# Menu Title Variables
ADULTTITLE     = glo_var.ADULT
BUILDTITLE     = glo_var.BUILD
CONTACTTITLE   = glo_var.CONTACTUS
CREDITSTITLE   = glo_var.WIZCREDITS
DEVTITLE       = glo_var.DEV
FIXESTITLE     = glo_var.FIXESTWEAKS
KRYPTONTITLE   = glo_var.KRYPTON
MAINTTITLE     = glo_var.MAINT
THEMETITLE     = glo_var.THEME
RESTORETITLE   = glo_var.REST
SAVETITLE      = glo_var.SAVE

BKUPBUILDTITLE = glo_var.BACKUPBUILD
BKUPLOGINTITLE = glo_var.BACKUPLOGIN
CHKREPOTITLE   = glo_var.CHKREPO
CHKSRCTITLE    = glo_var.CHKSOURCE
CLEARCACHETITLE= glo_var.CLEARCACHE
CLEARCRASHTITLE= glo_var.CLEARCRASH
CLEARPKGSTITLE = glo_var.CLEARPACK
CLEARTHUMBTITLE= glo_var.CLEARTHUMB
CONVERTTITLE   = glo_var.CONVERT
COVENANTTITLE  = glo_var.COVENANTTITLE
DELALLBKUPTITLE= glo_var.DELETEALL
DELBKUPTITLE   = glo_var.DELETEBACKUP
FORCETITLE     = glo_var.FORCECLOSE
FRESHTITLE     = glo_var.FRESHSTART
RELOADTITLE    = glo_var.RELOAD
RSTRBUILDTITLE = glo_var.RESTOREBUILDBCK
RSTRLOGINTITLE = glo_var.RESTORELOGIN
UPDATETITLE    = glo_var.FORCEUPDATE
VIEWLOGTITLE   = glo_var.VIEW
VIEWOLDLOGTITLE= glo_var.VIEWOLD
VIEWWIZLOGTITLE= glo_var.VIEWWIZ
YOUTUBETITLE   = glo_var.YOUTUBETITLE
SDTITLE        = glo_var.SDTITLE
DEBUGTITLE     = glo_var.DEBUGTITLE
DEBUGSKIN      = glo_var.DEBUGSKIN
CLEARADVTITLE  = glo_var.CLEARADVTITLE
ROOTTITLE      = glo_var.ROOTTITLE
###################################################################################


#######################################################################
# Active Menu Variables
ADULTACTIVE    = glo_var.ADULTACTIVE
ADVANCEDFILE   = glo_var.ADVANCEDFILE
DEVACTIVE      = glo_var.DEVELOPERACTIVE
FIXESACTIVE    = glo_var.FIXESACTIVE
THEMEACTIVE    = glo_var.THEMEACTIVE
###################################################################################


#######################################################################
# Menu File Variables
ADULTFILE      = glo_var.ADULTFILE
NOTIFICATION   = glo_var.NOTIFICATION
SUPPORT        = glo_var.SUPPORT
THEMEFILE      = glo_var.THEMEFILE
VERSION        = glo_var.VERSION
WIZARDFILE     = glo_var.WIZARDFILE
WIZVER         = glo_var.WIZVER
###################################################################################


###################################################################################
# Categories/Default Menu
def Categories():
    base_info.addDir(themehelper.menuTitle(BUILDTITLE), 'url', 'builds', ARTBU,FANART,'')
    if ADULTACTIVE == 'true': base_info.addDir(themehelper.menuTitle(ADULTTITLE),'url','adult',ARTA,FANART,'')
    if THEMEACTIVE == 'true': base_info.addDir(themehelper.menuTitle(THEMETITLE),'url','thememenu',ICON_THEMES,FANART,'')
    base_info.addDir(themehelper.menuTitle(SAVETITLE),'url','savedata',ICON_SAVE,FANART,'')
    base_info.addDir(themehelper.menuTitle(RESTORETITLE),'url','restoremenu',ARTR,FANART,'')
    base_info.addDir(themehelper.menuTitle(MAINTTITLE),'url','maint',ARTM,FANART,'')
    if FIXESACTIVE == 'true':
        base_info.addDir(themehelper.menuTitle(FIXESTITLE),'url','fixes',ICON_FIXESMENU,FANART,'')
    if DEVACTIVE == 'true': base_info.addDir(themehelper.menuTitle(DEVTITLE),'url','developer',ARTD,FANART,'')
    base_info.addDir2(themehelper.menuTitle(CONTACTTITLE),'url','contact',ARTS,FANART,'')
    base_info.addDir2(themehelper.menuTitle(CREDITSTITLE),'url','wizcreds',ARTC,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
###################################################################################


###################################################################################
#Builds Menu
def Builds_Menu():
    base_info.addDir2('[COLOR dodgerblue]Standard Builds[/COLOR]', 'http://', 'section', ARTBU, ARTBU, '')
    if base_info.checkVersion("version") > 0:
        base_info.addDir2('[COLOR red]Installed Build: [/COLOR][COLOR snow]'+ base_info.checkVersion("build") +'[/COLOR]', 'http://', 'section', ARTBU, ARTBU, '')
        base_info.addDir2('[COLOR red]Installed Version: [/COLOR][COLOR snow]'+ base_info.checkVersion("version") +'[/COLOR]', 'http://', 'section', ARTBU, ARTBU, '')
        base_info.addDir2('[COLOR red]Current Version: [/COLOR][COLOR snow]'+ base_info.checkVersion("newversion") +'[/COLOR]', 'http://', 'section', ARTBU, ARTBU, '')
    base_info.addDir2('[COLOR red]============================================[/COLOR]', 'http://', 'section', ARTBU, ARTBU, '')
    base_info.addDir2(' ', 'http://', 'section', ARTBU, ARTBU, '')
    link = base_info.OPEN_URL(glo_var.BASEURL + 'wizard.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        base_info.addDir2(themehelper.buildTitle(name),url,'install',iconimage,fanart,description)
        xbmc.executebuiltin('Container.SetViewMode(50)')
####################################################################################


###################################################################################
# Adult Menu
def Adult_Menu():
    base_info.addDir2('[COLOR dodgerblue]Adult (18+) Builds[/COLOR]', 'http://', 'section', ARTA, ARTA, '')
    if base_info.checkVersion("version") > 0:
        base_info.addDir2('[COLOR red]Installed Build: [/COLOR][COLOR snow]'+ base_info.checkVersion("build") +'[/COLOR]', 'http://', 'section', ARTA, ARTA, '')
        base_info.addDir2('[COLOR red]Installed Version: [/COLOR][COLOR snow]'+ base_info.checkVersion("version") +'[/COLOR]', 'http://', 'section', ARTA, ARTA, '')
        base_info.addDir2('[COLOR red]Current Version: [/COLOR][COLOR snow]'+ base_info.checkVersion("newversion") +'[/COLOR]', 'http://', 'section', ARTA, ARTA, '')
    base_info.addDir2('[COLOR red]============================================[/COLOR]', 'http://', 'section', ARTA, ARTA, '')
    base_info.addDir2(' ', 'http://', 'section', ARTA, ARTA, '')
    link = base_info.OPEN_URL(ADULTFILE).replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,image,fanart,description in match:
        base_info.addDir2(themehelper.buildTitle(name),url,'adultwiz',image,fanart,description)
        xbmc.executebuiltin('Container.SetViewMode(50)')

####################################################################################


###################################################################################
#Krypton Build Menu
def Krypton_Menu():
    base_info.addDir2('[COLOR dodgerblue]Standard Krypton Builds[/COLOR]', 'http://', 'install', ARTK, ARTK, '')
    if base_info.checkVersion("version") > 0:
        base_info.addDir2('[COLOR red]Installed Build: [/COLOR][COLOR snow]'+ base_info.checkVersion("build") +'[/COLOR]', 'http://', 'section', ARTK, ARTK, '')
        base_info.addDir2('[COLOR red]Installed Version: [/COLOR][COLOR snow]'+ base_info.checkVersion("version") +'[/COLOR]', 'http://', 'section', ARTK, ARTK, '')
        base_info.addDir2('[COLOR red]Current Version: [/COLOR][COLOR snow]'+ base_info.checkVersion("newversion") +'[/COLOR]', 'http://', 'section', ARTK, ARTK, '')
    base_info.addDir2('[COLOR red]============================================[/COLOR]', 'http://', 'section', ARTK, ARTK, '')
    base_info.addDir2(' ', 'http://', 'section', ARTK, ARTK, '')
    link = base_info.OPEN_URL(KRYPTONFILE).replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,image,fanart,description in match:
        base_info.addDir2(themehelper.buildTitle(name), url,'kryptonwiz',image,fanart,description)
        xbmc.executebuiltin('Container.SetViewMode(50)')
####################################################################################


###################################################################################
#Theme Menu
def Theme_Menu():
    base_info.addDir2('[COLOR dodgerblue]Build Themes[/COLOR]', 'http://', 'section', ICON_THEMES, ARTBU, '')
    base_info.addDir2('[COLOR snow]These themes are customized for our builds[/COLOR]', 'http://', 'section', ICON_THEMES, ARTA, '')
    base_info.addDir2('[COLOR red]============================================[/COLOR]', 'http://', 'section', ICON_THEMES, ARTBU, '')
    base_info.addDir2(' ', 'http://', 'section', ICON_THEMES, ARTBU, '')
    link = base_info.OPEN_URL(THEMEFILE).replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        base_info.addDir2(themehelper.buildTitle(name),url,'theme',iconimage,fanart,description)
    xbmc.executebuiltin('Container.SetViewMode(50)')
####################################################################################


###################################################################################
#Backup Menu
def Backup_Menu():
    base_info.addDir2('[COLOR dodgerblue]Settings to Keep[/COLOR]', 'http://', 'section', ICON_SAVE, ARTBU, '')
    base_info.addDir2('[COLOR red]============================================[/COLOR]', 'http://', 'section', ICON_SAVE, ARTBU, '')
    on = '[COLOR green]ON[/COLOR]'; off = '[COLOR red]OFF[/COLOR]'
    sources    = 'true' if KEEPSOURCES   == 'true' else 'false'
    advanced   = 'true' if KEEPADVANCED  == 'true' else 'false'
    profiles   = 'true' if KEEPPROFILES  == 'true' else 'false'
    favourites = 'true' if KEEPFAVS      == 'true' else 'false'
    mySources = 'Keep \'Sources\': %s ' % sources.replace('true',on).replace('false',off)
    myProfiles = 'Keep \'Profiles\': %s' % profiles.replace('true',on).replace('false',off)
    myAdvanced = 'Keep \'Advancedsettings\': %s' % advanced.replace('true',on).replace('false',off)
    myFavs = 'Keep \'Favourites\': %s' % favourites.replace('true',on).replace('false',off)
    base_info.addFile(themehelper.actionTitlePlain(mySources),  'togglesetting', 'keepsources',    icon=ICONSAVE, themeit=THEME1)
    base_info.addFile(themehelper.actionTitlePlain(myProfiles), 'togglesetting', 'keepprofiles',    icon=ICONSAVE, themeit=THEME1)
    base_info.addFile(themehelper.actionTitlePlain(myAdvanced), 'togglesetting', 'keepadvanced',   icon=ICONSAVE, themeit=THEME1)
    base_info.addFile(themehelper.actionTitlePlain(myFavs)    , 'togglesetting', 'keepfavourites', icon=ICONSAVE, themeit=THEME1)
    base_info.addDir2(' ', 'http://', 'section', ICON_SAVE, ARTBU, '')

    base_info.addDir2('[COLOR dodgerblue]Backup Management[/COLOR]', 'http://', 'section', ICON_SAVE, ARTBU, '')
    base_info.addDir2('[COLOR red]============================================[/COLOR]', 'http://', 'section', ICON_SAVE, ARTBU, '')
    base_info.addDir2(themehelper.actionTitle(ROOTTITLE),'url','rootpatch',ICON_FIXES,FANART,'')
    base_info.addDir2(themehelper.actionTitle(BKUPLOGINTITLE),'url','backupdata',ARTBL,FANART,'')
    base_info.addDir2(themehelper.actionTitle(BKUPBUILDTITLE),'url','backup',ARTB,FANART,'')
    base_info.addDir(themehelper.actionTitle(DELBKUPTITLE),'url','deletesingle',ARTDB,FANART,'')
    base_info.addDir2(themehelper.actionTitle(DELALLBKUPTITLE),'url','deleteall',ARTDA,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
####################################################################################

###################################################################################
#Restore Menu
def Restore_Menu():
    base_info.addDir2('[COLOR dodgerblue]Restore Data[/COLOR]', 'http://', 'section', ARTRB, ARTBU, '')
    base_info.addDir2('[COLOR red]============================================[/COLOR]', 'http://', 'section', ARTRB, ARTBU, '')
    base_info.addDir(themehelper.actionTitle(RSTRBUILDTITLE),'url','restore',ARTRB,FANART,'')
    base_info.addDir(themehelper.actionTitle(RSTRLOGINTITLE),'url','restoredata',ARTRL,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
####################################################################################

###################################################################################
#Maintenance Menu
def Maintenance():
    base_info.addDir2('[COLOR dodgerblue]Maintenance Items[/COLOR]', 'http://', 'section', ARTM, ARTBU, '')
    base_info.addDir2('[COLOR red]============================================[/COLOR]', 'http://', 'section', ARTM, ARTBU, '')
    base_info.addDir2(themehelper.actionTitle(CLEARCACHETITLE),'url','clearcache',ARTCI,FANART,'')
    base_info.addDir2(themehelper.actionTitle(CLEARPKGSTITLE),'url','clearpackages',ARTP,FANART,'')
    base_info.addDir2(themehelper.actionTitle(CLEARTHUMBTITLE),'url','clearthumb',ARTTH,FANART,'')
    base_info.addDir2(themehelper.actionTitle(CLEARCRASHTITLE),'url','clearcrashlogs',ARTCCL,FANART,'')
    base_info.addDir2(' ', 'http://', 'section', ARTM, ARTBU, '')

    base_info.addDir2('[COLOR dodgerblue]Log Viewer[/COLOR]', 'http://', 'section', ARTV, ARTBU, '')
    base_info.addDir2('[COLOR red]============================================[/COLOR]', 'http://', 'section', ARTV, ARTBU, '')
    base_info.addDir2(themehelper.actionTitle(VIEWLOGTITLE),'url','viewlog',ARTV,FANART,'')
    base_info.addDir2(themehelper.actionTitle(VIEWOLDLOGTITLE),'url','viewoldlog',ARTV,FANART,'')
    base_info.addDir2(themehelper.actionTitle(VIEWWIZLOGTITLE),'url','viewwizlog',ARTV,FANART,'')
    base_info.addDir2(' ', 'http://', 'section', ARTV, ARTBU, '')

    base_info.addDir2('[COLOR dodgerblue]Additional Tools[/COLOR]', 'http://', 'section', ARTM, ARTBU, '')
    base_info.addDir2('[COLOR red]============================================[/COLOR]', 'http://', 'section', ARTM, ARTBU, '')
    base_info.addDir2(themehelper.actionTitle(FORCETITLE),'url','forceclose',ARTFC,FANART,'')
    base_info.addDir2(themehelper.actionTitle(FRESHTITLE),'url','freshstart',ARTF,FANART,'')
    base_info.addDir2(themehelper.actionTitle(RELOADTITLE),'url','reloadskin',ARTFC,FANART,'')
    base_info.addDir2(themehelper.actionTitle(UPDATETITLE),'url','forceupdate',ARTFC,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
####################################################################################

###################################################################################
# Fixes and Tweaks Menu
def Fixes_Menu():
    base_info.addDir2('[COLOR dodgerblue]Addon Fixes[/COLOR]', 'http://', 'section', ICON_FIXESMENU, ARTBU, '')
    base_info.addDir2('[COLOR red]============================================[/COLOR]', 'http://', 'section', ICON_FIXESMENU, ARTBU, '')
    base_info.addDir2(themehelper.actionTitle(SDTITLE),'url','sdfix',ICON_FIXES,FANART,'')
    base_info.addDir2(themehelper.actionTitle(YOUTUBETITLE),'url','youtubefix',ICON_FIXES,FANART,'')
    base_info.addDir2(themehelper.actionTitle(COVENANTTITLE),'url','covenantfix',ICON_FIXES,FANART,'')
    base_info.addDir2(' ', 'http://', 'section', ICON_FIXESMENU, ARTBU, '')

    base_info.addDir2('[COLOR dodgerblue]Advanced Settings Tweaks[/COLOR]', 'http://', 'section', ICON_TWEAKS, ARTBU, '')
    base_info.addDir2('[COLOR red]============================================[/COLOR]', 'http://', 'section', ICON_TWEAKS, ARTBU, '')
    base_info.addDir2(themehelper.actionTitle(CLEARADVTITLE),'url','clearadv',ICON_TWEAKS,FANART,'')
    link = base_info.OPEN_URL(ADVANCEDFILE).replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        base_info.addDir2(themehelper.actionTitle(name),url,'advsettings',iconimage,fanart,description)
    xbmc.executebuiltin('Container.SetViewMode(50)')
###################################################################################

###################################################################################
#Developer Menu
def Developer_Menu():
    base_info.addDir2(themehelper.actionTitle(CHKREPOTITLE),'url','checkrepos',ARTCR,FANART,'')
    base_info.addDir2(themehelper.actionTitle(CHKSRCTITLE), 'url','checksources',ARTCS,FANART,'')
    base_info.addDir2(themehelper.actionTitle(CONVERTTITLE),'url','convertpath',ARTCP,FANART,'')
    base_info.addDir2(themehelper.actionTitle(DEBUGTITLE),'url','debugtoggle',ARTCP,FANART,'')
    base_info.addDir2(themehelper.actionTitle(DEBUGSKIN),'url','skindebugtoggle',ARTCP,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
###################################################################################

####################################################################################
#Define Paramaters
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
        return param

params=get_params()
url         = None
name        = None
mode        = None
iconimage   = None
fanart      = None
description = None
try:     mode=urllib.unquote_plus(params["mode"])
except:  pass
try:     name=urllib.unquote_plus(params["name"])
except:  pass
try:     url=urllib.unquote_plus(params["url"])
except:  pass
try:     iconimage=urllib.unquote_plus(params["iconimage"])
except:  pass
try:     fanart=urllib.unquote_plus(params["fanart"])
except:  pass
try:     description=urllib.unquote_plus(params["description"])
except:  pass

base_info.loga('[ Version : \'%s\' ] [ Mode : \'%s\' ] [ Name : \'%s\' ] [ Url : \'%s\' ]' % (VERSION, mode if not mode == '' else None, name, url))

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if base_info.getS('auto-view')=='true':
        base_info.ebi("Container.SetViewMode(%s)" % base_info.getS(viewType) )
#######################################################################

#######################################################################
# Below we are creating the different modes
if mode==None               : Categories()
elif mode=='adult'          : Adult_Menu()
elif mode=='advsettings'    : advanced.PatchAdvanced(name,url,description)
elif mode=='krypton'        : Krypton_Menu()
elif mode=='adultwiz'       : base_info.Wizard_Adult(name,url,description)
elif mode=='kryptonwiz'     : base_info.Wizard_Krypton(name,url,description)
elif mode=='backup'         : backuprestore.Backup()
elif mode=='backupdata'     : backuprestore.Backup_Login()
elif mode=='builds'         : Builds_Menu()
elif mode=='checkrepos'     : base_info.Broken_Repos()
elif mode=='checksources'   : base_info.Broken_Sources()
elif mode=='clearadv'       : advanced.ClearAdvanced()
elif mode=='clearcache'     : base_info.Delete_Cache(url)
elif mode=='clearcrashlogs' : base_info.Delete_Crash_Logs()
elif mode=='clearpackages'  : base_info.Delete_Packages(url)
elif mode=='clearthumb'     : base_info.Clear_Thumb()
elif mode=='contact'        : contact.contact(CONT_NOT)
elif mode=='convertpath'    : backuprestore.Convert_Special(url)
elif mode=='covenantfix'    : covenant.AddonFix()
elif mode=='debugtoggle'    : xbmc.executebuiltin("ToggleDebug")
elif mode=='delete'         : backuprestore.Delete_Backup(url)
elif mode=='deleteall'      : backuprestore.Delete_All_Backups()
elif mode=='deletesingle'   : backuprestore.ListBackDel()
elif mode=='developer'      : Developer_Menu()
elif mode=='fixes'          : Fixes_Menu()
elif mode=='forceclose'     : base_info.killxbmc()
elif mode=='freshstart'     : base_info.Fresh_Start()
elif mode=='install'        : base_info.Wizard(name,url,description)
elif mode=='maint'          : Maintenance()
elif mode=='reloadskin'     : xbmc.executebuiltin('ReloadSkin()')
elif mode=='restore'        : backuprestore.Restore()
elif mode=='restoredata'    : backuprestore.Restore_Login()
elif mode=='restorezip'     : backuprestore.Read_Zip(url)
elif mode=='restorelog'     : backuprestore.Read_Login_Data_Zip(url)
elif mode=='restoremenu'    : Restore_Menu()
elif mode=='rootpatch'      : backuprestore.reset_backup_location()
elif mode=='savedata'       : Backup_Menu()
elif mode=='sdfix'          : sportsdevil.SDFix()
elif mode=='skindebugtoggle': xbmc.executebuiltin('Skin.ToggleDebug()')
elif mode=='theme'          : base_info.Wizard_Theme(name,url,description)
elif mode=='thememenu'      : Theme_Menu()
elif mode=='togglesetting'  : base_info.setS(name, 'false' if base_info.getS(name) == 'true' else 'true'); base_info.ebi('Container.Refresh')
elif mode=='forceupdate'    : wiz.forceUpdate()
elif mode=='viewlog'        : base_info.viewLogFile('kodi.log')
elif mode=='viewoldlog'     : base_info.viewLogFile('kodi.old.log')
elif mode=='viewwizlog'     : base_info.viewLogFile('wizard.log')
elif mode=='wizcreds'       : contact.credits(CREDITSFILE)
elif mode=='wizardupdate'   : base_info.wizardUpdate()
elif mode=='youtubefix'     : youtube.YoutubeFix()
#######################################################################

#######################################################################
#End of Directory
xbmcplugin.endOfDirectory(int(sys.argv[1]))
#######################################################################