#!/usr/bin/env python2

# TODO 
# - titre
# - prevoir le fondu en lsv 
# - reecrire l'equivalent de run.py dans ce fichier 
# (grosso-modo, ajouter la gestion de la fenetre)

import wx
import wx.lib.colourselect as csel
import time

import mod

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

    customColorsButtons = []

    # Pour stocker les boutons, on utilise une liste comme un tableau
    buttons = [] 

    currentColorButton = None

    currentFrame = 1
    currentFrameSpin = None
    maxFrameSpin = None

    blendTimeSpin = None
    blendFramesSpin = None

    copyFrameSpin = None

    values = {}
    
    currentPath = ""

    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        self.SetAutoLayout(True)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        t = wx.StaticText(self, -1,
                          "Select color for each frame to create an animation (frame 1 to <Last frame>).\n"
                          "Between two consecutive frames, the light is gradually modified by a color blend\n"
                          "of the specified number of additional frames. Set 0 additional frames for a simple\n"
                          "transition with no blend at all.\n"
                          "On every color button, clicks have following effects:\n"
                          "- left click: opens a color choice menu\n"
                          "- middle click: replace hovered button color with 'current' color\n"
                          "- right click: replace 'current' color with hovered button color\n"
                          )
        mainSizer.Add(t, 0, wx.ALL, 3)


        # Bouton de la couleur courante (on a besoin de le creer en avance)
        self.currentColorButton = csel.ColourSelect(self, -1, "", self.defaultColor, 
                                                    size = wx.DefaultSize)

        # b = wx.Button(self, -1, "Show All Colours")
        # self.Bind(wx.EVT_BUTTON, self.OnShowAll, id=b.GetId())
        # mainSizer.Add(b, 0, wx.ALL, 3)

        # Bouton de selection de la frame
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

        b = wx.Button(self, -1, "Play animation") 
        self.Bind(wx.EVT_BUTTON, self.OnPlayAnimation, id=b.GetId())
        frameSelectionSizer.Add(b, 0, wx.ALL, 3)


        
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

        self.customColorsButtons = [None for i in range(0, self.customColorsNumber)]
        for i in range(0, self.customColorsNumber):
            b = mod.ModColourSelect(self, -1, "", self.customColors[i], wx.DefaultSize,
                                    self.currentColorButton.GetColour, 
                                    self.currentColorButton.SetColour)
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
        b = self.currentColorButton # Deja cree
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
        self.rangeEndSpin = sc
        sc.SetRange(1, self.ledNumber)
        sc.SetValue(1)
        currentColorSizer.Add(sc, 0, wx.ALL, 3)

        currentColorSizer.Add(wx.StaticText(self, -1, "(included)"), 0, wx.ALL, 3)

        b = wx.Button(self, -1, "Paste") 
        self.Bind(wx.EVT_BUTTON, self.OnMakeRange, id=b.GetId())
        currentColorSizer.Add(b, 0, wx.ALL, 3)


        # Boutons d'actions
        actionsSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(actionsSizer, 0, wx.ALL, 3)

        b = wx.Button(self, -1, "Open") 
        self.Bind(wx.EVT_BUTTON, self.OnOpen, id=b.GetId())
        actionsSizer.Add(b, 0, wx.ALL, 3)

        b = wx.Button(self, -1, "Save as") 
        self.Bind(wx.EVT_BUTTON, self.OnSaveAs, id=b.GetId())
        actionsSizer.Add(b, 0, wx.ALL, 3)

        b = wx.Button(self, -1, "Save") 
        self.Bind(wx.EVT_BUTTON, self.OnSave, id=b.GetId())
        actionsSizer.Add(b, 0, wx.ALL, 3)


        self.Layout()
        mainSizer.Fit(self)

        

    def BuildButtons(self, colorSizer):
        self.buttons = [None for i in range(0, self.ledNumber)]

        def f(l, sizer):
            for i in l:
                b = mod.ModColourSelect(self, -1, str(i), self.defaultColor, wx.DefaultSize,
                                        self.currentColorButton.GetColour, 
                                        self.currentColorButton.SetColour)

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


    def saveCurrentFrame(self):
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

        self.currentFrame = frame
        
        print "Loaded ",
        print self.values[frame],
        print "for frame " + str(frame)


    def writeValues(self, output):
        None # TODO


    def OnCurrentFrameSelected(self, event):
        self.saveCurrentFrame()
        # TODO : load
        self.loadValues(self.currentFrameSpin.GetValue())

        #self.currentFrame = self.currentFrameSpin.GetValue()

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



    def OnSpin(self, evt):
        # FIXME : sert a qqchose ?
        []
        


    def OnPlayAnimation(self, evt):
        self.saveCurrentFrame()

        # TODO
        for frame in range(1, self.maxFrameSpin.GetValue() + 1):
            self.loadValues(frame)

            self.currentFrameSpin.SetValue(frame)

            self.Update()
            
            # TODO : faire les frames intermediaires
            (_, s, _) = self.values[frame]
            time.sleep(s / 1000.0)




    def OnOpen(self, evt):
        # TODO : gerer le contenu non-sauvegarde
        openFileDialog = wx.FileDialog(self,  "Open LNA file", "", "",
                                       "LedNuit Animation files (*.lna)|*.lna", 
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # Annule


        self.currentPath = openFileDialog.GetPath() 
        

        f = open(self.currentPath, 'r')

        self.loadFromFile(f)

        f.close()



    def AskSavePath(self):
        saveFileDialog = wx.FileDialog(self, "Open LNA file", "", "",
                                       "LedNuit Animation files (*.lna)|*.lna", 
                                       wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return False

        path = saveFileDialog.GetPath()

        if not path.endswith(".lna"):
            path += ".lna"


        self.currentPath = path
        print "Write to: " + path

        return True
        
    def OnSaveAs(self, evt):
        if(self.AskSavePath()):
            self.OnSave(evt)

        
    def OnSave(self, event):
        self.saveCurrentFrame()

        if self.currentPath == "":
            if not self.AskSavePath():
                return # On ne nous a pas donne de path

        
        f = open(self.currentPath, 'w')

        self.writeToFile(f)

        f.close()



    def OnMakeRange(self, event):
        begin = self.rangeBeginSpin.GetValue()
        end = self.rangeEndSpin.GetValue()

        color = self.currentColorButton.GetColour()

        for i in range(begin, end + 1):
            self.buttons[i - 1].SetColour(color)


    def writeToFile(self, f):
        # On indique le format, juste au cas ou on veuille le modifier plus tard
        f.write("Format:1\n")

        for frame in range(1, self.maxFrameSpin.GetValue() + 1):
            f.write(repr(self.values[frame]) + "\n")

    # TODO : attention, cette fonction plante probablement assez salement sur des mauvais fichiers
    def loadFromFile(self, f):
        # Pour l'instant, on n'utilise pas la ligne de format
        f.readline()

        frame = 0
        
        for line in f:
            frame += 1
            # FIXME : attention, on fait un simple eval... Pas tres robuste...
            self.values[frame] = eval(line)

        self.currentFrameSpin.SetValue(1)
        self.maxFrameSpin.SetValue(frame)

        self.loadValues(1)

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