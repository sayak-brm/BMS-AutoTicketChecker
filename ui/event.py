"""
   Copyright 2019-2021 Sayak Brahmacahri

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

import wx
import wx.adv

import bms

class event_wx(wx.Frame):
    def __init__(self, parent, event, city_id, pref_venues, movie, date, *args, **kwds):
        self.event = event
        self.channel = ''
        self.url = ''
        self._parent = parent
        self.city_id = city_id
        self.pref_venues = ','.join(pref_venues) if len(pref_venues) > 0 else ''
        self.movie = movie
        self.date = date

        # begin wxGlade: event_wx.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((450, 282))
        self.SetSizeHints(450, 282, 450, 282)
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.choice_city = wx.Choice(self.panel_1, wx.ID_ANY, choices=bms.Event.get_cities())
        self.text_ctrl_venues = wx.TextCtrl(self.panel_1, wx.ID_ANY, self.pref_venues)
        self.text_ctrl_movie = wx.TextCtrl(self.panel_1, wx.ID_ANY, self.movie)
        self.datepicker_ctrl_2 = wx.adv.DatePickerCtrl(self.panel_1, wx.ID_ANY, style=wx.adv.DP_DEFAULT | wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        self.button_2 = wx.Button(self.panel_1, wx.ID_STOP, "")
        self.hyperlink_3 = wx.adv.HyperlinkCtrl(self.panel_1, wx.ID_ANY, "BUY NOW", "")
        self.hyperlink_2 = wx.adv.HyperlinkCtrl(self.panel_1, wx.ID_ANY, "Subscribe to Notifications", "", style=wx.adv.HL_ALIGN_CENTRE)
        self.label_8 = wx.StaticText(self.panel_1, wx.ID_ANY, "", style=wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE)
        self.label_8.SetForegroundColour(wx.Colour(255, 255, 255))
        self.label_8.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))

        self.city = self.choice_city.GetString(self.city_id)

        self.__set_properties()
        self.__do_layout()
        self.SetSizeHints(450, 282, 450, 282)

        self.Bind(wx.EVT_BUTTON, self.handle_stop, self.button_2)
        self.Bind(wx.EVT_CLOSE, self.handle_close, self)
        # end wxGlade

        self.set_status('Status: Not Configured', '#7f7f7f')
        self.choice_city.SetSelection(self.city_id)
        self.datepicker_ctrl_2.SetValue(self.date)

    def config(self):
        self.channel = self.event.get_channel()
        if self.event.urls: self.url = self.event.urls[0]
        else: self.url = 'https://in.bookmyshow.com'
        self.hyperlink_2.SetURL(self.channel)
        self.hyperlink_2.SetLabel('Subscribe: {}'.format(self.channel))
        self.hyperlink_3.SetURL(self.url)
        self.set_status('Status: Configured', '#999932')
        self.hyperlink_3.Show()
        self.hyperlink_2.Show()
        self.SetSizeHints(450, 317, 450, 317)
        self.SetSize((450, 317))

    def set_status(self, msg, col):
        if self.event.urls: self.url = self.event.urls[0]
        else: self.url = 'https://in.bookmyshow.com'
        self.hyperlink_2.SetURL(self.channel)
        self.label_8.SetLabel(msg)
        get_rgb = lambda h: tuple(int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        self.label_8.SetBackgroundColour(wx.Colour(*get_rgb(col)))

    def __set_properties(self):
        # begin wxGlade: event_wx.__set_properties
        self.SetTitle("{}-{} - BMS ATC".format(self.city, self.movie))
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap(bms.cd + "/res/icon.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.choice_city.Enable(False)
        self.choice_city.SetSelection(0)
        self.text_ctrl_venues.Enable(False)
        self.text_ctrl_movie.Enable(False)
        self.datepicker_ctrl_2.Enable(False)
        self.button_2.SetBitmap(wx.Bitmap(bms.cd + "/res/error_small.png", wx.BITMAP_TYPE_ANY))
        self.button_2.Enable(False)
        self.hyperlink_3.Hide()
        self.hyperlink_2.Hide()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: event_wx.__do_layout
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_3 = wx.GridBagSizer(10, 10)
        grid_sizer_3.Add(self.label_8, (0, 0), (1, 2), wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
        label_9 = wx.StaticText(self.panel_1, wx.ID_ANY, "City")
        grid_sizer_3.Add(label_9, (1, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_3.Add(self.choice_city, (1, 1), (1, 1), wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        label_10 = wx.StaticText(self.panel_1, wx.ID_ANY, "Pref. Venues")
        grid_sizer_3.Add(label_10, (2, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_3.Add(self.text_ctrl_venues, (2, 1), (1, 1), wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        label_11 = wx.StaticText(self.panel_1, wx.ID_ANY, "Search Movie")
        grid_sizer_3.Add(label_11, (3, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_3.Add(self.text_ctrl_movie, (3, 1), (1, 1), wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        label_12 = wx.StaticText(self.panel_1, wx.ID_ANY, "Date")
        grid_sizer_3.Add(label_12, (4, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_3.Add(self.datepicker_ctrl_2, (4, 1), (1, 1), wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        grid_sizer_3.Add(self.button_2, (5, 0), (1, 2), wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
        grid_sizer_3.Add(self.hyperlink_3, (6, 0), (1, 1), 0, 0)
        grid_sizer_3.Add(self.hyperlink_2, (6, 1), (1, 1), wx.ALIGN_CENTER, 0)
        grid_sizer_3.AddGrowableCol(1)
        sizer_10.Add(grid_sizer_3, 1, wx.ALL | wx.EXPAND, 5)
        self.panel_1.SetSizer(sizer_10)
        sizer_9.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_9)
        self.Layout()
        # end wxGlade

    def handle_stop(self, event):  # wxGlade: event_wx.<event_handler>
        self._parent.quit = True
        self.button_2.Enable(False)
        self.set_status('Status: Stopped', '#999932')
        event.Skip()

    def handle_close(self, event):  # wxGlade: event_wx.<event_handler>
        self.Show(False)
        if self._parent.quit == True:
            event.Skip()
            self.Destroy()