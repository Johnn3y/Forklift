# items.py
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
gi.require_version('Notify','0.7')
from gi.repository import Notify
import threading

import youtube_dl
from .cd import cd
import urllib.request
import time
NONE="NONE"

class Download(threading.Thread):
	def __init__(self,model,url,ydl_opts,path):
		threading.Thread.__init__(self)
		#self.iter=DownloadingStorage.get_new_list().append(None)
		self.model=model
		self.iter=model.append(None)
		self.url=url
		self.ydl_opts=ydl_opts
		self.path=path

	def my_hook(self,d):
		status=['finished','error','downloading']
		for stat in status:
			if stat is d['status']:
				self.model.set_value(self.iter,0,d['status'])
		if d['status']=='finished' or d['status']=='error':
			Notify.init("Gtube-dl")
			notification=Notify.Notification.new(self.model.get_value(self.iter,0),self.model.get_value(self.iter,1))
			notification.show()
		if d['status']=='downloading':
			for a,b in enumerate(['status','filename','tmpfilename','downloaded_bytes','total_bytes','total_bytes_estimate','elapsed','eta','speed','fragment_index','fragment_count']):
				try:
					self.model.set_value(self.iter,a,str(d[b]))
				except(TypeError,KeyError):
					pass

	#def prepareDL(self,url,ydl_opts,path):
	#	t=threading.Thread(target=self.machDownload,args=(url,ydl_opts,path))
	#	t.daemon=True
	#	t.start()

	def run(self):
		self.ydl_opts['progress_hooks']=[self.my_hook]
		with cd(self.path),youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
			try:
				ydl.download([self.url])
			except youtube_dl.utils.DownloadError as e:
				Notify.init("Gtube-dl")
				notification=Notify.Notification.new('Error',e)


class InfoExtraction(threading.Thread):

	def __init__(self,url,model,errormodel):
		threading.Thread.__init__(self)
		self.url=url
		self.model=model
		self.errormodel=errormodel



	def run(self):
		with youtube_dl.YoutubeDL() as ydl:
			try:
				test=ydl.extract_info(self.url,False)

		#nopliter=MainTS.get_tree().append(None)
				if test.get('_type') is 'playlist':
			#print(test)
			#test['playlist_id']=test.get('id')
			#test['playlist_title']=test.get('title')
			#test['playlist_webpage_url']=test.get('webpage_url')

			#playlistIter=MainTS.get_tree().append(None)
			#MainTS.get_tree().set_value(playlistIter,test.get('id'),test.get('title'),test.get(webpage_url))
					for entry in test.get('entries'):
						try:
							self.extrahiere(entry)
						except AttributeError:
							pass

				else:
					self.extrahiere(test)
			except youtube_dl.utils.DownloadError as e:
				iter=self.errormodel.append(None)
				self.errormodel.set_value(iter,0,str(e))
				time.sleep(3)
				self.errormodel.remove(iter)
	def extrahiere(self,jsohn):

		videoIter=None
		videoIter=self.model.append(None)
		for i,txt in enumerate(["title","alt_title","webpage_url","id","uploader",
		"uploader_id","uploader_url","uploader_date","license","creator","thumbnail","description",]):
			self.model.set_value(videoIter,i,jsohn.get(txt))

		if jsohn.get('formats') is not None:
			for a,b in enumerate(["default","best","worst"]):
				formatIter=self.model.append(videoIter)
				self.model.set_value(formatIter,0,b)
			for forma in jsohn.get('formats'):
				formatIter=self.model.append(videoIter)
				for i,txt in enumerate(["format_id"]):#,"url","player_url","ext","format_note","acodec","preference","abr","filesize","tbr","vcodec","format"]):
					self.model.set_value(formatIter,i,str(forma[txt]))
