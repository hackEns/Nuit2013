import wx
import wx.lib.colourselect as csel

class ModColourSelect(csel.ColourSelect):

    getMainColor = None
    setMainColor = None
    
    def __init__(self, parent, id, label, colour, size, getMainColor, setMainColor):
        csel.ColourSelect.__init__(self, parent, id, label, colour, size = size)

        self.getMainColor = getMainColor
        self.setMainColor = setMainColor

        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleClick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)

    def OnMiddleClick(self, event):
        self.SetColour(self.getMainColor())

    def OnRightClick(self, event):
        self.setMainColor(self.GetColour())