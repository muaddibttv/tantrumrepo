#######################################################################
#Import Modules Section
import sys
import glo_var
#######################################################################

def menuTitle(title):
    buildit = glo_var.COLOR + glo_var.GROUP_NAME + glo_var.COLOR2 + glo_var.COLOR1 + title + glo_var.COLOR2
    return buildit
    
def buildTitle(title):
    buildit = glo_var.COLOR1 + 'Install ' + title + glo_var.COLOR2
    return buildit
    
def actionTitle(title):
    buildit = glo_var.COLOR1 + title + glo_var.COLOR2
    return buildit
    
def actionTitlePlain(title):
    buildit = title
    return buildit
    
