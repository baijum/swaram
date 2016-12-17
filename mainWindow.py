#!/usr/bin/env python

# mainWindow - main interface window for Swaram
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

import signal
import gtk
import gobject
import gtk.glade
import gnome.ui
import string
import sys
import time
import os
import re

import swaramBase
import prefWindow
import messageDialog

swaramBaseConfigure = swaramBase.swaramBase()
swaramBaseConfigure.setup_conf_files()

home = os.environ.get('HOME')
if not os.access(home+'/.swaram', os.F_OK):
    os.mkdir(home+'/.swaram',0755)
swaram_dir = home+'/.swaram'
tmp_time = time.ctime()
man_state = 0

domain = "swaram"

if os.access("swaram.glade", os.F_OK):
    xml = gtk.glade.XML ("./swaram.glade", domain=domain)
else:
    xml = gtk.glade.XML ("/usr/share/swaram/swaram.glade", domain=domain)

if os.access("VERSION", os.F_OK):
    version_file = "./VERSION"
else:
    version_file = '/usr/share/swaram/VERSION'

fd = open(version_file,'r')
VERSION = fd.readline()
fd.close()

class mainWindow:

    def version():
        global VERSION
        return VERSION
    
    def destroy(self, *args):
        self.on_file_stop_button_clicked()
        gtk.mainquit()

    def __init__(self):
        self.toplevel = xml.get_widget ('mainWindow')
        self.notebook = xml.get_widget('notebook1')
        self.text_read_button = xml.get_widget("text_read_button")
        self.text_close_button = xml.get_widget("text_close_button")
        self.file_read_button = xml.get_widget("file_read_button")
        self.file_save_button = xml.get_widget("file_save_button")
        self.file_pause_button = xml.get_widget("file_pause_button")
        self.file_stop_button = xml.get_widget("file_stop_button")
        self.file_close_button = xml.get_widget("file_close_button")
        self.file_about_button = xml.get_widget("file_about_button")
        self.man_read_button = xml.get_widget("man_read_button")
        self.man_stop_button = xml.get_widget("man_stop_button")
        self.man_close_button = xml.get_widget("man_close_button")
        self.man_about_button = xml.get_widget("man_about_button")
        self.textEntryToRead = xml.get_widget('textEntryToRead')
        self.fileEntryToRead = xml.get_widget('fileEntryToRead')
        self.manEntryToRead = xml.get_widget('manEntryToRead')

        self.toplevel.connect("destroy", self.destroy)

        self.prefWin = prefWindow.prefWindow(self,xml)

        self.toplevel.show_all ()

        xml.signal_connect("on_text_read_button_clicked", self.on_text_read_button_clicked)
        xml.signal_connect("on_text_close_button_clicked", self.on_text_close_button_clicked)
        xml.signal_connect("on_file_read_button_clicked", self.on_file_read_button_clicked)
        xml.signal_connect("on_file_save_button_clicked", self.on_file_save_button_clicked)
        xml.signal_connect("on_file_pause_button_clicked", self.on_file_pause_button_clicked)
        xml.signal_connect("on_file_stop_button_clicked", self.on_file_stop_button_clicked)
        xml.signal_connect("on_file_close_button_clicked", self.on_text_close_button_clicked)
        xml.signal_connect("on_file_about_button_clicked", self.on_file_about_button_clicked)
        xml.signal_connect("on_file_pref_button_clicked", self.on_file_pref_button_clicked)
        xml.signal_connect("on_man_read_button_clicked", self.on_man_read_button_clicked)
        xml.signal_connect("on_man_stop_button_clicked", self.on_file_stop_button_clicked)
        xml.signal_connect("on_man_close_button_clicked", self.on_text_close_button_clicked)
        xml.signal_connect("on_man_about_button_clicked", self.on_file_about_button_clicked)
        xml.signal_connect("on_man_pref_button_clicked", self.on_file_pref_button_clicked)
        xml.signal_connect("on_man_rbutton_toggled", self.on_manual_toggled)
        xml.signal_connect("on_info_rbutton_toggled", self.on_manual_toggled)
        xml.signal_connect("on_exit_activate", self.on_exit_activate)

        gtk.mainloop()

    def on_text_read_button_clicked(self, *args):
        self.on_file_stop_button_clicked()
        text = self.textEntryToRead.get_text()
        print "You are asked to read :" , text
        f=open(swaram_dir+'/gf','w')
        f.write(text)
        f.close()
        os.system('nt2w -o '+swaram_dir+'/gf.wav '+swaram_dir+'/gf')
        os.system('play '+swaram_dir+'/gf.wav')

    def on_text_close_button_clicked(self, *args):
        self.on_file_stop_button_clicked()
        gtk.mainquit()

    def on_file_read_button_clicked(self, *args):
        self.on_file_stop_button_clicked()
        global tmp_time

        file = self.fileEntryToRead.get_text()
        if os.access('/tmp/',3) == 0 :
            messageDialog.show_message_dialog("Sorry! you don't have write access to /tmp/ directory")
            gtk.mainquit()
        print "You are asked to read :" , file
        tmp_time = time.ctime()

        os.mkdir('/tmp/'+tmp_time,0744)
        os.chdir('/tmp/'+tmp_time)

        fto = 'fto'
        ftt = 'ftt'

        try:
            file_type_one = re.search('(?<=\.)htm', file)
            fto = file_type_one.group(0)
        except:
            pass

        try:
            file_type_two = re.search('(?<=\.)pdf', file)
            ftt = file_type_two.group(0)
        except:
            pass

        viewer_state = swaramBaseConfigure.get_viewer_state()

        try:
            if fto == 'htm':
                viewer = swaramBaseConfigure.get_html_viewer()
                if viewer_state == 'disable':
                    viewer = 'nil'
                os.spawnlp(os.P_WAIT, 'cp', 'cp', file, '/tmp/'+tmp_time+'/new_file.html')
                fd = os.popen('lynx -nolist -dump new_file.html > new_file.txt.tmp')
                fd.close()
            elif ftt == 'pdf':
                viewer = swaramBaseConfigure.get_pdf_viewer()
                if viewer_state == 'disable':
                    viewer = 'nil'
                os.spawnlp(os.P_WAIT, 'cp', 'cp', file, '/tmp/'+tmp_time+'/new_file.pdf')
                ##FIXME: .tmp extension, any problem?
                os.spawnlp(os.P_WAIT, 'pdftotext', 'pdftotext', 'new_file.pdf', 'new_file.txt.tmp')
            else:
                viewer = swaramBaseConfigure.get_text_viewer()
                if viewer_state == 'disable':
                    viewer = 'nil'
                os.spawnlp(os.P_WAIT, 'cp', 'cp', file, '/tmp/'+tmp_time+'/new_file.txt.tmp')
        except:
            pass

        fd = os.popen('fmt new_file.txt.tmp > new_file.txt.tmp2')
        fd.close()
        swaramBaseConfigure.open_viewer(viewer, file)
        self.read_text_file()

    def on_file_save_button_clicked(self, *args):
        print "file_save_button_clicked"

    def on_file_pause_button_clicked(self, *args):
        print "file_pause_button_clicked"

    def on_file_stop_button_clicked(self, *args):
        global tmp_time
        os.spawnlp(os.P_WAIT, 'killall', 'killall', '-q9', 'festival')
        os.spawnlp(os.P_WAIT, 'killall', 'killall', '-q9', 'sox')
        os.spawnlp(os.P_WAIT, 'rm', 'rm', '-rf', '/tmp/'+tmp_time)

    def on_file_about_button_clicked(self, *args):
        global VERSION
        dlg = gnome.ui.About("Swaram",
                             VERSION,
                             "Copyright 2003 Baiju M <baijum81@lycos.com>",
                             "Swaram is a frontend for 'festival'\n"
                             "Swaram is licensed under GNU GPL\n"
                             "Please see the COPYING file with the source",
                             ())
        dlg.run()
	dlg.destroy()

    def on_man_read_button_clicked(self, *args):
        self.on_file_stop_button_clicked()
        global tmp_time,man_state

        viewer_state = swaramBaseConfigure.get_viewer_state()
	viewer = swaramBaseConfigure.get_text_viewer()
        if viewer_state == 'disable':
            viewer = 'nil'

        man  = self.manEntryToRead.get_text()
        if os.access('/tmp/',3) == 0 :
            messageDialog.show_message_dialog("Sorry! you don't have write access to /tmp/ directory")
            gtk.mainquit()

        print "You are asked to read :" , man
        tmp_time = time.ctime()
        os.mkdir('/tmp/'+tmp_time,0744)
        os.chdir('/tmp/'+tmp_time)
        if man_state == 1:
            fd = os.popen('info '+str(man)+' > new_file.txt.tmp')
            fd.close()
            swaramBaseConfigure.open_viewer(viewer,'new_file.txt.tmp')
            self.read_text_file()
        elif man_state == 0:
            fd = os.popen('man '+str(man)+' | col -bx > new_file.txt.tmp')
            fd.close()
            swaramBaseConfigure.open_viewer(viewer,'new_file.txt.tmp')
            self.read_text_file()

    def on_manual_toggled(self, *args):
        global man_state
        if xml.get_widget ('man_rbutton').get_active():
            man_state = 0 
        elif xml.get_widget ('info_rbutton').get_active():
            man_state = 1

    def on_file_pref_button_clicked(self, *args):
        self.prefWin.newPrefWin()

    def on_exit_activate(self, *args):
        self.destroy()

    def read_text_file(self, *args):
        global tmp_time
        fd = os.popen('fmt new_file.txt.tmp > new_file.txt.tmp2')
        fd.close()
        fd = open('new_file.txt.tmp2','r')
        lines = fd.readlines()
        fd.close()

        fd=open('new_file.txt','w')
        for i in range(len(lines)):
            if lines[i] != '\n':
                if lines[i-1] == '\n' and i != 0:
                    fd.write('\n'+lines[i])
                else:
                    fd.write(lines[i])
        fd.close()

        fd = open('new_file.txt','r')
        lines = fd.readlines()
        length = len(lines)
        fd.close()

        no_of_lines = swaramBaseConfigure.split_lines(length)

        swaramBaseConfigure.read(tmp_time, no_of_lines)
