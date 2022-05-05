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
BACKGROUND = '''\
/* XPM */
static char *ui[] = {
/* columns rows colors chars-per-pixel */
"66 64 6 1 ",
"  c None",
". c black",
"X c #202020",
"o c #004941",
"O c #007D71",
"+ c gray78",
/* pixels */
"                                                                  ",
"                                                                  ",
"  ............................................................    ",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+    ",
"  .XXoooXXXoooXXXoooXXXoooXXXXXXoooXXXoooXXXoooXXXoooXXXoooXX+    ",
"  .XoXXXoXoXXXoXoXXXoXoXXXoXXXXoXXXoXoXXXoXoXXXoXoXXXoXoXXXoX+    ",
"  .XoXXXoXoXXXoXoXXXoXoXXXoXXXXoXXXoXoXXXoXoXXXoXoXXXoXoXXXoX+    ",
"  .XXoooXXXoooXXXoooXXXoooXXXXXXoooXXXoooXXXoooXXXoooXXXoooXX+    ",
"  .XoXXXoXoXXXoXoXXXoXoXXXoXXXXoXXXoXoXXXoXoXXXoXoXXXoXoXXXoX+    ",
"  .XoXXXoXoXXXoXoXXXoXoXXXoXXXXoXXXoXoXXXoXoXXXoXoXXXoXoXXXoX+    ",
"  .XXoooXXXoooXXXoooXXXoooXXXXXXoooXXXoooXXXoooXXXoooXXXoooXX+    ",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+    ",
"  .XXoooXXXoooXXXoooXXXoooXXXXXXoooXXXoooXXXoooXXXoooXXXoooXX+    ",
"  .XoXXXoXoXXXoXoXXXoXoXXXoXXXXoXXXoXoXXXoXoXXXoXoXXXoXoXXXoX+    ",
"  .XoXXXoXoXXXoXoXXXoXoXXXoXXXXoXXXoXoXXXoXoXXXoXoXXXoXoXXXoX+    ",
"  .XXoooXXXoooXXXoooXXXoooXXXXXXoooXXXoooXXXoooXXXoooXXXoooXX+    ",
"  .XoXXXoXoXXXoXoXXXoXoXXXoXXXXoXXXoXoXXXoXoXXXoXoXXXoXoXXXoX+    ",
"  .XoXXXoXoXXXoXoXXXoXoXXXoXXXXoXXXoXoXXXoXoXXXoXoXXXoXoXXXoX+    ",
"  .XXoooXXXoooXXXoooXXXoooXXXXXXoooXXXoooXXXoooXXXoooXXXoooXX+    ",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+    ",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+    ",
"  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    ",
"                                                                  ",
"                                                                  ",
"  ............................................................    ",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  .XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX+  XO",
"  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    ",
"                                                                  ",
"                                                                  "
};
'''
FONT = '''\
/* XPM */
static char *_x8_lcd[] = {
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
    graph_width = 58
    graph_max_height = 36
    graph_coords = (3, 25)

    def __init__(self, args=None):
        super().__init__(args)
        self.fonts = [wmdocklib.BitmapFonts(FONT, (6, 8))]
        self.background = BACKGROUND
        self.conf = {}
        self.critical = 0
        self.warning = 0
        self._history = {}
        self._read_config()
        self._current_graph = ''
        if list(self._history.keys()):
            self._current_graph = list(self._history.keys())[0]
        helpers.add_mouse_region(0, self.graph_coords[0], self.graph_coords[1],
                                 width=self.graph_width,
                                 height=self.graph_max_height)

    def run(self):
        self.prepare_pixmaps()
        self.open_xwindow()
        try:
            self.main_loop()
        except KeyboardInterrupt:
            pass

    def main_loop(self):

        count = 0
        while True:
            if self._on_event(self.check_for_events()):
                count = 0

            position = 1
            if count == 0:
                # suport up to two reading. all surplus entries will be
                # ignored.
                for item in self.conf.get('readings', [])[:2]:
                    self._put_string(item, position)
                    position += self.fonts[0].height
                self._draw_graph()
                self._draw_graph_label()

            count += 1
            if count >= 10:
                count = 0
            self.redraw()
            time.sleep(0.1)

    def get_reading(self, item):

        if not self.conf:
            return ' ', 0

        temp = None
        temps = psutil.sensors_temperatures()
        for shw in temps.get(item.get('sensor'), []):
            if shw.label == item.get('label'):
                temp = shw
                break

        value = int(temp.current)
        name = item.get('name')
        self._history[name] = self._history[name][1:]
        self._history[name].append(value)
        charset_width = self.fonts[0].charset_width
        char_width = self.fonts[0].width

        # shift charset depending on the threshold defined in config, assuming
        # charset is the same row(s) copied with different color for warning
        # and critival.
        # FIXME: remove hardcoded multiplies in favor of automatically
        # computed factors.
        displacement = 0
        if item.get('override_warning') and value >= item['override_warning']:
            displacement = int(charset_width / char_width) * 2
        elif temp.high and value >= temp.high:
            displacement = int(charset_width / char_width) * 2

        if (item.get('override_critical') and
                value >= item['override_critical']):
            displacement = int(charset_width / char_width) * 4
        elif temp.critical and value >= temp.critical:
            displacement = int(charset_width / char_width) * 4

        if (len(str(value)) - len(item.get('unit', ''))) <= 5:
            value = (f'{value:{5 - len(item.get("unit", ""))}}'
                     f'{item.get("unit", "")}')
        else:
            value = f'{value:5}'

        string = f"{value}".replace('°', '\\').upper()

        if displacement:
            string = ''.join([chr(ord(i) + displacement) for i in string])

        return string, displacement

    def _switch_graph(self):
        for key in self._history:
            if key != self._current_graph:
                self._current_graph = key
                break

    def _read_config(self):
        conf = os.path.join(XDG_CONF_DIR, 'pywmtemp.yaml')
        if self.args.config:
            conf = self.args.config

        try:
            with open(conf) as fobj:
                self.conf = yaml.safe_load(fobj)
        except OSError:
            # TODO: add some logging?
            pass

        for item in self.conf.get('readings', [])[:2]:
            self._history[item.get('name')] = [0 for _ in
                                               range(self.graph_width)]

    def _on_event(self, event):
        if not event:
            return

        if event.get('type') == 'buttonrelease' and event.get('button') == 1:
            x = event.get('x', 0)
            y = event.get('y', 0)
            if helpers.check_mouse_region(x, y) > -1:
                self._switch_graph()
            return True

    def _draw_graph(self):
        if not self._current_graph:
            return

        for count, item in enumerate(self._history[self._current_graph]):
            height = int((item/100) * self.graph_max_height)
            helpers.copy_xpm_area(65, self.graph_coords[1],
                                  1, self.graph_max_height,
                                  self.graph_coords[0] + count,
                                  self.graph_coords[1])
            helpers.copy_xpm_area(64, self.graph_coords[1],
                                  1, self.graph_max_height - height,
                                  self.graph_coords[0] + count,
                                  self.graph_coords[1])

    def _put_string(self, item, position):
        temp, displacement = self.get_reading(item)
        name = item.get('name', '').upper()
        name = f'{name[:4]:4}'
        if displacement:
            name = ''.join([chr(ord(i) + displacement)
                            for i in name])

        self.fonts[0].add_string(name, 1, position)
        self.fonts[0].add_string(temp[:5], 28, position)

    def _draw_graph_label(self):
        name = self._current_graph.upper()
        name = name[:4]
        # ugly as hell 1 pixel border for the upper and left side of the label
        helpers.copy_xpm_area(1, 65,
                              len(name) * self.fonts[0].width + 1, 1,
                              4, 51)
        helpers.copy_xpm_area(1, 65,
                              1, self.fonts[0].height + 1,
                              4, 51)
        self.fonts[0].add_string(name, 2, 49)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Alternate config file')
    args = parser.parse_args()

    dockapp = SensorDockApp(args)
    dockapp.run()


if __name__ == '__main__':
    main()
