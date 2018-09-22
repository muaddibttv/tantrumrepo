#######################################################################
#Import Modules Section
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs
import os 
import sys
import glob
import shutil
import urllib2,urllib
import re
import glo_var
import base_info
import time
from datetime import date, datetime, timedelta
#######################################################################

#######################################################################
#Global Variables
#Do Not Edit These Variables or any others in this wizard!
ADDONS         = glo_var.ADDONS
ADDON_ID       = glo_var.ADDON_ID
ADDONTITLE     = glo_var.ADDONTITLE
ART            = glo_var.ART
FANART         = glo_var.FANART
BACKGROUND     = glo_var.BACKGROUND if not glo_var.BACKGROUND == '' or not base_info.workingURL(glo_var.BACKGROUND) else FANART
cr             = glo_var.COLOR
cr2            = glo_var.COLOR2
FONTHEADER     = glo_var.FONTHEADER if not glo_var.FONTHEADER == '' else "Font16"
FONTSETTINGS   = glo_var.FONTSETTINGS if not glo_var.FONTSETTINGS == '' else "Font14"
HEADERIMAGE    = glo_var.HEADERIMAGE
HEADERMESSAGE  = glo_var.HEADERMESSAGE
HEADERTYPE     = glo_var.HEADERTYPE if glo_var.HEADERTYPE == 'Image' else 'Text'
HOMEPATH       = glo_var.HOMEPATH
NOTIFY         = glo_var.ENABLE
NOTEID         = base_info.getS('noteid')
NOTEDISMISS    = base_info.getS('notedismiss')
THEME          = glo_var.THEME1
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
THREEDAYS      = TODAY + timedelta(days=3)
UPDATECHECK    = glo_var.UPDATECHECK if str(glo_var.UPDATECHECK).isdigit() else 1
NEXTCHECK      = TODAY + timedelta(days=UPDATECHECK)
#######################################################################

#######################################################################
#NOTIFICATIONS
ACTION_PREVIOUS_MENU 			=  10	## ESC action
ACTION_NAV_BACK 				=  92	## Backspace action
ACTION_MOVE_LEFT				=   1	## Left arrow key
ACTION_MOVE_RIGHT 				=   2	## Right arrow key
ACTION_MOVE_UP 					=   3	## Up arrow key
ACTION_MOVE_DOWN 				=   4	## Down arrow key
ACTION_MOUSE_WHEEL_UP 			= 104	## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN			= 105	## Mouse wheel down
ACTION_MOVE_MOUSE 				= 107	## Down arrow key
ACTION_SELECT_ITEM				=   7	## Number Pad Enter
ACTION_BACKSPACE				= 110	## ?
ACTION_MOUSE_LEFT_CLICK 		= 100
ACTION_MOUSE_LONG_CLICK 		= 108
#######################################################################

#######################################################################
def notification(msg='', resize=False, L=0 ,T=0 ,W=1280 ,H=720 , TxtColor='0xFF0000', Font=FONTSETTINGS, BorderWidth=15):
	class MyWindow(xbmcgui.WindowDialog):
		scr={};
		def __init__(self,msg='',L=0,T=0,W=1280,H=720,TxtColor='0xFF0000',Font='font14',BorderWidth=10):
			image_path = os.path.join(ART, 'ContentPanel.png')
			self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
			self.addControl(self.border); 
			self.BG=xbmcgui.ControlImage(L+BorderWidth,T+BorderWidth,W-(BorderWidth*2),H-(BorderWidth*2), BACKGROUND, aspectRatio=0, colorDiffuse='0x9FFFFFFF')
			self.addControl(self.BG)
			if HEADERTYPE == 'Image':
				iLogoW=144; iLogoH=68
				self.iLogo=xbmcgui.ControlImage((L+(W/2))-(iLogoW/2),T+10,iLogoW,iLogoH,HEADERIMAGE,aspectRatio=0)
				self.addControl(self.iLogo)
			else:
				title = HEADERMESSAGE
				times = int(float(FONTHEADER[-2:]))
				temp = title.replace('[', '<').replace(']', '>')
				temp = re.sub('<[^<]+?>', '', temp)
				title_width = len(str(temp))*(times - 1)
				title = THEME % title
				self.title=xbmcgui.ControlTextBox(L+(W-title_width)/2,T+BorderWidth,title_width,30,font=FONTHEADER,textColor='0xFF1E90FF')
				self.addControl(self.title)
				self.title.setText(title)
			msg = THEME % msg
			self.TxtMessage=xbmcgui.ControlTextBox(L+BorderWidth+10,T+30+BorderWidth,W-(BorderWidth*2)-20,H-(BorderWidth*2)-75,font=Font,textColor=TxtColor)
			self.addControl(self.TxtMessage)
			self.TxtMessage.setText(msg)
			focus=os.path.join(ART, 'button-focus_lightblue.png'); nofocus=os.path.join(ART, 'button-focus_grey.png')
			w1      = int((W-(BorderWidth*5))/3); h1 = 35
			t       = int(T+H-h1-(BorderWidth*1.5))
			space   = int(L+(BorderWidth*1.5))
			dismiss = int(space+w1+BorderWidth)
			later   = int(dismiss+w1+BorderWidth)
			self.buttonDismiss=xbmcgui.ControlButton(dismiss,t,w1,h1,"Dismiss",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.buttonRemindMe=xbmcgui.ControlButton(later,t,w1,h1,"Remind Me Later",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.addControl(self.buttonDismiss); self.addControl(self.buttonRemindMe)
			self.buttonRemindMe.controlLeft(self.buttonDismiss); self.buttonRemindMe.controlRight(self.buttonDismiss)
			self.buttonDismiss.controlLeft(self.buttonRemindMe); self.buttonDismiss.controlRight(self.buttonRemindMe)
			self.setFocus(self.buttonRemindMe);
		def doRemindMeLater(self):
			try:
				base_info.setS("notedismiss","false")
				base_info.loga("[Notification] NotifyID %s Remind Me Later" % base_info.getS('noteid'))
			except: pass
			self.CloseWindow()
		def doDismiss(self):
			try:    
				base_info.setS("notedismiss","true")
				base_info.log("[Notification] NotifyID %s Dismissed" % base_info.getS('noteid'))
			except: pass
			self.CloseWindow()			
		def onAction(self,action):
			try: F=self.getFocus()
			except: F=False
			if   action == ACTION_PREVIOUS_MENU: self.doRemindMeLater()
			elif action == ACTION_NAV_BACK: self.doRemindMeLater()
		def onControl(self,control):
			if   control==self.buttonRemindMe: self.doRemindMeLater()
			elif control== self.buttonDismiss: self.doDismiss()
			else:
				try:    self.setFocus(self.buttonRemindMe)
				except: pass
		def CloseWindow(self): self.close()
	if resize==False: maxW=1280; maxH=720; W=int(maxW/1.5); H=int(maxH/1.5); L=int((maxW-W)/2); T=int((maxH-H)/2); 
	TempWindow=MyWindow(msg=msg,L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth)
	TempWindow.doModal()
	del TempWindow

def firstRun(msg='', TxtColor='0xFFFFFFFF', Font='font12', BorderWidth=10):
	class MyWindow(xbmcgui.WindowDialog):
		scr={};
		def __init__(self,L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font12',BorderWidth=10):
			image_path = os.path.join(ART, 'ContentPanel.png')
			self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
			self.addControl(self.border); 
			self.BG=xbmcgui.ControlImage(L+BorderWidth,T+BorderWidth,W-(BorderWidth*2),H-(BorderWidth*2), FANART, aspectRatio=0, colorDiffuse='0x9FFFFFFF')
			self.addControl(self.BG)
			title = cr+ADDONTITLE+cr2
			times = int(float(Font[-2:]))
			temp = title.replace('[', '<').replace(']', '>')
			temp = re.sub('<[^<]+?>', '', temp)
			title_width = len(str(temp))*(times - 1)
			title = THEME % title
			self.title=xbmcgui.ControlTextBox(L+(W-title_width)/2,T+BorderWidth,title_width,30,font='font14',textColor='0xFF1E90FF')
			self.addControl(self.title)
			self.title.setText(title)
			msg   = "Currently no build installed from %s.\n\nSelect 'Build Menu' to install a Build or 'Ignore' to never see this message again.\n\nThank you for choosing %s." % (cr+ADDONTITLE+cr2, cr+ADDONTITLE+cr2)
			msg   = THEME % msg
			self.TxtMessage=xbmcgui.ControlTextBox(L+(BorderWidth*2),T+30+BorderWidth,W-(BorderWidth*4),H-(BorderWidth*2)-75,font=Font,textColor=TxtColor)
			self.addControl(self.TxtMessage)
			self.TxtMessage.setText(msg)
			focus=os.path.join(ART, 'button-focus_lightblue.png'); nofocus=os.path.join(ART, 'button-focus_grey.png')
			w1        = int((W-(BorderWidth*5))/3); h1 = 35
			t         = int(T+H-h1-(BorderWidth*1.5))
			save      = int(L+(BorderWidth*1.5))
			buildmenu = int(save+w1+BorderWidth)
			ignore    = int(buildmenu+w1+BorderWidth)
			self.buttonSAVEMENU=xbmcgui.ControlButton(save,t,w1,h1,"Save Data Menu",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.buttonBUILDMENU=xbmcgui.ControlButton(buildmenu,t,w1,h1,"Build Menu",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.buttonIGNORE=xbmcgui.ControlButton(ignore,t,w1,h1,"Ignore",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
			self.addControl(self.buttonSAVEMENU); self.addControl(self.buttonBUILDMENU); self.addControl(self.buttonIGNORE)
			self.buttonIGNORE.controlLeft(self.buttonBUILDMENU); self.buttonIGNORE.controlRight(self.buttonSAVEMENU)
			self.buttonBUILDMENU.controlLeft(self.buttonSAVEMENU); self.buttonBUILDMENU.controlRight(self.buttonIGNORE)
			self.buttonSAVEMENU.controlLeft(self.buttonIGNORE); self.buttonSAVEMENU.controlRight(self.buttonBUILDMENU)
			self.setFocus(self.buttonIGNORE)
		def doSaveMenu(self):
			base_info.loga("[Check Updates] [User Selected: Open Save Data Menu] [Next Check: %s]" % str(NEXTCHECK))
			base_info.setS('lastbuildcheck', str(NEXTCHECK))
			self.CloseWindow()
 			url = 'plugin://%s/?mode=savedata' % ADDON_ID
			xbmc.executebuiltin('ActivateWindow(10025, "%s", return)' % url)
		def doBuildMenu(self):
			base_info.loga("[Check Updates] [User Selected: Open Build Menu] [Next Check: %s]" % str(NEXTCHECK))
			base_info.setS('lastbuildcheck', str(NEXTCHECK))
			self.CloseWindow()
			url = 'plugin://%s/?mode=builds' % ADDON_ID
			xbmc.executebuiltin('ActivateWindow(10025, "%s", return)' % url)
		def doIgnore(self):
			base_info.loga("[First Run] [User Selected: Ignore Build Menu] [Next Check: %s]" % str(NEXTCHECK))
			base_info.setS('lastbuildcheck', str(NEXTCHECK))
			self.CloseWindow()
		def onAction(self,action):
			try: F=self.getFocus()
			except: F=False
			if   action == ACTION_PREVIOUS_MENU: self.doIgnore()
			elif action == ACTION_NAV_BACK: self.doIgnore()
			elif action == ACTION_MOVE_LEFT and not F: self.setFocus(self.buttonBUILDMENU)
			elif action == ACTION_MOVE_RIGHT and not F: self.setFocus(self.buttonIGNORE)
		def onControl(self,control):
			if   control==self.buttonIGNORE: self.doIgnore()
			elif control==self.buttonBUILDMENU:  self.doBuildMenu()
			elif control==self.buttonSAVEMENU:  self.doSaveMenu()
			else:
				try:    self.setFocus(self.buttonIGNORE); 
				except: pass
		def CloseWindow(self): self.close()
	maxW=1280; maxH=720; W=int(700); H=int(300); L=int((maxW-W)/2); T=int((maxH-H)/2); 
	TempWindow=MyWindow(L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth); 
	TempWindow.doModal() 
	del TempWindow