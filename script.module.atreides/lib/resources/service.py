# -*- coding: UTF-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# @tantrumdev wrote this file.  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.module.atreides
# Addon Provider: 69 Death Squad

import glob
import os
import re
import traceback

import xbmc
import xbmcgui
import xbmcaddon

from lib.resources.lib.modules import log_utils

addon_name = 'Atreides'
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
addon_path = xbmc.translatePath(('special://home/addons/script.module.atreides')).decode('utf-8')


def main():
    xbmcgui.Dialog().notification(addon_name, 'Gathering scraper details', addon_icon)
    settings_xml_path = os.path.join(addon_path, 'resources/settings.xml')
    scraper_path = os.path.join(addon_path, 'lib/resources/lib/sources/en')
    log_utils.log('Atreides Scraper Path: %s' % (str(scraper_path)), log_utils.LOGNOTICE)
    try:
        xml = openfile(settings_xml_path)
    except Exception:
        failure = traceback.format_exc()
        log_utils.log('Atreides Service - Exception: \\n %s' % (str(failure)), log_utils.LOGNOTICE)
        return

    new_settings = []
    new_settings.insert(0, '<category label="32345">')
    match = re.search('(<category label="32345">.*?</category>)', xml, re.DOTALL | re.I)
    if match:
        old_settings = match.group(1)
        log_utils.log('Atreides Service - Old Settings: \\n %s' % (str(old_settings)), log_utils.LOGNOTICE)
        for file in glob.glob("%s/*.py" % (scraper_path)):
            if '__init__' not in file:
                file = file.replace('.py', '')
                new_settings.append(
                    '        <setting id="provider.%s" type="bool" label="%s" default="true" />\\n' %
                    (file.lower(),
                     file.upper()))
        new_settings.append('    </category>')

        xml = xml.replace(old_settings, new_settings)
        savefile(settings_xml_path, xml)

        disable_this()
        xbmcgui.Dialog().notification(addon_name, 'Scraper settings updated', addon_icon)


def disable_this():
    addonxml_path = os.path.join(kodi.get_path(), 'addon.xml')
    xml_content = openfile(addonxml_path)
    if re.search('point="xbmc.service"', xml_content):
        xml_content = xml_content.replace('point="xbmc.service"',
                                          'point="xbmc.jen"')
        savefile(addonxml_path, xml_content)
    else:
        pass


def openfile(path_to_the_file):
    try:
        fh = open(path_to_the_file, 'rb')
        contents = fh.read()
        fh.close()
        return contents
    except Exception:
        failure = traceback.format_exc()
        print('Service Open File Exception - %s \n %s' % (path_to_the_file, str(failure)))
        return None


def savefile(path_to_the_file, content):
    try:
        fh = open(path_to_the_file, 'wb')
        fh.write(content)
        fh.close()
    except Exception:
        failure = traceback.format_exc()
        print('Service Save File Exception - %s \n %s' % (path_to_the_file, str(failure)))


if __name__ == '__main__':
    main()
