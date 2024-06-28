import playback
import display
import navigation
import device
import sys
import os
import time

# How often to update the top screen, in tenths of a second (50 = 5 seconds).
refreshTime = 50

# Provide a name for the values that PiPod.getKeyPressed() will return
K_u = 0
K_d = 1
K_UP = 2
K_DOWN = 3
K_LEFT = 4
K_RIGHT = 5
K_RETURN = 6
K_ESCAPE = 7

def needToUpdate():
    # Call every Class's method to see if they modified the screen
    need = False
    if( view.query4Update() ):
        need = True
        view.clearUpdateFlag()
    if( music.query4Update() ):
        need = True
        music.clearUpdateFlag()
    if( menu.query4Update() ):
        need = True
        menu.clearUpdateFlag()
    return need

music = playback.music()
music.enableEQ()
view = display.view()
menu = navigation.menu()
PiPod = device.PiPod()

updateScreenCounter = 0
refreshNow = False
stopRefreshing = False

# Check to see if a music metadata file has been created. If not, create one.
try:
    with open("/home/pi/info.csv", "r") as myFile:
        myFile.close()
except FileNotFoundError:
    view.popUp("Updating Library\nPlease Wait...")
    music.updateLibrary()  # This creates the info.csv file by reading every .MP3 file metadata.
menu.loadMetadata()   # This reads the info.csv file
status = PiPod.getStatus()
songMetadata = music.getStatus()

# Set the display of the playback mode to match the actual playback mode.
view.setPlayMode( music.getPlaybackMode() )
# Cause the screen to be drawn immediately.
menu.setUpdateFlag()

while True:
    music.loop()    # Checks if song has ended, and starts playing next song on que (if not empty).
    PiPod.scan_switches()
    pressed = PiPod.getKeyPressed()   # If no key was pressed, returns -1.
    if( pressed != -1 ):
        # This code only runs if a key was pressed.
        PiPod.clearKeyPressed()
        if pressed == K_ESCAPE:    # Button on the top upper left. Moves UP the menu tree.
            if menu.menuDict["current"] != "musicController":
                action = menu.escape()

        elif pressed == K_u:
            music.volumeUp()
            refreshNow = True

        elif pressed == K_d:
            music.volumeDown()
            refreshNow = True

        elif pressed == K_UP:      # "up" arrow on the front navigation button array.
            if menu.menuDict["current"] == "musicController":
                menu.gotomenu()
            else:
                action = menu.up()

        elif pressed == K_DOWN:
            if menu.menuDict["current"] != "musicController":
                action = menu.down()

        elif pressed == K_LEFT:
            # Before calling the code to handle the keypress, check the status of the K_DOWN button.
            state17 = PiPod.isPressed(17)     # state17 = 1 (DOWN button NOT pressed) or 0 (DOWN button IS pressed).
            if( menu.menuDict["current"] == "musicController" ):
                if( state17 == 1 ):
                    music.prev()
                else:
                    music.backup( 5000 )   # Back up 5 seconds
                    refreshNow = True
            else:
                # DOWN+LEFT and DOWN+RIGHT do small jumps up/down a list.
                action = menu.left( state17 )

        elif pressed == K_RIGHT:
            # Before calling the code to handle the keypress, check the status of the K_DOWN button.
            state17 = PiPod.isPressed(17)     # state17 = 1 (DOWN button NOT pressed) or 0 (DOWN button IS pressed).
            if( menu.menuDict["current"] == "musicController" ):
                if( state17 == 1 ):
                    music.next()
                else:
                    music.jumpForward( 5000 )   # Jump forward 5 seconds
                    refreshNow = True
            else:
                # DOWN+LEFT and DOWN+RIGHT do small jumps up/down a list.
                action = menu.right( state17 )

        elif pressed == K_RETURN:    # Center navigation button
            if menu.menuDict["current"] == "musicController":
                music.playPause()
            else:
                currentMode = music.getPlaybackMode()
                currentSongInformation = music.getSong()
                action = menu.select( currentMode, currentSongInformation )
                if action == "playGotoTop":
                    songSelectedItem = 0     # Play starting at the top of the list
                    music.loadList(menu.menuDict["Queue"], songSelectedItem )
                    menu.upTree(2)
                elif action == "play":
                    songSelectedItem = menu.getSelectedItem()    # Play the list starting at the highlighted item
                    music.loadList(menu.menuDict["Queue"], songSelectedItem )
                    menu.upTree(2)
                elif action == "switch2Genre":    # Keep playing current song. Wipe list of prior songs. Append Que.
                    music.wipePrior()
                    music.insertList( menu.menuDict["Queue"] )
                    menu.upTree(2)
                #elif action == "clearQueue":
                    #menu.menuDict["Queue"] = []
                    #music.clearQueue()
                elif action == "updateLibrary":
                    view.popUp("Updating Library")
                    music.player.stop
                    music.updateLibrary()  # Re-create the info.csv file
                    menu.loadMetadata()    # Re-read the info.csv file
                    menu.setUpdateFlag()
                elif action == "shutdown":
                    #view.popUp("Shutting down now\nThank You\nFor Playing.")
                    view.shutdownImage()
                    stopRefreshing = True
                    os.system("sudo shutdown now")
                elif action == "playAtIndex":
                    if menu.menuDict["selectedItem"] == 0:
                        music.clearQueue()
                        menu.menuDict["Queue"] = []
                    else:
                        music.playAtIndex(menu.menuDict["selectedItem"]-1)
                elif action == "setSongSelectedItem":
                    # Change menuDict["selectedItem"] so that the currently-playing Song is centered on the list.
                    songList = list( menu.menuDict["Songs"] )
                    thisSong = music.playlist[music.currentSongIndex]
                    if thisSong != ['', '', '', '', '', '']:
                        thisIndex = songList.index( thisSong )
                        menu.setSelectedItem( thisIndex )
                elif action == "setAlbumSelectedItem":
                    # Change menuDict["selectedItem"] so that the currently-playing song's Album is centered.
                    # Find the album of the current song.
                    thisSong = music.playlist[music.currentSongIndex]
                    if thisSong != ['', '', '', '', '', '']:
                        thisAlbum = thisSong[2]   # [2] points to the Album name for this song
                        # Now get the index of that album on the list of Albums.
                        albumList = list( menu.menuDict["Albums"] )
                        thisIndex = albumList.index( thisAlbum )
                        menu.setSelectedItem( thisIndex )
                elif action == "setArtistSelectedItem":
                    # Change menuDict["selectedItem"] so that the currently-playing song's Artist is centered.
                    # Find the artist of the current song.
                    thisSong = music.playlist[music.currentSongIndex]
                    if thisSong != ['', '', '', '', '', '']:
                        thisArtist = thisSong[1]   # [1] points to the Artist name of the song
                        # Now get the index of that artist on the list of Artists.
                        artistList = list( menu.menuDict["Artists"] )
                        thisIndex = artistList.index( thisArtist )
                        menu.setSelectedItem( thisIndex )
                elif action == "setGenreSelectedItem":
                    # Change menuDict["selectedItem"] so that the currently-playing song's Album is centered.
                    # Find the album of the current song.
                    thisSong = music.playlist[music.currentSongIndex]
                    if thisSong != ['', '', '', '', '', '']:
                        thisGenre = thisSong[4]     # [4] points to the Genre of the song
                        # Now get the index of that genre on the list of Genres.
                        genreList = list( menu.menuDict["Genres"] )
                        thisIndex = genreList.index( thisGenre )
                        menu.setSelectedItem( thisIndex )
                elif action == "EQOn":
                    music.enableEQ()
                elif action == "EQOff":
                    music.disableEQ()
                elif (action == "Normal" or action == "Shuffle" or action == "Repeat1"):
                    view.setPlayMode( action ) # Used to show the current play mode on the "set mode" screen
                    currentMode = music.getPlaybackMode()
                    if( currentMode != action ):
                        menu.setUpdateFlag()
                        music.setPlaybackMode(action)
                        # Now fill the playback que according to the new Playback Mode
                        if action == "Shuffle":
                            music.shuffle()
                        if action == "Normal":
                            music.unshuffle()
                elif action == "insertQueue":    # Take the list of currently-playing songs, and insert the Queue into it.
                    music.insertList( menu.menuDict["Queue"] )
                    menu.upTree(2)     # Set screen back at top-level screen
                elif action == "showTopScreen":
                    menu.upTree(2)
                #else:
                    #print("No command found for that keypress")
        # The next line gets executed every time a key was pressed.
        pass

    # Done handling key presses, so continue.
    updateScreenCounter += 1
    if( ((updateScreenCounter >= refreshTime) or (refreshNow)) and (stopRefreshing == False) ):
        # This code only runs once every 5 seconds, or if some code specifically requested it.
        refreshNow = False
        updateScreenCounter = 0
        if ( menu.menuDict["current"] == "musicController" ):
            status = PiPod.getStatus()         # Reads battery voltage
            if( float(status[1]) <= 3.15 ):
                # If battery voltage is too low, shutdown the unit.
                view.shutdownImage()
                stopRefreshing = True
                os.system("sudo shutdown now")
            songMetadata = music.getStatus()   # Get song length, how far in, song info, vol, playlist, index of current song
            temp = view.update(status, menu.menuDict, songMetadata) # Creates the screen and writes to frame buffer
            temp = view.partialUpdate(status, menu.menuDict, songMetadata) # Only upates the time into song, and the bar.
            view.partialRefresh()   # No screen flash
            #view.setBaseImage()    # Causes screen flash

    # Now we check to see if any Class has modified the screen.
    if( needToUpdate() and (stopRefreshing == False) ):
        status = PiPod.getStatus()         # Reads battery voltage
        songMetadata = music.getStatus()   # Get song length, how far in, song info, vol, playlist, index of current song
        temp = view.update(status, menu.menuDict, songMetadata) # Creates the screen and writes to frame buffer
        view.setBaseImage()

    time.sleep(0.1) # Pause 0.1 seconds. No need to check for key presses faster than that.
