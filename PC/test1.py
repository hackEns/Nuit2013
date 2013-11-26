#!/usr/bin/env python2

# TODO 
# - titre
# - prevoir le fondu en lsv 
# - actions
# - 

import  wx
import  wx.lib.colourselect as  csel

#----------------------------------------------------------------------------

class TestColourSelect(wx.Panel):
    
    # Parametres
    sep = 13
    ledNumber = 26

    defaultColor = (0, 0, 0)
    defaultBlendTime = 100
    defaultBlendFrames = 0


    # Donnees
    customColorsNumber = 12
    customColors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
        (255, 255, 255),
        ]
    customColors.extend(
        [defaultColor for i in range(len(customColors), customColorsNumber)]
        ) # Ajouter le bon nombre de "defaut" pour que la liste soit de la bonne taille
    print customColors


    # Pour stocker les boutons, on utilise une liste comme un tableau
    buttons = [] 


    currentFrame = 1
    currentFrameSpin = 0 # Dummy value
    maxFrameSpin = 0 # Dummy

    blendTimeSpin = 0 # Dummy
    blendFramesSpin = 0 # Dummy

    copyFrameSpin = 0 # Dummy

    values = {}


    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        self.SetAutoLayout(True)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        t = wx.StaticText(self, -1,
                          "Select color for each frame to create an animation (frame 1 to <Last frame>).\n"
                          "Between two consecutive frames, the light is gradually modified by a color blend\n"
                          "of TODO"
                          )
        mainSizer.Add(t, 0, wx.ALL, 3)


        # b = wx.Button(self, -1, "Show All Colours")
        # self.Bind(wx.EVT_BUTTON, self.OnShowAll, id=b.GetId())
        # mainSizer.Add(b, 0, wx.ALL, 3)

        # Bouton de selection de la frame
        # TODO : on modified => last augmente
        frameSelectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(frameSelectionSizer)
        
        frameSelectionSizer.Add(wx.StaticText(self, -1, "Frame:"), 0, wx.ALL, 3)

        sc = wx.SpinCtrl(self, -1, "", (30, 50))
        self.currentFrameSpin = sc
        sc.SetRange(1,100000)
        sc.SetValue(self.currentFrame)
        frameSelectionSizer.Add(sc, 0, wx.ALL, 3)
        self.Bind(wx.EVT_SPINCTRL, self.OnCurrentFrameSelected, sc)

        frameSelectionSizer.Add(wx.StaticText(self, -1, 7 * " " + "Last frame:"), 0, wx.ALL, 3)

        sc = wx.SpinCtrl(self, -1, "", (30, 50))
        self.maxFrameSpin = sc
        sc.SetRange(1,100000)
        sc.SetValue(1)
        frameSelectionSizer.Add(sc, 0, wx.ALL, 3)
        self.Bind(wx.EVT_SPINCTRL, self.OnSpin, sc)

        
        # Frame copying
        frameCopySizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(frameCopySizer)
        
        frameCopySizer.Add(wx.StaticText(self, -1, "Copy colors from frame "), 0, wx.ALL, 3)

        sc = wx.SpinCtrl(self, -1, "", (30, 50))
        self.copyFrameSpin = sc
        sc.SetRange(1,100000)
        sc.SetValue(1)
        frameCopySizer.Add(sc, 0, wx.ALL, 3)
        self.Bind(wx.EVT_SPINCTRL, self.OnSpin, sc)


        b = wx.Button(self, -1, "Copy") 
        self.Bind(wx.EVT_BUTTON, self.OnCopyColors, id=b.GetId())
        frameCopySizer.Add(b, 0, wx.ALL, 3)




        # colorSizer = wx.FlexGridSizer(1, 2) # sizer to contain all the example buttons
        # colorSizer = wx.GridSizer(1, 2) # sizer to contain all the example buttons
        # colorSizer = wx.BoxSizer(wx.HORIZONTAL) # sizer to contain all the example buttons
        
        mainSizer.Add(wx.StaticText(self, -1, "Leds colors for current frame:"), 0, wx.ALL, 3)


        f = (lambda : wx.BoxSizer(wx.HORIZONTAL))
        colorSizer = [f (), f ()]

        # build each button and save a reference to it
        self.BuildButtons(colorSizer)
        
        
        # TODO : sur 2 lignes
        # TODO : bouton de rappel dernieres couleurs, couleurs perso

        for i in colorSizer :
            mainSizer.Add(i, 0, wx.ALL, 3)



        # Controle du temps de la frame
        frameSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(frameSizer)
        
        frameSizer.Add(wx.StaticText(self, -1, "Blend time (ms):"), 0, wx.ALL, 3)
        
        sc = wx.SpinCtrl(self, -1, "", (30, 50))
        self.blendTimeSpin = sc
        sc.SetRange(1,100000)
        sc.SetValue(self.defaultBlendTime)
        frameSizer.Add(sc, 0, wx.ALL, 3)

        frameSizer.Add(wx.StaticText(self, -1, 7 * " " + "Blend (additional) frames:"), 0, wx.ALL, 3)
        
        sc = wx.SpinCtrl(self, -1, "", (30, 50))
        self.blendFramesSpin = sc
        sc.SetRange(0,255)
        sc.SetValue(self.defaultBlendFrames)
        frameSizer.Add(sc, 0, wx.ALL, 3)



        # Boutons des couleurs perso
        mainSizer.Add(wx.StaticText(self, -1, "Custom colors:"), 0, wx.ALL, 3)
        
        customColorsSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(customColorsSizer, 0, wx.ALL, 3)

        self.customColorsButtons = range(0, self.customColorsNumber)
        for i in range(0, self.customColorsNumber):
            b = csel.ColourSelect(self, -1, "", self.customColors[i], size = wx.DefaultSize)
            self.customColorsButtons[i] = b
            
            b.Bind(csel.EVT_COLOURSELECT, self.OnSelectColour)
            # b.Bind(csel.EVT_BUTTON, f)

            customColorsSizer.AddMany([
                    (b, 0, wx.ALL, 3),
                    ])



        # Couleur courante, creation de range
        currentColorSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(currentColorSizer, 0, wx.ALL, 3)
        
        currentColorSizer.Add(wx.StaticText(self, -1, "Current color:"), 0, wx.ALL, 3)
        b = csel.ColourSelect(self, -1, "", self.defaultColor, size = wx.DefaultSize)
        # b.Bind(csel.EVT_COLOURSELECT, self.OnSelectColour)
        currentColorSizer.Add(b)


        currentColorSizer.Add(wx.StaticText(self, -1, 7 * " " + "Paste on"), 0, wx.ALL, 3)
        sc = wx.SpinCtrl(self, -1, "", (30, 50))
        self.rangeBeginSpin = sc
        sc.SetRange(1, self.ledNumber)
        sc.SetValue(1)
        currentColorSizer.Add(sc, 0, wx.ALL, 3)
        
        currentColorSizer.Add(wx.StaticText(self, -1, "(included) to"), 0, wx.ALL, 3)
        sc = wx.SpinCtrl(self, -1, "", (30, 50))
        self.rangeBeginSpin = sc
        sc.SetRange(1, self.ledNumber)
        sc.SetValue(1)
        currentColorSizer.Add(sc, 0, wx.ALL, 3)

        currentColorSizer.Add(wx.StaticText(self, -1, "(included)"), 0, wx.ALL, 3)

        b = wx.Button(self, -1, "Paste") 
        # TODO
        # self.Bind(wx.EVT_BUTTON, self.OnCreateRange, id=b.GetId())
        currentColorSizer.Add(b, 0, wx.ALL, 3)

        

        self.Layout()

        

    def BuildButtons(self, colorSizer):
        self.buttons = range(0, self.ledNumber)

        def f(l, sizer):
            for i in l:
                b = csel.ColourSelect(self, -1, str(i), self.defaultColor, size = wx.DefaultSize)
                self.buttons[i - 1] = b

                b.Bind(csel.EVT_COLOURSELECT, self.OnSelectColour)
                
                sizer.AddMany([
                        (b, 0, wx.ALL, 3),
                        ])
                

        f(range(1, self.sep + 1), colorSizer[0])
        f(range(self.sep + 1, self.ledNumber + 1), colorSizer[1])



    def getColors(self):
        f = lambda t : t[0:4] 
        return [f(self.buttons[i].GetColour()) for i in range(0, self.ledNumber)] # TODO
        

    def setColors(self, colors):
        for i, c in list(enumerate(colors)):
            self.buttons[i].SetColour(c)
            


    def createDefaultValue(self, frame):
        self.values[frame] = ([self.defaultColor for i in range(1, self.ledNumber + 1)], 
                              self.defaultBlendTime, self.defaultBlendFrames)


    def saveCurrentValues(self):
        self.values[self.currentFrame] = (self.getColors(),
                                          self.blendTimeSpin.GetValue(),
                                          self.blendFramesSpin.GetValue()
                                          )

        print "Stored ",
        print self.values[self.currentFrame],
        print "for frame " + str(self.currentFrame)


    def loadValues(self, frame):
        if not (frame in self.values):
            self.createDefaultValue(frame)

        (colors, blendTime, blendFrames) = self.values[frame]

        self.setColors(colors)

        self.blendTimeSpin.SetValue(blendTime)
        self.blendFramesSpin.SetValue(blendFrames)

        print "Loaded ",
        print self.values[frame],
        print "for frame " + str(frame)


    def OnCurrentFrameSelected(self, event):
        self.saveCurrentValues()
        # TODO : load
        self.loadValues(self.currentFrameSpin.GetValue())

        self.currentFrame = self.currentFrameSpin.GetValue()

        if (self.maxFrameSpin.GetValue() < self.currentFrame) :
            self.maxFrameSpin.SetValue(self.currentFrame)


    def OnSelectColour(self, event):
        # TODO : rappel dernieres couleurs
        self.log.WriteText("Colour selected: %s" % str(event.GetValue()))


    def OnCopyColors(self, event):
        target = self.copyFrameSpin.GetValue()

        if target in self.values:
            self.setColors(self.values[target][0])

            print "Copied colors from frame " + str(target)

        else:
            print "Error, no information stored about frame " + str(target)

    # def OnShowAll(self, event):
    #     # show the state of each button
    #     result = []
    #     colour = self.colourDefaults.GetColour() # default control value
    #     result.append("Default Colour/Size: " + str(colour))

    #     for name, button in self.buttonRefs:
    #         colour = button.GetColour() # get the colour selection button result
    #         result.append(name + ": " + str(colour))  # create string list for easy viewing of results

    #     out_result = ',  '.join(result)
    #     self.log.WriteText("Colour Results: " + out_result + "\n")



    def OnSpin(self, evt):
        # TODO
        []
        




#---------------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestColourSelect(nb, log)
    return win

#---------------------------------------------------------------------------




overview = """\
A coloured button that when clicked allows the user to select a colour from the wxColourDialog.
"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
