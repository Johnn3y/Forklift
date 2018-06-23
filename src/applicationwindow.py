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
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from .items import InfoExtraction,Download

UI_FILE = "/org/johnn3y/gtubedl/applicationwindow.ui"
class ApplicationWindow():
	def create_window(self,app):
		self.builder = Gtk.Builder()
		self.builder.add_from_resource(UI_FILE)

		self.window = self.builder.get_object('applicationwindow')
		self.builder.connect_signals(self)

		tv= self.builder.get_object('gtktv')
		tv.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)

		tv.drag_dest_set(Gtk.DestDefaults.ALL,[],Gdk.DragAction.COPY)
		tv.drag_dest_add_text_targets()
		for i,txt in enumerate(["title","alt_title","webpage_url","id","uploader",
		"uploader_id","uploader_url","uploader_date","license","creator","thumbnail","description",]):
			if txt=="title":#Temporary
				column=Gtk.TreeViewColumn(txt)
				cell=Gtk.CellRendererText()
				column.pack_start(cell,True)
				column.set_cell_data_func(cell, self.get_anything, i)
				tv.append_column(column)



		########
		treeview=self.builder.get_object('treeview')
		#treeview.set_model(DownloadingStorage.get_new_list())

		for a,gt,b in [("Filename",Gtk.CellRendererText(),self.get_title),("Status",Gtk.CellRendererText(),self.get_status),("Progress",Gtk.CellRendererProgress(),self.get_progress)]:
			column=Gtk.TreeViewColumn(a)
			cell=gt
			column.pack_start(cell,True)
			column.set_cell_data_func(cell, b)
			treeview.append_column(column)


		errortv=self.builder.get_object('errortv')
		column=Gtk.TreeViewColumn("")
		cell=Gtk.CellRendererText()
		column.pack_start(cell,True)
		column.set_cell_data_func(cell,self.get_errormsg)
		errortv.append_column(column)

		combobox=self.builder.get_object('newcb')
		rentext=Gtk.CellRendererText()
		combobox.pack_start(rentext,True)
		combobox.add_attribute(rentext,"text",0)

		self.window.show_all()

		return self.window
	def get_status(self, columnm, cell, model, iter, data):
		cell.set_property('text',model.get_value(iter, 0))

	def get_progress(self, columnm, cell, model, iter, data):
		downloaded_bytes=model.get_value(iter, 3)

		try:
			downloaded_bytes=float(downloaded_bytes)
			total_bytes=float(model.get_value(iter, 4))
			cell.set_property('value',(downloaded_bytes/total_bytes)*100)
		except TypeError:#NoneType
			try:
				total_bytes_estimate=float(model.get_value(iter, 5))
				cell.set_property('value',(downloaded_bytes/total_bytes_estimate)*100)
			except TypeError:#NoneType
				cell.set_property('pulse',0)

	def get_title(self, columnm, cell, model, iter, data):
		cell.set_property('text',model.get_value(iter, 1))
	def get_vidname(self, columnm, cell, model, iter, data):
		cell.set_property('text',model.get_value(iter, 0))

	def get_anything(self, columnm, cell, model, iter, data):
		cell.set_property('text',model.get_value(iter, data))



	def on_popover_toggled(self, togglebutton):
		popover = self.builder.get_object('addpopover')
		if togglebutton.get_active():
			popover.show_all()

	def on_ok_clicked(self, okbutton):
		url1=self.builder.get_object('addpopoverentry')
		self.ubergabe(url1.get_text())
		self.on_cancel_clicked(None)

	def on_paste_clicked(self, pastebutton):
		clipboard=Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
		self.ubergabe(clipboard.wait_for_text())

	def ubergabe(self,url):
		#url2=[]
		#url2.append(url)
		#ttt=Neu()
		#ttt.prepare(url2)
		thread=InfoExtraction(url,self.builder.get_object('realts'),self.builder.get_object('errorls'))
		thread.start()

	def dlubergabe(self, item):
		pass
		#dlprocess=Neu2()
		#dlprocess.prepareDL(item.webpage_url,item.ydl_opts,item.path)

	def on_properties_clicked(self, propertiesbutton):
		return None

	def on_delete_clicked(self, deletebutton):
		return None

	def on_drag_data_received(self, widget, drag_content,x,y,data,info,time):
		self.ubergabe(data.get_text())

	def on_popover_closed(self,popover):
		button = self.builder.get_object('addbutton')
		button.set_active(False)

	def on_downloadpopover_closed(self,popover):
		button = self.builder.get_object('detailsbutton')
		button.set_active(False)

	def on_downloadpopover2_closed(self,popover):
		button = self.builder.get_object('settingsbutton')
		button.set_active(False)

	def on_selectionbutton_toggled(self,button):
		listbox=self.builder.get_object('box2')
		ab=self.builder.get_object('actionbar')
		if button.get_active():
			listbox.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
			listbox.set_activate_on_single_click(False)
			ab=self.builder.get_object('actionbar')
			#ab.pack_start(self.builder.get_object('downloadselectedbutton'))
			#ab.pack_end(self.builder.get_object('deleteselectedbutton'))
			ab.set_visible(True)
		else:
			listbox.set_selection_mode(Gtk.SelectionMode.NONE)
			listbox.set_activate_on_single_click(True)
			ab.set_visible(False)

	def on_new_deleteselectedbutton_clicked(self,button):
		selection=self.builder.get_object('gtktv').get_selection()
		selection.set_mode(Gtk.SelectionMode.MULTIPLE)
		(model,pathlist)= selection.get_selected_rows()
		for path in pathlist:
			tree_iter=model.get_iter(path)
			model.remove(tree_iter)

	def on_downloadselectedbutton_clicked(self,selection):
		#lists=self.listbox.get_selected_rows()
		#for l in lists:
		#	item=MyList.get_list().get_item(l.get_index())
		#	self.dlubergabe(item)
		self.builder.get_object('settingspopover').popdown()
		selection=self.builder.get_object('gtktv').get_selection()
		selection.set_mode(Gtk.SelectionMode.MULTIPLE)
		(model,pathlist)= selection.get_selected_rows()
		value=[]
		for path in pathlist:
			tree_iter=model.get_iter(path)
			value.append(model.get_value(tree_iter,2))
			#print("I selected",value)
		ydl_opts={}

		newcb=self.builder.get_object('newcb')
		patth=newcb.get_active_iter()
		#cbiter=model.get_iter(patth)
		try:
			form=model[patth][0]
			ydl_opts['format']=form
		except TypeError:
			pass


		url=self.builder.get_object('ficb').get_uri()
		url=url.replace("file://","")
		ydl_opts['postprocessors']=[]
		if self.builder.get_object('defaultsetbutton').get_active():
			pass
		else:
			ydl_opts['keeporiginal']=self.builder.get_object('keepori').get_active()
			zi=[("audcb","FFmpegExtractAudio",'preferredcodec'),("vidcb","FFmpegVideoConvertor","preferredformat")]

			for aha,behe,ceh in zi:
				gg=self.builder.get_object(aha).get_active_id()
				if gg != "off":
					aq={}
					aq={'key':behe,ceh:gg}
					if aha=="audcb":
						pass
					ydl_opts['postprocessors'].append(aq)
		for a,b in [("username","ruser"),("password","rpw")]:
			c=self.builder.get_object(b).get_text()
			if c !="":
				ydl_opts[a]=c

		embt=self.builder.get_object('embedthumbnail')
		if embt.get_active():
			ydl_opts['postprocessors'].append({'key':'EmbedThumbnail'})
		print(ydl_opts)
		for v in value:
			n2=Download(self.builder.get_object('dloadstatusts'),v,ydl_opts,url)
			n2.start()

	def on_deleteselectedbutton_clicked(self,button):
		for l in lists:
			MyList.get_list().remove(l.get_index())

	def on_postprocessorsetbutton_toggled(self,button):
		pass

	def on_settingsbutton_toggled(self,togglebutton):
		popover=self.builder.get_object('settingspopover')
		pathchooser=self.builder.get_object('ficb')
		pathchooser.set_current_folder('.')
		if togglebutton.get_active():
			popover.show_all()

	def on_detailsbutton_toggled(self,togglebutton):
		popover=self.builder.get_object('downloadpopover')
		if togglebutton.get_active():
			popover.show_all()

	def on_cancel_clicked(self,button):
		popover = self.builder.get_object('addpopover')
		popover.popdown()

	def on_errorls_row_inserted(self,row,iter,data):
		reveal = self.builder.get_object('reveal')
		reveal.set_reveal_child(True)

	def on_errorls_row_deleted(self,model,data):
		reveal = self.builder.get_object('reveal')
		reveal.set_reveal_child(False)

	def get_errormsg(self, columnm, cell, model, iter, data):
		cell.set_property('text',model.get_value(iter, 0))

	def on_window_destroy(self, window):
		Gtk.main_quit()
