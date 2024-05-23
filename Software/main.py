
import playback
import display
import navigation
import device
import sys
import os
import time

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
        #print("display.py asked")
        need = True
    if( music.query4Update() ):
        #print("playback.py asked")
        need = True
    if( menu.query4Update() ):
        #print("navigation.py asked")
        need = True
    return need

def clearUpdateFlags():
    music.clearUpdateFlag()
    menu.clearUpdateFlag()
    view.clearUpdateFlag()
    return

done = False
music = playback.music()
music.enableEQ()
view = display.view()
menu = navigation.menu()
PiPod = device.PiPod()

updateScreenCounter = 0

try:
    with open("/home/drh/info.csv", "r") as myFile:
        myFile.close()
except FileNotFoundError:
    view.popUp("Updating Library\nPlease Wait...")
    music.updateLibrary()  # This creates the info.csv file by reading every .MP3 file metadata.
menu.loadMetadata()   # This reads the info.csv file
status = PiPod.getStatus()
songMetadata = music.getStatus()

#Set the display of the playback mode to match the actual playback mode.
view.setPlayMode( music.getPlaybackMode() )

menu.setUpdateFlag()

status = PiPod.getStatus()         # Reads battery voltage
songMetadata = music.getStatus()   # Get song length, how far in, song info, vol, playlist, index of current song
temp = view.update(status, menu.menuDict, songMetadata) # Creates the screen and writes to frame buffer
#view.setBaseImage()
temp = view.partialUpdate(status, menu.menuDict, songMetadata) # Only upates the time into song, and the bar.
view.partialRefresh()

while not done:
    PiPod.scan_switches()
    music.loop()    # Checks if song has ended, and starts playing next song on que (if not empty).
    pressed = PiPod.getKeyPressed()   # If no key was pressed, returns -1.
    if( pressed != -1 ):
        PiPod.clearKeyPressed()
        # The following code only runs if a key was pressed.
        if pressed == K_ESCAPE:
            if menu.menuDict["current"] != "musicController":
                action = menu.escape()

        elif pressed == K_u:
            music.volumeUp()

        elif pressed == K_d:
            music.volumeDown()

        elif pressed == K_UP:
            if menu.menuDict["current"] == "musicController":
                menu.gotomenu()
            else:
                action = menu.up()

        elif pressed == K_DOWN:
            if menu.menuDict["current"] == "musicController":
                music.backup( 5000 ) # Back up this many milliseconds
                menu.setUpdateFlag() # Indicate that the screen needs to be updated.
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            music.backup( 5000 ) # Back up this many milliseconds
            else:
                action = menu.down()

        elif pressed == K_LEFT:
            if menu.menuDict["current"] == "musicController":
                music.prev()
            else:
                action = menu.left()

        elif pressed == K_RIGHT:
            if menu.menuDict["current"] == "musicController":
                music.next()
            else:
                action = menu.right()

        elif pressed == K_RETURN:
            if menu.menuDict["current"] == "musicController":
                music.playPause()
            else:
                currentMode = music.getPlaybackMode()
                action = menu.select( currentMode )
                if action == "play":
                    music.loadList(menu.menuDict["Queue"])
                    music.play()
                elif action == "clearQueue":
                    menu.menuDict["Queue"] = []
                    music.clearQueue()
                elif action == "updateLibrary":
                    view.popUp("Updating Library")
                    music.player.stop
                    music.updateLibrary()  # Re-create the info.csv file
                    menu.loadMetadata()    # Re-read the info.csv file
                    menu.setUpdateFlag()
                elif action == "shutdown":
                    #view.popUp("Shutting down now\nThank You\nFor Playing.")
                    view.shutdownImage()
                    os.system("sudo shutdown now")
                elif action == "exit":
                    view.clearAndDisplay()
                    view.shutdownScreen()
                    sys.exit(0)
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
                    if thisSong != ['', '', '', '', '']:
                        thisIndex = songList.index( thisSong )
                        menu.setSelectedItem( thisIndex )
                elif action == "setAlbumSelectedItem":
                    # Change menuDict["selectedItem"] so that the currently-playing song's Album is centered.
                    # Find the album of the current song.
                    thisSong = music.playlist[music.currentSongIndex]
                    if thisSong != ['', '', '', '', '']:
                        thisAlbum = thisSong[2]   # [2] points to the Album name for this song
                        # Now get the index of that album on the list of Albums.
                        albumList = list( menu.menuDict["Albums"] )
                        thisIndex = albumList.index( thisAlbum )
                        menu.setSelectedItem( thisIndex )
                elif action == "setArtistSelectedItem":
                    # Change menuDict["selectedItem"] so that the currently-playing song's Artist is centered.
                    # Find the artist of the current song.
                    thisSong = music.playlist[music.currentSongIndex]
                    if thisSong != ['', '', '', '', '']:
                        thisArtist = thisSong[1]   # [1] points to the Artist name of the song
                        # Now get the index of that artist on the list of Artists.
                        artistList = list( menu.menuDict["Artists"] )
                        thisIndex = artistList.index( thisArtist )
                        menu.setSelectedItem( thisIndex )
                elif action == "setGenreSelectedItem":
                    # Change menuDict["selectedItem"] so that the currently-playing song's Album is centered.
                    # Find the album of the current song.
                    thisSong = music.playlist[music.currentSongIndex]
                    if thisSong != ['', '', '', '', '']:
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

        # The next line gets executed every time a key was pressed.
        pass

    # Done handling key presses, so continue.
    updateScreenCounter += 1
    if( updateScreenCounter >= 50 ):
        # This code only runs once every 5 seconds.
        updateScreenCounter = 0
        if ( menu.menuDict["current"] == "musicController" ):
            status = PiPod.getStatus()         # Reads battery voltage
            songMetadata = music.getStatus()   # Get song length, how far in, song info, vol, playlist, index of current song
            temp = view.update(status, menu.menuDict, songMetadata) # Creates the screen and writes to frame buffer
            temp = view.partialUpdate(status, menu.menuDict, songMetadata) # Only upates the time into song, and the bar.
            view.partialRefresh()

    # Now we check to see if any Class has modified the screen.
    if( needToUpdate() ):
        clearUpdateFlags()
        status = PiPod.getStatus()         # Reads battery voltage
        songMetadata = music.getStatus()   # Get song length, how far in, song info, vol, playlist, index of current song
        temp = view.update(status, menu.menuDict, songMetadata) # Creates the screen and writes to frame buffer
        view.refresh()
        # If just drew the top screen, set it as the base image for later partial updates.
        if( menu.menuDict["current"] == "musicController"):
            view.setBaseImage()
        pass

    time.sleep(0.1) # Pause 0.1 seconds. No need to check for key presses faster than that.
