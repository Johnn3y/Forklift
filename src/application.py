# application.py
#
# Copyright (C) 2018 - johnn3y
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
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk
from .applicationwindow import ApplicationWindow

ABOUTDIALOG_FILE="/org/johnn3y/gtubedl/aboutdialog.ui"
APPMENU_FILE="/org/johnn3y/gtubedl/menus-appmenu.ui"

class Application(Gtk.Application):

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)

		GLib.set_application_name("Gtube-dl")
		GLib.set_prgname('gtube-dl')
		self.set_application_id("org.johnn3y.gtubedl")

	def do_startup(self):
		Gtk.Application.do_startup(self)

		self.build_app_menu()





	def do_activate(self):
		applicationwindow=ApplicationWindow()
		self.window=applicationwindow.create_window(self)
		self.window.set_application(self)#ka was ich da mach
		self.window.set_title("Gtube-dl")#ka was ich da mach
		self.window.present()



	def build_app_menu(self):
		#print("bam")
		actionEntries=[('about',self.on_about),('quit',self.on_quit),]

		for action,callback in actionEntries:
			simpleAction = Gio.SimpleAction.new(action,None)
			simpleAction.connect('activate',callback)
			self.add_action(simpleAction)

		build=Gtk.Builder()
		build.add_from_resource(APPMENU_FILE)
		obj=build.get_object("app-menu")
		self.set_app_menu(build.get_object("app-menu"))

	def on_about(self,action,param):
		builder=Gtk.Builder()
		builder.add_from_resource(ABOUTDIALOG_FILE)
		about=builder.get_object('aboutdialog')
		about.set_transient_for(self.window)
		about.show()

	def on_about_response(self,dialog,response):
		dialog.destroy()

	def on_quit(self,action,param):
		self.quit()