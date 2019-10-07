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
gi.require_version('Gtk','3.0')
from gi.repository import Notify, GObject, Gio, GLib
import threading

try:
	import youtube_dl
except:
    pass
from .cd import cd
import urllib.request
import time
NONE="NONE"


class Format(GObject.GObject):
    format_id = GObject.Property(type=str)
    url = GObject.Property(type=str)
    player_url = GObject.Property(type=str)
    ext = GObject.Property(type=str)
    format_note = GObject.Property(type=str)
    acodec = GObject.Property(type=str)
    preference = GObject.Property(type=str)
    abr = GObject.Property(type=str)
    filesize = GObject.Property(type=str)
    tbr = GObject.Property(type=str)
    vcodec = GObject.Property(type=str)
    format = GObject.Property(type=str)
    width = GObject.Property(type=str)
    height = GObject.Property(type=str)
    title_repr = GObject.Property(type=str)
    subtitle_repr = GObject.Property(type=str)
    icon_name = GObject.Property(type=str)

    def __init__(self, dic):
        GObject.GObject.__init__(self)
        for l in ['format_id', 'url', 'player_url', 'ext', 'format_note', 'acodec', 'preference',
                  'abr', 'filesize', 'tbr', 'format', 'vcodec', 'width', 'height']:
            self.set_property(l, dic.get(l))

        # Create title and subtitle reprs.
        sst = ""
        fs = ""
        onlys = ""
        def h(x): return '' if x is None else x
        self.icon_name = "video-x-generic"
        for x, y, z in ((self.vcodec, " - audio only", "audio-x-generic"), (self.acodec, " - video only", "video-x-generic")):
            if x == 'none':
                onlys += y
                if x != self.vcodec:
                    for f, g in ((self.width, 'x'), (self.height, ' ')):
                        if f is not None:
                            fs += f+g
                else:
                    self.icon_name = z

        for x, y in ((self.tbr, "k - "), (self.filesize, " Bytes")):
            if x is not None:
                sst += x+y
        self.title_repr = h(self.ext)+" - "+h(fs) + \
            "("+h(self.format_note)+") "+h(onlys)
        self.subtitle_repr = self.format_id+" - "+sst


class DownloadProgressItem(GObject.GObject):
    status = GObject.Property(type=str)
    filename = GObject.Property(type=str)
    tmpfilename = GObject.Property(type=str)
    downloaded_bytes = GObject.Property(type=str)
    total_bytes = GObject.Property(type=str)
    total_bytes_estimate = GObject.Property(type=str)
    elapsed = GObject.Property(type=str)
    eta = GObject.Property(type=str)
    speed = GObject.Property(type=str)
    fragment_index = GObject.Property(type=str)
    fragment_count = GObject.Property(type=str)

    def __init__(self, refresh_bind_model):
        GObject.GObject.__init__(self)
        self.refresh_bind_model = refresh_bind_model
    def my_hook(self, d):
        for a in ['status', 'filename', 'tmpfilename', 'downloaded_bytes',
                  'total_bytes', 'total_bytes_estimate', 'fragment_index', 'fragment_count']:
            try:
                self.set_property(a, d.get(a))
            except(TypeError, KeyError):
                pass
        GLib.idle_add(self.refresh_bind_model)


class Item(GObject.GObject):
    playlist_id = GObject.Property(type=str)
    playlist_title = GObject.Property(type=str)
    playlist_webpage_url = GObject.Property(type=str)
    title = GObject.Property(type=str)
    alt_title = GObject.Property(type=str)
    webpage_url = GObject.Property(type=str)
    id = GObject.Property(type=str)
    uploader = GObject.Property(type=str)
    uploader_id = GObject.Property(type=str)
    uploader_url = GObject.Property(type=str)
    uploader_date = GObject.Property(type=str)
    license = GObject.Property(type=str)
    creator = GObject.Property(type=str)
    thumbnail = GObject.Property(type=str)
    description = GObject.Property(type=str)
    formats = GObject.Property(type=Gio.ListStore)
    extractor = GObject.Property(type=str)
    extractor_key = GObject.Property(type=str)
    subtitle = GObject.Property(type=str)

    def __init__(self, a):
        GObject.GObject.__init__(self)
        for u in ['playlist_id', 'playlist_title', 'playlist_webpage_url', 'title', 'alt_title',
                  'webpage_url', 'id', 'uploader', 'uploader_id', 'uploader_url', 'uploader_date', 'license',
                  'creator', 'thumbnail', 'description', 'extractor', 'extractor_key']:
            self.set_property(u, a.get(u))

        self.formats = Gio.ListStore.new(Format)
        for f in a['formats']:
            b = Format(f)
            self.formats.append(b)

        self.subtitle = ""
        if self.uploader is not None:
             self.subtitle += self.uploader+ " "
        if self.extractor == 'generic':
            self.subtitle +="@ "+self.webpage_url
        elif self.extractor is not None:
             self.subtitle +="@ "+self.extractor

class Download(threading.Thread):
    def __init__(self, url, ydl_opts, path):
        threading.Thread.__init__(self)
        self.url = url
        self.ydl_opts = ydl_opts
        self.path = path

    def my_hook(self, d):
        status = ['finished', 'error', 'downloading']
        for stat in status:
            if stat is d['status']:
                self.model.set_value(self.iter, 0, d['status'])
        if d['status'] == 'finished' or d['status'] == 'error':
            Notify.init("Forklift")
            notification = Notify.Notification.new(self.model.get_value(
                self.iter, 0), self.model.get_value(self.iter, 1))
            notification.show()
        if d['status'] == 'downloading':
            for a, b in enumerate(['status', 'filename', 'tmpfilename', 'downloaded_bytes', 'total_bytes', 'total_bytes_estimate', 'elapsed', 'eta', 'speed', 'fragment_index', 'fragment_count']):
                try:
                    self.model.set_value(self.iter, a, str(d[b]))
                except(TypeError, KeyError):
                    pass

    def run(self):
        # self.ydl_opts['progress_hooks']=[self.my_hook]
        with cd(self.path), youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            try:
                ydl.download([self.url])
            except youtube_dl.utils.DownloadError as e:
                Notify.init("Forklift")
                notification = Notify.Notification.new('Error', str(e))
                notification.show()


class InfoExtraction(threading.Thread):

    def __init__(self, url, callback):
        threading.Thread.__init__(self)
        self.url = url
        self.callback = callback

    def run(self):
        with youtube_dl.YoutubeDL() as ydl:
            try:
                d = ydl.extract_info(self.url, download = False)
                if d is not None:
                    if d.get('_type') is 'playlist':
                        playlist_dic={'playlist_id':d.get('playlist_id'),
                        'playlist_title':d.get('playlist_title')
                        ,'playlist_webpage_url':d.get('playlist_webpage_url')}
                        for entry in d['entries']:
                            entry.update(playlist_dic)
                            GLib.idle_add(self.callback, Item(entry))
                    else:
                        GLib.idle_add(self.callback, Item(d))
            except youtube_dl.utils.DownloadError as e:
                self.d = None
                Notify.init("Forklift")
                n=Notify.Notification.new(str(e))
                n.show()
