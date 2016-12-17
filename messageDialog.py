#!/usr/bin/python

import gtk

def show_message_dialog(text):
    dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, text)
    dlg.set_position(gtk.WIN_POS_CENTER)
    dlg.set_modal(gtk.TRUE)
    dlg.run()
    dlg.destroy()
