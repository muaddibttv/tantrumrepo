#######################################################################
#Import Modules Section
import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os
import sys
import glob
import urllib
import urllib2
from urllib2 import urlopen
from resources.libs import extract
from resources.libs import downloader
import re
import time
import requests
import shutil
import glo_var
from resources.libs import skinSwitch
import backuprestore
from datetime import date, datetime, timedelta
#######################################################################

#######################################################################
#Global Variables
#Do Not Edit These Variables or any others in this wizard!
ADDON               = glo_var.THISADDON
ADDON_DATAPATH      = glo_var.ADDON_DATAPATH
ADDON_ID            = glo_var.ADDON_ID
ADDONDATA           = glo_var.ADDONDATA
AddonID             = glo_var.AddonID
ADDONS              = glo_var.ADDONS
ADDONTITLE          = glo_var.ADDONTITLE
BASEURL             = glo_var.BASEURL
CHECKVERSION        = xbmc.translatePath('special://home/userdata/version.txt')
COLORNAME           = glo_var.COLORNAME
cr                  = glo_var.COLOR
cr1                 = glo_var.COLOR1
cr2                 = glo_var.COLOR2
cr3                 = glo_var.COLOR3
cr4                 = glo_var.COLOR4
DATABASE            = glo_var.DATABASE
DIALOG              = glo_var.DIALOG
dialog              = glo_var.dialog
dp                  = glo_var.dp
EXCLUDES            = glo_var.EXCLUDES
FANART              = glo_var.FANART
gn                  = glo_var.GROUP_NAME
HOMEPATH            = glo_var.HOMEPATH
ICON                = glo_var.ICON
KODIV               = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
LOGPATH             = glo_var.LOGPATH
module_log_enabled  = False; http_debug_log_enabled=False; LIST="list"; THUMBNAIL="thumbnail"; MOVIES="movies"; TV_SHOWS="tvshows"; SEASONS="seasons"; EPISODES="episodes"; OTHER="other";
PACKAGESPATH        = glo_var.PACKAGESPATH
skin                = xbmc.getSkinDir()
THUMBSPATH          = glo_var.THUMBSPATH
USER_AGENT          = glo_var.USER_AGENT
USERDATAPATH        = glo_var.USERDATAPATH
VERSION             = ADDON.getAddonInfo('version')
WIZLOG              = os.path.join(ADDONDATA, 'wizard.log')
WIZARDFILE          = glo_var.WIZARDFILE
WIZVER              = glo_var.WIZVER
__settings__        = xbmcaddon.Addon(id=AddonID); __language__=__settings__.getLocalizedString               
#######################################################################
# All add commands are listed below: These are used to add directories or items to the menus.
# In between the brackets you will find the information each add command is looking for.
def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==90 : ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else: ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir2(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        if not url == None: u += "&url="+urllib.quote_plus(url)        
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==90 : ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else: ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addItem(name,url,mode,iconimage,fanart,description):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty( "Fanart_Image", fanart )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

def addFile(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
    u = sys.argv[0]
    if not mode == None: u += "?mode=%s" % urllib.quote_plus(mode)
    if not name == None: u += "&name="+urllib.quote_plus(name)
    if not url == None: u += "&url="+urllib.quote_plus(url)
    ok=True
    if themeit: display = themeit % display
    liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
    liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
    liz.setProperty( "Fanart_Image", fanart )
    if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok    
	

#######################################################################

#######################################################################
# Creating Variables
def addonId(add):
    try:    return xbmcaddon.Addon(id=add)
    except: return False

def addonInfo(add, info):
    addon = addonId(add)
    if addon: return addon.getAddonInfo(info)
    else: return False

def Broken_Sources():
    dialog = xbmcgui.Dialog()
    SOURCES_FILE =  xbmc.translatePath('special://home/userdata/sources.xml')
    if not os.path.isfile(SOURCES_FILE):
        dialog.ok(cr+ADDONTITLE+cr2,cr+'Error:'+cr2 +cr1+'It appears you do not currently have a ' +cr2 +cr+'sources.xml'+cr2+cr1+' file on your system. We are unable to perform this test.'+cr2)
        sys.exit(0)
    dp.create(cr+ADDONTITLE+cr2,cr+"Testing Internet Connection..."+cr2,'', cr1+'Please Wait...'+cr2) 
    try: OPEN_URL_NORMAL("http://www.google.com")
    except:
        dialog.ok(cr+ADDONTITLE+cr2,cr+'Error:'+cr2 +cr1+'It appears you do not currently have an active internet connection. This will cause false positives in the test. Please try again with an active internet connection.'+cr2)
        sys.exit(0)
    found = 0
    passed = 0
    dp.update(0,cr+"Checking Sources..."+cr2,'', cr1+'Please Wait...'+cr2) 
    a=open(SOURCES_FILE).read() 
    b=a.replace('\n','U').replace('\r','F')
    match=re.compile('<source>(.+?)</source>').findall(str(b))
    counter = 0
    for item in match:
        name=re.compile('<name>(.+?)</name>').findall(item)[0]
        checker=re.compile('<path pathversion="1">(.+?)</path>').findall(item)[0]
        if "http" in str(checker):
            dp.update(0,"",cr+"Checking: " + name + cr2, "")
            try:
                checkme = requests.get(checker)
            except:
                checkme = "null"
                pass
            try:
                error_out = 0
                if not "this does not matter its just a test" in ("%s" % checkme.text):
                    error_out = 0
            except:
                error_out = 1
            if error_out == 0:
                if not ".zip" in ("%s" % checkme.text):     
                    if not "repo" in ("%s" % checkme.text):                 
                        choice = xbmcgui.Dialog().yesno(cr+"Error conencting to the following: "+cr2, cr1+"Source Name: " + name + cr2, cr+"Source URL: " + checker + cr2,cr1+"Would you like to remove this source now?"+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2)
                        counter = counter + 1
                        if choice == 1:
                            found = 1
                            h=open(SOURCES_FILE).read()
                            i=h.replace('\n','U').replace('\r','F')
                            j=i.replace(str(item), '')
                            k=j.replace('U','\n').replace('F','\r')
                            l=k.replace('<source></source>','').replace('        \n','')
                            f= open(SOURCES_FILE, mode='w')
                            f.write(l)
                            f.close()
                    else:
                        passed = passed + 1
                else:
                    passed = passed + 1
            else:
                choice = xbmcgui.Dialog().yesno(cr+"Error conencting to the following: "+cr2, cr1+"Source Name: " + name + cr2, cr+"Source URL: " + checker + cr2,cr1+"Would you like to remove this source now?"+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+r2)
                counter = counter + 1
                if choice == 1:
                    found = 1
                    h=open(SOURCES_FILE).read()
                    i=h.replace('\n','U').replace('\r','F')
                    j=i.replace(str(item), '')
                    k=j.replace('U','\n').replace('F','\r')
                    l=k.replace('<source></source>','').replace('        \n','')
                    f= open(SOURCES_FILE, mode='w')
                    f.write(l)
                    f.close()
                else:
                    passed = passed + 1
            if dp.iscanceled():
                dialog = xbmcgui.Dialog()
                dialog.ok(cr+ADDONTITLE+cr2, cr+'The source check was cancelled'+cr2)
                dp.close()
                sys.exit()
            dp.update(0,"","",cr4+"Alive: " + str(passed) + cr2+ cr3+"        Dead: " + str(counter) + cr2)
    dialog.ok(cr+ADDONTITLE+cr2,cr1+'We have checked your sources and found:'+cr2, cr+'WORKING SOURCES: '+cr2+cr4 + str(passed) + cr2,cr1+'DEAD SOURCES: '+cr2+cr3 + str(counter) + cr2)

def Broken_Repos():
    dialog = xbmcgui.Dialog()
    dp.create(cr+ADDONTITLE+cr2,cr+"Testing Internet Connection..."+cr2,'', cr1+'Please Wait...'+cr2) 
    try:
        OPEN_URL_NORMAL("http://www.google.com")
    except:
        dialog.ok(cr+ADDONTITLE+cr2,cr+'Error:'+cr2+cr1+' It appears you do not currently have an active internet connection. This will cause false positives in the test. Please try again with an active internet connection.'+cr2)
        sys.exit(0)
    passed = 0
    failed = 0
    HOMEPATH =  xbmc.translatePath('special://home/addons/')
    dp.update(0,cr1+"We are currently checking:"+cr2,'',cr+"Alive:"+cr2+cr4+ "0"+cr2+cr1+ "       Dead:"+cr2+cr3+" 0"+cr2)
    url = HOMEPATH
    for root, dirs, files in os.walk(url):
        for file in files:
            if file == "addon.xml":
                a=open((os.path.join(root, file))).read()   
                if "info compressed=" in str(a):
                    match = re.compile('<info compressed="false">(.+?)</info>').findall(a)
                    for checker in match:
                        dp.update(0,"",cr + checker + cr2, "")
                        try:
                            Common.OPEN_URL_NORMAL(checker)
                            passed = passed + 1
                        except:
                            try:
                                checkme = requests.get(checker)
                            except:
                                pass
                            try:
                                error_out = 0
                                if not "this does not matter its just a test" in ("%s" % checkme.text):
                                    error_out = 0
                            except:
                                error_out = 1
                            if error_out == 0:
                                if not "addon id=" in ("%s" % checkme.text):    
                                    failed = failed + 1
                                    match = re.compile('<addon id="(.+?)".+?ame="(.+?)" version').findall(a)
                                    for repo_id,repo_name in match:
                                        dialog = xbmcgui.Dialog()
                                        default_path = xbmc.translatePath("special://home/addons/")
                                        file_path = xbmc.translatePath(file)
                                        full_path = default_path + repo_id
                                        choice = xbmcgui.Dialog().yesno(cr+ADDONTITLE+cr2,cr+"The "+cr2+cr1 + repo_name + cr2+cr1+" appears to be broken. We attempted to connect to the repo but it was unsuccessful."+cr2,cr+'To remove this repository please click YES'+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2)
                                        if choice == 1:
                                            try:
                                                shutil.rmtree(full_path)
                                            except:
                                                dialog.ok(cr+ADDONTITLE+cr2,cr+"Sorry we were unable to remove " + repo_name + cr2)
                                else:
                                    passed = passed + 1
                            else:
                                failed = failed + 1
                                match = re.compile('<addon id="(.+?)".+?ame="(.+?)" version').findall(a)
                                for repo_id,repo_name in match:
                                    dialog = xbmcgui.Dialog()
                                    default_path = xbmc.translatePath("special://home/addons/")
                                    file_path = xbmc.translatePath(file)
                                    full_path = default_path + repo_id
                                    choice = xbmcgui.Dialog().yesno(cr+ADDONTITLE+cr2,cr+"The "+cr2+ cr1 + repo_name + cr2 + cr +" appears to be broken. We attempted to connect to the repo but it was unsuccessful."+cr2,cr+'To remove this repository please click YES'+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2)
                                    if choice == 1:
                                        try:
                                            shutil.rmtree(full_path)
                                        except:
                                            dialog.ok(cr+ADDONTITLE+cr2,cr+"Sorry we were unable to remove " + repo_name + cr2)
                        if dp.iscanceled():
                            dialog = xbmcgui.Dialog()
                            dialog.ok(cr+ADDONTITLE+cr2, cr1+'The repository check was cancelled'+cr2)
                            dp.close()
                            sys.exit()
                        dp.update(0,"","",cr+"Alive: "+cr2+cr4 + str(passed) + cr2+cr1+ "       Dead: "+cr2+cr3 + str(failed) + cr2)
    dialog.ok(cr+ADDONTITLE+cr2,cr1+'We have checked your repositories and found:'+cr2, cr+'Working Repositories: '+cr2+cr4 + str(passed) + cr2,cr1+'Dead Repositories: '+cr2+cr3 + str(failed) + cr2)

def checkBuild(name, ret):
    if not workingURL(WIZARDFILE) == True: return False
    link = OPEN_URL(WIZARDFILE).replace('\n','').replace('\r','').replace('\t','').replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"')
    match = re.compile('name="%s".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"' % name).findall(link)
    if len(match) > 0:
        for version, url, gui, kodi, theme, icon, fanart, description in match:
            if ret   == 'version':       return version
            elif ret == 'url':           return url
            elif ret == 'gui':           return gui
            elif ret == 'kodi':          return kodi
            elif ret == 'theme':         return theme
            elif ret == 'icon':          return icon
            elif ret == 'fanart':        return fanart
            elif ret == 'description':   return description
            elif ret == 'all':           return '%s|||%s|||%s|||%s|||%s|||%s|||%s|||%s|||%s' % (name, version, url, gui, kodi, theme, icon, fanart, description)
    else: return False

def checkVersion(ret):
    if not os.path.exists(CHECKVERSION):
        file = open(CHECKVERSION,'w') 
        file.write("<version>0</version>")
        file.close()
    checkurl = (glo_var.VERSION)
    vers = open(CHECKVERSION, "r")
    regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
    for line in vers:
        currversion = regex.findall(line)
        for build,vernumber in currversion:
            if vernumber > 0:
                if ret   == 'version': return vernumber
                elif ret == 'build':   return build
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
                            if ret   == 'newversion': return newversion
                                   
def checkTheme(name, theme, ret):
    themeurl = checkBuild(name, 'theme')
    if not workingURL(themeurl) == True: return False
    link = OPEN_URL(themeurl).replace('\n','').replace('\r','').replace('\t','')
    match = re.compile('name="%s".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"' % theme).findall(link)
    if len(match) > 0:
        for url, icon, fanart, description in match:
            if ret   == 'url':           return url
            elif ret == 'icon':          return icon
            elif ret == 'fanart':        return fanart
            elif ret == 'description':   return description
            elif ret == 'all':           return '%s|||%s|||%s|||%s|||%s|||%s' % (name, theme, url, icon, fanart, description)
    else: return False

def checkWizard(ret):
    if not workingURL(WIZVER) == True: return False
    link = OPEN_URL(WIZVER).replace('\n','').replace('\r','').replace('\t','')
    match = re.compile('id="%s".+?ersion="(.+?)".+?ip="(.+?)"' % ADDON_ID).findall(link)
    if len(match) > 0:
        for version, zip in match:
            if ret   == 'version':       return version
            elif ret == 'zip':           return zip
            elif ret == 'all':           return '%s|||%s|||%s' % (ADDON_ID, version, zip)
    else: return False

def Clear_Thumb():
    DIALOG = xbmcgui.Dialog()
    latest = latestDB('Textures')
    if DIALOG.yesno(cr+ADDONTITLE+cr2, cr1+"Would you like to delete the %s and Thumbnails folder?" % latest+cr2, cr1+"They will repopulate on startup"+cr2, nolabel=cr1+'No, Cancel'+cr2,yeslabel=cr+'Yes, Remove'+cr2):
        try: removeFile(os.join(DATABASE, latest))
        except: log(cr1+'Failed to delete, Purging DB.'+cr2); purgeDb(latest)
        removeFolder(THUMBSPATH)
        killxbmc()
    else: log(cr1+'Clear Thumbnails Cancelled'+cr2)

def currSkin():
    return xbmc.getSkinDir()

def defaultSkin():
    log("[Default Skin Check]")
    tempgui = os.path.join(USERDATAPATH, 'guitemp.xml')
    gui = tempgui if os.path.exists(tempgui) else GUISETTINGS
    if not os.path.exists(gui): return False
    log("Reading gui file: %s" % gui)
    guif = open(gui, 'r+')
    msg = guif.read().replace('\n','').replace('\r','').replace('\t','').replace('    ',''); guif.close()
    log("Opening gui settings")
    match = re.compile('<lookandfeel>.+?<ski.+?>(.+?)</skin>.+?</lookandfeel>').findall(msg)
    log("Matches: %s" % str(match))
    if len(match) > 0:
        skinid = match[0]
        addonxml = os.path.join(ADDONS, match[0], 'addon.xml')
        if os.path.exists(addonxml):
            addf = open(addonxml, 'r+')
            msg2 = addf.read().replace('\n','').replace('\r','').replace('\t',''); addf.close()
            match2 = re.compile('<addon.+?ame="(.+?)".+?>').findall(msg2)
            if len(match2) > 0: skinname = match2[0]
            else: skinname = 'no match'
        else: skinname = 'no file'
        log("[Default Skin Check] Skin name: %s" % skinname)
        log("[Default Skin Check] Skin id: %s" % skinid)
        setS('defaultskin', skinid)
        setS('defaultskinname', skinname)
        setS('defaultskinignore', 'false')
    if os.path.exists(tempgui):
        log("Deleting Temp Gui File.")
        os.remove(tempgui)
    log("[Default Skin Check] End")

def Delete_Cache(url):
    print '############################################################       DELETING STANDARD CACHE             ###############################################################'
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                DIALOG = xbmcgui.Dialog()
                if DIALOG.yesno(cr+gn+cr2+cr1+" Wizard"+cr2, cr3+ str(file_count)+cr2 + cr1+" Cache files found", "Do you want to delete them?"+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2):
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                DIALOG = xbmcgui.Dialog()
                if DIALOG.yesno(cr+gn+cr2+cr1+" Wizard"+cr2, cr3+ str(file_count)+cr2 + cr1+" Cache files found in 'Other'", "Do you want to delete them?"+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                DIALOG = xbmcgui.Dialog()
                if DIALOG.yesno(cr+gn+cr2+cr1+" Wizard"+cr2, cr3+ str(file_count)+cr2 + cr1+" Cache files found in 'LocalAndRental'", "Do you want to delete them?"+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
            else:
                pass
    wtf_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
    if os.path.exists(wtf_cache_path)==True:    
        for root, dirs, files in os.walk(wtf_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                DIALOG = xbmcgui.Dialog()
                if DIALOG.yesno(cr+gn+cr2+cr1+" Wizard"+cr2, cr3+str(file_count)+cr2 + cr1+" Cache files found", "Do you want to delete them?"+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))    
            else:
                pass
    channel4_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.4od/cache'), '')
    if os.path.exists(channel4_cache_path)==True:    
        for root, dirs, files in os.walk(channel4_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                DIALOG = xbmcgui.Dialog()
                if DIALOG.yesno(cr+gn+cr2+cr1+" Wizard"+cr2, cr3+str(file_count)+cr2 + cr1+" Cache files found", "Do you want to delete them?"+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))    
            else:
                pass
    iplayer_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
    if os.path.exists(iplayer_cache_path)==True:    
        for root, dirs, files in os.walk(iplayer_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                DIALOG = xbmcgui.Dialog()
                if DIALOG.yesno(cr+gn+cr2+cr1+" Wizard"+cr2, cr3+str(file_count)+cr2 + cr1+" Cache files found", "Do you want to delete them?"+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))   
            else:
                pass
    downloader_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
    if os.path.exists(downloader_cache_path)==True:    
        for root, dirs, files in os.walk(downloader_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                DIALOG = xbmcgui.Dialog()
                if DIALOG.yesno(cr+gn+cr2+cr1+" Wizard"+cr2, cr3+str(file_count)+cr2 + cr1+" Cache files found", "Do you want to delete them?"+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
            else:
                pass
    itv_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
    if os.path.exists(itv_cache_path)==True:    
        for root, dirs, files in os.walk(itv_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                DIALOG = xbmcgui.Dialog()
                if DIALOG.yesno(cr+gn+cr2+cr1+" Wizard"+cr2, cr3+str(file_count)+cr2 + cr1+"Cache files found", "Do you want to delete them?"+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))    
            else:
                pass
    temp_cache_path = os.path.join(xbmc.translatePath('special://home/temp'), '')
    if os.path.exists(temp_cache_path)==True:    
        for root, dirs, files in os.walk(temp_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                DIALOG = xbmcgui.Dialog()
                if DIALOG.yesno(cr+gn+cr2+cr1+" Wizard"+cr2, cr3+str(file_count)+cr2 + cr1+" Cache files found", "Do you want to delete them?"+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))                      
            else:
                pass
    DIALOG = xbmcgui.Dialog()
    DIALOG.ok(cr+gn+cr2+cr1+" Wizard"+cr2, "Complete")  

def Delete_Crash_Logs(over=None):
    crashfiles = []
    tracefiles = []
    for file in glob.glob(os.path.join(LOGPATH, '*crashlog*.*')):
        crashfiles.append(file)
    for file in glob.glob(os.path.join(LOGPATH, '*stacktrace*.*')):
        tracefiles.append(file)
    totalfiles = len(crashfiles) + len(tracefiles)
    if totalfiles > 0:
        if over:
            yes=1
        else:
            yes=DIALOG.yesno(ADDONTITLE, 'Would you like to delete the Crash logs?', '%s Files Found' % (totalfiles), nolabel="No, Cancel", yeslabel="Yes, Remove")
        if yes:
            if len(crashfiles) > 0:
                for f in crashfiles:
                    os.remove(f)
            if len(tracefiles) > 0:
                for f in tracefiles:
                    os.remove(f)
            LogNotify(ADDONTITLE, '[COLOR white]Clear Crash Logs[/COLOR] [COLOR red]%s Crash Logs Removed[/COLOR]' % (totalfiles))
        else:
            LogNotify(ADDONTITLE, '[COLOR white]Clear Crash Logs[/COLOR] [COLOR red]Clear Crash Logs Cancelled[/COLOR]')
    else:
        LogNotify(ADDONTITLE, '[COLOR white]Clear Crash Logs[/COLOR] [COLOR red]No Crash Logs Found[/COLOR]')

def Delete_Packages(url):
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    try:    
        for root, dirs, files in os.walk(packages_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                DIALOG = xbmcgui.Dialog()
                if DIALOG.yesno(cr1+"Delete Package Cache Files"+cr2, cr3+str(file_count)+cr2 + cr1+" files found", "Do you want to delete them?"+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2):                      
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                    DIALOG = xbmcgui.Dialog()
                    DIALOG.ok(cr+gn+cr2+cr1+" Wizard"+cr2, "Complete")  
    except: 
        DIALOG = xbmcgui.Dialog()
        DIALOG.ok(cr+gn+cr2+cr1+" Wizard"+cr2, cr1+"Sorry we were not able to remove Package Files")

def ebi(proc):
    xbmc.executebuiltin(proc)

def getS(name):
    try: return ADDON.getSetting(name)
    except: return False

KEEPFAVS         = getS('keepfavourites')
KEEPSOURCES      = getS('keepsources')
KEEPPROFILES     = getS('keepprofiles')
KEEPADVANCED     = getS('keepadvanced')
KEEPVERSION      = getS('keepversion')
LOGFILES         = ['log', 'xbmc.old.log', 'kodi.log', 'kodi.old.log', 'spmc.log', 'spmc.old.log', 'tvmc.log', 'tvmc.old.log']

def percentage(part, whole):
    return 100 * float(part)/float(whole)

def Fresh_Start(install=None):
    SAVE = xbmcgui.Dialog().yesno(cr+gn+' Wizard'+cr2,cr1+'Would you like to save your login data before running Fresh Start?'+cr2,'','',yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2)
    if SAVE == 1:
         BACKUP = backuprestore.Backup_Login()    
    if install == 'restore': yes_pressed=DIALOG.yesno(ADDONTITLE, cr1+"Do you wish to restore your"+cr2, cr1+"Kodi configuration to default settings"+cr2, cr1+"Before installing the local backup?"+cr2, nolabel=cr1+'No'+cr2, yeslabel=cr+'Yes'+cr2)
    elif install: yes_pressed=DIALOG.yesno(ADDONTITLE, cr1+"Do you wish to restore your"+cr2, cr1+"Kodi configuration to default settings"+cr2, cr1+"Before installing?"+cr2,(install), nolabel=cr1+'No'+cr2, yeslabel=cr+'Yes'+cr2)
    else: yes_pressed=DIALOG.yesno(ADDONTITLE, cr1+"Do you wish to restore your"+cr2, cr1+"Kodi configuration to default settings?"+cr2, nolabel=cr1+'No'+cr2, yeslabel=cr+'Yes'+cr2)
    if yes_pressed:
        if not currSkin() in ['skin.confluence', 'skin.estuary']:
            skin = 'skin.confluence' if KODIV < 17 else 'skin.estuary'
            yes=DIALOG.yesno(ADDONTITLE, cr1+"The skin needs to be set back to %s" % (skin[5:]+cr2), cr1+"Before doing a fresh install to clear all Texture files,"+cr2, cr1+"Would you like us to do that for you?"+cr2, yeslabel=cr+"Switch Skins"+cr2, nolabel=cr1+"I'll Do It"+cr2);
            if yes:
                skinSwitch.swapSkins(skin)
                x = 0
                xbmc.sleep(1000)
                while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 150:
                    x += 1
                    xbmc.sleep(200)
                if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
                    ebi('SendClick(11)')
                else: LogNotify(ADDONTITLE,'Fresh Install: Skin Swap Timed Out!'); return False
                xbmc.sleep(1000)
            else: LogNotify(ADDONTITLE,'Fresh Install: Cancelled!'); return False
        if not currSkin() in ['skin.confluence', 'skin.estuary']:
            LogNotify(ADDONTITLE,'Fresh Install: Skin Swap Failed!')
            return
        dp.create(ADDONTITLE,"Disabling All Problematic Addons:",'', '')
        xbmcPath=os.path.abspath(HOMEPATH)
        dp.update(0,"Clearing all files and folders:",'', '')
        total_files = sum([len(files) for r, d, files in os.walk(xbmcPath)]); del_file = 0;
        for root, dirs, files in os.walk(xbmcPath,topdown=True):
            EXCLUDES.append('My_Builds')
            dirs[:] = [d for d in dirs if d not in EXCLUDES]
            for name in files:
                del_file += 1
                fold = root.split('\\')
                x = len(fold)-1
                print os.path.join(root,name)
                if name == 'sources.xml' and fold[-1] == 'userdata' and KEEPSOURCES == 'true': loga("Keep Sources: %s" % os.path.join(root, name))
                elif name == 'favourites.xml' and fold[-1] == 'userdata' and KEEPFAVS == 'true': loga("Keep Favourites: %s" % os.path.join(root, name))
                elif name == 'version.txt' and fold[-1] == 'userdata' and KEEPFAVS == 'true': loga("Keep Version Text: %s" % os.path.join(root, name))                
                elif name == 'profiles.xml' and fold[-1] == 'userdata' and KEEPPROFILES == 'true': loga("Keep Profiles: %s" % os.path.join(root, name))
                elif name == 'advancedsettings.xml' and fold[-1] == 'userdata' and KEEPADVANCED == 'true':  loga("Keep Advanced Settings: %s" % os.path.join(root, name))
                elif name in LOGFILES: loga("Keep Log File: %s" % name)
                elif name.endswith('.db'):
                    try:
                        if name.endswith('.db') and name.startswith('Addon') and KODIV >= 17: loga("Ignoring %s on v%s" % (name, KODIV))
                        else: os.remove(os.path.join(root,name))
                    except Exception, e: 
                        loga('Failed to delete, Purging DB')
                        loga("-> %s / %s" % (Exception, str(e)))
                        purgeDb(os.path.join(root,name))
                else:
                    dp.update(int(percentage(del_file, total_files)), '', 'File: %s' % (name), '')
                    try: os.remove(os.path.join(root,name))
                    except Exception, e: 
                        loga("Error removing %s" % os.path.join(root, name))
                        loga("-> %s / %s" % (Exception, str(e)))
            if dp.iscanceled(): 
                dp.close()
                LogNotify(ADDONTITLE, "Fresh Start Cancelled")
                return False
        for root, dirs, files in os.walk(xbmcPath,topdown=True):
            dirs[:] = [d for d in dirs if d not in EXCLUDES]
            for name in dirs:
                dp.update(100, '', 'Cleaning Up Empty Folder: %s' % (name), '')
                if name not in ["Database","userdata","temp","addons","addon_data"]:
                    shutil.rmtree(os.path.join(root,name),ignore_errors=True, onerror=None)
            if dp.iscanceled(): 
                dp.close()
                LogNotify(ADDONTITLE, "Fresh Start Cancelled")
                return False
        dp.close()
        if install == 'restore': 
            DIALOG.ok(ADDONTITLE, "Your current setup for kodi has been cleared!", "Now we will install the local backup")
        elif install: 
            DIALOG.ok(ADDONTITLE, "Your current setup for kodi has been cleared!", "Now we will install: %s v%s" % (install, checkBuild(install,'version')))
            buildWizard(install, 'normal')
        else:
            killxbmc()
    else: 
        if not install == 'restore': LogNotify(ADDONTITLE,'Fresh Install: Cancelled!'); ebi('Container.Refresh')

def get_params():
    url=None
    name=None
    buildname=None
    updated=None
    author=None
    version=None
    mode=None
    iconimage=None
    description=None
    video=None
    link=None
    skins=None
    videoaddons=None
    audioaddons=None
    programaddons=None
    audioaddons=None
    sources=None
    local=None
    try:     url=urllib.unquote_plus(params["url"])
    except:  pass
    try:     guisettingslink=urllib.unquote_plus(params["guisettingslink"])
    except:  pass
    try:     name=urllib.unquote_plus(params["name"])
    except:  pass
    try:     iconimage=urllib.unquote_plus(params["iconimage"])
    except:  pass
    try:     fanart=urllib.unquote_plus(params["fanart"])
    except:  pass
    try:     mode=str(params["mode"])
    except:  pass
    try:     link=urllib.unquote_plus(params["link"])
    except:  pass
    try:     skins=urllib.unquote_plus(params["skins"])
    except:  pass
    try:     videoaddons=urllib.unquote_plus(params["videoaddons"])
    except:  pass
    try:     audioaddons=urllib.unquote_plus(params["audioaddons"])
    except:  pass
    try:     programaddons=urllib.unquote_plus(params["programaddons"])
    except:  pass
    try:     pictureaddons=urllib.unquote_plus(params["pictureaddons"])
    except:  pass
    try:     local=urllib.unquote_plus(params["local"])
    except:  pass
    try:     sources=urllib.unquote_plus(params["sources"])
    except:  pass
    try:     adult=urllib.unquote_plus(params["adult"])
    except:  pass
    try:     buildname=urllib.unquote_plus(params["buildname"])
    except:  pass
    try:     updated=urllib.unquote_plus(params["updated"])
    except:  pass
    try:     version=urllib.unquote_plus(params["version"])
    except:  pass
    try:     author=urllib.unquote_plus(params["author"])
    except:  pass
    try:     description=urllib.unquote_plus(params["description"])
    except:  pass
    try:     video=urllib.unquote_plus(params["video"])
    except:  pass        
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

def get_setting(name): _log("get_setting name='"+name+"'"); dev=__settings__.getSetting(name); _log("get_setting ->'"+str(dev)+"'"); return dev

def killxbmc():
	choice = DIALOG.yesno('Force Close Kodi', 'You are about to close Kodi', 'Would you like to continue?', nolabel='No, Cancel',yeslabel='Yes, Close')
	if choice == 0: return
	elif choice == 1: pass
	myplatform = platform()
	log("Platform: " + str(myplatform))
	os._exit(1)
	log("Force close failed!  Trying alternate methods.")
	if myplatform == 'osx': # OSX
		log("############ try osx force close #################")
		try: os.system('killall -9 XBMC')
		except: pass
		try: os.system('killall -9 Kodi')
		except: pass
		DIALOG.ok("[COLOR=red][B]WARNING !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
	elif myplatform == 'linux': #Linux
		log("############ try linux force close #################")
		try: os.system('killall XBMC')
		except: pass
		try: os.system('killall Kodi')
		except: pass
		try: os.system('killall -9 xbmc.bin')
		except: pass
		try: os.system('killall -9 kodi.bin')
		except: pass
		DIALOG.ok("[COLOR=red][B]WARNING !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
	elif myplatform == 'android': # Android 
		log("############ try android force close #################")
		try: os.system('adb shell am force-stop org.xbmc.kodi')
		except: pass
		try: os.system('adb shell am force-stop org.kodi')
		except: pass
		try: os.system('adb shell am force-stop org.xbmc.xbmc')
		except: pass
		try: os.system('adb shell am force-stop org.xbmc')
		except: pass		
		try: os.system('adb shell kill org.xbmc.kodi')
		except: pass
		try: os.system('adb shell kill org.kodi')
		except: pass
		try: os.system('adb shell kill org.xbmc.xbmc')
		except: pass
		try: os.system('adb shell kill org.xbmc')
		except: pass
		try: os.system('Process.killProcess(android.os.Process.org.xbmc,kodi());')
		except: pass
		try: os.system('Process.killProcess(android.os.Process.org.kodi());')
		except: pass
		try: os.system('Process.killProcess(android.os.Process.org.xbmc.xbmc());')
		except: pass
		try: os.system('Process.killProcess(android.os.Process.org.xbmc());')
		except: pass
		DIALOG.ok(ADDONTITLE, "Press the HOME button on your remote and [COLOR=red][B]FORCE STOP[/COLOR][/B] KODI via the Manage Installed Applications menu in settings on your Amazon home page then re-launch KODI")
	elif myplatform == 'windows': # Windows
		log("############ try windows force close #################")
		try:
			os.system('@ECHO off')
			os.system('tskill XBMC.exe')
		except: pass
		try:
			os.system('@ECHO off')
			os.system('tskill Kodi.exe')
		except: pass
		try:
			os.system('@ECHO off')
			os.system('TASKKILL /im Kodi.exe /f')
		except: pass
		try:
			os.system('@ECHO off')
			os.system('TASKKILL /im XBMC.exe /f')
		except: pass
		DIALOG.ok("[COLOR=red][B]WARNING !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
	else: #ATV
		log("############ try atv force close #################")
		try: os.system('killall AppleTV')
		except: pass
		log("############ try raspbmc force close #################") #OSMC / Raspbmc
		try: os.system('sudo initctl stop kodi')
		except: pass
		try: os.system('sudo initctl stop xbmc')
		except: pass
		DIALOG.ok("[COLOR=red][B]WARNING !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","iOS detected. Press and hold both the Sleep/Wake and Home button for at least 10 seconds, until you see the Apple logo.")

def latestDB(DB):
    if DB in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
        match = glob.glob(os.path.join(DATABASE,'%s*.db' % DB))
        comp = '%s(.+?).db' % DB[1:]
        highest = 0
        for file in match :
            try: check = int(re.compile(comp).findall(file)[0])
            except: check = 0
            if highest < check :
                highest = check
        return '%s%s.db' % (DB, highest)
    else: return False

def _log(message):
    if module_log_enabled: xbmc.log(message)

def log(log):
    xbmc.log("[%s]: %s" % (cr+ADDONTITLE+cr2, log))
    if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)

def loga(msg, level=xbmc.LOGDEBUG):
    if getS('addon_debug') == 'true' and level == xbmc.LOGDEBUG:
        level = xbmc.LOGNOTICE
    try:
        if isinstance(msg, unicode):
            msg = '%s' % (msg.encode('utf-8'))
        xbmc.log('%s: %s' % (ADDONTITLE, msg), level)
    except Exception as e:
        try: xbmc.log('Logging Failure: %s' % (e), level)
        except: pass
    if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
    if not os.path.exists(WIZLOG): f = open(WIZLOG, 'w'); f.close()
    with open(WIZLOG, 'a') as f:
        line = "[%s %s] %s" % (datetime.now().date(), str(datetime.now().time())[:8], msg)
        f.write(line.rstrip('\r\n')+'\n')    

def LogNotify(title,message,times=2000,icon=ICON):
    xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % (title , message , times, icon))

def lookandFeelData(do='save'):
    scan = ['lookandfeel.enablerssfeeds', 'lookandfeel.font', 'lookandfeel.rssedit', 'lookandfeel.skincolors', 'lookandfeel.skintheme', 'lookandfeel.skinzoom', 'lookandfeel.soundskin', 'lookandfeel.startupwindow', 'lookandfeel.stereostrength']
    if do == 'save':
        for item in scan:
            query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"%s"}, "id":1}' % (item)
            response = xbmc.executeJSONRPC(query)
            if not 'error' in response:
                match = re.compile('{"value":(.+?)}').findall(str(response))
                setS(item.replace('lookandfeel', 'default'), match[0])
                log("%s saved to %s" % (item, match[0]))
    else:
        for item in scan:
            value = getS(item.replace('lookandfeel', 'default'))
            query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"%s","value":%s}, "id":1}' % (item, value)
            response = xbmc.executeJSONRPC(query)
            log("%s restored to %s" % (item, value))

def message(text1,text2="",text3=""):
    _log("message text1='"+text1+"', text2='"+text2+"', text3='"+text3+"'")
    if text3=="": xbmcgui.Dialog().ok(text1,text2)
    elif text2=="": xbmcgui.Dialog().ok("",text1)
    else: xbmcgui.Dialog().ok(text1,text2,text3)

def open_settings_dialog(): _log("open_settings_dialog"); __settings__.openSettings() 

def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link 

def OPEN_URL_NORMAL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'python-requests/2.9.1')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link  

def purgeDb(name):
    log('Purging DB %s.' % name)
    if os.path.exists(name):
        try:
            textdb = database.connect(name)
            textexe = textdb.cursor()
        except Exception, e:
            log(str(e))
            return False
    else: log('%s not found.' % name); return False
    textexe.execute("""SELECT name FROM sqlite_master WHERE type = 'table';""")
    for table in textexe.fetchall():
        if table[0] == 'version': 
            log('Data from table `%s` skipped.' % table[0])
        else:
            try:
                textexe.execute("""DELETE FROM %s""" % table[0])
                textdb.commit()
                log('Data from table `%s` cleared.' % table[0])
            except e: log(str(e))
    log('%s DB Purging Complete.' % name)
    show = name.replace('\\', '/').split('/')
    LogNotify("Purge Database", "%s Complete" % show[len(show)-1])  

def REMOVE_EMPTY_FOLDERS():
    print"########### Start Removing Empty Folders #########"
    empty_count = 0
    used_count = 0
    try:
        for curdir, subdirs, files in os.walk(HOMEPATH):
            if len(subdirs) == 0 and len(files) == 0:
                empty_count += 1
                os.rmdir(curdir)
                print "successfully removed: "+curdir
            elif len(subdirs) > 0 and len(files) > 0:
                used_count += 1
    except: pass

def removeFile(path):
    log(cr1+"Deleting File: %s"+cr2 % path)
    try:    os.remove(path)
    except: return False

def removeFolder(path):
    log("Deleting Folder: %s" % path)
    try: shutil.rmtree(path,ignore_errors=True, onerror=None)
    except: return False

def setS(name, value):
    try: ADDON.setSetting(name, value)
    except: return False

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )

def TextBoxes(heading,announce):
    class TextBox():
        WINDOW=10147
        CONTROL_LABEL=1
        CONTROL_TEXTBOX=5
        def __init__(self,*args,**kwargs):
            xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, ))
            self.win=xbmcgui.Window(self.WINDOW)
            xbmc.sleep(500)
            self.setControls()
        def setControls(self):
            self.win.getControl(self.CONTROL_LABEL).setLabel(heading)
            try: f=open(announce); text=f.read()
            except: text=announce
            self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
            return
    TextBox()
    while xbmc.getCondVisibility('Window.IsVisible(10147)'):
        time.sleep(.5)

def TextBoxesPlain(announce):
    class TextBox():
        WINDOW=10147
        CONTROL_LABEL=1
        CONTROL_TEXTBOX=5
        def __init__(self,*args,**kwargs):
            xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, ))
            self.win=xbmcgui.Window(self.WINDOW)
            xbmc.sleep(500)
            self.setControls()
        def setControls(self):
            self.win.getControl(self.CONTROL_LABEL).setLabel(cr+gn+' Wizard'+cr2)
            try: f=open(announce); text=f.read()
            except: text=announce
            self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
            return
    TextBox()
    while xbmc.getCondVisibility('Window.IsVisible(10147)'):
        time.sleep(.5)

def log_check(logname):
    ret = False
    if logname == 'kodi.log':
        if os.path.exists(os.path.join(LOGPATH,'xbmc.log')):
            ret = os.path.join(LOGPATH,'xbmc.log')
        elif os.path.exists(os.path.join(LOGPATH,'kodi.log')):
            ret = os.path.join(LOGPATH,'kodi.log')
        elif os.path.exists(os.path.join(LOGPATH,'spmc.log')):
            ret = os.path.join(LOGPATH,'spmc.log')
        elif os.path.exists(os.path.join(LOGPATH,'tvmc.log')):
            ret = os.path.join(LOGPATH,'tvmc.log')
    elif logname == 'kodi.old.log':
        if os.path.exists(os.path.join(LOGPATH,'xbmc.old.log')):
            ret = os.path.join(LOGPATH,'xbmc.log')
        elif os.path.exists(os.path.join(LOGPATH,'kodi.old.log')):
            ret = os.path.join(LOGPATH,'kodi.log')
        elif os.path.exists(os.path.join(LOGPATH,'spmc.old.log')):
            ret = os.path.join(LOGPATH,'spmc.log')
        elif os.path.exists(os.path.join(LOGPATH,'tvmc.old.log')):
            ret = os.path.join(LOGPATH,'tvmc.log')
    else:
        if os.path.exists(WIZLOG):
            ret = WIZLOG   
    return ret  

def viewLogFile(logname):
    log     = log_check(logname)
    if os.path.exists(log) or not log == False:
        f = open(log,mode='r'); msg = f.read(); f.close()
        TextBoxes("%s - %s" % (cr+ADDONTITLE+cr2, logname), msg)
    else: 
        LogNotify('View Log', 'No Log File Found!')

def ForeceUpdate():
    xbmc.executebuiltin("ActivateWindow(busydialog)")
    xbmc.executebuiltin("UpdateAddonRepos")
    xbmc.executebuiltin("UpdateLocalAddons")
    xbmc.executebuiltin("Dialog.Close(busydialog)")

def Wizard(name,url,description):
    if workingURL(url) == False: return False
    name = re.sub('\[.*?]','',name)
    fresh = xbmcgui.Dialog().yesno(cr+gn+" Wizard"+cr2, cr+'                    Would you like to run a Fresh Start?'+cr2, cr1+'                     Before installing the latest Build?'+cr2, '', yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2)
    if fresh:
        BACKUP = Fresh_Start()
    else:
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        dp = xbmcgui.DialogProgress()
        dp.create(cr+gn+" Wizard"+cr2,"[COLOR snow][B]The Chosen Build is Whizzing down your Wires[/B][/COLOR] ",'', '[COLOR snow][B]Put the kettle on[/B][/COLOR]')
        lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "[COLOR snow][B]Extracting[/B][/COLOR]"+cr+gn+cr2+"[COLOR snow][B]Build now, Please Wait[/B][/COLOR]")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    DIALOG = xbmcgui.Dialog()
    DIALOG.ok("[COLOR dodgerblue][B]DOWNLOAD COMPLETE![/B][/COLOR]", '[COLOR snow][B]To ensure all changes are saved you must now close Kodi[/B][/COLOR]', ' ')
    killxbmc()

def Wizard_Adult(name,url,description):
    if workingURL(url) == False: return False
    name = re.sub('\[.*?]','',name)
    fresh = xbmcgui.Dialog().yesno(cr+gn+" Wizard"+cr2, cr+'                    Would you like to run a Fresh Start?'+cr2, cr1+'                     Before installing the latest Build?'+cr2, '', yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2)
    if fresh:
        BACKUP = Fresh_Start()
    else:    
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        dp = xbmcgui.DialogProgress()
        dp.create(cr+gn+" ADULT BUILD WIZARD"+cr2,cr1+"The Adult Build is Cumming "+cr2,'', cr1+'Grab some lube and tissues'+cr2)
        lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", cr1+"Extracting"+cr2+ cr+gn+ cr2+ cr3+" ADULT"+cr2+ cr+"Build"+cr2+ cr1+ "now, Please Wait"+cr2)
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    DIALOG = xbmcgui.Dialog()
    DIALOG.ok(cr+"DOWNLOAD COMPLETE!"+cr2, cr1+'To ensure all changes are saved you must now close Kodi'+cr2, ' ')
    killxbmc()

def Wizard_Krypton(name,url,description):
    if workingURL(url) == False: return False
    name = re.sub('\[.*?]','',name)
    fresh = xbmcgui.Dialog().yesno(cr+gn+" Wizard"+cr2, cr+'                    Would you like to run a Fresh Start?'+cr2, cr1+'Before installing the latest Krypton Build?'+cr2, '', yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2)
    if fresh:
        BACKUP = Fresh_Start()
    else:    
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        dp = xbmcgui.DialogProgress()
        dp.create(cr+gn+" KRYPTON BUILD WIZARD"+cr2,cr1+"The Krypton Build is on its Way "+cr2,'', cr1+''+cr2)
        lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", cr1+"Extracting"+cr2+ cr+gn+ cr2+ cr3+" KRYPTON"+cr2+ cr+"Build"+cr2+ cr1+ "now, Please Wait"+cr2)
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    DIALOG = xbmcgui.Dialog()
    DIALOG.ok(cr+"DOWNLOAD COMPLETE!"+cr2, cr1+'To ensure all changes are saved you must now close Kodi'+cr2, cr1+'Android users can click okay and it WILL force close itself.'+cr2)
    killxbmc()
	
def Wizard_Theme(name,url,description):
    if workingURL(url) == False: return False
    name = re.sub('\[.*?]','',name)
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create(cr+gn+" THEME WIZARD"+cr2,cr1+"The Chosen Theme is Whizzing down your Wires "+cr2,'', cr1+'Put the kettle on'+cr2)
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", cr1+"Extracting"+cr2+ cr+gn+"  Build"+cr1+ "now, Please Wait"+cr2)
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    DIALOG = xbmcgui.Dialog()
    DIALOG.ok(cr+"DOWNLOAD COMPLETE!"+cr2, cr1+'To ensure all changes are saved you must now close Kodi'+cr2, ' ')
    killxbmc()

def wizardUpdate(startup=None):
    if workingURL(WIZVER):
        ver = checkWizard('version')
        zip = checkWizard('zip')
        if ver > VERSION:
            yes = DIALOG.yesno(ADDONTITLE, '[COLOR %s]There is a new version of the [COLOR %s]%s[/COLOR]!' % (COLORNAME, COLORNAME, ADDONTITLE), 'Would you like to download [COLOR %s]v%s[/COLOR]?[/COLOR]' % (COLORNAME, ver), nolabel='[B]Remind Me Later[/B]', yeslabel="[B]Update Wizard[/B]")
            if yes:
                log("[Auto Update Wizard] Installing wizard v%s" % ver)
                dp.create(ADDONTITLE,'Downloading Update...','', 'Please Wait')
                lib=os.path.join(PACKAGESPATH, '%s-%s.zip' % (ADDON_ID, ver))
                try: os.remove(lib)
                except: pass
                downloader.download(zip, lib, dp)
                xbmc.sleep(2000)
                dp.update(0,"", "Installing %s update" % ADDONTITLE)
                extract.all(lib, ADDONS, dp)
                dp.close()
                xbmc.sleep(1000)
                ebi('UpdateAddonRepos()')
                ebi('UpdateLocalAddons()')
                xbmc.sleep(1000)
                LogNotify(ADDONTITLE,'Add-on updated')
                log("[Auto Update Wizard] Wizard updated to v%s" % ver)
                ebi('RunScript("%s/startup.py")' % ADDON_ID)
            else: log("[Auto Update Wizard] Install New Wizard Ignored: %s" % ver)
        else: 
            if not startup: LogNotify(ADDONTITLE, "No New Version of Wizard")
            log("[Auto Update Wizard] No New Version v%s" % ver)
    else: log("[Auto Update Wizard] Url for wizard file not valid: %s" % WIZVER)

def workingURL(url):
    if url == 'http://': return False
    try: 
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        response.close()
    except Exception, e:
        return e
    return True    
	
def addFile(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
	u = sys.argv[0]
	if not mode == None: u += "?mode=%s" % urllib.quote_plus(mode)
	if not name == None: u += "&name="+urllib.quote_plus(name)
	if not url == None: u += "&url="+urllib.quote_plus(url)
	ok=True
	if themeit: display = themeit % display
	liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
	liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
	liz.setProperty( "Fanart_Image", fanart )
	if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok
	
#######################################################################
# The code below determines the platform of the device.
def platform():
    if xbmc.getCondVisibility('system.platform.android'):   return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):   return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'): return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):     return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):    return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):     return 'ios'
#######################################################################
