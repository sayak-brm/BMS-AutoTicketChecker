"""
   Copyright 2019 Sayak Brahmacahri

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import threading
import time

import wx

import bms
import ui.event

class EventHandler(threading.Thread):
    def __init__(self, parent, event_id, city, pref_venues, movie, date):
        threading.Thread.__init__(self)
        self._parent = parent
        self.event_id = event_id
        self.quit = False
        self.city_id = city
        self.city = self._parent.choice_1.GetString(self.city_id)
        self.pref_venues = list(filter(None, [venue.strip() for venue in pref_venues.upper().split(',')]))
        self.movie = movie
        self.date_ob = date
        self.event = bms.Event(self.city, self.pref_venues, self.movie, self.date_ob.Format('%Y%m%d'))
        self.viewer = ui.event.event_wx(self, self.event, self.city_id, self.pref_venues, self.movie, self.date_ob, None, wx.ID_ANY, "",
                               style = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.FULL_REPAINT_ON_RESIZE)

    def run(self):
        try:
            self.check()
            self.quit = True
            for i in range(self._parent.list_ctrl_1.GetItemCount()):
                if int(self._parent.list_ctrl_1.GetItem(i).GetText()) == self.event_id:
                    self._parent.list_ctrl_1.DeleteItem(i)
                    break
        except RuntimeError: pass

    def check(self):
        self.viewer.Show(True)
        try: self.event.config()
        except Exception as ex:
            self.viewer.set_status('Configuration Error', '#c64343')
            wx.MessageBox('Error: {}'.format(str(ex)), 'Config Error - BMS ATC', wx.OK | wx.ICON_ERROR)
            return

        self.viewer.config()
        self.viewer.button_2.Enable(True)

        while True:
            self.viewer.set_status('Status: Running', '#5f9f9f')
            try:
                self.event.get_shows()
            except Exception as ex:
                self.viewer.set_status('Error: {}'.format(str(ex)), '#c64343')

            if not self.event.tickets_available():
                for _ in range(5*4*60):
                    if self.quit:
                        return
                    time.sleep(.25)
            else: break

        self.viewer.button_2.Enable(False)
        self.viewer.set_status('TICKETS AVAILABLE!', '#00d86c')

        pref = False if len(self.pref_venues) > 0 else True
        for venue_id in self.event.shows.keys():
            pref = pref or venue_id in self.pref_venues
        if pref: self.event.send_push()

        wx.MessageBox('{} available in {} on {}! BOOK NOW!'.format(self.event.title, self.city, self.date_ob.Format('%d/%m/%Y')), 'AVAILABLE - BMS ATC', wx.OK | wx.ICON_INFORMATION)