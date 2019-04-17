import time

import wx
import wx.adv

import bms
import event as evh

class main_wx(wx.Frame):
    def __init__(self, *args, **kwds):
        self.event_handlers = []

        # begin wxGlade: main_wx.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((450, 273))
        self.notebook_1 = wx.Notebook(self, wx.ID_ANY)
        self.notebook_1_Start = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.choice_1 = wx.Choice(self.notebook_1_Start, wx.ID_ANY, choices=bms.Event.get_cities())
        self.text_ctrl_2 = wx.TextCtrl(self.notebook_1_Start, wx.ID_ANY, "")
        self.text_ctrl_1 = wx.TextCtrl(self.notebook_1_Start, wx.ID_ANY, "")
        self.datepicker_ctrl_1 = wx.adv.DatePickerCtrl(self.notebook_1_Start, wx.ID_ANY, style=wx.adv.DP_DEFAULT | wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        self.button_quit = wx.Button(self.notebook_1_Start, wx.ID_EXIT, "")
        self.button_check = wx.Button(self.notebook_1_Start, wx.ID_ANY, "Check Tickets")
        self.notebook_1_Running = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.list_ctrl_1 = wx.ListCtrl(self.notebook_1_Running, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES)
        self.notebook_1_About = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.hyperlink_1 = wx.adv.HyperlinkCtrl(self.notebook_1_About, wx.ID_ANY, "https://github.com/sayak-brm/BMS-AutoTicketChecker", "https://github.com/sayak-brm/BMS-AutoTicketChecker", style=wx.adv.HL_ALIGN_CENTRE)

        self.__set_properties()
        self.__do_layout()
        self.SetSizeHints(self.GetSize().x, self.GetSize().y,self.GetSize().x, self.GetSize().y)

        self.Bind(wx.EVT_BUTTON, self.handle_quit, self.button_quit)
        self.Bind(wx.EVT_BUTTON, self.handle_check, self.button_check)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.handle_event, self.list_ctrl_1)
        self.Bind(wx.EVT_CLOSE, self.handle_quit, self)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: main_wx.__set_properties
        self.SetTitle("BMS AutoTicketChecker")
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(wx.Bitmap(bms.cd + "/res/icon.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.button_quit.SetBitmap(wx.Bitmap(bms.cd + "/res/error_small.png", wx.BITMAP_TYPE_ANY))
        self.button_check.SetBitmap(wx.Bitmap(bms.cd + "/res/check_small.png", wx.BITMAP_TYPE_ANY))
        self.list_ctrl_1.AppendColumn("", format=wx.LIST_FORMAT_LEFT, width=0)
        self.list_ctrl_1.AppendColumn("City", format=wx.LIST_FORMAT_LEFT, width=100)
        self.list_ctrl_1.AppendColumn("Pref. Venues", format=wx.LIST_FORMAT_LEFT, width=100)
        self.list_ctrl_1.AppendColumn("Movie", format=wx.LIST_FORMAT_LEFT, width=100)
        self.list_ctrl_1.AppendColumn("Date", format=wx.LIST_FORMAT_LEFT, width=100)
        self.hyperlink_1.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT, 0, ""))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: main_wx.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.GridBagSizer(10, 10)
        label_city = wx.StaticText(self.notebook_1_Start, wx.ID_ANY, "City")
        grid_sizer_1.Add(label_city, (0, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.choice_1, (0, 1), (1, 1), wx.EXPAND, 0)
        label_venues = wx.StaticText(self.notebook_1_Start, wx.ID_ANY, "Pref. Venues")
        grid_sizer_1.Add(label_venues, (1, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_2, (1, 1), (1, 1), wx.EXPAND, 0)
        label_movie = wx.StaticText(self.notebook_1_Start, wx.ID_ANY, "Search Movie")
        grid_sizer_1.Add(label_movie, (2, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.text_ctrl_1, (2, 1), (1, 1), wx.EXPAND, 0)
        label_date = wx.StaticText(self.notebook_1_Start, wx.ID_ANY, "Date")
        grid_sizer_1.Add(label_date, (3, 0), (1, 1), wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.datepicker_ctrl_1, (3, 1), (1, 1), wx.EXPAND, 0)
        grid_sizer_1.Add(self.button_quit, (4, 0), (1, 1), wx.EXPAND, 0)
        grid_sizer_1.Add(self.button_check, (4, 1), (1, 1), wx.EXPAND, 0)
        grid_sizer_1.AddGrowableCol(1)
        sizer_2.Add(grid_sizer_1, 1, wx.ALL | wx.EXPAND, 2)
        self.notebook_1_Start.SetSizer(sizer_2)
        sizer_3.Add(self.list_ctrl_1, 1, wx.ALL | wx.EXPAND, 0)
        self.notebook_1_Running.SetSizer(sizer_3)
        bitmap_1 = wx.StaticBitmap(self.notebook_1_About, wx.ID_ANY, wx.Bitmap(bms.cd + "/res/about.png", wx.BITMAP_TYPE_ANY))
        bitmap_1.SetMinSize((84, 84))
        sizer_5.Add(bitmap_1, 0, wx.ALIGN_CENTER | wx.TOP, 13)
        label_title = wx.StaticText(self.notebook_1_About, wx.ID_ANY, "BMS AutoTicketChecker")
        label_title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_5.Add(label_title, 0, wx.ALIGN_CENTER, 0)
        label_author = wx.StaticText(self.notebook_1_About, wx.ID_ANY, "Version: 0.3.3", style=wx.ALIGN_CENTER)
        label_author.SetFont(wx.Font(9, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT, 0, ""))
        sizer_5.Add(label_author, 0, wx.ALIGN_CENTER, 0)
        label_5 = wx.StaticText(self.notebook_1_About, wx.ID_ANY, "Author: @sayakbrm (GitHub)")
        label_5.SetFont(wx.Font(9, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT, 0, ""))
        sizer_5.Add(label_5, 0, wx.ALIGN_CENTER, 0)
        sizer_5.Add(self.hyperlink_1, 0, wx.ALIGN_CENTER, 0)
        sizer_4.Add(sizer_5, 1, wx.EXPAND, 0)
        self.notebook_1_About.SetSizer(sizer_4)
        self.notebook_1.AddPage(self.notebook_1_Start, "Start")
        self.notebook_1.AddPage(self.notebook_1_Running, "Movies")
        self.notebook_1.AddPage(self.notebook_1_About, "About")
        sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def handle_quit(self, event):  # wxGlade: main_wx.<event_handler>
        for event_handler in self.event_handlers:
            event_handler.quit = True
            try: event_handler.viewer.Destroy()
            except RuntimeError: pass
        time.sleep(.5)
        event.Skip()
        self.Destroy()

    def handle_check(self, event):  # wxGlade: main_wx.<event_handler>
        city = self.choice_1.GetSelection()
        pref_venues = self.text_ctrl_2.GetLineText(0)
        movie = self.text_ctrl_1.GetLineText(0)
        date = self.datepicker_ctrl_1.GetValue()
        ev_id = self.list_ctrl_1.Append([len(self.event_handlers), self.choice_1.GetString(city), pref_venues, movie, date.Format('%Y%m%d')])
        ev = evh.EventHandler(self, len(self.event_handlers), city, pref_venues, movie, date)
        ev.start()
        self.event_handlers.append(ev)
        event.Skip()

    def handle_event(self, event):  # wxGlade: main_wx.<event_handler>
        self.event_handlers[int(self.list_ctrl_1.GetItemText(event.GetIndex()))].viewer.Show(True)
        event.Skip()