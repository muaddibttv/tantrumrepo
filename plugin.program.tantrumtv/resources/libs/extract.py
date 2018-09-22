#######################################################################
#Import Modules Section
import zipfile
import xbmcgui
import glo_var
#######################################################################

#######################################################################
#Global Variables
#Do Not Edit These Variables or any others in this wizard!
cr                  = glo_var.COLOR
cr1                 = glo_var.COLOR1
cr2                 = glo_var.COLOR2
cr3                 = glo_var.COLOR3
cr4                 = glo_var.COLOR4
gn                  = glo_var.GROUP_NAME
#######################################################################

#######################################################################
# Creating Functions
def all(_in, _out, dp=None):
    if dp:
        return allWithProgress(_in, _out, dp)
    return allNoProgress(_in, _out)
        
def allNoProgress(_in, _out):
    try:
        zin = zipfile.ZipFile(_in, 'r')
        zin.extractall(_out)
    except Exception, e:
        print str(e)
    return True

def allWithProgress(_in, _out, dp):
    zin = zipfile.ZipFile(_in,  'r')
    nFiles = float(len(zin.infolist()))
    count  = 0
    errors = 0
    try:
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            filenamefull = item.filename
            dp.update(int(update),cr1+'Extracting... Errors:  '+cr2 + str(errors) ,filenamefull, '')
            try: zin.extract(item, _out)
            except Exception, e:
				errors += 1
				choice = xbmcgui.Dialog().yesno(cr3+'Error!'+cr2, filenamefull , str(e), nolabel=cr1+'Exit'+cr2,yeslabel=cr+'Continue'+cr2)
				if choice == 0:break
				elif choice == 1:pass
    except Exception, e:
        print str(e)
    return True
#######################################################################