import tkinter as tk
import tkinter.filedialog as tkfile
import tkinter.messagebox as tkmsg
import tkinter.colorchooser as tkcolor
import os
import sys
import re

# Simple xbm Image Editor
# Python 3.x; developed on a Windows 10 PC
# Author: Mike Cavender
# License: New BSD; see License.txt
# Classes:
#   BitLabel   Tkinter Label wrapper
#   XbmFile    xbm file I/O, record parsing and composition
#   XbmEditor  user interface, bitmap editing

# -------------------- Class BitLabel --------------------

class BitLabel(tk.Label):
    # This Tkinter Label widget wrapper just adds two attributes
    # to edit grid Labels in a documented fashion

    def __init__(self, parent, pRow, pCol, pState, **kwargs):
        self.location = 'R'+str(pRow+1)+' C'+str(pCol+1) # Row/col of Label
        self.state = pState                         # Foreground or background
        tk.Label.__init__(self, parent, **kwargs)

# -------------------- Class XbmFile --------------------

class XbmFile:
    # This class contains xbm file i/o, record parsing and composition methods

    def __init__(self, pWdth, pHgt):
        self.file = ''             # Current bitmap file
        self.inNm = ''             # Internal bitmap name
        self.wdth = pWdth          # Bitmap width
        self.hgt = pHgt            # Bitmap height

    # -------------------- Input methods --------------------

    def parseFile(self):
        # Parse the input xbm file
        iBytLst = []
        fIn = open(self.file)

        for rcd in fIn:
            wdthMtch = re.search('#define.+width ([0-9]+)', rcd)
            if wdthMtch == None:
                hgtMtch = re.search('#define.+height ([0-9]+)', rcd)
                if hgtMtch == None:
                    # Get the 0x.. strings
                    bitMtchLst = re.findall(r'(0[xX][0-9a-fA-F][0-9a-fA-F])',
                                            rcd)
                    # Extract the hex characters
                    for ent in bitMtchLst:
                        iBytLst.append(ent[2:])
                else:
                    # Get the height
                    self.hgt = int(hgtMtch.group(1))
            else:
                # Get the width
                self.wdth = int(wdthMtch.group(1))
                # Get the name
                namMtchLst = re.split('_width', rcd)
                namIx = namMtchLst[0].rfind(' ')
                if namIx > -1:
                    self.inNm = namMtchLst[0][namIx+1:]

        fIn.close()

        iBytAr = bytearray.fromhex(''.join(iBytLst))
        return iBytAr

    def extractBits(self, iBytAr):
        # Convert input bitmap bytes to bits
        iLen = len(iBytAr)
        iIx = -1
        row = 0
        bitGrid = {}
        # For each bitmap row
        while row < self.hgt and iIx < iLen:
            # Discard any leftover bits from the previous row
            bCt = 8
            # For each bitmap column
            for col in range(0, self.wdth):
                # Reverse bits in each byte; low-order becomes high-order
                if bCt > 7:
                    # Get the next bitmap byte
                    iIx += 1
                    if iIx < iLen:
                        byt = iBytAr[iIx]
                        bCt = 0
                    else:
                        # This will not happen for valid xbm files
                        break
                # Get the next bitmap bit
                byt, bit = divmod(byt, 2)
                bCt += 1
                bitGrid[row,col] = bit
            row += 1

        return (bitGrid)

    def bldEmptyBitGrid(self):
        bitGrid = {}
        for gRow in range(0, self.hgt):
            for gCol in range(0, self.wdth):
                bitGrid[gRow,gCol] = 0
        return bitGrid

    # -------------------- Output methods --------------------

    def buildBytes(self, oBitGrid):
        # Convert grid bits to bitmap bytes
        oBytAr = bytearray()

        # For each bitmap row
        for row in range(0, self.hgt):
            # Setup to process first group - max of 8 bits
            # Group size is origin 1
            if self.wdth < 8:
                grpSz = self.wdth
            else:
                grpSz = 8
            # Bit ix is origin 0
            bIx = grpSz - 1
            fin = 0
            byt = 0
            # For each bitmap column
            for col in range(0, self.wdth):
                # Process each group of bits right-to-left
                # Bit grid bits are reversed in byt
                byt *= 2
                byt += oBitGrid[row,fin+bIx]
                bIx -= 1
                if bIx < 0:
                    # Store a full bitmap byte
                    oBytAr.append(byt)
                    fin += grpSz
                    # Setup for next group - max of 8 bits
                    remain = self.wdth - fin
                    # Group size is origin 1
                    if remain < 8:
                        grpSz = remain
                    else:
                        grpSz = 8
                    # Bit ix is origin 0
                    bIx = grpSz - 1
                    byt = 0

        return oBytAr

    def writeFile(self, oBytAr):
        # Write xbm bitmap file
        oBytStr = oBytAr.hex()
        fOut = open(self.file, 'w')
        fOut.write('#define '+self.inNm+'_width '+str(self.wdth)+'\n')
        fOut.write('#define '+self.inNm+'_height '+str(self.hgt)+'\n')
        fOut.write('static unsigned char '+self.inNm+'_bits[] = {\n')
        oLen = len(oBytStr)
        oBt = 0
        while oBt < oLen:
            oBytLine = ['  ']
            lBt = 0
            while lBt < 8 and oBt < oLen:
                oBytLine.append(' 0x'+oBytStr[oBt]+oBytStr[oBt+1])
                oBt += 2
                if oBt < oLen:
                    oBytLine.append(',')
                else:
                    oBytLine.append('};')
                lBt += 1
            fOut.write(''.join(oBytLine)+'\n')
        fOut.close()

# -------------------- Class XbmEditor --------------------

class XbmEditor:
    # This class contains the user interface and the bitmap editing methods

    def __init__(self):
        self.gridMax = 2500        # Max bitmap grid size
        self.dimMax = 128          # Max bitmap width and height
        self.btnW = 6              # Top btn width in chars
        self.wdthDflt = 16         # Bitmap width default
        self.hgtDflt = 16          # Bitmap height default
        self.fgState = 1           # Foreground bit
        self.bgState = 0           # Background bit
        self.scrFont = ('Verdana', 9, 'normal')

        self.xFile = XbmFile(self.wdthDflt, self.hgtDflt) # I/O class
        self.xImg = None           # tk.BitmapImage()
        self.bImg = None           # Blank tk.BitmapImage for edit grid
        self.fgColor = '#2375fc'   # Foreground color
        self.bgColor = None        # Background color
        self.bgNone = None         # Background color for None
        self.changed = False       # Bitmap changed since last save
        self.scrBits = {}          # Screen bitmap bit dictionary

        # -------------------- Main window --------------------

        self.root = tk.Tk()
        self.root.title('Simple xbm Image Editor')
        self.root.protocol('WM_DELETE_WINDOW', self.wrapUp)

        # -------------------- Screen widgets --------------------

        # -------------------- Button frame --------------------
        btnFrame = tk.Frame(self.root)
        # Exit app
        btnExit = tk.Button(btnFrame, text='Exit', width=self.btnW,
            font=self.scrFont, command=self.exitAppClick)
        btnExit.grid(row=0, column=0, sticky=tk.W)
        # New bitmap
        self.btnNew = tk.Button(btnFrame, text='New', width=self.btnW,
            font=self.scrFont, command=self.newBitmapClick)
        self.btnNew.grid(row=0, column=1, sticky=tk.W)
        # Load bitmap
        self.btnLoad = tk.Button(btnFrame, text='Open', width=self.btnW,
            font=self.scrFont, command=self.loadBitmapClick)
        self.btnLoad.grid(row=0, column=2, sticky=tk.W)
        # Save bitmap
        self.btnSave = tk.Button(btnFrame, text='Save', width=self.btnW,
            font=self.scrFont, command=self.saveBitmapClick)
        self.btnSave.grid(row=0, column=3, sticky=tk.W)
        # Rotate
        self.btnRotate = tk.Button(btnFrame, text='Rotate',
            width=self.btnW, font=self.scrFont, command=self.rotateClick)
        self.btnRotate.grid(row=0, column=4, sticky=tk.W)
        # Help
        btnHelp = tk.Button(btnFrame, text='Help', width=self.btnW,
            font=self.scrFont, command=self.helpClick)
        btnHelp.grid(row=0, column=5, sticky=tk.W)
        # File name
        lblFrFile = tk.LabelFrame(btnFrame, font=self.scrFont)
        self.lblFile = tk.Label(lblFrFile, font=self.scrFont)
        self.lblFile.grid(row=0, column=0, sticky=tk.W, padx=3, pady=3)
        lblFrFile.grid(row=0, column=6, sticky=tk.W, padx=5)
        btnFrame.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        # -------------------- Control frame --------------------
        ctlFrame = tk.Frame(self.root)
        # Internal name
        lblFrNm = tk.LabelFrame(ctlFrame, text='Internal name',
                                font=self.scrFont)
        self.entNm = tk.Entry(lblFrNm, font=self.scrFont, width=10,
                              insertofftime=0, insertwidth=1)
        self.entNm.grid(row=0, column=0, sticky=tk.W, padx=3, pady=6)
        lblFrNm.grid(row=0, column=0, sticky=tk.W, padx=3, pady=3)
        # Width
        lblFrWdth = tk.LabelFrame(ctlFrame, text='Width', font=self.scrFont)
        self.sbWdth = tk.Spinbox(lblFrWdth, font=self.scrFont, from_=1,
                                 to=self.dimMax, width=3, wrap=True,
                                 insertofftime=0, insertwidth=1)
        self.sbWdth.grid(row=0, column=0, sticky=tk.W, padx=3, pady=3)
        for i in range(1, self.wdthDflt):
            self.sbWdth.invoke('buttonup')
        self.btnWdth = tk.Button(lblFrWdth, text='Apply',
            width=self.btnW, font=self.scrFont, command=self.chgWdthClick)
        self.btnWdth.grid(row=0, column=1, sticky=tk.W, padx=3, pady=3)
        lblFrWdth.grid(row=0, column=1, sticky=tk.W, padx=3, pady=3)
        # Height
        lblFrHgt = tk.LabelFrame(ctlFrame, text='Height', font=self.scrFont)
        self.sbHgt = tk.Spinbox(lblFrHgt, font=self.scrFont, from_=1,
                                to=self.dimMax, width=3, wrap=True,
                                insertofftime=0,insertwidth=1)
        self.sbHgt.grid(row=0, column=0, sticky=tk.W, padx=3, pady=3)
        for i in range(1, self.hgtDflt):
            self.sbHgt.invoke('buttonup')
        self.btnHgt = tk.Button(lblFrHgt, text='Apply', width=self.btnW,
                                font=self.scrFont, command=self.chgHgtClick)
        self.btnHgt.grid(row=0, column=1, sticky=tk.W, padx=3, pady=3)
        lblFrHgt.grid(row=0, column=2, sticky=tk.W, padx=3, pady=3)
        # Edit grid location
        lblFrLoc = tk.LabelFrame(ctlFrame, text='Row Col', font=self.scrFont)
        self.lblLoc = tk.Label(lblFrLoc, width=7, font=self.scrFont)
        self.lblLoc.grid(row=0, column=0, padx=3, pady=6)
        lblFrLoc.grid(row=0, column=3, sticky=tk.W, padx=3, pady=3)
        # Foreground
        lblFrFg = tk.LabelFrame(ctlFrame, text='Foreground', font=self.scrFont)
        self.lblFg = tk.Label(lblFrFg, font=self.scrFont,
                              text=self.fgColor, background=self.fgColor)
        self.lblFg.grid(row=0, column=0, sticky=tk.W, padx=3)
        self.btnFg = tk.Button(lblFrFg, text='Change', width=self.btnW,
                               font=self.scrFont, command=self.chgFgClick)
        self.btnFg.grid(row=0, column=1, sticky=tk.W, padx=3, pady=3)
        lblFrFg.grid(row=0, column=4, sticky=tk.W, padx=3, pady=3)
        # Background
        lblFrBg = tk.LabelFrame(ctlFrame, text='Background', font=self.scrFont)
        self.lblBg = tk.Label(lblFrBg, font=self.scrFont)
        if self.bgColor == None:
            self.lblBg.configure(text='None')
        else:
            self.lblBg.configure(text=self.bgColor)
            self.lblBg.configure(background=self.bgColor)
        self.lblBg.grid(row=0, column=0, sticky=tk.W)
        self.btnBg = tk.Button(lblFrBg, text='Change', width=self.btnW,
                               font=self.scrFont, command=self.chgBgClick)
        self.btnBg.grid(row=0, column=1, sticky=tk.W, padx=3, pady=3)
        lblFrBg.grid(row=0, column=5, sticky=tk.W, padx=3, pady=3)
        ctlFrame.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        # -------------------- Bitmap frame --------------------
        bitmapFrame = tk.Frame(self.root)
        # Bitmap - actual size
        lblFrBitmap = tk.LabelFrame(bitmapFrame)
        self.lblBitmap = tk.Label(lblFrBitmap)
        self.lblBitmap.grid(row=0, column=0, padx=7, pady=7)
        lblFrBitmap.grid(row=0, column=0, sticky=tk.N)
        # Get the no-background color
        self.bgNone = self.lblBitmap.cget('background')

        # -------------------- Edit frame --------------------
        self.editFrame = tk.Frame(bitmapFrame)
        # Create a blank image for the edit grid bits and the actual size bitmap
        self.bImg = tk.BitmapImage()
        self.initGifs()
        # Up arrow
        arrUp = tk.PhotoImage(data=self.arrowUp)
        self.btnUp = tk.Button(self.editFrame, image=arrUp,
                               command=self.upArrowClick)
        self.btnUp.arrUp = arrUp
        self.btnUp.grid(row=0, column=1)
        # Left arrow
        arrLeft = tk.PhotoImage(data=self.arrowLeft)
        self.btnLeft = tk.Button(self.editFrame, image=arrLeft,
                                 command=self.leftArrowClick)
        self.btnLeft.arrLeft = arrLeft
        self.btnLeft.grid(row=1, column=0)
        # Right arrow
        arrRight = tk.PhotoImage(data=self.arrowRight)
        self.btnRight = tk.Button(self.editFrame, image=arrRight,
                                  command=self.rightArrowClick)
        self.btnRight.arrRight = arrRight
        self.btnRight.grid(row=1, column=2)
        # Down arrow
        arrDown = tk.PhotoImage(data=self.arrowDown)
        self.btnDown = tk.Button(self.editFrame, image=arrDown,
                                 command=self.downArrowClick)
        self.btnDown.arrDown = arrDown
        self.btnDown.grid(row=2, column=1)
        self.editFrame.grid(row=0, column=1, padx=5, pady=5)

        bitmapFrame.grid(row=2, column=0, padx=5, pady=5)

        # Start with an empty edit grid of default size
        self.newBitmapClick()

    # -------------------- Events --------------------

    def exitAppClick(self):
        self.wrapUp()
    
    def newBitmapClick(self):
        # Check for current work
        self.chkChanged()
        if self.changed == True:
            return
        # See if bitmap is too big to edit
        if self.isBitmapTooBig(self.xFile.wdth, self.xFile.hgt):
            return
        self.btnNew.configure(state=tk.DISABLED)
        self.btnNew.update_idletasks()
        if not self.xFile.file == '':
            splitFldr, splitFile = os.path.split(self.xFile.file)
            self.xFile.file = splitFldr+'/NewImage.xbm'
        self.lblFile.configure(text=self.xFile.file)
        self.delScrBits()
        self.loadScrBits(self.xFile.bldEmptyBitGrid())
        self.lblBitmap.configure(image=self.bImg)
        self.btnNew.configure(state=tk.NORMAL)

    def loadBitmapClick(self):
        # Check for current work
        self.chkChanged()
        if self.changed == True:
            return
        self.btnLoad.configure(state=tk.DISABLED)
        self.btnLoad.update_idletasks()
        if self.xFile.file == '':
            iFile = tkfile.askopenfilename(defaultextension='.xbm',
                filetypes=[('xbm files', '.xbm'), ('all files', '.*')],
                initialdir=os.path.splitdrive(sys.prefix)[0], title='Open')
        else:
            splitFldr, splitFile = os.path.split(self.xFile.file)
            iFile = tkfile.askopenfilename(defaultextension='.xbm',
                filetypes=[('xbm files', '.xbm'), ('all files', '.*')],
                initialdir=splitFldr, initialfile=splitFile, title='Open')
        if not iFile == '':
            self.processInputFile(iFile)
        self.btnLoad.configure(state=tk.NORMAL)

    def saveBitmapClick(self):
        nm = self.entNm.get()
        if nm.isidentifier():
            self.xFile.inNm = nm
        else:
            tkmsg.showerror('Invalid Name',
                    'A valid internal name is required. Internal\n'+ \
                    'name may only contain letters, numbers\n'+ \
                    'and _. It cannot start with a number.')
            return
        self.btnSave.configure(state=tk.DISABLED)
        self.btnSave.update_idletasks()
        if self.xFile.file == '':
            saveFile = tkfile.asksaveasfilename(defaultextension='.xbm',
                filetypes=[('xbm files', '.xbm'), ('all files', '.*')],
                initialdir=os.path.splitdrive(sys.prefix)[0], title='Save')
        else:
            splitFldr, splitFile = os.path.split(self.xFile.file)
            saveFile = tkfile.asksaveasfilename(defaultextension='.xbm',
                filetypes=[('xbm files', '.xbm'), ('all files', '.*')],
                initialdir=splitFldr, initialfile=splitFile, title='Save')
        if not saveFile == '':
            self.saveBitmap(saveFile)
            self.changed = False
        self.btnSave.configure(state=tk.NORMAL)

    def rotateClick(self):
        self.btnRotate.configure(state=tk.DISABLED)
        self.btnRotate.update_idletasks()
        self.rotateEditGrid()
        self.changed = True
        self.btnRotate.configure(state=tk.NORMAL)

    def helpClick(self):
        self.xEditHelp()

    def chgWdthClick(self):
        self.btnWdth.configure(state=tk.DISABLED)
        self.btnWdth.update_idletasks()
        newWdth = self.sbWdth.get()
        if self.isDimValid(newWdth):
            newWdth = int(newWdth)
            if self.isBitmapTooBig(newWdth, self.xFile.hgt):
                self.chgWdthSb(self.xFile.wdth)
            else:
                self.chgEditGridWdth(newWdth)
                self.changed = True
        else:
            self.chgWdthSb(self.xFile.wdth)
        self.btnWdth.configure(state=tk.NORMAL)
        self.btnWdth.focus_set()

    def chgHgtClick(self):
        self.btnHgt.configure(state=tk.DISABLED)
        self.btnHgt.update_idletasks()
        newHgt = self.sbHgt.get()
        if self.isDimValid(newHgt):
            newHgt = int(newHgt)
            if self.isBitmapTooBig(self.xFile.wdth, newHgt):
                self.chgHgtSb(self.xFile.hgt)
            else:
                self.chgEditGridHgt(newHgt)
                self.changed = True
        else:
            self.chgHgtSb(self.xFile.hgt)
        self.btnHgt.configure(state=tk.NORMAL)
        self.btnHgt.focus_set()

    def chgFgClick(self):
        self.btnFg.configure(state=tk.DISABLED)
        self.btnFg.update_idletasks()
        triple, color = tkcolor.askcolor(self.fgColor, parent=self.root,
                                         title='Foreground Color')
        self.chgFgColor(color)
        self.btnFg.configure(state=tk.NORMAL)

    def chgBgClick(self):
        self.btnBg.configure(state=tk.DISABLED)
        self.btnBg.update_idletasks()
        triple, color = tkcolor.askcolor(self.bgColor, parent=self.root,
                                         title='Background Color')
        self.chgBgColor(color)
        self.btnBg.configure(state=tk.NORMAL)

    def upArrowClick(self):
        self.btnUp.configure(state=tk.DISABLED)
        self.btnUp.update_idletasks()
        self.shiftEditGridUp()
        self.changed = True
        self.btnUp.configure(state=tk.NORMAL)

    def leftArrowClick(self):
        self.btnLeft.configure(state=tk.DISABLED)
        self.btnLeft.update_idletasks()
        self.shiftEditGridLeft()
        self.changed = True
        self.btnLeft.configure(state=tk.NORMAL)

    def rightArrowClick(self):
        self.btnRight.configure(state=tk.DISABLED)
        self.btnRight.update_idletasks()
        self.shiftEditGridRight()
        self.changed = True
        self.btnRight.configure(state=tk.NORMAL)

    def downArrowClick(self):
        self.btnDown.configure(state=tk.DISABLED)
        self.btnDown.update_idletasks()
        self.shiftEditGridDown()
        self.changed = True
        self.btnDown.configure(state=tk.NORMAL)

    def bitClick(self, event):
        event.widget.configure(state=tk.DISABLED)
        event.widget.update_idletasks()
        if event.widget.state == self.bgState:
            # Switch to foreground color
            self.chgEditBitColor(event.widget, self.fgState)
        else:
            # Switch to background color
            self.chgEditBitColor(event.widget, self.bgState)
        self.changed = True
        event.widget.configure(state=tk.NORMAL)

    def bitEnter(self, event):
        self.lblLoc.configure(text=event.widget.location)

    # -------------------- Input file methods --------------------

    def processInputFile(self, iFile):
        # Save the bitmap file name
        self.xFile.file = iFile
        self.lblFile.configure(text=iFile)
        # Display the bitmap in actual size
        if not self.dispActualBitmap():
            return
        # Load the bitmap into the edit grid
        iBytAr = self.xFile.parseFile()
        self.entNm.delete(0, tk.END)
        self.entNm.insert(tk.END, self.xFile.inNm)
        # See if bitmap is too big to edit
        if self.isBitmapTooBig(self.xFile.wdth, self.xFile.hgt):
            self.xFile.wdth = self.wdthDflt
            self.xFile.hgt = self.hgtDflt
            iBitGrid = self.xFile.bldEmptyBitGrid()
        else:
            iBitGrid = self.xFile.extractBits(iBytAr)
        self.chgWdthSb(self.xFile.wdth)
        self.chgHgtSb(self.xFile.hgt)
        self.delScrBits()
        self.loadScrBits(iBitGrid)

    def isDimValid(self, dimension):
        if dimension.isdigit():
            dimI = int(dimension)
            if dimI >= 1 and \
               dimI <= self.dimMax:
                return True
        tkmsg.showerror('Invalid Value',
            'Value must be a number, from 1 to '+str(self.dimMax))
        return False

    def isBitmapTooBig(self, wdth, hgt):
        # See if bitmap is too big to edit
        gridSz = wdth * hgt

        if gridSz > self.gridMax:
            tkmsg.showerror('Too big to edit',
                'Maximum bitmap size is '+str(self.gridMax)+' bits\n'+ \
                self.xFile.inNm+' size is '+str(gridSz)+' bits')
            return True
        return False

    # -------------------- Screen methods --------------------

    def dispActualBitmap(self):
        # Display the bitmap in actual size
        try:
            if self.bgColor == None:
                self.xImg = tk.BitmapImage(file=self.xFile.file,
                                           foreground=self.fgColor)
            else:
                self.xImg = tk.BitmapImage(file=self.xFile.file,
                                           foreground=self.fgColor,
                                           background=self.bgColor)
            self.lblBitmap.configure(image=self.xImg)
        except:
            exc = sys.exc_info()
            if hasattr(exc[0], '__name__'):
                nm = exc[0].__name__
            else:
                nm = str(exc[0])
            tkmsg.showerror('Bitmap File Error',
                                    '%s: %s\n%s' % (nm, str(exc[1]),
                                                    self.xFile.file))
            return False
        return True

    def chgWdthSb(self, wdth):
        # Change the width spinbox
        # Eliminate any direct width entry
        self.sbWdth.invoke('buttonup')
        # Update width spinbox
        scrSb = int(self.sbWdth.get())
        diff = abs(scrSb - wdth)
        if scrSb < wdth:
            for i in range(0, diff):
                self.sbWdth.invoke('buttonup')
        else: 
            for i in range(0, diff):
                self.sbWdth.invoke('buttondown')

    def chgHgtSb(self, hgt):
        # Change the height spinbox
        # Eliminate any direct height entry
        self.sbHgt.invoke('buttonup')
        # Update height spinbox
        scrSb = int(self.sbHgt.get())
        diff = abs(scrSb - hgt)
        if scrSb < hgt:
            for i in range(0, diff):
                self.sbHgt.invoke('buttonup')
        else: 
            for i in range(0, diff):
                self.sbHgt.invoke('buttondown')

    def delScrBits(self):
        # Remove the edit grid
        if len(self.scrBits) > 0:
            self.bitFrame.destroy()  # Screen bitmap bit container
            self.scrBits.clear()     # Screen bitmap bit dictionary

    def loadScrBits(self, iBitGrid):
        # Load the edit grid
        self.bitFrame = tk.Frame(self.editFrame)

        for gRow in range(0, self.xFile.hgt):
            for gCol in range(0, self.xFile.wdth):
                if iBitGrid[gRow,gCol] == 1:
                    # Foreground bit
                    self.addEditGridBit(gRow, gCol, self.fgState)
                else:
                    # Background bit
                    self.addEditGridBit(gRow, gCol, self.bgState)

        self.bitFrame.grid(row=1, column=1, padx=5, pady=5)

    def chgFgColor(self, color):
        if color == None:
            return
        self.fgColor = color
        self.lblFg.configure(text=self.fgColor)
        self.lblFg.configure(background=self.fgColor)
        if self.xImg == None:
            pass
        else:
            self.xImg.configure(foreground=self.fgColor)
        if len(self.scrBits) > 0:
            self.chgEditGridColor(self.fgState)

    def chgBgColor(self, color):
        self.bgColor = color
        if self.bgColor == None:
            self.lblBg.configure(text='None')
            self.lblBg.configure(background=self.bgNone)
            if self.xImg == None:
                pass
            else:
                self.xImg.configure(background=self.bgNone)
        else:
            self.lblBg.configure(text=self.bgColor)
            self.lblBg.configure(background=self.bgColor)
            if self.xImg == None:
                pass
            else:
                self.xImg.configure(background=self.bgColor)
        if len(self.scrBits) > 0:
            self.chgEditGridColor(self.bgState)

    def chgEditGridColor(self, fgbg):
        for gRow in range(0, self.xFile.hgt):
            for gCol in range(0, self.xFile.wdth):
                if self.scrBits[gRow,gCol].state == fgbg:
                    self.chgEditBitColor(self.scrBits[gRow,gCol], fgbg)

    def chgEditGridWdth(self, newWdth):
        if newWdth > self.xFile.wdth:
            for gCol in range(self.xFile.wdth, newWdth):
                for gRow in range(0, self.xFile.hgt):
                    self.addEditGridBit(gRow, gCol, self.bgState)
        else:
            for gCol in range(self.xFile.wdth-1, newWdth-1, -1):
                for gRow in range(0, self.xFile.hgt):
                    self.delEditGridBit(gRow, gCol)
        self.xFile.wdth = newWdth

    def chgEditGridHgt(self, newHgt):
        if newHgt > self.xFile.hgt:
            for gRow in range(self.xFile.hgt, newHgt):
                for gCol in range(0, self.xFile.wdth):
                    self.addEditGridBit(gRow, gCol, self.bgState)
        else:
            for gRow in range(self.xFile.hgt-1, newHgt-1, -1):
                for gCol in range(0, self.xFile.wdth):
                    self.delEditGridBit(gRow, gCol)
        self.xFile.hgt = newHgt

    def addEditGridBit(self, gRow, gCol, fgbg):
        if fgbg == self.fgState:
            clr = self.fgColor
        else:
            clr = self.bgColor
        if clr == None:
            self.scrBits[gRow,gCol] = BitLabel(self.bitFrame, gRow, gCol,
                fgbg, image=self.bImg, width=5, height=5, relief=tk.RAISED)
        else:
            self.scrBits[gRow,gCol] = BitLabel(self.bitFrame, gRow, gCol,
                fgbg, image=self.bImg, width=5, height=5,
                background=clr, relief=tk.RAISED)
        self.scrBits[gRow,gCol].bind("<Button-1>", self.bitClick)
        self.scrBits[gRow,gCol].bind("<Enter>", self.bitEnter)
        self.scrBits[gRow,gCol].grid(row=gRow, column=gCol)

    def delEditGridBit(self, gRow, gCol):
        self.scrBits[gRow,gCol].grid_forget()
        self.scrBits[gRow,gCol].destroy()
        del self.scrBits[gRow,gCol]

    def shiftEditGridUp(self):
        # Shift second through last rows up
        for gRow in range(0, self.xFile.hgt-1):
            for gCol in range(0, self.xFile.wdth):
                if not self.scrBits[gRow,gCol].state == \
                   self.scrBits[gRow+1,gCol].state:
                    self.chgEditBitColor(self.scrBits[gRow,gCol],
                                         self.scrBits[gRow+1,gCol].state)
        # Initialize last row
        for gCol in range(0, self.xFile.wdth):
            if self.scrBits[self.xFile.hgt-1,gCol].state == self.fgState:
                self.chgEditBitColor(self.scrBits[self.xFile.hgt-1,gCol],
                                     self.bgState)
    def shiftEditGridLeft(self):
        # Shift second through last columns left
        for gCol in range(0, self.xFile.wdth-1):
            for gRow in range(0, self.xFile.hgt):
                if not self.scrBits[gRow,gCol].state == \
                   self.scrBits[gRow,gCol+1].state:
                    self.chgEditBitColor(self.scrBits[gRow,gCol],
                                         self.scrBits[gRow,gCol+1].state)
        # Initialize last column
        for gRow in range(0, self.xFile.hgt):
            if self.scrBits[gRow,self.xFile.wdth-1].state == self.fgState:
                self.chgEditBitColor(self.scrBits[gRow, self.xFile.wdth-1],
                                     self.bgState)

    def shiftEditGridRight(self):
        # Shift last through second columns right
        for gCol in range(self.xFile.wdth-1, 0, -1):
            for gRow in range(0, self.xFile.hgt):
                if not self.scrBits[gRow,gCol].state == \
                   self.scrBits[gRow,gCol-1].state:
                    self.chgEditBitColor(self.scrBits[gRow,gCol],
                                         self.scrBits[gRow,gCol-1].state)
        # Initialize first column
        for gRow in range(0, self.xFile.hgt):
            if self.scrBits[gRow,0].state == self.fgState:
                self.chgEditBitColor(self.scrBits[gRow,0], self.bgState)

    def shiftEditGridDown(self):
        # Shift last through second rows down
        for gRow in range(self.xFile.hgt-1, 0, -1):
            for gCol in range(0, self.xFile.wdth):
                if not self.scrBits[gRow,gCol].state == \
                   self.scrBits[gRow-1,gCol].state:
                    self.chgEditBitColor(self.scrBits[gRow,gCol],
                                         self.scrBits[gRow-1,gCol].state)
        # Initialize first row
        for gCol in range(0, self.xFile.wdth):
            if self.scrBits[0,gCol].state == self.fgState:
                self.chgEditBitColor(self.scrBits[0,gCol], self.bgState)

    def rotateEditGrid(self):
        rFgBits = [] # List of rotated foreground bits
        # Can only rotate a square
        if self.xFile.hgt < self.xFile.wdth:
            lastRC = self.xFile.hgt
        else:
            lastRC = self.xFile.wdth
        # Build a list of rotated foreground bits from within the rotate square
        for gRow in range(0, lastRC):
            for gCol in range(0, lastRC):
                if self.scrBits[gRow,gCol].state == self.fgState:
                    newRow = gCol
                    newCol = lastRC - gRow - 1
                    rFgBits.append((newRow,newCol))
        # Change the edit grid foreground bits to background bits
        for gRow in range(0, self.xFile.hgt):
            for gCol in range(0, self.xFile.wdth):
                if self.scrBits[gRow,gCol].state == self.fgState:
                    self.chgEditBitColor(self.scrBits[gRow,gCol], self.bgState)
        # Load the edit grid with rotated foreground bits
        for newRow, newCol in rFgBits:
            self.chgEditBitColor(self.scrBits[newRow,newCol], self.fgState)

    def chgEditBitColor(self, scrBit, fgbg):
        scrBit.state = fgbg
        if fgbg == self.fgState:
           # Changing to foreground
            scrBit.configure(background=self.fgColor)
        else:
            # Changing to background
            if self.bgColor == None:
                scrBit.configure(background=self.bgNone)
            else:
                scrBit.configure(background=self.bgColor)

    # -------------------- Output file methods --------------------

    def saveBitmap(self, saveFile):
        # Save the bitmap file name
        self.xFile.file = saveFile
        self.lblFile.configure(text=saveFile)
        # Get the bits from the edit grid, build hex bytes, write bitmap file
        oBitGrid = self.buildBits()
        oBytAr = self.xFile.buildBytes(oBitGrid)
        self.xFile.writeFile(oBytAr)
        # Display the saved bitmap in actual size
        self.dispActualBitmap()

    def buildBits(self):
        # Unload edit grid bits to bit grid dictionary
        oBitGrid = {}
        for gRow in range(0, self.xFile.hgt):
            for gCol in range(0, self.xFile.wdth):
                if self.scrBits[gRow,gCol].state == self.fgState:
                    oBitGrid[gRow,gCol] = 1
                else:
                    oBitGrid[gRow,gCol] = 0
        return oBitGrid

    def chkChanged(self):
        if self.changed:
            if tkmsg.askyesno('Save?',
                    'Bitmap has changed. Do you want to save it?'):
                self.saveBitmapClick()
            else:
                self.changed = False

    # -------------------- Help dialog --------------------

    def xEditHelp(self):
        tkmsg.showinfo('Simple xbm Image Editor Help',
            'Main buttons:\n'
            'New\tStart a new bitmap. Set width and height before clicking.\n'
            '\tCurrent work will be lost.\n'
            'Open\tLoad an existing xbm file into the bitmap edit area.\n'
            '\tCurrent work will be lost.\n'
            'Save\tSave the current bitmap edit area to an xbm file. Save a\n'
            '\tbitmap to update the actual-size bitmap displayed on\n'
            '\tthe screen.\n'
            'Rotate\tRotate the current bitmap edit area 90 degrees clockwise.\n'
            '\tIf the bitmap is not square, only the square portion of the\n'
            '\tbitmap will be preserved.\n\n'
            'Internal name:  Required. May only contain letters, numbers\n'
            '\tand _. Cannot start with a number.\n'
            'Width:\tBitmap width. Set before clicking the New button.\n'
            '\tThe width of the current bitmap edit area may also be\n'
            '\tchanged.\n'
            'Height:\tBitmap height. Set before clicking the New button.\n'
            '\tThe height of the current bitmap edit area may also be\n'
            '\tchanged.\n\n'
            'Row Col:\tDisplays the current coordinates of the mouse pointer\n'
            '\twhen in the edit grid.\n'
            'Foreground and Background:  Colors are not stored in xbm files.\n'
            '\tUse these options to test various colors for your application.\n'
            '\tCancel out of the background Color Chooser dialog to return\n'
            '\tto a transparent background.\n\n'
            'Actual-size bitmap:  Displays the bitmap as it will appear in\n'
            '\tyour application. Updated during Open and Save operations.\n'
            'Edit grid arrows: Shift the bitmap edit area contents up, down,\n'
            '\tleft or right.\n'
            'Bitmap edit area:  Click the tiles to toggle them between\n'
            '\tforeground and background. Click the arrows to shift the\n'
            '\tcontents of the edit grid. Adjust the width and height of\n'
            '\tthe edit grid with the spinboxes. Experiment with edit grid\n'
            '\tcolors by changing foreground and background. Save to\n'
            '\treflect changes in the actual-size bitmap.')

    # -------------------- Initialize gif images --------------------

    def initGifs(self):
        # ArrowUp16.gif
        self.arrowUp = \
            ('R0lGODlhEAAQAPcAAAEBAUN1qZnN/1eLvSdNc8Ph/2GTx02Bszlrn7PZ/2eZ'
             'zT9zpUl7r6PR/1uNwc3l/2GVx1GFtzltnwAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAQABAABwhaAAEIHEiwoMGD'
             'CBMqXFhQgQKGAAw8eGBg4YACDzA6SBghY4GPBSIcZPAggcmTDxgUXPCggcuX'
             'Lh8sGIjggYCbOHM+QCCQAIIABwYYcGhgwIEACAhAXMq06cGAADs=')
        # ArrowLeft16.gif
        self.arrowLeft = \
            ('R0lGODlhEAAQAPcAAAEBAUF1p4Gz55nN/1mLv7fb/ydNc4+96zNnmU+DtanT'
             '/2GTx8Ph/01zmYW36Ut9saPR/zltn2WXy83l/0V5q4G1553P/12Rw73f/5fB'
             '6zVpm1WHu6/X/8nj/z1vo4u56WeZzQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAQABAABwhoAAEIHEiwoMGC'
             'IBocNChhgoSFBBdMmLAAosALEzp0uGCRwAQGIAlA3NABQwGTGxYm6FCgZcsE'
             'Cx9k4ECT5gOIFA5AUMCTgsUAHyAIDWARgIcKFgZ4KAoggoABEZgCQCAAgdSp'
             'Bq4aDAgAOw==')
        # ArrowRight16.gif
        self.arrowRight = \
            ('R0lGODlhEAAQAPcAAAEBAUF1p4Gz55nN/1mLv7fb/ydNc4+96zNnmU+DtanT'
             '/2GTx8Ph/01zmYW36Ut9saPR/zltn2WXy83l/0V5q4G1553P/12Rw73f/5fB'
             '6zVpm1WHu6/X/8nj/z1vo4u56WeZzQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAQABAABwhoAAEIHEiwYMEG'
             'IAwqBCBhgoSFBRdMmLAA4sALHTpMuGARAAEGICcQsLihAAaTHTZATFCgZcsO'
             'CRY+4ECTZoYHCyko2AnhAAWIASAI/RDAoocBFip46BhhgIAIHQEgEIAgKgAD'
             'Va1GDQgAOw==')
        # ArrowDown16.gif
        self.arrowDown = \
            ('R0lGODlhEAAQAPcAAAEBAUl7r4u136PR/5vD7WGVx5O74zNnmcPh/3Wl1U1z'
             'mVGFt4G155nN/42767PZ/6nL722dz5m/5zlrn83l/4Gt2T9zpVuNwYO16QAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
             'AAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAQABAABwhgAAEIHEiwoMGD'
             'CBMqVKggQoIKAgxIkGBAQIUEERQILEChIwIKHz92pFBg4AUICFKqTAnhQsEF'
             'BB7InElgwcEADgboHOAgQEILDBo0YGBh4QQGDCYsFHjgwNKnUKNKBRAQADs=')

    # -------------------- End --------------------

    def wrapUp(self):
        self.chkChanged()
        if self.changed == False:
            self.root.destroy()

# -------------------- Main --------------------
if __name__ == '__main__':
    xEdit = XbmEditor()
    xEdit.root.mainloop()
