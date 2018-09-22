#######################################################################
#Import Modules Section
import xbmc
import os
import base_info
import shutil
import glo_var
#######################################################################

#######################################################################
#Global Variables
#Do Not Edit These Variables or any others in this wizard!
ADDON_DATAPATH      = glo_var.ADDON_DATAPATH
ADDONTITLE      = glo_var.ADDONTITLE
ADDONS          = glo_var.ADDONS
cr              = glo_var.COLOR
cr1             = glo_var.COLOR1
cr2             = glo_var.COLOR2
cr3             = glo_var.COLOR3
cr4             = glo_var.COLOR4
DATABASES       = glo_var.DATABASES
DP              = glo_var.DP  
EXCLUDES        = glo_var.EXCLUDES
HOMEPATH        = glo_var.HOMEPATH
NAVI            = glo_var.NAVI
#######################################################################

#######################################################################
# Creating Functions
def WIPE_BACKUPRESTORE():
	DP.create(cr+ADDONTITLE+cr2,cr1+"Restoring Kodi."+cr2,cr1+'In Progress.............'+cr2, cr1+'Please Wait'+cr2)
	try:
		for root, dirs, files in os.walk(HOMEPATH,topdown=True):
			dirs[:] = [d for d in dirs if d not in EXCLUDES]
			for name in files:
				try:
					os.remove(os.path.join(root,name))
					os.rmdir(os.path.join(root,name))
				except: pass
			else:
				continue     
			for name in dirs:
				try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
				except: pass
	except: pass
	DP.create(cr+ADDONTITLE+cr2,cr1+"Wiping Install"+cr2,cr1+'Removing empty folders.'+cr2, cr1+'Please Wait'+cr2)
	base_info.REMOVE_EMPTY_FOLDERS()
	base_info.REMOVE_EMPTY_FOLDERS()
	base_info.REMOVE_EMPTY_FOLDERS()
	base_info.REMOVE_EMPTY_FOLDERS()
	base_info.REMOVE_EMPTY_FOLDERS()
	base_info.REMOVE_EMPTY_FOLDERS()
	base_info.REMOVE_EMPTY_FOLDERS()
	base_info.REMOVE_EMPTY_FOLDERS()
	if os.path.exists(NAVI):
		try:
			shutil.rmtree(NAVI)
		except:
			pass
	if os.path.exists(DATABASES):
		try:
			for root, dirs, files in os.walk(DATABASES,topdown=True):
				dirs[:] = [d for d in dirs]
				for name in files:
					try:
						os.remove(os.path.join(root,name))
						os.rmdir(os.path.join(root,name))
					except: pass    
				for name in dirs:
					try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
					except: pass
		except: pass
	if os.path.exists(ADDON_DATAPATH):
		try:
			for root, dirs, files in os.walk(ADDON_DATAPATH,topdown=True):
				dirs[:] = [d for d in dirs]
				for name in files:
					try:
						os.remove(os.path.join(root,name))
						os.rmdir(os.path.join(root,name))
					except: pass       
				for name in dirs:
					try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
					except: pass
		except: pass
#######################################################################