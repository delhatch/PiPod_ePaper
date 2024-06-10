import csv
import random
import string

alphaList = list(string.ascii_uppercase)

class menu():
    menuDict = {
        "selectedItem": 0,
        "Main": ["Songs", "Shutdown", "Albums","Artists","Genres","Play Mode","Settings", "Queue"],
        "Songs": [],
        "Artists": [],
        "Albums": [],
        "Genres": [],
        "Play Mode":["Normal","Shuffle","Repeat 1 Song"],
        "Settings": ["Shutdown", "Turn EQ On","Turn EQ Off","Sleep", "Update library"],
        "current": "musicController",
        "Queue": [],
        "history": [],
    }

    def __init__(self):
        self.changedScreen = False
        return

    def query4Update(self):
        if( self.changedScreen == True ):
            return True
        else:
            return False

    def clearUpdateFlag(self):
        self.changedScreen = False

    def setUpdateFlag(self):
        self.changedScreen = True

    def setSelectedItem( self, value ):
        self.menuDict["selectedItem"] = value

    def getSelectedItem( self ):
        return self.menuDict["selectedItem"]

    def upTree(self, numLevels):
        self.changedScreen = True
        self.menuDict["selectedItem"] = 0  # Select the first item on the upcoming list.
        for i in range( numLevels ):
            if self.menuDict["history"]:  # If the menu history is not empty, back up one
                self.menuDict["current"] = self.menuDict["history"][-1::][0]
                self.menuDict["history"].pop()
            else:
                self.menuDict["current"] = "musicController"  # If no history, set to top screen
        return None

    def escape(self):
        self.changedScreen = True
        self.menuDict["selectedItem"] = 0  # Select the first item on whatever list will be relevant.
        if self.menuDict["history"]:  # If the menu history is not empty, back up one
            self.menuDict["current"] = self.menuDict["history"][-1::][0]
            self.menuDict["history"].pop()
        else:
            self.menuDict["current"] = "musicController"  # If no history, set to top screen
        return None

    def up(self):
        self.changedScreen = True
        if self.menuDict["selectedItem"] > 0:
            self.menuDict["selectedItem"] -= 1
        return None

    def down(self):
        self.changedScreen = True
        if self.menuDict["current"] == "Queue" and self.menuDict["selectedItem"] < len(self.menuDict[self.menuDict["current"]]):
            self.menuDict["selectedItem"] += 1
        elif self.menuDict["selectedItem"] < len(self.menuDict[self.menuDict["current"]]) - 1:
            self.menuDict["selectedItem"] += 1
        return None

    def left(self, downButton):
        # downButton is the state of the navigation Down button at the instant of a Left keypress. 0 = pressed, 1 = not pressed
        if( (self.menuDict["current"] == "list" or self.menuDict["current"] == "Songs") and (downButton == 1) ):  # move to previous letter in the alphabet
            self.changedScreen = True
            songInfo = self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]]
            # Get first letter of selected song.
            firstL = songInfo[3][0]
            # Now scan up until find a song who's first letter is smaller than this one. Save that letter.
            if (firstL in alphaList) and (firstL != 'A') and (self.menuDict["selectedItem"] != 0):
                nextL = chr(ord(firstL) - 1)
                # Find index of the first song that starts with a letter LESS THAN this one
                index = self.menuDict["selectedItem"]
                index -= 1
                nextSong = self.menuDict[self.menuDict["current"]][index]
                nextSongFirstL = nextSong[3][0]
                while( nextSongFirstL >= nextL ):
                    index -= 1
                    nextSong = self.menuDict[self.menuDict["current"]][index]
                    nextSongFirstL = nextSong[3][0]
                self.menuDict["selectedItem"] = index + 1
            else:
                # Selected song title did not start with a letter in B-Z. So just go to top of list.
                self.menuDict["selectedItem"] = 0
        elif( (self.menuDict["current"] == "list" or self.menuDict["current"] == "Songs") and (downButton == 0) ):  # DOWN was pressed, jump up 10 songs
            self.changedScreen = True
            index = self.menuDict["selectedItem"]
            index -= 10
            if( index < 0 ):
                index = 0
            self.menuDict["selectedItem"] = index

        elif( (self.menuDict["current"] == "Artists") and (downButton == 1) ):  # Jump to next artist whos name is alphabetically greater.
            # Get first letter of the currently selected artist's name.
            self.changedScreen = True
            artistName = self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]]
            firstL = artistName[0]
            # Now scan up until find an Artist who's first letter is smaller than this one. Save that letter.
            if (firstL in alphaList) and (firstL != 'A') and (self.menuDict["selectedItem"] != 0):
                nextL = chr(ord(firstL) - 1)
                # Find index of the first Artist that starts with a letter LESS THAN this one
                index = self.menuDict["selectedItem"]
                index -= 1
                nextArtist = self.menuDict[self.menuDict["current"]][index]
                nextArtistFirstL = nextArtist[0]
                while( nextArtistFirstL >= nextL ):
                    index -= 1
                    nextArtist = self.menuDict[self.menuDict["current"]][index]
                    nextArtistFirstL = nextArtist[0]
                self.menuDict["selectedItem"] = index + 1
            else:
                # Selected Artist did not start with a letter in B-Z. So just go to top of list.
                self.menuDict["selectedItem"] = 0
        elif( (self.menuDict["current"] == "Artists") and (downButton == 0) ):  # DOWN button was pressed, so jump up 8 artists
            self.changedScreen = True
            index = self.menuDict["selectedItem"]
            index -= 8
            if( index < 0 ):
                index = 0
            self.menuDict["selectedItem"] = index

        elif( (self.menuDict["current"] == "Albums") and (downButton == 1) ):  # Jump to next Album whos name is alphabetically greater.
            # Get first letter of the currently selected Album's name.
            self.changedScreen = True
            albumName = self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]]
            firstL = albumName[0]
            # Now scan up until find an Album who's first letter is smaller than this one. Save that letter.
            if (firstL in alphaList) and (firstL != 'A') and (self.menuDict["selectedItem"] != 0):
                nextL = chr(ord(firstL) - 1)
                # Find index of the first Artist that starts with a letter LESS THAN this one
                index = self.menuDict["selectedItem"]
                index -= 1
                nextAlbum = self.menuDict[self.menuDict["current"]][index]
                nextAlbumFirstL = nextAlbum[0]
                while( nextAlbumFirstL >= nextL ):
                    index -= 1
                    nextAlbum = self.menuDict[self.menuDict["current"]][index]
                    nextAlbumFirstL = nextAlbum[0]
                self.menuDict["selectedItem"] = index + 1
            else:
                # Selected Album title did not start with a letter in B-Z. So just go to top of list.
                self.menuDict["selectedItem"] = 0
        elif( (self.menuDict["current"] == "Albums") and (downButton == 0) ):  # DOWN button was pressed, so jump up 8 albums
            self.changedScreen = True
            index = self.menuDict["selectedItem"]
            index -= 8
            if( index < 0 ):
                index = 0
            self.menuDict["selectedItem"] = index

        return "updateList"

    def right(self, downButton ):
        if( (self.menuDict["current"] == "list" or self.menuDict["current"] == "Songs") and (downButton == 1) ):  # move to next letter in the alphabet
            self.changedScreen = True
            songInfo = self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]]
            #songTitle = songInfo[3]
            # Get first letter of selected song.
            firstL = songInfo[3][0]
            # Increment to next letter.
            if (firstL in alphaList) and (firstL != 'Z'):
                nextL = chr(ord(firstL) + 1)
                # Find index of the first song that starts with that letter, or greater.
                index = self.menuDict["selectedItem"]
                index += 1
                nextSong = self.menuDict[self.menuDict["current"]][index]
                nextSongFirstL = nextSong[3][0]
                while( nextSongFirstL <= firstL ):
                    index += 1
                    nextSong = self.menuDict[self.menuDict["current"]][index]
                    nextSongFirstL = nextSong[3][0]
                self.menuDict["selectedItem"] = index
            elif ( firstL != 'Z'):
                # Selected song title did not start with a letter in A-Z. So just go to first 'A' song.
                index = self.menuDict["selectedItem"]
                index += 1
                nextSong = self.menuDict[self.menuDict["current"]][index]
                nextSongFirstL = nextSong[3][0]
                while( nextSongFirstL != 'A' ):
                    index += 1
                    if( index > (len(self.menuDict[self.menuDict["current"]]) - 1) ):
                        index = len(self.menuDict[self.menuDict["current"]]) - 1
                    nextSong = self.menuDict[self.menuDict["current"]][index]
                    nextSongFirstL = nextSong[3][0]
                self.menuDict["selectedItem"] = index
        elif( (self.menuDict["current"] == "list" or self.menuDict["current"] == "Songs") and (downButton == 0) ):  # DOWN was pressed, jump down 10 songs
            self.changedScreen = True
            index = self.menuDict["selectedItem"]
            index += 10
            if( index > (len(self.menuDict[self.menuDict["current"]])-1) ):
                index = len(self.menuDict[self.menuDict["current"]]) - 1
            self.menuDict["selectedItem"] = index

        elif( (self.menuDict["current"] == "Artists") and (downButton == 1) ):  # Jump to next artist whos name is alphabetically greater.
            # Get first letter of the currently selected artist's name.
            self.changedScreen = True
            artistName = self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]]
            firstL = artistName[0]
            if (firstL in alphaList) and (firstL != 'Z'):
                nextL = chr(ord(firstL) + 1)
                # Find index of the first song that starts with that letter, or greater.
                index = self.menuDict["selectedItem"]
                index += 1
                nextArtist = self.menuDict[self.menuDict["current"]][index]
                nextArtistFirstL = nextArtist[0]
                while( nextArtistFirstL <= firstL ):
                    index += 1
                    nextArtist = self.menuDict[self.menuDict["current"]][index]
                    nextArtistFirstL = nextArtist[0]
                self.menuDict["selectedItem"] = index
            elif ( firstL != 'Z'):
                index = self.menuDict["selectedItem"]
                index += 1
                nextArtist = self.menuDict[self.menuDict["current"]][index]
                nextArtistFirstL = nextArtist[0]
                while( nextArtistFirstL != 'A' ):
                    index += 1
                    nextArtist = self.menuDict[self.menuDict["current"]][index]
                    nextArtistFirstL = nextArtist[0]
                self.menuDict["selectedItem"] = index
        elif( (self.menuDict["current"] == "Artists") and (downButton == 0) ):  # DOWN was pressed, jump down 8 artists
            self.changedScreen = True
            index = self.menuDict["selectedItem"]
            index += 8
            if( index > (len(self.menuDict[self.menuDict["current"]])-1) ):
                index = len(self.menuDict[self.menuDict["current"]]) - 1
            self.menuDict["selectedItem"] = index

        elif( (self.menuDict["current"] == "Albums") and (downButton == 1) ):  # move songs on the selected album to queue
            # Get first letter of the currently selected artist's name.
            self.changedScreen = True
            albumName = self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]]
            firstL = albumName[0]
            if (firstL in alphaList) and (firstL != 'Z'):
                nextL = chr(ord(firstL) + 1)
                # Find index of the first song that starts with that letter, or greater.
                index = self.menuDict["selectedItem"]
                index += 1
                nextAlbum = self.menuDict[self.menuDict["current"]][index]
                nextAlbumFirstL = nextAlbum[0]
                while( nextAlbumFirstL <= firstL ):
                    index += 1
                    nextAlbum = self.menuDict[self.menuDict["current"]][index]
                    nextAlbumFirstL = nextAlbum[0]
                self.menuDict["selectedItem"] = index
            elif ( firstL != 'Z'):
                index = self.menuDict["selectedItem"]
                index += 1
                nextAlbum = self.menuDict[self.menuDict["current"]][index]
                nextAlbumFirstL = nextAlbum[0]
                while( nextAlbumFirstL != 'A' ):
                    index += 1
                    nextAlbum = self.menuDict[self.menuDict["current"]][index]
                    nextAlbumFirstL = nextAlbum[0]
                self.menuDict["selectedItem"] = index
        elif( (self.menuDict["current"] == "Albums") and (downButton == 0) ):  # DOWN was pressed, jump down 8 albums
            self.changedScreen = True
            index = self.menuDict["selectedItem"]
            index += 8
            if( index > (len(self.menuDict[self.menuDict["current"]])-1) ):
                index = len(self.menuDict[self.menuDict["current"]]) - 1
            self.menuDict["selectedItem"] = index

        return "updateList"

    def gotomenu(self):
        #if self.menuDict["current"] == "musicController":
        self.changedScreen = True
        self.menuDict["selectedItem"] = 0
        self.menuDict["current"] = "Main"
        return None

    def select(self, playMode):
        # The only use of 'playMode' is that if the list of songs is currently on the screen, then build the
        #     song list que appropriate to the playback mode currently in place.
        #print("Entering select with", self.menuDict["current"] )
        if self.menuDict["current"] == "Artists":
            # Screen is showing a list of Artists, and one was just clicked on,
            #    so build a list of all songs by that Artist, then exit.
            self.changedScreen = True
            tempList = []
            for item in self.menuDict["Songs"]:
                if item[1] == self.menuDict["Artists"][self.menuDict["selectedItem"]]:
                    tempList.append(item)
            self.menuDict["list"] = tempList
            self.menuDict["current"] = "list"  # Says "the next thing to do is to display this list"
            self.menuDict["selectedItem"] = 0

        elif self.menuDict["current"] == "Albums":
            # Screen is showing a list of Albums, and one was just clicked on,
            #    so build a list of all songs on that Album, then exit.
            self.changedScreen = True
            tempList = []
            for item in self.menuDict["Songs"]:
                if item[2] == self.menuDict["Albums"][self.menuDict["selectedItem"]]:
                    tempList.append(item)
            self.menuDict["list"] = tempList   # Puts into list
            self.menuDict["current"] = "list"  # Says "the next thing to do is to display this list"
            self.menuDict["selectedItem"] = 0

        elif self.menuDict["current"] == "Genres":
            # Screen is showing a list of genres, and one was just clicked on.
            self.changedScreen = True
            tempList = []
            for item in self.menuDict["Songs"]:
                if item[4] == self.menuDict["Genres"][self.menuDict["selectedItem"]]:
                    tempList.append(item)
            self.menuDict["list"] = tempList
            self.menuDict["current"] = "list"
            self.menuDict["selectedItem"] = 0

        elif self.menuDict["current"] == "Queue": # Screen shows "Clear queue" + songs on the que.
            # And, user clicked on a song. So start playing that song.
            if self.menuDict["Queue"]:
                return "playAtIndex"

        elif self.menuDict["current"] == "list": # Not 'Songs' list, not 'Queue' list
            # Executed when a list (eg, songs by album/artist/genre) is shown and
            #    upon a song being selected by hitting ENTER.
            tempList = list(self.menuDict[self.menuDict["current"]])
            self.menuDict["Queue"] = tempList
            return "playGotoTop"

        elif self.menuDict["current"] == "Songs":
            # Screen is showing a list of all the Songs, and a song was clicked on.
            if( playMode == "Normal" ):
                #tempList = list(self.menuDict[self.menuDict["current"]]) # List of all Songs, sorted alphabetically.
                #indexOfSelected = self.menuDict["selectedItem"]
                self.menuDict["Queue"] = list(self.menuDict[self.menuDict["current"]])   # Put all songs onto the Queue, sorted alpha
            elif( playMode == "Shuffle" ):
                #indexOfSelected = self.menuDict["selectedItem"]
                self.menuDict["Queue"] = self.menuDict[self.menuDict["current"]]
                self.menuDict["Queue"] = random.sample( self.menuDict["Queue"], len(self.menuDict["Queue"]) )
                # Now put the selected song at the beginning of the que, so it plays first.
                self.menuDict["Queue"].insert(0, self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]])
                self.menuDict["selectedItem"] = 0   # The song to play is now the first one on the queue.
                #print("Que was empty. Filled SHUFFLE. Size:", len(self.menuDict["Queue"] ) )
            else:
                # Play mode is "Repeat1" so put just that song onto the play que. After it plays, main.py will figure it out.
                self.menuDict["Queue"].insert(0, self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]])
                self.menuDict["selectedItem"] = 0   # The song to play is now the first one on the queue.
            return "playGotoTop"

        elif self.menuDict["current"] == "Settings":
            if self.menuDict["Settings"][self.menuDict["selectedItem"]] == "Update library":
                return "updateLibrary"
            elif self.menuDict["Settings"][self.menuDict["selectedItem"]] == "Sleep":
                return "toggleSleep"
            elif self.menuDict["Settings"][self.menuDict["selectedItem"]] == "Shutdown":
                return "shutdown"
            elif self.menuDict["Settings"][self.menuDict["selectedItem"]] == "Turn EQ On":
                return "EQOn"
            elif self.menuDict["Settings"][self.menuDict["selectedItem"]] == "Turn EQ Off":
                return "EQOff"

        elif self.menuDict["current"] == "Play Mode":
            if self.menuDict["Play Mode"][self.menuDict["selectedItem"]] == "Normal":
                return "Normal"
            elif self.menuDict["Play Mode"][self.menuDict["selectedItem"]] == "Shuffle":
                return "Shuffle"
            elif self.menuDict["Play Mode"][self.menuDict["selectedItem"]] == "Repeat 1 Song":
                return "Repeat1"

        else:
            self.changedScreen = True
            #print("In 'else' with 'current' screen =", self.menuDict["current"] )
            if self.menuDict[self.menuDict["current"]]:  # Does current menu screen has sub-screens? If so, do:
                self.menuDict["history"].append(self.menuDict["current"])  # update history
                self.menuDict["current"] = self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]]  # go to next menu
                #print(self.menuDict["current"])
            self.menuDict["selectedItem"] = 0
            #print("Exiting 'else' with 'current' screen =", self.menuDict["current"] )
            if self.menuDict["current"] == "Songs":
                return "setSongSelectedItem"          # Clicked on "Songs". If one is playing, change index so it is centered later.
            if self.menuDict["current"] == "Shutdown":
                return "shutdown"
            if self.menuDict["current"] == "Albums":
                return "setAlbumSelectedItem"         # Clicked on "Albums". Set index so this album is centered later.
            if self.menuDict["current"] == "Artists":
                return "setArtistSelectedItem"        # Clicked on "Artists". As above.
            if self.menuDict["current"] == "Genres":
                return "setGenreSelectedItem"         # Clicked on "Genre". As above.
        return None

    def loadMetadata(self):
        file = open("/home/pi/info.csv", "rt")
        self.menuDict["Artists"] = []
        self.menuDict["Albums"] = []
        self.menuDict["Songs"] = []
        self.menuDict["Genres"] = []
        metadata = []
        try:
            reader = csv.reader(file)
            for row in reader:
                # If artist name is fully capitalized, let it remain so.
                artistClear = row[1].lstrip()
                albumClear = row[2].lstrip().lower().title()
                genreClear = row[4].lstrip().lower().title()
                if artistClear != "":
                    if artistClear not in self.menuDict["Artists"]:
                        self.menuDict["Artists"].append(artistClear)
                if albumClear != "":
                    if albumClear not in self.menuDict["Albums"]:
                        self.menuDict["Albums"].append(albumClear)
                if genreClear != "":
                    if genreClear not in self.menuDict["Genres"]:
                        self.menuDict["Genres"].append(genreClear)
                if row[3].lstrip() != "":
                    metadata.append(
                        [row[0], artistClear, albumClear, row[3].lstrip(), genreClear])  # [filename, artist, album, title, genre]
        finally:
            file.close()

        self.menuDict["Artists"].sort(key=lambda x: x.lower() ) # Put "all-caps" artists in order, as if lower case.
        self.menuDict["Albums"].sort()
        self.menuDict["Genres"].sort()
        self.menuDict["Songs"] = sorted(metadata, key=lambda meta: meta[3])
