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
gi.require_version('Dazzle', '1.0')
from gi.repository import Gtk, Gdk, GLib, GObject, Gio, Handy, Dazzle

DEFAULT_DOWNLOAD_FOLDER='.'
@Gtk.Template(resource_path='/com/github/Johnn3y/Forklift/applicationwindow.ui')
class ApplicationWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ApplicationWindow'
    addpopover = Gtk.Template.Child()
    addpopoverentry = Gtk.Template.Child()
    detailsbutton = Gtk.Template.Child()
    ficb = Gtk.Template.Child()
    downloadpopover = Gtk.Template.Child()
    addpopoverstack = Gtk.Template.Child()
    searchtype = Gtk.Template.Child()
    gtklb = Gtk.Template.Child()
    dnd_stack = Gtk.Template.Child()
    download_progress_listbox = Gtk.Template.Child()
    actionbar = Gtk.Template.Child()

    lstore = GObject.Property(type=Gio.ListStore)
    downloadprogressliststore = GObject.Property(type=Gio.ListStore)
    
    flb = Gtk.Template.Child()
    gtklb1 = Gtk.Template.Child()
    gtklb2 = Gtk.Template.Child()
    
    stack1_formats= Gtk.Template.Child()

    leaflet2 = Gtk.Template.Child()
    hbleaflet = Gtk.Template.Child()

    fw1button = Gtk.Template.Child()
    bw2button = Gtk.Template.Child()

    ab2 = Gtk.Template.Child()
    ab3 = Gtk.Template.Child()
    
    sg2 = Gtk.Template.Child()
    sg3 = Gtk.Template.Child()  
    swg = Gtk.Template.Child() 
    
    savebutton = Gtk.Template.Child() 
    
    conversionlb = Gtk.Template.Child()    
    
    selectedformatbox = Gtk.Template.Child()
    
    titlebar_stack = Gtk.Template.Child()
    extraction_threads_counter_label = Gtk.Template.Child() 
        
    extraction_thread_counter = GObject.Property(type=int)  

    authentification_expander_row = Gtk.Template.Child()
    custom_code_expander_row = Gtk.Template.Child()
    geobypass_expander_row = Gtk.Template.Child()
    
    formatcode_entry4 = Gtk.Template.Child()
    videopassword_entry = Gtk.Template.Child()
    username_entry = Gtk.Template.Child()
    password_entry = Gtk.Template.Child()
    ap_username_entry = Gtk.Template.Child()
    ap_password_entry = Gtk.Template.Child()
    ap_mso_entry = Gtk.Template.Child()  
    geo_bypass_country_entry = Gtk.Template.Child()
    geo_bypass_ip_block_entry = Gtk.Template.Child()  
    
    custom_code_action_row = Gtk.Template.Child()
    videopassword_action_row = Gtk.Template.Child()
    username_action_row = Gtk.Template.Child()
    password_action_row = Gtk.Template.Child()
    ap_username_action_row = Gtk.Template.Child()
    ap_password_action_row = Gtk.Template.Child()
    ap_mso_action_row = Gtk.Template.Child()  
    geo_bypass_country_action_row = Gtk.Template.Child()
    geo_bypass_ip_block_action_row = Gtk.Template.Child()  

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #uff=[{"title_repr":"Convert to wav","subtitle_repr":"wav","icon_name":"audio-x-generic-symbolic","ydl_opts":{'extractaudio':True,'postprocessors':[{'key': 'FFmpegExtractAudio', 'preferredcodec':"wav"}]}},{"title_repr":"Convert to mp3","subtitle_repr":"mp3","icon_name":"audio-x-generic-symbolic","ydl_opts":{'extractaudio':True,'postprocessors':[{'key': 'FFmpegExtractAudio', 'preferredcodec':"mp3"}]}},{"title_repr":"Convert to aac","subtitle_repr":"aac","icon_name":"audio-x-generic-symbolic","ydl_opts":{'extractaudio':True,'postprocessors':[{'key': 'FFmpegExtractAudio', 'preferredcodec':"aac"}]}},{"title_repr":"Convert to flac","subtitle_repr":"flac","icon_name":"audio-x-generic-symbolic","ydl_opts":{'extractaudio':True,'postprocessors':[{'key': 'FFmpegExtractAudio', 'preferredcodec':"flac"}]}},{"title_repr":"Convert to m4a","subtitle_repr":"m4a","icon_name":"audio-x-generic-symbolic","ydl_opts":{'extractaudio':True,'postprocessors':[{'key': 'FFmpegExtractAudio', 'preferredcodec':"m4a"}]}},{"title_repr":"Convert to opus","subtitle_repr":"opus","icon_name":"audio-x-generic-symbolic","ydl_opts":{'extractaudio':True,'postprocessors':[{'key': 'FFmpegExtractAudio', 'preferredcodec':"opus"}]}},{"title_repr":"Convert to vorbis","subtitle_repr":"vorbis","icon_name":"audio-x-generic-symbolic","ydl_opts":{'extractaudio':True,'postprocessors':[{'key': 'FFmpegExtractAudio', 'preferredcodec':"vorbis"}]}},{"title_repr":"Convert to mp4","subtitle_repr":"mp4","icon_name":"video-x-generic-symbolic","ydl_opts":{'postprocessors':[{'key': 'FFmpegVideoConvertor', 'format':"mp4"}]}},{"title_repr":"Convert to flv","subtitle_repr":"flv","icon_name":"video-x-generic-symbolic","ydl_opts":{'postprocessors':[{'key': 'FFmpegVideoConvertor', 'format':"flv"}]}},{"title_repr":"Convert to ogg","subtitle_repr":"ogg","icon_name":"video-x-generic-symbolic","ydl_opts":{'postprocessors':[{'key': 'FFmpegVideoConvertor', 'format':"ogg"}]}},{"title_repr":"Convert to avi","subtitle_repr":"avi","icon_name":"video-x-generic-symbolic","ydl_opts":{'postprocessors':[{'key': 'FFmpegVideoConvertor', 'format':"avi"}]}},{"title_repr":"Convert to mkv","subtitle_repr":"mkv","icon_name":"video-x-generic-symbolic","ydl_opts":{'postprocessors':[{'key': 'FFmpegVideoConvertor', 'format':"mkv"}]}},{"title_repr":"Convert to webm","subtitle_repr":"webm","icon_name":"video-x-generic-symbolic","ydl_opts":{'postprocessors':[{'key': 'FFmpegVideoConvertor', 'format':"webm"}]}}]
        #for u in uff:
        #    ar=FormatsRow(u["icon_name"],u["title_repr"],u["subtitle_repr"],u["ydl_opts"])
        #    self.conversionlb.prepend(ar)
        for a in self.conversionlb.get_children():
            if a.get_subtitle() in ['mp4','webm','mkv','avi','ogg','flv']:
                a.ydl_opts = {'postprocessors':[{'key': 'FFmpegVideoConvertor', 'format':a.get_subtitle()}]}
            elif a.get_subtitle() in ['mp3','wav','vorbis','opus','m4a','flac','aac']:
                a.ydl_opts = {'extractaudio':True,'postprocessors':[{'key': 'FFmpegExtractAudio', 'preferredcodec':a.get_subtitle()}]}


                
        self.leaflet2.connect("notify::folded",self.on_leaflet_visible_changed)

        self.dnd_stack.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        self.dnd_stack.drag_dest_add_text_targets()

        self.set_property("lstore",Gio.ListStore.new(Item))
        self.gtklb.bind_model(self.lstore, self.mflb)
        self.lstore.connect("items_changed",self.on_lstore_items_changed)


        self.empty_state = Dazzle.EmptyState(visible=True,icon_name=self.get_application().get_application_id()+"-symbolic",title=GLib.get_application_name(),subtitle="• Click ➕ above to type in URL or to search,\n• click 📋 above to paste URL from Clipboard, or\n• Drag-and-Drop URL here.")
        self.dnd_stack.add(self.empty_state)
        self.on_lstore_items_changed(None,None,None,None)

        self.set_property("downloadprogressliststore",Gio.ListStore.new(DownloadProgressItem))
        self.refresh_bind_model()
        self.ficb.set_current_folder(DEFAULT_DOWNLOAD_FOLDER)
        
        self.authentification_expander_row.connect("notify::enable-expansion",self.on_authentification_expander_row_enable_expansion_changed)
        self.custom_code_expander_row.connect("notify::enable-expansion",self.on_custom_code_expander_row_enable_expansion_changed)
        self.geobypass_expander_row.connect("notify::enable-expansion",self.on_geobypass_expander_row_enable_expansion_changed)

    def on_custom_code_expander_row_enable_expansion_changed(self, expander_row, event):
        self.custom_code_action_row.set_visible(expander_row.get_enable_expansion())
        self.selectedformatbox.set_visible(not expander_row.get_enable_expansion())
        self.savebutton.set_sensitive(self.custom_code_action_row.get_visible() or self.selectedformatbox.get_visible())
        #self.custom_code_action_row.set_title(self.formatcode_entry4.get_text())
        #self.custom_code_action_row.ydl_opts={"format":self.formatcode_entry4.get_text()}
        #self.on_formatcode_entry4_changed(self, self.formatcode_entry4)      
               
    def on_authentification_expander_row_enable_expansion_changed(self, expander_row, event):
        for a in [self.videopassword_action_row,self.username_action_row,self.password_action_row,
        self.ap_username_action_row,self.ap_password_action_row,self.ap_mso_action_row]:
            if expander_row.get_enable_expansion() == False:
                a.set_visible(False)
            else:
                a.set_visible(a.get_title()!="")
            
    @Gtk.Template.Callback()        
    def on_entry_changed(self, entry):
        #m={Entry:(ActionRow,is_not_pw_entry,ydl_code)}
        m={self.formatcode_entry4:(self.custom_code_action_row,True,"format"),
        self.videopassword_entry:(self.videopassword_action_row,False,"videopassword"),
        self.username_entry:(self.username_action_row,True,"username"),
        self.password_entry:(self.password_action_row,False,"password"),
        self.ap_username_entry:(self.ap_username_action_row,True,"ap_username"),
        self.ap_password_entry:(self.ap_password_action_row,False,"ap_password"),
        self.ap_mso_entry:(self.ap_mso_action_row,False,"ap_mso"),    
        self.geo_bypass_country_entry:(self.geo_bypass_country_action_row,True,"geo_bypass_country"),
        self.geo_bypass_ip_block_entry:(self.geo_bypass_ip_block_action_row,True,"geo_bypass_ip_block_entry")}
        m[entry][0].set_visible(entry.get_text()!="")
        def f():return "***" if entry.get_text()!="" else ""
        m[entry][0].set_title(entry.get_text() if m[entry][1] else f())
        m[entry][0].ydl_opts={m[entry][2]:entry.get_text()}

        
    def on_geobypass_expander_row_enable_expansion_changed(self, expander_row, event):
        if expander_row.get_enable_expansion() == False:
            self.geo_bypass_country_action_row.set_visible(False)
            self.geo_bypass_ip_block_action_row.set_visible(False)
             

    def on_lstore_items_changed(self, pos, rm, a, d):
        self.dnd_stack.set_visible_child(self.empty_state if len(self.lstore) == 0 else self.leaflet2)

    def mflb(self, item):
        return MyLabel(item)

    def lbfilter(self, item):
        #if self.lstore.get(item).is_selected():
        return MyLabel(item)

    def progress_model(self, item):
        return Downloadprogressactionrow(item)

    @Gtk.Template.Callback()
    def on_ok_clicked(self, okbutton):
        txt = self.addpopoverentry.get_text()
        if self.addpopoverstack.get_visible_child_name() == "searchbox":
            txt = self.searchtype.get_active_id()+':'+txt
        self.start_download(txt)
        self.addpopover.popdown()

    @Gtk.Template.Callback()
    def on_paste_clicked(self, pastebutton):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.start_download(clipboard.wait_for_text())

    def start_download(self, url):
        self.change_extraction_thread_counter(True)
        thread = InfoExtraction(url, self.callback, self.change_extraction_thread_counter, self.send_notification)
        thread.start()

    def callback(self, item):
        self.lstore.append(item)

    @Gtk.Template.Callback()
    def on_drag_data_received(self, widget, drag_content, x, y, data, info, time):
        self.start_download(data.get_text())

        
        
    def on_leaflet_visible_changed(self, leaflet, event):
        self.fw1button.set_visible(leaflet.get_fold()==Handy.Fold.FOLDED)
        self.ab2.set_visible(leaflet.get_fold()==Handy.Fold.FOLDED)
        self.ab3.set_visible(leaflet.get_fold()==Handy.Fold.FOLDED)

    @Gtk.Template.Callback()
    def on_new_deleteselectedbutton_clicked(self, button):
        for a in self.gtklb.get_selected_rows():
            self.lstore.remove(a.get_index())
            
    def change_extraction_thread_counter(self, inc):#if bool(inc) increment else decrement
        self.extraction_thread_counter+=1 if inc else -1
        self.titlebar_stack.set_visible_child_name("title" if self.extraction_thread_counter==0 else "exinfo")
        self.extraction_threads_counter_label.set_text(str(self.extraction_thread_counter))            
    def refresh_bind_model(self,i=0):
        self.download_progress_listbox.bind_model(
            self.downloadprogressliststore, self.progress_model)
    def real_download(self, url, ydl_opts, path):
        item = DownloadProgressItem(self.refresh_bind_model)
        self.downloadprogressliststore.append(item)
        ydl_opts['progress_hooks'] = [item.my_hook]
        t = Download(url, ydl_opts, path, self.send_notification)
        t.start()
    @Gtk.Template.Callback()
    def on_downloadselectedbutton_clicked(self, selection):
        self.set_visible_child_1(None)
        for a in self.gtklb.get_selected_rows():
            path, ydl_opts = self.get_settings()
            self.real_download(self.lstore.get_item(a.get_index()).webpage_url,ydl_opts,path)

    def get_settings(self):
        ydl_opts = {}
        path=self.ficb.get_file().get_path()
        if self.selectedformatbox.get_visible():
            ydl_opts.update(self.selectedformatbox.get_children()[0].ydl_opts)
        for a in [self.custom_code_action_row,self.videopassword_action_row,self.username_action_row,self.password_action_row,
        self.ap_username_action_row,self.ap_username_action_row,self.ap_mso_action_row,
        self.geo_bypass_country_action_row,self.geo_bypass_ip_block_action_row]:
            if a.get_visible():
                ydl_opts.update(a.ydl_opts)
        return path, ydl_opts

    def do_show_rows(self,t,a):
        self.gtklb1.insert(MyLabel(self.lstore.get_item(a.get_index())),-1)
    
    @Gtk.Template.Callback()
    def on_rows_changed(self,t):

        if len(self.selectedformatbox.get_children())!=0:
            self.selectedformatbox.remove(self.selectedformatbox.get_children()[0])
        if len(t.get_selected_rows()) !=0:
            title=t.get_selected_row().get_title()
            subtitle=t.get_selected_row().get_subtitle()
            icon_name=t.get_selected_row().get_icon_name()
            ydl_opts=t.get_selected_row().ydl_opts
            fr=FormatsRow(icon_name,title,subtitle,ydl_opts)
            self.selectedformatbox.add(fr)
        self.savebutton.set_sensitive(len(self.selectedformatbox.get_children())!=0)
    
    @Gtk.Template.Callback()
    def on_row_selected(self, t):
        self.actionbar.set_visible(len(t.get_selected_rows()) != 0)
            
        for a in self.sg2.get_widgets():
            a.set_visible(len(t.get_selected_rows()) != 0)
        for a in self.sg3.get_widgets():
            a.set_visible(len(t.get_selected_rows()) != 0)
        for i in self.gtklb1.get_children():
            self.gtklb1.remove(i)
        t.selected_foreach(self.do_show_rows)
        if len(t.get_selected_rows()) == 1:
            self.flb.bind_model(self.lstore.get_item(t.get_selected_rows()[0].get_index()).formats,self.formats_model)
        self.stack1_formats.set_visible(len(t.get_selected_rows()) == 1)


    def formats_model(self, a):
        return FormatsRow(a.icon_name,a.title_repr,a.subtitle_repr,a.ydl_opts)
        
    @Gtk.Template.Callback()        		
    def on_flb_selected_rows_changed(self, t):
        if len(t.get_selected_rows()) ==1:
            pass
        #self.selectedformatsbox.add(FormatsRow) 		
    @Gtk.Template.Callback()
    def on_download_progress_listbox_selected_rows(self, t):
        self.detailsbutton.set_visisble(len(t.get_selected_rows()) != 0)

    @Gtk.Template.Callback()
    def set_visible_child_1(self, button):
        self.leaflet2.set_visible_child_name("rb0")
        self.hbleaflet.set_visible_child_name("hb4")
        
    @Gtk.Template.Callback()
    def set_visible_child_2(self, button):
        self.leaflet2.set_visible_child_name("rb1")
        self.hbleaflet.set_visible_child_name("hb5")
        
    @Gtk.Template.Callback()
    def set_visible_child_3(self, button):
        self.leaflet2.set_visible_child_name("rb2")
        self.hbleaflet.set_visible_child_name("hb6")
        
    def send_notification(self,notification_title,notification_body):
        n=Gio.Notification.new(notification_title)
        n.set_body(notification_body)
        n.set_icon(Gio.Icon.new_for_string(self.get_application().get_application_id()))
        self.get_application().send_notification(None,n)        

@Gtk.Template(resource_path='/com/github/Johnn3y/Forklift/formats_actionrow.ui')
class FormatsRow(Handy.ActionRow):
    __gtype_name__ = 'FormatsRow'
    ydl_opts={}

    def __init__(self,icon_name,title,subtitle,ydl_opts, **kwargs):
        super().__init__(**kwargs)
        self.set_icon_name(icon_name)
        self.set_title(title)
        self.set_subtitle(subtitle)
        self.ydl_opts=ydl_opts

class H(Handy.Dialog):#Deprecated
    pass

@Gtk.Template(resource_path='/com/github/Johnn3y/Forklift/items_actionrow.ui')
class MyLabel(Handy.ExpanderRow):
    __gtype_name__ = 'lbl'
    
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

    def __init__(self, a, **kwargs):
        super().__init__(**kwargs)
        for i, j in ((a.title, self.set_title), (a.subtitle, self.set_subtitle)):
            if i is not None:
                j(i)
        e = (
            (self.title.set_text, a.title), (self.alt_title.set_text, a.alt_title), (self.webpage_url.set_uri, a.webpage_url), (self.webpage_url.set_label, "webpage_url"), (self.id.set_text, a.id), (self.uploader.set_text, a.uploader), (self.uploader_id.set_text, a.uploader_id), (self.uploader_url.set_uri, a.uploader_url), (self.uploader_url.set_label, "uploader_url"), (self.uploader_date.set_text, a.uploader_date), (self.license.set_text, a.license), (self.creator.set_text, a.creator), (self.thumbnail.set_uri, a.thumbnail), (self.thumbnail.set_label, "thumbnail"), (self.description.set_text, a.description))
        for x, y in e:
            try:
                x(y)
            except TypeError:
                pass


@Gtk.Template(resource_path='/com/github/Johnn3y/Forklift/downloadprogressactionrow.ui')
class Downloadprogressactionrow(Gtk.Box):
    __gtype_name__ = 'Downloadprogressactionrow'
    download_progress_actionrow = Gtk.Template.Child()
    download_progress_icon_box = Gtk.Template.Child()

    def __init__(self, item, **kwargs):
        super().__init__(**kwargs)
        self.download_progress_icon_box.add(Dazzle.ProgressIcon(progress = item.download_progress,visible=True,expand=True))
        for i, j in ((item.title, self.download_progress_actionrow.set_title),
                     (item.subtitle, self.download_progress_actionrow.set_subtitle)):
            if i is not None:
                j(i)

