#!/usr/bin/env python
"""
Simple dockapp
"""
import argparse
import os
import re
import sys
import time

import wmdocklib
from wmdocklib import helpers
from wmdocklib import pywmgeneral
import yaml


XDG_CONF_DIR = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
# expected bitmap contained font should be found in the same location as main
# program
FONT = '''\
/* XPM */
static char *_x8_lcd[] = {
/* columns rows colors chars-per-pixel */
"192 48 10 1 ",
"  c #202020",
". c #440000",
"X c #542A00",
"o c #004941",
"O c #007D71",
"+ c #920000",
"@ c #E00000",
"# c #A85500",
"$ c #FF8200",
"% c #20B6AE",
/* pixels */
" ooo   oOo   %o%   %o%   o%o  OoooO  %%o   oo%   oo%   %oo   ooo   ooo   ooo   ooo   ooo   oooO  %%%   oooO O%%%O O%%%O %ooo% O%%%O O%%%O O%%%O O%%%O O%%%O  ooo   ooo   oo%O  ooo  O%oo  O%%%O ",
"o   o o % o o% %o oO Oo oOOO% %   % %  Oo o  Oo o O o o O o %   % o O o o   o o   o o   o o   % %   % o   % o   % o   % %   % %   o %   o o   % %   % %   % o   o o   o o O o o   o o O o %   % ",
"o   o o % o oO Oo %OOO% %   o o  Oo oOO o o O o oO  o o  Oo oO Oo o O o o   o o   o o   o o  Oo %   % o   % o   % o   % %   % %   o %   o o   % %   % %   % o O o o O o oO  o %OOO% o  Oo o   % ",
" ooo   oOo   ooo   %o%   %%%   o%o   %oo   ooo   %oo   oo%  O%%%O O%%%O  ooo  O%%%O  ooo   o%o  OoooO  oooO O%%%O  %%%O O%%%O %%%%O O%%%O  oooO O%%%O O%%%O  ooo   ooo  Oooo   ooo   oooO  oo%O ",
"o   o o % o o   o %OOO% o   % oO  o % O % o   o oO  o o  Oo oO Oo o O o o   o o   o o   o oO  o %   % o   % %   o o   % o   % o   % %   % o   % %   % o   % o   o o   o oO  o %OOO% o  Oo o O o ",
"o   o o   o o   o oO Oo %OOOo %   % %  Oo o   o o O o o O o %   % o O o o O o o   o o OOo %   o %   % o   % %   o o   % o   % o   % %   % o   % %   % o   % o O o o O o o O o o   o o O o o   o ",
" ooo   o%o   ooo   %o%   o%o  OoooO  %%oO  ooo   oo%   %oo   ooo   ooo   o%o   ooo   o%%  Oooo   %%%   oooO O%%%O O%%%O  oooO O%%%O O%%%O  ooo% O%%%O O%%%O  ooo   o%o   oo%O  ooo  O%oo   o%o  ",
"                                                                         O                                                                                         O                            ",
" %%%   %%%  O%%%   %%%  O%%%  O%%%O O%%%O  %%%O OoooO  oOo  O%%%O OoooO Oooo   %O%  O%%%   %%%  O%%%   %%%  O%%%   %%%  O%O%O OoooO OoooO OoooO OoooO OoooO O%%%O O%%o   o%o   o%%O  o%o   ooo  ",
"%   % %   % %   % %   o %   % %   o %   o %   o %   % o % o o   % %   % %   o % % % %   % %   % %   % %   % %   % %   O o % o %   % %   % %   % %   % %   % o   % %   o o% %o o   % oO Oo o   o ",
"% OO% %   % %   % %   o %   % %   o %   o %   o %   % o % o o   % %   % %   o % % % %   % %   % %   % %   % %   % %   o o % o %   % %   % %   % O% %O %O O% o  %O %   o o % o o   % %   % o   o ",
"Oo%oO O%%%O O%%%  Oooo  OoooO O%%%O O%%%  Ooo%% O%%%O  oOo   oooO O%%%  Oooo  OoOoO OoooO OoooO O%%%  OoooO O%%%   %%%   oOo  OoooO OoooO OoOoO o%%%o o%o%o  o%o  Oooo   ooo   oooO  ooo   ooo  ",
"% OO% %   % %   % %   o %   % %   o %   o %   % %   % o % o o   % %   % %   o % % % %   % %   % %   o % % % %   % o   % o % o %   % %   % % % % O% %O o % o O%  o %   o o   o o   % o   o o   o ",
"%     %   % %   % %   o %   % %   o %   o %   % %   % o % o %   % %   % %   o % % % %   % %   % %   o %  %% %   % O   % o % o %   % O% %O % % % %   % o % o %   o %   o o   o o   % o   o o   o ",
" %%%  OoooO O%%%   %%%  O%%%  O%%%O Oooo   %%%  OoooO  oOo   %%%  OoooO O%%%O Oo oO OoooO  %%%  Oooo   %%%O OoooO  %%%   o%o   %%%   O%O  O%O%O OoooO  oOo  O%%%O O%%o   ooo   o%%O  ooo   ooo  ",
"                                                                                                                                                                                                ",
" XXX   X#X   $X$   $X$   X$X  #XXX#  $$X   XX$   XX$   $XX   XXX   XXX   XXX   XXX   XXX   XXX#  $$$   XXX# #$$$# #$$$# $XXX$ #$$$# #$$$# #$$$# #$$$# #$$$#  XXX   XXX   XX$#  XXX  #$XX  #$$$# ",
"X   X X $ X X$ $X X# #X X###$ $   $ $  #X X  #X X # X X # X $   $ X # X X   X X   X X   X X   $ $   $ X   $ X   $ X   $ $   $ $   X $   X X   $ $   $ $   $ X   X X   X X # X X   X X # X $   $ ",
"X   X X $ X X# #X $###$ $   X X  #X X## X X # X X#  X X  #X X# #X X # X X   X X   X X   X X  #X $   $ X   $ X   $ X   $ $   $ $   X $   X X   $ $   $ $   $ X # X X # X X#  X $###$ X  #X X   $ ",
" XXX   X#X   XXX   $X$   $$$   X$X   $XX   XXX   $XX   XX$  #$$$# #$$$#  XXX  #$$$#  XXX   X$X  #XXX#  XXX# #$$$#  $$$# #$$$# $$$$# #$$$#  XXX# #$$$# #$$$#  XXX   XXX  #XXX   XXX   XXX#  XX$# ",
"X   X X $ X X   X $###$ X   $ X#  X $ # $ X   X X#  X X  #X X# #X X # X X   X X   X X   X X#  X $   $ X   $ $   X X   $ X   $ X   $ $   $ X   $ $   $ X   $ X   X X   X X#  X $###$ X  #X X # X ",
"X   X X   X X   X X# #X $###X $   $ $  #X X   X X # X X # X $   $ X # X X # X X   X X ##X $   X $   $ X   $ $   X X   $ X   $ X   $ $   $ X   $ $   $ X   $ X # X X # X X # X X   X X # X X   X ",
" XXX   X$X   XXX   $X$   X$X  #XXX#  $$X#  XXX   XX$   $XX   XXX   XXX   X$X   XXX   X$$  #XXX   $$$   XXX# #$$$# #$$$#  XXX# #$$$# #$$$#  XXX$ #$$$# #$$$#  XXX   X$X   XX$#  XXX  #$XX   X$X  ",
"                                                                         #                                                                                         #                            ",
" $$$   $$$  #$$$   $$$  #$$$  #$$$# #$$$#  $$$# #XXX#  X#X  #$$$# #XXX# #XXX   $#$  #$$$   $$$  #$$$   $$$  #$$$   $$$  #$#$# #XXX# #XXX# #XXX# #XXX# #XXX# #$$$# #$$X   X$X   X$$#  X$X   XXX  ",
"$   $ $   $ $   $ $   X $   $ $   X $   X $   X $   $ X $ X X   $ $   $ $   X $ $ $ $   $ $   $ $   $ $   $ $   $ $   # X $ X $   $ $   $ $   $ $   $ $   $ X   $ $   X X$ $X X   $ X# #X X   X ",
"$ ##$ $   $ $   $ $   X $   $ $   X $   X $   X $   $ X $ X X   $ $   $ $   X $ $ $ $   $ $   $ $   $ $   $ $   $ $   X X $ X $   $ $   $ $   $ #$ $# $# #$ X  $# $   X X $ X X   $ $   $ X   X ",
"#X$X# #$$$# #$$$  #XXX  #XXX# #$$$# #$$$  #XX$$ #$$$#  X#X   XXX# #$$$  #XXX  #X#X# #XXX# #XXX# #$$$  #XXX# #$$$   $$$   X#X  #XXX# #XXX# #X#X# X$$$X X$X$X  X$X  #XXX   XXX   XXX#  XXX   XXX  ",
"$ ##$ $   $ $   $ $   X $   $ $   X $   X $   $ $   $ X $ X X   $ $   $ $   X $ $ $ $   $ $   $ $   X $ $ $ $   $ X   $ X $ X $   $ $   $ $ $ $ #$ $# X $ X #$  X $   X X   X X   $ X   X X   X ",
"$     $   $ $   $ $   X $   $ $   X $   X $   $ $   $ X $ X $   $ $   $ $   X $ $ $ $   $ $   $ $   X $  $$ $   $ #   $ X $ X $   $ #$ $# $ $ $ $   $ X $ X $   X $   X X   X X   $ X   X X   X ",
" $$$  #XXX# #$$$   $$$  #$$$  #$$$# #XXX   $$$  #XXX#  X#X   $$$  #XXX# #$$$# #X X# #XXX#  $$$  #XXX   $$$# #XXX#  $$$   X$X   $$$   #$#  #$#$# #XXX#  X#X  #$$$# #$$X   XXX   X$$#  XXX   XXX  ",
"                                                                                                                                                                                                ",
" ...   .+.   @.@   @.@   .@.  +...+  @@.   ..@   ..@   @..   ...   ...   ...   ...   ...   ...+  @@@   ...+ +@@@+ +@@@+ @...@ +@@@+ +@@@+ +@@@+ +@@@+ +@@@+  ...   ...   ..@+  ...  +@..  +@@@+ ",
".   . . @ . .@ @. .+ +. .+++@ @   @ @  +. .  +. . + . . + . @   @ . + . .   . .   . .   . .   @ @   @ .   @ .   @ .   @ @   @ @   . @   . .   @ @   @ @   @ .   . .   . . + . .   . . + . @   @ ",
".   . . @ . .+ +. @+++@ @   . .  +. .++ . . + . .+  . .  +. .+ +. . + . .   . .   . .   . .  +. @   @ .   @ .   @ .   @ @   @ @   . @   . .   @ @   @ @   @ . + . . + . .+  . @+++@ .  +. .   @ ",
" ...   .+.   ...   @.@   @@@   .@.   @..   ...   @..   ..@  +@@@+ +@@@+  ...  +@@@+  ...   .@.  +...+  ...+ +@@@+  @@@+ +@@@+ @@@@+ +@@@+  ...+ +@@@+ +@@@+  ...   ...  +...   ...   ...+  ..@+ ",
".   . . @ . .   . @+++@ .   @ .+  . @ + @ .   . .+  . .  +. .+ +. . + . .   . .   . .   . .+  . @   @ .   @ @   . .   @ .   @ .   @ @   @ .   @ @   @ .   @ .   . .   . .+  . @+++@ .  +. . + . ",
".   . .   . .   . .+ +. @+++. @   @ @  +. .   . . + . . + . @   @ . + . . + . .   . . ++. @   . @   @ .   @ @   . .   @ .   @ .   @ @   @ .   @ @   @ .   @ . + . . + . . + . .   . . + . .   . ",
" ...   .@.   ...   @.@   .@.  +...+  @@.+  ...   ..@   @..   ...   ...   .@.   ...   .@@  +...   @@@   ...+ +@@@+ +@@@+  ...+ +@@@+ +@@@+  ...@ +@@@+ +@@@+  ...   .@.   ..@+  ...  +@..   .@.  ",
"                                                                         +                                                                                         +                            ",
" @@@   @@@  +@@@   @@@  +@@@  +@@@+ +@@@+  @@@+ +...+  .+.  +@@@+ +...+ +...   @+@  +@@@   @@@  +@@@   @@@  +@@@   @@@  +@+@+ +...+ +...+ +...+ +...+ +...+ +@@@+ +@@.   .@.   .@@+  .@.   ...  ",
"@   @ @   @ @   @ @   . @   @ @   . @   . @   . @   @ . @ . .   @ @   @ @   . @ @ @ @   @ @   @ @   @ @   @ @   @ @   + . @ . @   @ @   @ @   @ @   @ @   @ .   @ @   . .@ @. .   @ .+ +. .   . ",
"@ ++@ @   @ @   @ @   . @   @ @   . @   . @   . @   @ . @ . .   @ @   @ @   . @ @ @ @   @ @   @ @   @ @   @ @   @ @   . . @ . @   @ @   @ @   @ +@ @+ @+ +@ .  @+ @   . . @ . .   @ @   @ .   . ",
"+.@.+ +@@@+ +@@@  +...  +...+ +@@@+ +@@@  +..@@ +@@@+  .+.   ...+ +@@@  +...  +.+.+ +...+ +...+ +@@@  +...+ +@@@   @@@   .+.  +...+ +...+ +.+.+ .@@@. .@.@.  .@.  +...   ...   ...+  ...   ...  ",
"@ ++@ @   @ @   @ @   . @   @ @   . @   . @   @ @   @ . @ . .   @ @   @ @   . @ @ @ @   @ @   @ @   . @ @ @ @   @ .   @ . @ . @   @ @   @ @ @ @ +@ @+ . @ . +@  . @   . .   . .   @ .   . .   . ",
"@     @   @ @   @ @   . @   @ @   . @   . @   @ @   @ . @ . @   @ @   @ @   . @ @ @ @   @ @   @ @   . @  @@ @   @ +   @ . @ . @   @ +@ @+ @ @ @ @   @ . @ . @   . @   . .   . .   @ .   . .   . ",
" @@@  +...+ +@@@   @@@  +@@@  +@@@+ +...   @@@  +...+  .+.   @@@  +...+ +@@@+ +. .+ +...+  @@@  +...   @@@+ +...+  @@@   .@.   @@@   +@+  +@+@+ +...+  .+.  +@@@+ +@@.   ...   .@@+  ...   ...  ",
"                                                                                                                                                                                          +++++ "
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
        conf = os.path.join(XDG_CONF_DIR, 'pywmtemp.yaml')
        if self.args.config:
            conf = self.args.config

        with open(conf) as fobj:
            self.conf = yaml.safe_load(fobj)

    def _find_sys_files(self):
        for root, dirs, files in os.walk('/sys/devices'):
            for fname in files:
                match = re.match(r'^temp(?P<n>\d)_label', fname)
                if not match:
                    continue
                with open(os.path.join(root, fname)) as fobj:
                    sys_label = fobj.read().strip()
                    for item in self.conf['readings']:
                        if item.get('find_sys_label') == sys_label:
                            item['fname'] = os.path.join(root,
                                                         f'temp{match["n"]}_'
                                                         f'input')

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

        while True:
            self.check_for_events()
            position = 1
            for item in self.conf['readings']:
                self.add_string(self.get_reading(item), 1, position)
                position += self.char_height
            while position < self.max_rows * self.char_height:
                self.add_string(' ' * self.max_chars_in_line, 1, position)
                position += self.char_height
            pywmgeneral.put_pixel(32, 32, int('ffff88', 16))
            pywmgeneral.put_pixel(33, 33, int('ffff88', 16))
            pywmgeneral.put_pixel(32, 33, int('ffff88', 16))
            pywmgeneral.put_pixel(33, 32, int('ffff88', 16))
            self.redraw()
            time.sleep(0.5)

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
