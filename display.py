import pygame
import os
import sys

picdir = '/home/drh/e-Paper/RaspberryPi_JetsonNano/python/pic/'
libdir = '/home/drh/e-Paper/RaspberryPi_JetsonNano/python/lib/'
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13d
import time
from PIL import Image, ImageDraw, ImageFont

noRefresh = False # If True, the screen will NOT refresh.
displayPlayMode = "Normal"
primaryColor = 0     # 0 = black
secondaryColor = 255 # white

class view():
    def __init__(self):
        self.epd = epd2in13d.EPD()
        self.epd.init()
        self.epd.Clear()

        pygame.init()
        pygame.key.set_repeat(500,100)  # This is only for attached PC keyboards. Can remove?

        self.dispWidth, self.dispHeight = (212,104)
        #self.font = pygame.font.Font("/home/drh/PiPod_Zero2W/Sofware/TerminusTTF-4.46.0.ttf", 18)
        self.textHeight15 = 15
        self.textHeight19 = 22
        self.font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), self.textHeight15 )
        self.font19 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), self.textHeight19 )
        self.noRefresh = False
        self.displayPlayMode = "Normal"
        # Drawing on the display in Landscape mode
        self.Himage = Image.new('1', (self.epd.height, self.epd.width), 255)  # 255 = clear the frame
        self.draw = ImageDraw.Draw(self.Himage)
        self.changedScreen = False

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

    def refresh(self):
        if self.noRefresh == False:
            # Wait for the screen to be available
            self.epd.ReadBusy()
            # Refresh the e-Paper screen
            self.epd.display(self.epd.getbuffer(self.Himage))
        return

    def setNoRefresh(self):
        self.noRefresh = True

    def setDoRefresh(self):
        self.noRefresh = False

    def clear(self):
        # Sets all of the pixels in the Himage frame buffer to white.
        self.draw.rectangle( [(0,0),(self.dispWidth, self.dispHeight)], outline=255, fill=255 )

    def clearAndDisplay(self):
        self.epd.Clear()
        return

    def shutdownScreen(self):
        #TODO: Put any shutdown code here
        pass

    def popUp(self, text):
        #self.lcd.fill(backgroundColor)
        #text = self.font.render(text, True, primaryColor)
        #self.lcd.blit(text, ((self.dispWidth - text.get_width()) / 2, (self.dispHeight - text.get_height()) / 2))
        self.clear()
        self.draw.text( ( ((self.dispWidth - 40)/2), (self.dispHeight - 10)/2 ), text, font=self.font15, fill=0 )
        self.refresh()

    def listView(self, menu, selectedItem):
        self.clear()
        index = 0
        marginTop = (self.dispHeight - 9) / 2 - (21 * selectedItem)  # text height 18/2=9
        marginLeft = 10
        marginTop += 21 * (selectedItem - 12 if selectedItem > 12 else 0)
        index += (selectedItem - 12 if selectedItem > 12 else 0)
        for item in menu[
                    selectedItem - 12 if selectedItem > 12 else 0:selectedItem + 12]:  # I'm sorry, if selected item is more then 4 start slicing the list
            if ( item == "Normal") and ( self.displayPlayMode == "Normal" ):
                    item = '\u2192' + " Normal " + '\u2190'
            elif ( item == "Shuffle") and ( self.displayPlayMode == "Shuffle" ):
                    item = '\u2192' + " Shuffle " + '\u2190'
            elif ( item == "Repeat 1 Song") and ( self.displayPlayMode == "Repeat1" ):
                    item = '\u2192' + " Repeat 1 Song " + '\u2190'
            if index == selectedItem:
                #text = self.font.render(item, True, secondaryColor)
                item = '\u2192' + item
                color = primaryColor
            else:
                #text = self.font.render(item, True, primaryColor)
                color = primaryColor
            #self.lcd.blit(text, (marginLeft, marginTop))
            self.draw.text( (marginLeft, marginTop), item, font=self.font15, fill=color ) # 0 = black
            marginTop += 21
            index += 1
        #self.changedScreen = True
        return

    def musicController(self, selectedItem, batLevel, chargeStatus, \
                        currentSong, currentTime, songLength, volume, queLength, queIndex):
        self.clear()

        # Status bar
        volumeText = str(volume) + "%"
        #self.lcd.blit(volumeText, (10, 1))
        self.draw.text( (10,1), volumeText, font=self.font15, fill=0 )

        if currentSong[1] == "":  # If there is no song being played, show 0/0
            #queText = self.font.render(str(queIndex) + "/" + str(queLength-1), True, primaryColor)
            queText = str(queIndex) + "/" + str(queLength-1)
        else:
            #queText = self.font.render(str(queIndex+1) + "/" + str(queLength), True, primaryColor)
            queText = str(queIndex+1) + "/" + str(queLength)
        #self.lcd.blit(queText, (140, 1))
        self.draw.text( ((self.dispWidth/2)-15,1), queText, font=self.font15, fill=0 )

        chargeText = str(batLevel)
        #self.lcd.blit(chargeText, (self.dispWidth - chargeText.get_width() - 10, 1))
        self.draw.text( (self.dispWidth - 40, 1), chargeText, font=self.font15, fill=0 )

        #pygame.draw.line(self.lcd, primaryColor, (0, 20), (self.dispWidth, 20))
        self.draw.line( [(0,20),(self.dispWidth,20)], fill=0, width=2 )

        # Current song information
        if currentSong:
            artist = str( currentSong[1] )
            #album = self.font.render(currentSong[2], True, primaryColor)
            title = str( currentSong[3] )
            #genre = self.font.render(currentSong[4], True, primaryColor)
            #print(currentSong[4])
            #self.lcd.blit(title, (10, 30))
            #self.lcd.blit(artist, (10, 51))
            #self.lcd.blit(album, (10, 72))
            #self.lcd.blit(genre, (10, 93))
            self.draw.text( (2,30), title, font=self.font15, fill=0 )
            self.draw.text( (2,51), artist, font=self.font15, fill=0 )

        # Time bar
        #pygame.draw.rect(self.lcd, primaryColor, (10, self.dispHeight - 18, self.dispWidth - 20, 15), 1)
        self.draw.rectangle( [(40,self.dispHeight-15),(self.dispWidth-40,self.dispHeight-1)], outline=0 )  # No fill. Border rectangle.

        if songLength > 0:
            progress = round((self.dispWidth - 80) * currentTime / songLength)
            #pygame.draw.rect(self.lcd, primaryColor, (10, self.dispHeight - 18, progress, 15))
            self.draw.rectangle( [(40,self.dispHeight-15),(40+progress, self.dispHeight-1)], outline=0, fill=0 )
            currentTimeText = str("{0:02d}:{1:02d} / ".format(int(currentTime / 1000 / 60), round(currentTime / 1000 % 60)) )
            songLengthText = str("{0:02d}:{1:02d}".format(int(songLength / 1000 / 60), round(songLength / 1000 % 60)) )
        else:
            currentTimeText = str("00:00")
            songLengthText = str("00:00")

        #self.lcd.blit(currentTimeText, (10, self.dispHeight - 39))
        #self.lcd.blit(songLengthText, (10 + currentTimeText.get_width(), self.dispHeight - 39))
        self.draw.text( (1,self.dispHeight-16), currentTimeText, font=self.font15, fill=0 )
        self.draw.text( (self.dispWidth-37,self.dispHeight-16), songLengthText, font=self.font15, fill=0 )

        #self.changedScreen = True
        return
