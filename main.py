import playback
import display
import navigation
import device
import pygame
import RPi.GPIO as GPIO
import sys
import os

done = False
music = playback.music()
music.enableEQ()
view = display.view()
menu = navigation.menu()
PiPod = device.PiPod()
clock = pygame.time.Clock()

# Updating 6750 files takes 50 seconds
#view.popUp("Updating Library")
#music.updateLibrary()  # This creates the info.csv file by reading every .MP3 file metadata.
menu.loadMetadata()   # This reads the info.csv file
status = PiPod.getStatus()
songMetadata = music.getStatus()

# This timer is used to control the speed of the loop.
# But we want to update the LCD screen 5 times per second.
displayUpdate = pygame.USEREVENT + 1
pygame.time.set_timer(displayUpdate, 4000) # Do loop 1/200mS = 5 times per second.

view.update(status, menu.menuDict, songMetadata)

while not done:
    PiPod.scan_switches()
    music.loop()    # Checks if song has ended, and starts playing next song on que (if not empty).
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if menu.menuDict["current"] == "musicController":
                    isAsleep = PiPod.toggleSleep()
                    if isAsleep == True:
                        view.setNoRefresh()
                    else:
                        view.setDoRefresh()
                else:
                    action = menu.escape()

            elif event.key == pygame.K_u:
                music.volumeUp()

            elif event.key == pygame.K_d:
                music.volumeDown()

            elif event.key == pygame.K_UP:
                if status[2]:
                    music.volumeUp()
                elif menu.menuDict["current"] == "musicController":
                    menu.gotomenu()
                else:
                    action = menu.up()

            elif event.key == pygame.K_DOWN:
                if status[2]:
                    music.volumeDown()
                elif menu.menuDict["current"] == "musicController":
                    music.backup( 5000 ) # Back up this many milliseconds
                    #music.shuffle()
                    #menu.menuDict["Queue"] = music.playlist
                else:
                    action = menu.down()

            elif event.key == pygame.K_LEFT:
                if status[2] or menu.menuDict["current"] == "musicController":
                    music.prev()
                else:
                    action = menu.left()

            elif event.key == pygame.K_RIGHT:
                if status[2] or menu.menuDict["current"] == "musicController":
                    music.next()
                else:
                    action = menu.right()
                    #if action == "updateList":
                    #    music.updateList(menu.menuDict["Queue"])

            elif event.key == pygame.K_RETURN:
                if status[2] or menu.menuDict["current"] == "musicController":
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
                        #music.clearQueue()    # TODO? If in, can't play a song after Library update.
                    elif action == "toggleSleep":
                        PiPod.toggleSleep()
                    elif action == "shutdown":
                        view.popUp("Shutdown")
                        os.system("sudo shutdown now")
                        while True:
                            pass
                    elif action == "reboot":
                        view.popUp("Rebooting")
                        os.system("sudo reboot")
                        while True:
                            pass
                    elif action == "exit":
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
                            music.setPlaybackMode(action)
                            # Now fill the playback que according to the new Playback Mode
                            if action == "Shuffle":
                                music.shuffle()
                            if action == "Normal":
                                music.unshuffle()

        if event.type  == displayUpdate:
            if PiPod.isAsleep() == False:
                #print(menu.menuDict["selectedItem"] )
                status = PiPod.getStatus()         # Reads battery voltage, gets "status[2]" = backlight on/off
                songMetadata = music.getStatus()   # Get song length, how far in, song info, vol, playlist, index of current song
                temp = view.update(status, menu.menuDict, songMetadata) # Creates the screen and writes to frame buffer
                #menu.setSelectedItem( temp )
                #print("Got back", temp )
                view.refresh()
        # The next line gets executed every time we check for an event on the que, no matter the event.
        pass
    clock.tick(5)  # Limit the framerate to X FPS, to retain CPU resources

