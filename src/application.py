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
from .applicationwindow import ApplicationWindow
from gi.repository import GLib, Gio, Gtk, Handy
import sys

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '0.0')

APPMENU_FILE = "/com/github/Johnn3y/Forklift/menus-appmenu.ui"


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        GLib.set_application_name("Forklift")
        GLib.set_prgname('Forklift')
        self.set_application_id("com.github.Johnn3y.Forklift")

    def do_startup(self):
        Gtk.Application.do_startup(self)

        self.build_app_menu()

    def do_activate(self):
        self.window = ApplicationWindow(application=self, title="Forklift")
        self.window.present()

    def build_app_menu(self):
        # print("bam")
        actionEntries = [('about', self.on_about)]

        for action, callback in actionEntries:
            simpleAction = Gio.SimpleAction.new(action, None)
            simpleAction.connect('activate', callback)
            self.add_action(simpleAction)

        build = Gtk.Builder()
        build.add_from_resource(APPMENU_FILE)
        obj = build.get_object("app-menu")
        self.set_app_menu(build.get_object("app-menu"))

    def on_about(self, action, param):
        ad = AboutDialog()
        ad.set_transient_for(self.window)
        ad.show()


@Gtk.Template(resource_path='/com/github/Johnn3y/Forklift/aboutdialog.ui')
class AboutDialog(Gtk.AboutDialog):
    __gtype_name__ = "AboutDialog"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @Gtk.Template.Callback()
    def on_about_response(self, dialog, response):
        dialog.destroy()
