import os
import sys
import time

picdir = '/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/'
libdir = '/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib/'
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V4
import time
from PIL import Image, ImageDraw, ImageFont

noRefresh = False # If True, the screen will NOT refresh.
displayPlayMode = ""
primaryColor = 0     # 0 = black
secondaryColor = 255 # white

class view():
    def __init__(self):
        self.epd = epd2in13_V4.EPD()
        self.epd.init()
        self.epd.Clear(0xff)

        self.dispWidth, self.dispHeight = (250,122)
        self.textHeight15 = 15
        self.textHeight19 = 19
        self.font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), self.textHeight15 )
        self.font19 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), self.textHeight19 )
        self.noRefresh = False
        self.displayPlayMode = ""
        # Drawing on the display in Landscape mode
        self.Himage = Image.new('1', (self.epd.height, self.epd.width), 255)  # 255 = clear the frame
        self.draw = ImageDraw.Draw(self.Himage)
        self.changedScreen = False

    def shutdownImage(self):
        myImage = Image.open('/home/pi/PiPod_ePaper/music1.bmp')
        # Wait for the screen to be available
        self.epd.ReadBusy()
        self.epd.display(self.epd.getbuffer(myImage))
        return

    def setBaseImage(self):
        # Wait for the screen to be available
        self.epd.ReadBusy()
        time.sleep(0.2)
        self.epd.displayPartBaseImage( self.epd.getbuffer(self.Himage) )

    def query4Update(self):
        if( self.changedScreen == True ):
            return True
        else:
            return False

    def clearUpdateFlag(self):
        # Call this method once you are sure it's screen changes have been taken care of.
        self.changedScreen = False

    def setPlayMode(self, PlayMode):
        self.displayPlayMode = PlayMode

    def update(self, status, menuDict, songMetadata):
        # Note: menuDict is navigate.py's ENTIRE menuDict structure, including ["Songs"][].
        if menuDict["current"] == "musicController":
            self.musicController(
            menuDict["selectedItem"],
            status[1],
            status[0],
            songMetadata["currentSong"],
            songMetadata["currentTime"],
            songMetadata["songLength"],
            songMetadata["volume"],
            len(songMetadata["playlist"]),
            songMetadata["index"]
            )
        elif menuDict["current"] == "Songs":
            # menuDict["selectedItem"] is the index of the item on the list that should be centered and highlighted.
            self.listView( list(map(lambda x: x[3], menuDict[menuDict["current"]])), menuDict["selectedItem"] )
        elif menuDict["current"] == "Queue":
            self.listView(["Clear queue"] + list(map(lambda x: x[3], menuDict[menuDict["current"]])), menuDict["selectedItem"] )
        elif menuDict["current"] == "list":  # This means I am looking at a list of Artists/Albums/Genres.
            self.listView(list(map(lambda x: x[3], menuDict["list"])), menuDict["selectedItem"] )
        else:
            self.listView(menuDict[menuDict["current"]], menuDict["selectedItem"] )

        return None

    def partialUpdate(self, status, menuDict, songMetadata):
        self.partialMusicController(
        menuDict["selectedItem"],
        status[1],
        status[0],
        songMetadata["currentSong"],
        songMetadata["currentTime"],
        songMetadata["songLength"],
        songMetadata["volume"],
        len(songMetadata["playlist"]),
        songMetadata["index"]
        )

    def refresh(self):
        # Wait for the screen to be available
        self.epd.ReadBusy()
        #time.sleep(0.2)
        # Refresh the e-Paper screen
        self.epd.display(self.epd.getbuffer(self.Himage))
        return

    def partialRefresh(self):
        # Wait for the screen to be available
        self.epd.ReadBusy()
        #time.sleep(0.2)
        # Refresh the e-Paper screen
        self.epd.displayPartial(self.epd.getbuffer(self.Himage))
        return

    #def setNoRefresh(self):
        #self.noRefresh = True

    #def setDoRefresh(self):
        #self.noRefresh = False

    def clear(self):
        # Sets all of the pixels in the Himage frame buffer to white.
        self.draw.rectangle( [(0,0),(self.dispWidth, self.dispHeight)], outline=255, fill=255 )

    def clearAndDisplay(self):
        self.epd.Clear()
        return

    #def shutdownScreen(self):
        #TODO: Put any shutdown code here
        #pass

    def popUp(self, text):
        self.clear()
        newline_index = text.find('\n')
        if ( newline_index != -1 ):
            line1 = text[:newline_index]
            numlines = 1 + text.count('\n')
        else:
            line1 = text
            numlines = 1
        if( numlines <= 4 ):
            twidth, theight = self.draw.textsize( line1, font = self.font15 )
            self.draw.multiline_text( ( (self.dispWidth/2) - (twidth/2), (self.dispHeight/2)-(10*numlines) ), text, fill=0, font=self.font15, spacing=4, align="center" )
        else:
            self.draw.text( (0,0), "Too many lines in popUp()", fill=0, font=self.font15 )
        self.refresh()

    def listView(self, menu, selectedItem):
        #self.changedScreen = True
        self.clear()
        color = primaryColor
        index = 0
        marginTop = (self.dispHeight - 9) / 2 - (21 * selectedItem)  # text height 18/2=9
        marginLeft = 10
        marginTop += 21 * (selectedItem - 12 if selectedItem > 12 else 0)
        index += (selectedItem - 12 if selectedItem > 12 else 0)
        for item in menu[
                    selectedItem - 12 if selectedItem > 12 else 0:selectedItem + 12]:  # If > 4 items in list, start slicing the displayed list
            # This adds a character to mark the current playback mode, so it can be displayed in underline mode. Gets stripped later.
            if ( item == "Normal") and ( self.displayPlayMode == "Normal" ):
                    item = '\u2193' + "Normal"
            elif ( item == "Shuffle") and ( self.displayPlayMode == "Shuffle" ):
                    item = '\u2193' + "Shuffle"
            elif ( item == "Repeat 1 Song") and ( self.displayPlayMode == "Repeat1" ):
                    item = '\u2193' + "Repeat 1 Song"
            if index == selectedItem:
                if item[0] == '\u2193':
                    shortItem = item[1:]
                    item = '\u2192' + shortItem
                    twidth, theight = self.draw.textsize(item, font=self.font19)
                    lx, ly = marginLeft, marginTop + theight
                    self.draw.text( (marginLeft, marginTop), item, font=self.font19, fill=color) # 0 = black
                    self.draw.line( (lx + 18, ly, lx + twidth, ly), fill=color)
                else:
                    item = '\u2192' + item
                    self.draw.text( (marginLeft, marginTop), item, font=self.font19, fill=color)
                marginTop += 23
            else:
                if item[0] == '\u2193':
                    shortItem = item[1:]
                    twidth, theight = self.draw.textsize(shortItem, font=self.font15)
                    lx, ly = marginLeft, marginTop + theight
                    self.draw.text( (marginLeft, marginTop), shortItem, font=self.font15, fill=color) # 0 = black
                    self.draw.line( (lx, ly, lx + twidth, ly), fill=color)
                else:
                    self.draw.text( (marginLeft, marginTop), item, font=self.font15, fill=color, underline=False)
                marginTop += 20
            index += 1
        return

    def musicController(self, selectedItem, batLevel, chargeStatus, \
                        currentSong, currentTime, songLength, volume, queLength, queIndex):
        self.clear()

        # Status bar
        volumeText = str(volume) + "%"
        self.draw.text( (3,1), volumeText, font=self.font15, fill=0 )

        chargeText = str(batLevel) + " V"
        self.draw.text( (self.dispWidth - 45, 1), chargeText, font=self.font15, fill=0 )

        if currentSong[1] == "":  # If there is no song being played, show 0/0
            queText = str(queIndex) + "/" + str(queLength-1)
        else:
            queText = str(queIndex+1) + "/" + str(queLength)
        #lengthQueText = self.draw.textlength( queText, self.font15 ) # How many pixels needed for this text (to center)
        lengthQueText = self.draw.textlength( (str(queIndex+1) + "/"), self.font15 ) # How many pixels needed (to center '/')

        # Now center the queText
        #start = 125 - int( (lengthQueText / 2) )   # Screen is 250 pixels wide, so mid-point = 125. (to center text)
        start = (125 - int( lengthQueText )) + 5   # Screen is 250 pixels wide, so mid-point = 125. (to center the '/')

        self.draw.text( (int(start),1), queText, font=self.font15, fill=0 )
        self.draw.line( [(0,20),(self.dispWidth,20)], fill=0, width=2 )

        # Current song information
        if currentSong:
            artist = str( currentSong[1] )
            album = str( currentSong[2] )
            title = str( currentSong[3] )
            genre = str( currentSong[4] )
            track = str( currentSong[5] )
            self.draw.text( (2,25), title, font=self.font19, fill=0 )
            self.draw.text( (2,46), artist, font=self.font19, fill=0 )
            albumLine = "Album: " + album
            genreLine = "Genre: " + genre
            self.draw.text( (2,70), albumLine, font=self.font15, fill=0 )
            self.draw.text( (2,86), genreLine, font=self.font15, fill=0 )
            if( track != '0' ):
                trackLine = "Track: " + track
                lengthTrackLine = self.draw.textlength( trackLine, self.font15 ) # How many pixels needed for this text
                self.draw.text( (self.dispWidth - (lengthTrackLine+2), 86), trackLine, font=self.font15, fill=0 ) # Right justify

        # Time bar
        self.draw.rectangle( [(40,self.dispHeight-15),(self.dispWidth-40,self.dispHeight-1)], outline=0 )  # No fill. Border rectangle.

        if songLength > 0:
            progress = round((self.dispWidth - 80) * currentTime / songLength)
            self.draw.rectangle( [(40,self.dispHeight-15),(40+progress, self.dispHeight-1)], outline=0, fill=0 )
            currentTimeText = str("{0:02d}:{1:02d}".format(int(currentTime / 1000 / 60), round(currentTime / 1000 % 60)) )
            songLengthText = str("{0:02d}:{1:02d}".format(int(songLength / 1000 / 60), round(songLength / 1000 % 60)) )
        else:
            currentTimeText = str("00:00")
            songLengthText = str("00:00")

        self.draw.text( (1,self.dispHeight-16), currentTimeText, font=self.font15, fill=0 )
        self.draw.text( (self.dispWidth-37,self.dispHeight-16), songLengthText, font=self.font15, fill=0 )

        return

    def partialMusicController(self, selectedItem, batLevel, chargeStatus, \
                        currentSong, currentTime, songLength, volume, queLength, queIndex):
        # Draw a white rectangle over the "how far into current song" and the bar.
        self.draw.rectangle( [(0,self.dispHeight-15),(self.dispWidth-40,self.dispHeight)], outline=255 )  # No fill. No border.

        # Time bar
        self.draw.rectangle( [(40,self.dispHeight-15),(self.dispWidth-40,self.dispHeight-1)], outline=0 )  # No fill. Border rectangle.

        if songLength > 0:
            progress = round((self.dispWidth - 80) * currentTime / songLength)
            self.draw.rectangle( [(40,self.dispHeight-15),(40+progress, self.dispHeight-1)], outline=0, fill=0 )
            currentTimeText = str("{0:02d}:{1:02d}".format(int(currentTime / 1000 / 60), round(currentTime / 1000 % 60)) )
        else:
            currentTimeText = str("00:00")

        self.draw.text( (1,self.dispHeight-16), currentTimeText, font=self.font15, fill=0 )
        return
