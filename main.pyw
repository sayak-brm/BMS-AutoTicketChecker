#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import wx

import bms
import ui.main

class AutoTicketChecker(wx.App):
    def OnInit(self):
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        self.frame = ui.main.main_wx(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = AutoTicketChecker(0)
    app.MainLoop()
