#!/usr/bin/env python

# mainWindow - preference window interface for Swaram
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

import os
import string
import gtk

import mainWindow
import swaramBase

class prefWindow:
	def __init__(self, parent, xml):
		self.parent = parent

		self.prefWin = xml.get_widget('prefWindow')
 		self.prefWin.connect("delete-event", self.on_pref_close_button_clicked)
		self.prefWin.set_position(gtk.WIN_POS_CENTER)
		self.pref_cbutton=xml.get_widget('pref_cbutton')
		self.pref_close_button = xml.get_widget('pref_close_button')
		self.table1 = xml.get_widget('table1')
		self.textViewer = xml.get_widget('textViewerEntry')
		self.htmlViewer = xml.get_widget('htmlViewerEntry')
		self.pdfViewer = xml.get_widget('pdfViewerEntry')

		xml.signal_connect("on_pref_close_button_clicked", self.on_pref_close_button_clicked)
		xml.signal_connect("on_pref_cbutton_toggled", self.on_pref_cbutton_toggled)

	def busy(self):
		self.prefWin.set_sensitive(gtk.FALSE)
		self.prefWin.window.set_cursor(busy_cursor)

	def newPrefWin(self):
		swaramBaseConfigure = swaramBase.swaramBase()
		(text_viewer, html_viewer, pdf_viewer, viewer_state) = swaramBaseConfigure.get_viewers()
		self.textViewer.set_text(text_viewer)
		self.htmlViewer.set_text(html_viewer)
		self.pdfViewer.set_text(pdf_viewer)
		if viewer_state == 'enable':
			self.pref_cbutton.set_active(gtk.TRUE)
		else:
			self.pref_cbutton.set_active(gtk.FALSE)
		self.prefWin.show_all()

	def on_pref_close_button_clicked(self, *args):
		swaramBaseConfigure = swaramBase.swaramBase()

		textViewer = self.textViewer.get_text()
		htmlViewer = self.htmlViewer.get_text()
		pdfViewer = self.pdfViewer.get_text()

		if self.pref_cbutton.get_active() == gtk.TRUE:
			viewerState = 'enable'
		else:
			viewerState = 'disable'

		swaramBaseConfigure.set_viewers(textViewer,htmlViewer,pdfViewer,viewerState)

		self.prefWin.hide()
		return gtk.TRUE
	
	def on_pref_cbutton_toggled(self, *args):
		self.table1.set_sensitive(self.pref_cbutton.get_active())
