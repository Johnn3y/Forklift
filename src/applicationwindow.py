# applicationwindow.py
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
from __future__ import unicode_literals
from .items import InfoExtraction, Download, Item, DownloadProgressItem

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '0.0')
from gi.repository import Gtk, Gdk, GObject, Gio, Handy
# import .items


@Gtk.Template(resource_path='/com/github/Johnn3y/Forklift/applicationwindow.ui')
class ApplicationWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ApplicationWindow'
    #gtktv = Gtk.Template.Child()
    # treeview=Gtk.Template.Child()
    # errortv=Gtk.Template.Child()
    # newcb=Gtk.Template.Child()
    addpopover = Gtk.Template.Child()
    addpopoverentry = Gtk.Template.Child()
    # realts=Gtk.Template.Child()
    # errorls=Gtk.Template.Child()
    addbutton = Gtk.Template.Child()
    detailsbutton = Gtk.Template.Child()
    settingsbutton = Gtk.Template.Child()
    ficb = Gtk.Template.Child()
    reveal = Gtk.Template.Child()
    downloadpopover = Gtk.Template.Child()
    settingspopover = Gtk.Template.Child()
    #dloadstatusts = Gtk.Template.Child()
    addpopoverstack = Gtk.Template.Child()
    searchtype = Gtk.Template.Child()
    gtklb = Gtk.Template.Child()
    vbox = Gtk.Template.Child()
    download_progress_listbox = Gtk.Template.Child()
    actionbar = Gtk.Template.Child()
    headerbar = Gtk.Template.Child()
    spinner = Gtk.Template.Child()
    geobypass_switch = Gtk.Template.Child()
    geobypass_box = Gtk.Template.Child()
    authentification_box = Gtk.Template.Child()
    authentification_switch = Gtk.Template.Child()
    video_box = Gtk.Template.Child()
    audio_box = Gtk.Template.Child()
    formatcode_box = Gtk.Template.Child()
    #
    vidcb = Gtk.Template.Child()
    audcb = Gtk.Template.Child()
    #
    video_radiobutton = Gtk.Template.Child()
    audio_radiobutton = Gtk.Template.Child()
    formatcode_radiobutton = Gtk.Template.Child()

    #
    formatcode_entry = Gtk.Template.Child()
    # authentification
    videopassword = Gtk.Template.Child()
    ap_mso = Gtk.Template.Child()
    ap_username = Gtk.Template.Child()
    ap_password = Gtk.Template.Child()
    ruser = Gtk.Template.Child()
    rpw = Gtk.Template.Child()
    usenetrc = Gtk.Template.Child()
    lstore = GObject.Property(type=Gio.ListStore)
    downloadprogressliststore = GObject.Property(type=Gio.ListStore)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.vbox.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        self.vbox.drag_dest_add_text_targets()

        self.set_property("lstore",Gio.ListStore.new(Item))
        self.gtklb.bind_model(self.lstore, self.mflb)

        self.set_property("downloadprogressliststore",Gio.ListStore.new(DownloadProgressItem))
        self.refresh_bind_model()
        self.show_all()
        self.actionbar.set_visible(False)

    def mflb(self, item):
        return MyLabel(title=item.title, subtitle=item.subtitle)

    def progress_model(self, item):
        return Downloadprogressactionrow(title=item.status, subtitle=item.filename)

    def get_status(self, columnm, cell, model, iter, data):
        cell.set_property('text', model.get_value(iter, 0))

    def get_progress(self, columnm, cell, model, iter, data):
        downloaded_bytes = model.get_value(iter, 3)

        try:
            downloaded_bytes = float(downloaded_bytes)
            total_bytes = float(model.get_value(iter, 4))
            cell.set_property('value', (downloaded_bytes/total_bytes)*100)
        except TypeError:  # NoneType
            try:
                total_bytes_estimate = float(model.get_value(iter, 5))
                cell.set_property(
                    'value', (downloaded_bytes/total_bytes_estimate)*100)
            except TypeError:  # NoneType
                cell.set_property('pulse', 0)

    @Gtk.Template.Callback()
    def on_popover_toggled(self, togglebutton):
        if togglebutton.get_active():
            self.addpopover.show_all()

    @Gtk.Template.Callback()
    def on_ok_clicked(self, okbutton):
        txt = self.addpopoverentry.get_text()
        if self.addpopoverstack.get_visible_child_name() == "searchbox":
            txt = self.searchtype.get_active_id()+':'+txt
        self.ubergabe(txt)
        self.addpopover.popdown()

    @Gtk.Template.Callback()
    def on_paste_clicked(self, pastebutton):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.ubergabe(clipboard.wait_for_text())

    def ubergabe(self, url):
        thread = InfoExtraction(url, self.callback)
        thread.start()

    def callback(self, item):
        self.lstore.append(item)

    def on_properties_clicked(self, propertiesbutton):
        return None

    @Gtk.Template.Callback()
    def on_drag_data_received(self, widget, drag_content, x, y, data, info, time):
        self.ubergabe(data.get_text())

    @Gtk.Template.Callback()
    def on_popover_closed(self, popover):

        self.addbutton.set_active(False)

    @Gtk.Template.Callback()
    def on_downloadpopover_closed(self, popover):

        self.detailsbutton.set_active(False)

    @Gtk.Template.Callback()
    def on_downloadpopover2_closed(self, popover):

        self.settingsbutton.set_active(False)

    @Gtk.Template.Callback()
    def on_new_deleteselectedbutton_clicked(self, button):
        for a in self.gtklb.get_selected_rows():
            self.lstore.remove(a.get_index())

    def refresh_bind_model(self,i=0):
        self.download_progress_listbox.bind_model(
            self.downloadprogressliststore, self.progress_model)
    def real_download(self, url, ydl_opts, path):
        item = DownloadProgressItem(self.refresh_bind_model)
        self.downloadprogressliststore.append(item)
        ydl_opts['progress_hooks'] = [item.my_hook]
        t = Download(url, ydl_opts, path)
        t.start()
    @Gtk.Template.Callback()
    def on_downloadselectedbutton_clicked(self, selection):
        self.settingspopover.popdown()

        for a in self.gtklb.get_selected_rows():
            # self.lstore.remove.get(a.get_index())#TODO Fix
            path, ydl_opts = self.get_settings()
            self.real_download(self.lstore.get_item(a.get_index()).webpage_url,ydl_opts,path)

    def get_settings(self):
        ydl_opts = {}
        path = self.ficb.get_uri().replace("file://", "")
        ydl_opts['postprocessors'] = []
        # defaultsetbutton=Gtk.Template.Child()
        if self.video_radiobutton.get_active():
            ydl_opts['postprocessors'].append(
                {'key': 'FFmpegVideoConvertor', 'format': self.vidcb.get_active_id()})
        if self.audio_radiobutton.get_active():
            ydl_opts['postprocessors'].append(
                {'key': 'FFmpegExtractAudio', 'preferredcodec': self.audcb.get_active_id()})
        if self.formatcode_radiobutton.get_active():
            ydl_opts['format'] = self.formatcode_entry.get_text()
        if self.geobypass_switch.get_active():
            for a, b in [("username", self.ruser), ("password", self.rpw), ("videopassword", self.videopassword), ("ap_mso", self.ap_mso), ("ap_username", self.ap_username), ("ap_password", self.ap_password), ("geo_bypass_country", self.geo_bypass_country), ("geo_bypass_ip_block", self.geo_bypass_ip_block)]:
                c = b.get_text()
                if c != "":
                    ydl_opts[a] = cpass
        if self.authentification_switch.get_active():
            ydl_opts["geo_bypass_country"] = self.geo_bypass_country
            ydl_opts["geo_bypass_ip_block"] = self.geo_bypass_ip_block
        return path, ydl_opts

    @Gtk.Template.Callback()
    def on_deleteselectedbutton_clicked(self, button):
        for l in lists:
            MyList.get_list().remove(l.get_index())

    @Gtk.Template.Callback()
    def on_settingsbutton_toggled(self, togglebutton):
        self.ficb.set_current_folder('.')
        if togglebutton.get_active():
            self.settingspopover.show()

    @Gtk.Template.Callback()
    def on_detailsbutton_toggled(self, togglebutton):

        if togglebutton.get_active():
            self.downloadpopover.show_all()

#	@Gtk.Template.Callback()
#	def on_errorls_row_inserted(self,row,iter,data):
#		self.reveal.set_reveal_child(True)

#	@Gtk.Template.Callback()
#	def on_errorls_row_deleted(self,model,data):
#		self.reveal.set_reveal_child(False)
#
#	def get_errormsg(self, columnm, cell, model, iter, data):
#		cell.set_property('text',model.get_value(iter, 0))

    @Gtk.Template.Callback()
    def on_row_selected(self, t):
        self.actionbar.set_visible(len(t.get_selected_rows()) != 0)

    @Gtk.Template.Callback()
    def on_download_progress_listbox_selected_rows(self, t):
        self.detailsbutton.set_visisble(len(t.get_selected_rows()) != 0)

    @Gtk.Template.Callback()
    def on_geobypass_switch_state_set(self, switch, state):
        self.geobypass_box.set_visible(state)

    @Gtk.Template.Callback()
    def on_authentification_switch_state_set(self, switch, state):
        self.authentification_box.set_visible(state)

    @Gtk.Template.Callback()
    def on_video_radiobutton_toggled(self, button):
        self.video_box.set_visible(button.get_active())

    @Gtk.Template.Callback()
    def on_audio_radiobutton_toggled(self, button):
        self.audio_box.set_visible(button.get_active())

    @Gtk.Template.Callback()
    def on_formatcode_radiobutton_toggled(self, button):
        self.formatcode_box.set_visible(button.get_active())

    @Gtk.Template.Callback()
    def on_row_activated(self, t, a):
        a = self.lstore.get_item(a.get_index())
        dialog = HandyDialog(a, self.real_download)
        dialog.set_transient_for(self)
        dialog.set_attached_to(self)
        dialog.set_visible(True)


@Gtk.Template(resource_path='/com/github/Johnn3y/Forklift/formats_actionrow.ui')
class FormatsRow(Gtk.Box):
    __gtype_name__ = 'Box2'
    formatsrow = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@Gtk.Template(resource_path='/com/github/Johnn3y/Forklift/handydialog.ui')
class HandyDialog(Handy.Dialog):
    __gtype_name__ = 'Dialog'
    vp = Gtk.Template.Child()
    flb = Gtk.Template.Child()
    filechooserdialog_button = Gtk.Template.Child()

    def __init__(self, a, real_download, **kwargs):
        super().__init__(**kwargs)
        self.filechooserdialog_button.set_current_folder('.')

        ipb = InfoPopoverBox()
        e = (
            (ipb.title.set_text, a.title), (ipb.alt_title.set_text, a.alt_title), (ipb.webpage_url.set_uri, a.webpage_url), (ipb.webpage_url.set_label, a.webpage_url), (ipb.id.set_text, a.id), (ipb.uploader.set_text, a.uploader), (ipb.uploader_id.set_text, a.uploader_id), (ipb.uploader_url.set_uri, a.uploader_url), (ipb.uploader_url.set_label, a.uploader_url), (ipb.uploader_date.set_text, a.uploader_date), (ipb.license.set_text, a.license), (ipb.creator.set_text, a.creator), (ipb.thumbnail.set_uri, a.thumbnail), (ipb.thumbnail.set_label, a.thumbnail), (ipb.description.set_text, a.description))
        for x, y in e:
            try:
                x(y)
            except TypeError:
                pass
        self.flb.bind_model(a.formats, self.formats_model)
        ipb.set_visible(True)
        self.vp.add(ipb)
        self.item = a
        self.real_download=real_download

    def formats_model(self, a):
        fr = FormatsRow()
        fr.formatsrow.set_icon_name(a.icon_name)
        fr.formatsrow.set_title(a.title_repr)
        fr.formatsrow.set_subtitle(a.subtitle_repr)
        return fr

    @Gtk.Template.Callback()
    def on_save_button_clicked(self, button):
        path = self.filechooserdialog_button.get_uri().replace("file://", "")
        selformatitem = self.item.formats.get_item(
            self.flb.get_selected_row().get_index())
        ydl_opts = {'format': selformatitem.format_id}
        self.real_download(self.item.webpage_url, ydl_opts, path)
        self.destroy()


@Gtk.Template(resource_path='/com/github/Johnn3y/Forklift/items_actionrow.ui')
class MyLabel(Gtk.Box):
    __gtype_name__ = 'Box'
    lbl = Gtk.Template.Child()

    def __init__(self, title="", subtitle="", **kwargs):
        super().__init__(**kwargs)
        for i, j in ((title, self.lbl.set_title), (subtitle, self.lbl.set_subtitle)):
            if i is not None:
                j(i)


@Gtk.Template(resource_path='/com/github/Johnn3y/Forklift/downloadprogressactionrow.ui')
class Downloadprogressactionrow(Gtk.Box):
    __gtype_name__ = 'Downloadprogressactionrow'
    download_progress_actionrow = Gtk.Template.Child()

    def __init__(self, title="", subtitle="", **kwargs):
        super().__init__(**kwargs)
        for i, j in ((title, self.download_progress_actionrow.set_title),
                     (subtitle, self.download_progress_actionrow.set_subtitle)):
            if i is not None:
                j(i)


@Gtk.Template(resource_path='/com/github/Johnn3y/Forklift/infopopoverbox.ui')
class InfoPopoverBox(Gtk.Box):
    __gtype_name__ = 'Expander'
    title = Gtk.Template.Child()
    alt_title = Gtk.Template.Child()
    webpage_url = Gtk.Template.Child()
    id = Gtk.Template.Child()
    uploader = Gtk.Template.Child()
    uploader_id = Gtk.Template.Child()
    uploader_url = Gtk.Template.Child()
    uploader_date = Gtk.Template.Child()
    license = Gtk.Template.Child()
    creator = Gtk.Template.Child()
    thumbnail = Gtk.Template.Child()
    description = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
