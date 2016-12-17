#!/usr/bin/env python

# swaramBase - basic functions for Swaram
# Copyright (C) 2003 Baiju M
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# Author: Baiju M <baijum81@lycos.com>

import time
import os
import string
import gtk
import messageDialog

text_viewer = 'less'
html_viewer = 'lynx'
pdf_viewer = 'gv'
viewer_state = 'enable'

class swaramBase:

    def __init__(self):
        pass

    def setup_conf_files(self):
        global text_viewer
        global html_viewer
        global pdf_viewer
        global viewer_state

        if os.access('/etc/swaram.conf',os.R_OK):

            pf = open('/etc/swaram.conf', 'r')
            prefs = pf.readlines()
            pf.close()

            try:

                for line in prefs:
                    line = string.strip(line)
                    if line != '' and line[0] != '#':
                        preference, values = string.split(line, "=")
                        preference = string.strip(preference)
                        if preference == "text_viewer":
                            text_viewer = string.strip(values)
                        elif preference == "html_viewer":
                            html_viewer = string.strip(values)
                        elif preference == "pdf_viewer":
                            pdf_viewer = string.strip(values)
                        elif preference == "viewer_state":
                            viewer_state = string.strip(values)

            except:
                messageDialog.show_message_dialog("/etc/swaram.conf file correpted.")
                pass
        else:
            messageDialog.show_message_dialog("/etc/swaram.conf is not available for reading.")
            pass

        self.read_swaramrc()

    def get_text_viewer(self):
        global text_viewer
        self.read_swaramrc()
        return text_viewer

    def get_html_viewer(self):
        global html_viewer
        self.read_swaramrc()
        return html_viewer

    def get_pdf_viewer(self):
        global pdf_viewer
        self.read_swaramrc()
        return pdf_viewer

    def get_viewer_state(self):
        global viewer_state
        self.read_swaramrc()
        return viewer_state

    def get_viewers(self):
        global text_viewer, html_viewer, pdf_viewer, viewer_state
        self.read_swaramrc()
        return (text_viewer, html_viewer, pdf_viewer, viewer_state)

    def set_viewers(self, textViewer='nil', htmlViewer='nil', pdfViewer='nil', viewerState='enable'):
        global text_viewer
        global html_viewer
        global pdf_viewer
        global viewer_state

        text_viewer = textViewer
        html_viewer = htmlViewer
        pdf_viewer = pdfViewer
        viewer_state = viewerState

        settings = os.environ.get('HOME')+'/.swaramrc'

        try:
            pf = open(settings, 'r')
            self.prefs = pf.readlines()
            pf.close()

            fd = open(settings, 'w')

            for line in self.prefs:
                if line == '' or line[0] == '#':
                    fd.write(line)
                else:
                    tokens = string.split(line, '=')
                    if tokens[0] == 'text_viewer':
                        fd.write("text_viewer="+text_viewer+"\n")
                    elif tokens[0] == 'html_viewer':
                        fd.write("html_viewer="+html_viewer+"\n")
                    elif tokens[0] == 'pdf_viewer':
                        fd.write("pdf_viewer="+pdf_viewer+"\n")
                    elif tokens[0] == 'viewer_state':
                        fd.write("viewer_state="+viewer_state+"\n")
            fd.close()

        except:
            pass

    def read_swaramrc(self):

        global text_viewer
        global html_viewer
        global pdf_viewer
        global viewer_state

        swaramrc = os.environ.get('HOME')+'/.swaramrc'

        try:
            pf = open(swaramrc, 'r')
            prefs = pf.readlines()
            pf.close()
        except:
            fd = open(swaramrc,'w')
            fd.write("text_viewer=less\n")
            fd.write("html_viewer=lynx\n")
            fd.write("pdf_viewer=gv\n")
            fd.write("viewer_state=enable\n")
            fd.close()

        pf = open(swaramrc, 'r')
        prefs = pf.readlines()
        pf.close()

        try:

            for line in prefs:
                line = string.strip(line)
                if line != '' and line[0] != '#':
                    preference, values = string.split(line, "=")
                    preference = string.strip(preference)
                    if preference == "text_viewer":
                        text_viewer = string.strip(values)
                    elif preference == "html_viewer":
                        html_viewer = string.strip(values)
                    elif preference == "pdf_viewer":
                        pdf_viewer = string.strip(values)
                    elif preference == "viewer_state":
                        viewer_state = string.strip(values)

        except:
            fd = open(swaramrc,'w')
            fd.write("text_viewer=less\n")
            fd.write("html_viewer=lynx\n")
            fd.write("pdf_viewer=gv")
            fd.write("viewer_state=enable\n")
            fd.close()

    def read(self, tmp_time, no_of_lines):
        fdp1 = os.popen4("ls x* > tmp_files;for i in `cat tmp_files`;do nt2w -o $i.wav $i;done")

        fd = open('/tmp/'+tmp_time+'/xaaa','r')
        lines=fd.readlines()
        fd.close()
        
        total_chars = 0
        for line in lines:
            total_chars = len(line)+total_chars

	if total_chars < (((no_of_lines - 1)/2)*75):
            time.sleep(no_of_lines*5)

        i = 0
        while i < 61:
            time.sleep(5)
            if os.access('/tmp/'+tmp_time+'/xaaa.wav', os.F_OK):
                fdp2 = os.popen4("for i in `cat tmp_files`;do play $i.wav;done")
                break
            elif i == 60:
                print "Sorry! Your system is too slow"
                break
            else:
                i = i + 1

    def split_lines(self,length):
        for i in range(5,50,2):
            if length < ((26**3)*i):
		os.system('split --lines='+str(i)+' --suffix-length=3 new_file.txt')
                return i
                break

    def open_viewer(self, viewer, file, man='no', info='no'):
        if viewer == 'nil':
            pass
        elif viewer == "less":
            os.spawnlp(os.P_NOWAIT, 'xterm','xterm','-e','less',file)
        elif viewer == "lynx":
            os.spawnlp(os.P_NOWAIT, 'xterm','xterm','-e','lynx',file)
        elif viewer == "links":
            os.spawnlp(os.P_NOWAIT, 'xterm','xterm','-e','links',file)
        else:
            try:
                os.spawnlp(os.P_NOWAIT, viewer, viewer, file)
            except:
                messageDialog.show_message_dialog(viewer+" is not supported.")
                pass
