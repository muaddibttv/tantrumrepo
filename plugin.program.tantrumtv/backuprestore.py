#######################################################################
#Import Modules Section
import xbmc, xbmcgui
import os
import sys
import shutil
from shutil import copyfile
import urllib
import re
import time
import zipfile
import glo_var
from os import listdir
from os.path import isfile, join
import base_info
from resources.libs import extract
from resources.libs import wipe
from resources.libs import skinSwitch
#######################################################################

#######################################################################
#Global Variables
#Do Not Edit These Variables or any others in this wizard!
USERDATAPATH     = glo_var.USERDATAPATH
ADDON_DATAPATH   = glo_var.ADDON_DATAPATH
ADDONTITLE       = glo_var.ADDONTITLE
BASEURL          = glo_var.BASEURL
cr               = glo_var.COLOR
cr1              = glo_var.COLOR1
cr2              = glo_var.COLOR2
cr3              = glo_var.COLOR3
cr4              = glo_var.COLOR4
DIALOG           = xbmcgui.Dialog()
DP               = glo_var.DP
EXCLUDES_FOLDER  = glo_var.EXCLUDES_FOLDER
gn               = glo_var.GROUP_NAME
HOMEPATH         = glo_var.HOMEPATH
ICON             = glo_var.ICON
USB              = xbmc.translatePath(glo_var.THISADDON.getSetting("zip"))
#######################################################################

#######################################################################
# Creating Functions
def reset_backup_location():
    choice = DIALOG.yesno('Reset Backup Location', 'You are about to reset the backup location to the device root path', 'Would you like to continue?', nolabel='No',yeslabel='Yes')
    if choice == 0: return
    elif choice == 1: pass
    thepath = "/"
    myplatform = base_info.platform()
    if myplatform == 'android': thepath = "/sdcard/"
    elif myplatform == 'linux': thepath = "/"
    elif myplatform == 'windows': thepath = "C:\\"
    elif myplatform == 'osx': thepath = "/"
    elif myplatform == 'atv2': thepath = "/"
    elif myplatform == 'ios': thepath = "/"
    glo_var.THISADDON.setSetting("zip", thepath)

#######################################################################
# Creating Functions
def check_path():
    if not "backupdir" in USB:
        if HOMEPATH in USB:
            DIALOG = xbmcgui.Dialog()
            DIALOG.ok(cr+ADDONTITLE+cr2, cr1+"Invalid path selected for your backups. The path you have selected will be removed during backup and cause an error. Please pick another path that is not in the Kodi directory."+cr2)
            base_info.open_settings_dialog()
            sys.exit(0)
    rootcheck = False
    myplatform = base_info.platform()
    if myplatform == 'android':
        if USB == "/sdcard/": rootcheck = True
    elif myplatform == 'linux':
        if USB == "/": rootcheck = True
    elif myplatform == 'windows':
        if USB == "C:\\": rootcheck = True
    elif myplatform == 'osx':
        if USB == "/": rootcheck = True
    elif myplatform == 'atv2':
        if USB == "/": rootcheck = True
    elif myplatform == 'ios':
        if USB == "/": rootcheck = True
    if rootcheck:
        DIALOG = xbmcgui.Dialog()
        DIALOG.ok(cr+ADDONTITLE+cr2, cr1+"Default root path selected for your backups. The path you have selected typically will not have permissions to be written to and cause an error. Please pick another path that is not the system root directory."+cr2)
        base_info.open_settings_dialog()
        sys.exit(0)
    if not os.path.exists(USB):
        os.makedirs(USB)
        
def _get_keyboard( default="", heading="", hidden=False ):
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default

def Backup():
    guisuccess=1
    check_path()
    if not os.path.exists(USB):
        os.makedirs(USB)
    vq = _get_keyboard( heading=cr1+"Please enter a name for this backup"+cr2 )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'.zip'))
    exclude_dirs =  ['backupdir','cache', 'Thumbnails','temp','Databases']
    exclude_files = ["spmc.log","spmc.old.log","xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","Textures13.db"]
    message_header = cr+gn+" Wizard"+cr2+cr1+" is creating your backup..."+cr2
    message_header2 = cr1+"Creating full backup..."+cr2
    message1 = cr1+"Archiving..."+cr2
    message2 = ""
    message3 = ""
    Convert_Special(USERDATAPATH)
    ARCHIVE_CB(HOMEPATH, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    DIALOG.ok(cr+gn+" Wizard"+cr2, cr1+'The backup completed successfully!.'+cr2,cr+"Backup Location: "+cr2,cr1+backup_zip+cr2)

def Backup_Login():
    check_path()
    if not os.path.exists(USB):
        os.makedirs(USB)
    vq = _get_keyboard( heading=cr1+"Please enter a name for this backup"+cr2 )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'_Login_Data.zip'))
    if not os.path.exists(EXCLUDES_FOLDER):
        os.makedirs(EXCLUDES_FOLDER)
    link=base_info.OPEN_URL(BASEURL + 'login.xml')
    plugins=re.compile('<plugin>(.+?)</plugin>').findall(link)
    for match in plugins:
        ADDONPATH = xbmc.translatePath(os.path.join(ADDON_DATAPATH,match))
        ADDONSETTINGS = xbmc.translatePath(os.path.join(ADDONPATH,'settings.xml'))
        EXCLUDEMOVE = xbmc.translatePath(os.path.join(EXCLUDES_FOLDER,match+'_settings.xml'))
        DIALOG = xbmcgui.Dialog()
        if os.path.exists(ADDONSETTINGS):
            copyfile(ADDONSETTINGS, EXCLUDEMOVE)
    exclude_dirs =  [' ']
    exclude_files = [" "]
    message_header = cr+gn+" Wizard"+cr2+cr1+ "is creating your backup..."+cr2
    message_header2 = cr1+"Creating full backup..."+cr2
    message1 = cr1+"Archiving..."+cr2
    message2 = ""
    message3 = ""
    ARCHIVE_CB(EXCLUDES_FOLDER, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    try:
        shutil.rmtree(EXCLUDEMOVE)
        shutil.rmdir(EXCLUDEMOVE)
    except: pass
    base_info.REMOVE_EMPTY_FOLDERS()
    base_info.REMOVE_EMPTY_FOLDERS()
    base_info.REMOVE_EMPTY_FOLDERS()
    base_info.REMOVE_EMPTY_FOLDERS()
    base_info.REMOVE_EMPTY_FOLDERS()
    base_info.REMOVE_EMPTY_FOLDERS()
    base_info.REMOVE_EMPTY_FOLDERS()
    base_info.REMOVE_EMPTY_FOLDERS()
    DIALOG.ok(cr+gn+" Wizard"+cr2, cr1+'The backup completed successfully!.'+cr2,cr+"Backup Location: "+cr2,cr1+backup_zip+cr2)

def Restore_Login():
    for file in os.listdir(USB):
        if file.endswith("_Login_Data.zip"):
            url =  xbmc.translatePath(os.path.join(USB,file))
            base_info.addItem(file,url,'restorelog',ICON,ICON,'')

def ARCHIVE_CB(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    ITEM =[]
    DP.create(message_header, message1, message2, message3)
    for BASEURL, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for BASEURL, dirs, files in os.walk(sourcefile):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files]
        for file in files:
            try:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                DP.update(int(progress),cr1+"Backing Up"+cr2,cr1+ '%s' %file+cr2, '')
                fn = os.path.join(BASEURL, file)
                zipobj.write(fn, fn[rootlen:]) 
            except: pass            
    zipobj.close()
    DP.close()

def Convert_Special(url):
    HOMEPATH =  xbmc.translatePath('special://home')
    DIALOG = xbmcgui.Dialog()
    DP.create(cr+ADDONTITLE+cr2,cr1+"Renaming paths..."+cr2,'', '')
    url = xbmc.translatePath('special://userdata')
    for root, dirs, files in os.walk(url):
        for file in files:
            if file.endswith(".xml"):
                 DP.update(0,cr1+"Fixing"+cr2,cr1 + file + cr2, cr1+"Please wait....."+cr2)
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(HOMEPATH, 'special://home/')
                 f= open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()

def Restore():
    for file in os.listdir(USB):
        if file.endswith(".zip"):
            url =  xbmc.translatePath(os.path.join(USB,file))
            base_info.addItem(file,url,'restorezip',ICON,ICON,'')

def Read_Zip(url):
    if not "_addon_data" in url:
        if not "tv_guide" in url:
            if DIALOG.yesno(cr+ADDONTITLE+cr2,cr1 + url + cr2,cr1+"Do you want to restore this backup?"+cr2):
                skinswap()
                wipe.WIPE_BACKUPRESTORE()
                _out = xbmc.translatePath(os.path.join('special://','home'))
            else:
                sys.exit(1)
        else:
            if DIALOG.yesno(cr+ADDONTITLE+cr2,cr1+  url + cr2,cr1+"Do you want to restore this backup?"+cr2):
                _out = GUIDE
            else:
                sys.exit(1)
    else:
        if DIALOG.yesno(cr+ADDONTITLE+cr2,cr1 + url + cr2,cr1+"Do you want to restore this backup?"+cr2):
            _out = ADDON_DATAPATH
        else:
            sys.exit(1)
    _in = url
    DP.create(ADDONTITLE,cr1+"Restoring File:"+cr2,_in,'')
    unzip(_in, _out, DP)
    
    if not "addon_data" in url:
        if not "tv_guide" in url:
            DIALOG.ok(cr+ADDONTITLE+cr2,cr1+'Restore Successful, please restart XBMC/Kodi for changes to take effect.'+cr2,'','')
            base_info.killxbmc()
        else:
            DIALOG.ok(cr+ADDONTITLE+cr2,cr1+'Your TV Guide settings have been restored.'+cr2,'','')
    else:
        DIALOG.ok(cr+ADDONTITLE+cr2,cr1+'Your Addon Data settings have been restored.'+cr2,'','')

def Read_Login_Data_Zip(url):
    DIALOG = xbmcgui.Dialog()
    if DIALOG.yesno(cr+ADDONTITLE+cr2,cr1 + url + cr2,cr1+"Do you want to restore this backup of your login data?"+cr2):
        _out = xbmc.translatePath(os.path.join('special://','home/tmp'))
        _in = url
        DP.create(cr+ADDONTITLE+cr2,cr1+"Restoring File:"+cr2,_in,'')
        unzip(_in, _out, DP)
        name = "RESTORE"
        link=base_info.OPEN_URL(BASEURL + 'login.xml')
        plugins=re.compile('<plugin>(.+?)</plugin>').findall(link)
        for match in plugins:
            ADDONPATH = xbmc.translatePath(os.path.join(ADDON_DATAPATH,match))
            ADDONSETTINGS = xbmc.translatePath(os.path.join(ADDONPATH,'settings.xml'))
            EXCLUDEMOVE = xbmc.translatePath(os.path.join(_out,match+'_settings.xml'))
            if os.path.exists(EXCLUDEMOVE):
                if not os.path.exists(ADDONPATH):
                    os.makedirs(ADDONPATH)
                if os.path.isfile(ADDONSETTINGS):
                    os.remove(ADDONSETTINGS)
                os.rename(EXCLUDEMOVE, ADDONSETTINGS)
                try:
                    os.remove(EXCLUDEMOVE)
                except: pass
        DIALOG = xbmcgui.Dialog()
        DIALOG.ok(cr+ADDONTITLE+cr2,cr1+'Login Data Successfully Restored'+cr2,'','')
    else:
        sys.exit(1)

def unzip(_in, _out, DP):
    zin    = zipfile.ZipFile(_in,  'r')
    nFiles = float(len(zin.infolist()))
    count  = 0
    try:
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            DP.update(int(update),'','',cr1 + str(item.filename) + cr2)
            try:
                zin.extract(item, _out)
            except Exception, e:
                print str(e)
    except Exception, e:
        print str(e)
        return False
    return True
        
def ListBackDel():
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    for file in os.listdir(USB):
        if file.endswith(".zip"):
            url =  xbmc.translatePath(os.path.join(USB,file))
            base_info.addDir2(file,url,'delete',ICON,ICON,'')

def Delete_Backup(url):
    if DIALOG.yesno(cr+ADDONTITLE+cr2,cr1 + url + cr2,cr1+"Do you want to delete this backup?"+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2):
        os.remove(url)
        DIALOG.ok(cr+ADDONTITLE+cr2,cr1 + url + cr2,cr1+"Successfully deleted."+cr2)
        xbmc.executebuiltin("Container.Refresh")

def Delete_All_Backups():
    if DIALOG.yesno(cr+ADDONTITLE+cr2,cr1+"Do you want to delete all backups?"+cr2,yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2):
        shutil.rmtree(USB)
        os.makedirs(USB)
        DIALOG.ok(cr+ADDONTITLE+cr2,cr1+"All backups successfully deleted."+cr2)

def skinswap():
    skin         =  xbmc.getSkinDir()
    KODIV        =  float(xbmc.getInfoLabel("System.BuildVersion")[:4])
    skinswapped = 0
    if skin not in ['skin.confluence','skin.estuary']:
        choice = xbmcgui.Dialog().yesno(cr+ADDONTITLE+cr2, cr1+'You are not using the default confluence skin.'+cr2,cr1+'Click Yes to switch to the default confluence skin now.'+cr2,cr1+'Please be patient as we attempt to switch your skin.'+cr2, yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2)
        if choice == 0:
            sys.exit(1)
        skin = 'skin.estuary' if KODIV >= 17 else 'skin.confluence'
        skinSwitch.swapSkins(skin)
        skinswapped = 1
        time.sleep(1)
    if skinswapped == 1:
        if not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
            xbmc.executebuiltin( "Action(Select)" )
    if skinswapped == 1:
        while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
            time.sleep(1)
    if skinswapped == 1:
        while xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
            xbmc.executebuiltin( "Action(Left)" )
            xbmc.executebuiltin( "Action(Select)" )
            time.sleep(1)
    skin         =  xbmc.getSkinDir()
    if skin not in ['skin.confluence','skin.estuary']:
        choice = xbmcgui.Dialog().yesno(cr+ADDONTITLE+cr2, cr3+'ERROR: AUTOSWITCH WAS NOT SUCCESFULL'+cr2,cr1+'CLICK YES TO MANUALLY SWITCH TO CONFLUENCE NOW'+cr2,cr1+'YOU CAN PRESS NO AND ATTEMPT THE AUTO SWITCH AGAIN IF YOU WISH'+cr2, yeslabel=cr+'YES'+cr2,nolabel=cr1+'NO'+cr2)
        if choice == 1:
            xbmc.executebuiltin("ActivateWindow(appearancesettings)")
            return
        else:
            sys.exit(1)
#######################################################################