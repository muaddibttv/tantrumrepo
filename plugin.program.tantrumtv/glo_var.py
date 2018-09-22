#######################################################################
#Import Modules Section
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, base64
import os
#######################################################################

#######################################################################
# Primary Addon Variables 
AddonID             = xbmcaddon.Addon().getAddonInfo('id')
THISADDON           = xbmcaddon.Addon(id=AddonID)
ADDON_ID            = xbmcaddon.Addon().getAddonInfo('id')
URL                 = base64.b64decode(b'aHR0cDovL3JlcG8udGFudHJ1bXR2LmNvbS9kbS93aXphcmQv')
ADDONTITLE          = base64.b64decode(b'VGFudHJ1bS5UViBJbnN0YWxsIFdpemFyZA==')
GROUP_NAME          = base64.b64decode(b'VGFudHJ1bS5UViA=')
PATH                = base64.b64decode(b'd2l6YXJk')
EXCLUDES            = [AddonID,'script.module.requests','temp','backupdir','script.module.urllib3','script.module.chardet','script.module.idna','script.module.certifi','repository.tantrumtv']
UPDATECHECK         = 0
AUTOUPDATE          = "Yes"
USER_AGENT          = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
#######################################################################

#######################################################################
# Notification Variables 
ENABLE              = THISADDON.getSetting('enablenotify')
HEADERTYPE          = base64.b64decode(b'dGV4dA==')
FONTHEADER          = base64.b64decode(b'Rm9udDE0')
HEADERIMAGE         = base64.b64decode(b'dXJsIHRvIGltYWdlLCBzaXplIG5lZWRzIHRvIGJlIDQyNHgxODA=')
FONTSETTINGS        = base64.b64decode(b'Rm9udDEy')
BACKGROUND          = ''
#######################################################################

#######################################################################
# Filename Variables 
BASEURL             = URL
ADULTFILE           = BASEURL + base64.b64decode(b'YWR1bHQudHh0')
ADVANCEDFILE        = BASEURL + base64.b64decode(b'YWR2YW5jZWQudHh0')
ADVSETTINGSFILE     = xbmc.translatePath(os.path.join('special://profile/','advancedsettings.xml'))
CREDITSFILE         = BASEURL + base64.b64decode(b'Y3JlZGl0cy50eHQ=')
KRYPTONFILE         = BASEURL + base64.b64decode(b'a3J5cHRvbi50eHQ=')
NOTIFICATION        = BASEURL + base64.b64decode(b'bm90aWZ5LnR4dA==')
SUPPORT             = BASEURL + base64.b64decode(b'c3VwcG9ydC50eHQ=')
THEMEFILE           = BASEURL + base64.b64decode(b'dGhlbWVzLnR4dA==')
VERSION             = BASEURL + base64.b64decode(b'dmVyc2lvbi50eHQ=')
WIZARDFILE          = BASEURL + base64.b64decode(b'd2l6YXJkLnR4dA==')
WIZVER              = BASEURL + base64.b64decode(b'd2l6dmVyLnR4dA==')
#######################################################################

#######################################################################
# Path Variables
HOMEPATH            = xbmc.translatePath('special://home/')
ADDONS              = os.path.join(HOMEPATH, 'addons')
USERDATAPATH        = os.path.join(HOMEPATH, 'userdata')
ADDON_DATAPATH      = xbmc.translatePath(os.path.join(USERDATAPATH,'addon_data'))
ADDONDATA           = os.path.join(USERDATAPATH, 'addon_data', ADDON_ID)
COVENANT            = xbmc.translatePath(os.path.join('special://home/addons/','plugin.video.covenant'))
COVENANTDATA        = xbmc.translatePath('special://userdata/addon_data/plugin.video.covenant')
EXCLUDES_FOLDER     = xbmc.translatePath(os.path.join(USERDATAPATH,'BACKUP'))
LOGPATH             = xbmc.translatePath('special://logpath/')
USB                 = xbmc.translatePath(os.path.join(HOMEPATH,'backupdir'))
THUMBSPATH          = os.path.join(USERDATAPATH,  'Thumbnails')
DATABASE            = os.path.join(USERDATAPATH, 'Database') 
DATABASES           = xbmc.translatePath(os.path.join(USERDATAPATH,'Database'))
NAVI                = xbmc.translatePath(os.path.join(ADDONS,'script.navi-x'))
PACKAGESPATH        = xbmc.translatePath(os.path.join('special://home/addons/' + 'packages'))
YOUTUBE             = xbmc.translatePath(os.path.join('special://home/addons/','plugin.video.youtube'))
YOUTUBEDATA         = xbmc.translatePath('special://userdata/addon_data/plugin.video.youtube')
#######################################################################

#######################################################################
# Theme Variables
COLOR               = '[COLOR red][B]'
COLOR1              = '[COLOR snow][B]'
COLOR2              = '[/B][/COLOR]'
COLOR3              = '[COLOR springgreen][B]'
COLOR4              = '[COLOR crimson][B]'
COLORNAME           = 'snow'
THEME1              = '[COLOR '+COLORNAME+'][B]%s[/B][/COLOR]'  
#######################################################################

#######################################################################
# Menu Title Variables
ADULT               = base64.b64decode(b'QWR1bHQgQnVpbGRzIE1lbnU=')
KRYPTON             = base64.b64decode(b'S3J5cHRvbiBCdWlsZHMgTWVudQ==')
BACKUPBUILD         = base64.b64decode(b'QmFja3VwIEJ1aWxkIChFeGM6IERhdGFiYXNlcyAmIFRodW1ibmFpbHMp')
BACKUPLOGIN         = base64.b64decode(b'QmFja3VwIExvZ2luIERhdGE=')
BUILD               = base64.b64decode(b'QnVpbGQgTWVudQ==')
CHKREPO             = base64.b64decode(b'Q2hlY2sgZm9yIEJyb2tlbiBSZXBvc2l0b3JpZXM=')
CHKSOURCE           = base64.b64decode(b'Q2hlY2sgZm9yIEJyb2tlbiBTb3VyY2Vz')
CLEARCACHE          = base64.b64decode(b'Q2xlYXIgQ2FjaGU=')
CLEARCRASH          = base64.b64decode(b'Q2xlYXIgQ3Jhc2ggTG9ncw==')
CLEARPACK           = base64.b64decode(b'Q2xlYXIgUGFja2FnZXM=')
CLEARTHUMB          = base64.b64decode(b'Q2xlYXIgVGh1bWJuYWlscw==')
CONTACTUS           = base64.b64decode(b'Q29udGFjdCBVcw==')
CONVERT             = base64.b64decode(b'Q29udmVydCBQYXRocyB0byBTcGVjaWFs')
COVENANTTITLE       = base64.b64decode(b'Q292ZW5hbnQgU2V0dGluZ3MgRml4IChLb2RpIDE3LjQtMTcuNS4xKQ==')
DELETEALL           = base64.b64decode(b'RGVsZXRlIEFsbCBCYWNrdXBz')
DELETEBACKUP        = base64.b64decode(b'RGVsZXRlIEEgQmFja3Vw')
DEV                 = base64.b64decode(b'RGV2ZWxvcGVyIE1lbnU=')
FIXESTWEAKS         = base64.b64decode(b'Rml4ZXMgYW5kIFR3ZWFrcyBNZW51')
FORCECLOSE          = base64.b64decode(b'Rm9yY2UgQ2xvc2U=')
FORCEUPDATE         = base64.b64decode(b'VXBkYXRlIEFkZG9ucyBhbmQgUmVwb3NpdG9yaWVz')
FRESHSTART          = base64.b64decode(b'RnJlc2ggU3RhcnQ=')
MAINT               = base64.b64decode(b'TWFpbnRlbmFuY2UgTWVudQ==')
RELOAD              = base64.b64decode(b'UmVsb2FkIFNraW4=')
REST                = base64.b64decode(b'UmVzdG9yZSBEYXRh')
RESTOREBUILDBCK     = base64.b64decode(b'UmVzdG9yZSBCdWlsZCBCYWNrdXA=')
RESTORELOGIN        = base64.b64decode(b'UmVzdG9yZSBMb2dpbiBEYXRh')
SAVE                = base64.b64decode(b'U2F2ZSBEYXRh')
THEME               = base64.b64decode(b'VGhlbWVzIE1lbnU=')
VIEW                = base64.b64decode(b'VmlldyBLb2RpIExvZw==')
VIEWOLD             = base64.b64decode(b'VmlldyBPbGQgS29kaSBMb2c=')
VIEWWIZ             = base64.b64decode(b'VmlldyBXaXphcmQgTG9n')
WIZCREDITS          = base64.b64decode(b'V2l6YXJkIENyZWRpdHM=')
YOUTUBETITLE        = base64.b64decode(b'WW91VHViZSBEYWlseSBMaW1pdCBGaXg=')
ROOTTITLE           = base64.b64decode(b'UmVzZXQgV2l6YXJkIEJhY2t1cCBMb2NhdGlvbiB0byBSb290')
SDTITLE             = base64.b64decode(b'Q2xlYW4gb3V0IFNwb3J0c0RldmlsIGFuZCBSZWluc3RhbGw=')
DEBUGTITLE          = base64.b64decode(b'VG9nZ2xlIERlYnVnIE9uL09mZg==')
DEBUGSKIN           = base64.b64decode(b'VG9nZ2xlIFNraW4gRGVidWc=')
CLEARADVTITLE       = base64.b64decode(b'Q2xlYXIgQWxsIEFkdmFuY2VkIFNldHRpbmdz')
#######################################################################

#######################################################################
# Active Menu Variables
ADULTACTIVE         = THISADDON.getSetting('adult')
DEVELOPERACTIVE     = THISADDON.getSetting('developer')
FIXESACTIVE         = THISADDON.getSetting('fixes')
THEMEACTIVE         = THISADDON.getSetting('theme')
#######################################################################

#######################################################################
# Icons/Artwork Variables
ART                 = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'resources/art/'))
ADULT_ICON          = ART + 'adult.png'
KRYPTON_ICON        = ART + 'krypton.png'
BACKUP_ICON         = ART + 'backupbuild.png'
BACKUPLOGIN_ICON    = ART + 'backuplogin.png'
BUILDS_ICON			= ART + 'builds.png'
CACHE_ICON          = ART + 'cache.png'
CHKREPO_ICON        = ART + 'repo.png'
CHKSOURCE_ICON      = ART + 'source.png'
CONVERTPATH_ICON    = ART + 'convert.png'
CREDIT_ICON         = ART + 'credits.png'
DELETEALL_ICON      = ART + 'deleteallbackups.png'
DELETEBACKUP_ICON   = ART + 'deletebackup.png'
DEV_ICON            = ART + 'developer.png'
FANART              = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID , 'fanart.jpg'))
ICON_FIXES          = ART + 'fixes.png'
ICON_TWEAKS         = ART + 'tweaks.png'
ICON_FIXESMENU      = ART + 'fixesandtweaks.png'
FRESHSTART_ICON     = ART + 'freshstart.png'
ICON                = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'icon.png'))
ICONSAVE            = ART + 'iconsave.png'
MAINT_ICON          = ART + 'maintenance.png'
PACKAGES_ICON       = ART + 'packages.png'
REST_ICON           = ART + 'restoredata.png'
RESTOREBACKUP_ICON  = ART + 'restorebackup.png'
RESTORELOGIN_ICON   = ART + 'restorelogin.png'
SAVE_ICON           = ART + 'save.png'
SUPPORT_ICON        = ART + 'contact.png'
THEME_ICON          = ART + 'themes.png'
THUMBNAILS_ICON     = ART + 'thumbnails.png'
FORCECLOSE_ICON     = ART + 'ForceClose.png'
CLEARCRASH_ICON     = ART + 'clearcrash.png'
VIEWLOG_ICON        = ART + 'viewlog.png'
ICONMAINT           = ART + 'maintenance.png'
#######################################################################

#######################################################################
#Global Variables, Do Not Edit These Variables
dialog              = xbmcgui.Dialog()
DIALOG              = xbmcgui.Dialog()
dp                  = xbmcgui.DialogProgress()
DP                  = xbmcgui.DialogProgress()
HEADERMESSAGE       = GROUP_NAME
PLUGIN              = os.path.join(ADDONS, ADDON_ID)
skin                = xbmc.getSkinDir()
#######################################################################