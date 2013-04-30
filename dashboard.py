#!/usr/bin/python

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import WebKit

win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)

webView = WebKit.WebView()
#webView.load_uri('http://xn--joursavantlt-lebb.fr/')
webView.load_uri('http://dashboard.pabloseminario.com/')
win.add(webView)

win.show_all()

cursor = Gdk.Cursor.new(Gdk.CursorType.BLANK_CURSOR)
win.get_window().set_cursor(cursor)

#win.fullscreen()

Gtk.main()
