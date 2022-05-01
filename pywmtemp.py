#!/usr/bin/env python
"""
Simple dockapp to show up temperature for selected labels
"""
import argparse
import os
import re
import sys
import time

import psutil
import wmdocklib
from wmdocklib import helpers
from wmdocklib import pywmgeneral
import yaml


XDG_CONF_DIR = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
# expected bitmap contained font should be found in the same location as main
# program
FONT = '''\
/* XPM */
static char *_x8_lcd_alt[] = {
/* columns rows colors chars-per-pixel */
"192 48 10 1 ",
"  c #202020",
". c #440000",
"X c #542A00",
"o c #004941",
"O c #920000",
"+ c #E00000",
"@ c #A85500",
"# c #FF8200",
"$ c #188A86",
"% c #20B2AE",
/* pixels */
" ooo   o$o   %o%   %o%   o%o  $ooo$  %%o   oo%   oo%   %oo   ooo   ooo   ooo   ooo   ooo   ooo$  %%%   ooo$ $%%%$ $%%%$ %ooo% $%%%$ $%%%$ $%%%$ $%%%$ $%%%$  ooo   ooo   oo%$  ooo  $%oo  $%%%$ ",
"o   o o % o o% %o o$ $o o$$$% %   % %  $o o  $o o $ o o $ o %   % o $ o o   o o   o o   o o   % %   % o   % o   % o   % %   % %   o %   o o   % %   % %   % o   o o   o o $ o o   o o $ o %   % ",
"o   o o % o o$ $o %$$$% %   o o  $o o$$ o o $ o o$  o o  $o o$ $o o $ o o   o o   o o   o o  $o %   % o   % o   % o   % %   % %   o %   o o   % %   % %   % o $ o o $ o o$  o %$$$% o  $o o   % ",
" ooo   o$o   ooo   %o%   %%%   o%o   %oo   ooo   %oo   oo%  $%%%$ $%%%$  ooo  $%%%$  ooo   o%o  $ooo$  ooo$ $%%%$  %%%$ $%%%$ %%%%$ $%%%$  ooo$ $%%%$ $%%%$  ooo   ooo  $ooo   ooo   ooo$  oo%$ ",
"o   o o % o o   o %$$$% o   % o$  o % $ % o   o o$  o o  $o o$ $o o $ o o   o o   o o   o o$  o %   % o   % %   o o   % o   % o   % %   % o   % %   % o   % o   o o   o o$  o %$$$% o  $o o $ o ",
"o   o o   o o   o o$ $o %$$$o %   % %  $o o   o o $ o o $ o %   % o $ o o $ o o   o o $$o %   o %   % o   % %   o o   % o   % o   % %   % o   % %   % o   % o $ o o $ o o $ o o   o o $ o o   o ",
" ooo   o%o   ooo   %o%   o%o  $ooo$  %%o$  ooo   oo%   %oo   ooo   ooo   o%o   ooo   o%%  $ooo   %%%   ooo$ $%%%$ $%%%$  ooo$ $%%%$ $%%%$  ooo% $%%%$ $%%%$  ooo   o%o   oo%$  ooo  $%oo   o%o  ",
"                                                                         $                                                                                         $                            ",
" %%%   %%%  $%%%   %%%  $%%%  $%%%$ $%%%$  %%%$ $ooo$  o$o  $%%%$ $ooo$ $ooo   %$%  $%%%   %%%  $%%%   %%%  $%%%   %%%  $%$%$ $ooo$ $ooo$ $ooo$ $ooo$ $ooo$ $%%%$ $%%o   o%o   o%%$  o%o   ooo  ",
"%   % %   % %   % %   o %   % %   o %   o %   o %   % o % o o   % %   % %   o % % % %   % %   % %   % %   % %   % %   $ o % o %   % %   % %   % %   % %   % o   % %   o o% %o o   % o$ $o o   o ",
"% $$% %   % %   % %   o %   % %   o %   o %   o %   % o % o o   % %   % %   o % % % %   % %   % %   % %   % %   % %   o o % o %   % %   % %   % $% %$ %$ $% o  %$ %   o o % o o   % %   % o   o ",
"$o%o$ $%%%$ $%%%  $ooo  $ooo$ $%%%$ $%%%  $oo%% $%%%$  o$o   ooo$ $%%%  $ooo  $o$o$ $ooo$ $ooo$ $%%%  $ooo$ $%%%   %%%   o$o  $ooo$ $ooo$ $o$o$ o%%%o o%o%o  o%o  $ooo   ooo   ooo$  ooo   ooo  ",
"% $$% %   % %   % %   o %   % %   o %   o %   % %   % o % o o   % %   % %   o % % % %   % %   % %   o % % % %   % o   % o % o %   % %   % % % % $% %$ o % o $%  o %   o o   o o   % o   o o   o ",
"%     %   % %   % %   o %   % %   o %   o %   % %   % o % o %   % %   % %   o % % % %   % %   % %   o %  %% %   % $   % o % o %   % $% %$ % % % %   % o % o %   o %   o o   o o   % o   o o   o ",
" %%%  $ooo$ $%%%   %%%  $%%%  $%%%$ $ooo   %%%  $ooo$  o$o   %%%  $ooo$ $%%%$ $o o$ $ooo$  %%%  $ooo   %%%$ $ooo$  %%%   o%o   %%%   $%$  $%$%$ $ooo$  o$o  $%%%$ $%%o   ooo   o%%$  ooo   ooo  ",
"                                                                                                                                                                                                ",
" XXX   X@X   #X#   #X#   X#X  @XXX@  ##X   XX#   XX#   #XX   XXX   XXX   XXX   XXX   XXX   XXX@  ###   XXX@ @###@ @###@ #XXX# @###@ @###@ @###@ @###@ @###@  XXX   XXX   XX#@  XXX  @#XX  @###@ ",
"X   X X # X X# #X X@ @X X@@@# #   # #  @X X  @X X @ X X @ X #   # X @ X X   X X   X X   X X   # #   # X   # X   # X   # #   # #   X #   X X   # #   # #   # X   X X   X X @ X X   X X @ X #   # ",
"X   X X # X X@ @X #@@@# #   X X  @X X@@ X X @ X X@  X X  @X X@ @X X @ X X   X X   X X   X X  @X #   # X   # X   # X   # #   # #   X #   X X   # #   # #   # X @ X X @ X X@  X #@@@# X  @X X   # ",
" XXX   X@X   XXX   #X#   ###   X#X   #XX   XXX   #XX   XX#  @###@ @###@  XXX  @###@  XXX   X#X  @XXX@  XXX@ @###@  ###@ @###@ ####@ @###@  XXX@ @###@ @###@  XXX   XXX  @XXX   XXX   XXX@  XX#@ ",
"X   X X # X X   X #@@@# X   # X@  X # @ # X   X X@  X X  @X X@ @X X @ X X   X X   X X   X X@  X #   # X   # #   X X   # X   # X   # #   # X   # #   # X   # X   X X   X X@  X #@@@# X  @X X @ X ",
"X   X X   X X   X X@ @X #@@@X #   # #  @X X   X X @ X X @ X #   # X @ X X @ X X   X X @@X #   X #   # X   # #   X X   # X   # X   # #   # X   # #   # X   # X @ X X @ X X @ X X   X X @ X X   X ",
" XXX   X#X   XXX   #X#   X#X  @XXX@  ##X@  XXX   XX#   #XX   XXX   XXX   X#X   XXX   X##  @XXX   ###   XXX@ @###@ @###@  XXX@ @###@ @###@  XXX# @###@ @###@  XXX   X#X   XX#@  XXX  @#XX   X#X  ",
"                                                                         @                                                                                         @                            ",
" ###   ###  @###   ###  @###  @###@ @###@  ###@ @XXX@  X@X  @###@ @XXX@ @XXX   #@#  @###   ###  @###   ###  @###   ###  @#@#@ @XXX@ @XXX@ @XXX@ @XXX@ @XXX@ @###@ @##X   X#X   X##@  X#X   XXX  ",
"#   # #   # #   # #   X #   # #   X #   X #   X #   # X # X X   # #   # #   X # # # #   # #   # #   # #   # #   # #   @ X # X #   # #   # #   # #   # #   # X   # #   X X# #X X   # X@ @X X   X ",
"# @@# #   # #   # #   X #   # #   X #   X #   X #   # X # X X   # #   # #   X # # # #   # #   # #   # #   # #   # #   X X # X #   # #   # #   # @# #@ #@ @# X  #@ #   X X # X X   # #   # X   X ",
"@X#X@ @###@ @###  @XXX  @XXX@ @###@ @###  @XX## @###@  X@X   XXX@ @###  @XXX  @X@X@ @XXX@ @XXX@ @###  @XXX@ @###   ###   X@X  @XXX@ @XXX@ @X@X@ X###X X#X#X  X#X  @XXX   XXX   XXX@  XXX   XXX  ",
"# @@# #   # #   # #   X #   # #   X #   X #   # #   # X # X X   # #   # #   X # # # #   # #   # #   X # # # #   # X   # X # X #   # #   # # # # @# #@ X # X @#  X #   X X   X X   # X   X X   X ",
"#     #   # #   # #   X #   # #   X #   X #   # #   # X # X #   # #   # #   X # # # #   # #   # #   X #  ## #   # @   # X # X #   # @# #@ # # # #   # X # X #   X #   X X   X X   # X   X X   X ",
" ###  @XXX@ @###   ###  @###  @###@ @XXX   ###  @XXX@  X@X   ###  @XXX@ @###@ @X X@ @XXX@  ###  @XXX   ###@ @XXX@  ###   X#X   ###   @#@  @#@#@ @XXX@  X@X  @###@ @##X   XXX   X##@  XXX   XXX  ",
"                                                                                                                                                                                                ",
" ...   .O.   +.+   +.+   .+.  O...O  ++.   ..+   ..+   +..   ...   ...   ...   ...   ...   ...O  +++   ...O O+++O O+++O +...+ O+++O O+++O O+++O O+++O O+++O  ...   ...   ..+O  ...  O+..  O+++O ",
".   . . + . .+ +. .O O. .OOO+ +   + +  O. .  O. . O . . O . +   + . O . .   . .   . .   . .   + +   + .   + .   + .   + +   + +   . +   . .   + +   + +   + .   . .   . . O . .   . . O . +   + ",
".   . . + . .O O. +OOO+ +   . .  O. .OO . . O . .O  . .  O. .O O. . O . .   . .   . .   . .  O. +   + .   + .   + .   + +   + +   . +   . .   + +   + +   + . O . . O . .O  . +OOO+ .  O. .   + ",
" ...   .O.   ...   +.+   +++   .+.   +..   ...   +..   ..+  O+++O O+++O  ...  O+++O  ...   .+.  O...O  ...O O+++O  +++O O+++O ++++O O+++O  ...O O+++O O+++O  ...   ...  O...   ...   ...O  ..+O ",
".   . . + . .   . +OOO+ .   + .O  . + O + .   . .O  . .  O. .O O. . O . .   . .   . .   . .O  . +   + .   + +   . .   + .   + .   + +   + .   + +   + .   + .   . .   . .O  . +OOO+ .  O. . O . ",
".   . .   . .   . .O O. +OOO. +   + +  O. .   . . O . . O . +   + . O . . O . .   . . OO. +   . +   + .   + +   . .   + .   + .   + +   + .   + +   + .   + . O . . O . . O . .   . . O . .   . ",
" ...   .+.   ...   +.+   .+.  O...O  ++.O  ...   ..+   +..   ...   ...   .+.   ...   .++  O...   +++   ...O O+++O O+++O  ...O O+++O O+++O  ...+ O+++O O+++O  ...   .+.   ..+O  ...  O+..   .+.  ",
"                                                                         O                                                                                         O                            ",
" +++   +++  O+++   +++  O+++  O+++O O+++O  +++O O...O  .O.  O+++O O...O O...   +O+  O+++   +++  O+++   +++  O+++   +++  O+O+O O...O O...O O...O O...O O...O O+++O O++.   .+.   .++O  .+.   ...  ",
"+   + +   + +   + +   . +   + +   . +   . +   . +   + . + . .   + +   + +   . + + + +   + +   + +   + +   + +   + +   O . + . +   + +   + +   + +   + +   + .   + +   . .+ +. .   + .O O. .   . ",
"+ OO+ +   + +   + +   . +   + +   . +   . +   . +   + . + . .   + +   + +   . + + + +   + +   + +   + +   + +   + +   . . + . +   + +   + +   + O+ +O +O O+ .  +O +   . . + . .   + +   + .   . ",
"O.+.O O+++O O+++  O...  O...O O+++O O+++  O..++ O+++O  .O.   ...O O+++  O...  O.O.O O...O O...O O+++  O...O O+++   +++   .O.  O...O O...O O.O.O .+++. .+.+.  .+.  O...   ...   ...O  ...   ...  ",
"+ OO+ +   + +   + +   . +   + +   . +   . +   + +   + . + . .   + +   + +   . + + + +   + +   + +   . + + + +   + .   + . + . +   + +   + + + + O+ +O . + . O+  . +   . .   . .   + .   . .   . ",
"+     +   + +   + +   . +   + +   . +   . +   + +   + . + . +   + +   + +   . + + + +   + +   + +   . +  ++ +   + O   + . + . +   + O+ +O + + + +   + . + . +   . +   . .   . .   + .   . .   . ",
" +++  O...O O+++   +++  O+++  O+++O O...   +++  O...O  .O.   +++  O...O O+++O O. .O O...O  +++  O...   +++O O...O  +++   .+.   +++   O+O  O+O+O O...O  .O.  O+++O O++.   ...   .++O  ...   ...  ",
"                                                                                                                                                                                          OOOOO "
};
'''


class SensorDockApp(wmdocklib.DockApp):
    """
    Discover and display values for defined in config temperatures or other
    readings using information found on /sys file system.
    """
    background_color = '#202020'
    x_offset = 4
    y_offset = 3
    font_dimentions = (6, 8)

    def __init__(self, args=None):
        super().__init__(args)
        self.font = FONT
        self.max_chars_in_line = None
        self.conf = {}
        self.critical = 0
        self.warning = 0

        self._read_config()
        self._find_sys_files()

    def _read_config(self):
        conf = os.path.join(XDG_CONF_DIR, 'pywmtemp.yaml2')
        if self.args.config:
            conf = self.args.config

        try:
            with open(conf) as fobj:
                self.conf = yaml.safe_load(fobj)
        except OSError:
            # TODO: add some logging?
            pass

    def run(self):
        self.prepare_pixmaps()
        self.max_chars_in_line = int((self.width - 2 * self.x_offset) /
                                     self.char_width)
        self.max_rows = int((self.height - 2 * self.x_offset) /
                            self.char_height)
        self.open_xwindow()

        if len(self.conf['readings']) > self.max_rows:
            print("Too many lines to fit into dockapp.")
            return

        append = True
        while self.max_rows - len(self.conf['readings']) > 0:
            if append:
                self.conf['readings'].append({'empty': 'empty'})
            else:
                self.conf['readings'].insert(0, {'empty': 'empty'})
            append = not append

        try:
            self.main_loop()
        except KeyboardInterrupt:
            pass

    def main_loop(self):

        count = 0
        while True:
            self.check_for_events()

            position = 1
            if count == 0:
                for item in self.conf['readings']:
                    self.add_string(self.get_reading(item), 1, position)
                    position += self.char_height

            count += 1
            if count >= 10:
                count = 0
            self.redraw()
            time.sleep(0.1)

    def get_reading(self, item):
        if 'fname' not in item:
            return ' ' * self.max_chars_in_line

        with open(item['fname']) as fobj:
            value = fobj.read().strip()

        if item.get('divide'):
            value = int(int(value)/int(item['divide']))
        label = item['label']
        if len(f"{label}{value}{item['unit']}") > self.max_chars_in_line:
            return 'ERRTOOLNG'

        while len(f"{label}{value}{item['unit']}") != self.max_chars_in_line:
            label += ' '

        # shift charset depending on the threshold defined in config, assuming
        # charset is the same row(s) copied with different color for warning
        # and critival.
        # FIXME: remove hardcoded multiplies in favor of automatically
        # computed factors.
        displacement = 0
        if item.get('override_warning'):
            if value >= item['override_warning']:
                displacement = int(self.charset_width / self.char_width) * 2
        if item.get('override_critical'):
            if value >= item['override_critical']:
                displacement = int(self.charset_width / self.char_width) * 4

        string = f"{label}{value}{item['unit']}".replace('°', '\\').upper()
        if displacement:
            string = ''.join([chr(ord(i) + displacement) for i in string])

        return string


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Alternate config file')
    args = parser.parse_args()

    dockapp = SensorDockApp(args)
    dockapp.run()


if __name__ == '__main__':
    main()
