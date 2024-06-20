import vlc
import random
import alsaaudio
import os
import csv
import taglib
import time

# 32 Hz, 64, 128, 256, 512, 1 kHz, 2 kHz, 4, 8, 16 kHz
MY_EQ = [10,8,3,0,0,0,0,0,7,10]  # gain, in dB, for each band.
eqFreqs = []

class music():
    playbackMode = "Shuffle"        # mode = Normal, Shuffle, Repeat1
    UseMeta = False  # If False, use MP3 filename as the source of title/artist metadata.
                     # If True,  use the metadata inside the MP3 file.
    volume = 50      # alsaaudio volume
    playlist = [["", "", "", "", "", ""]]   # data: path to MP3 file, Artist, Album, Title, Genre, Track
    volVLC = 0
    currentSongIndex = 0   # This is the source-of-truth about which song on the "playlist[]" will get played.
        # NOTE: The variable menu.menuDict["selectedItem"] is only for displaying lists; the selected item on that list.
    flagEQ = False
    AlbumNoKey = 0
    AlbumEmptyField = 0
    ArtistNoKey = 0
    ArtistEmptyField = 0
    TitleNoKey = 0
    TitleEmptyField = 0
    GenreNoKey = 0
    GenreEmptyField = 0
    TrackNoKey = 0
    TrackEmptyField = 0

    def __init__(self):
        self.vlcInstance = vlc.Instance('--no-video --quiet')
        self.player = self.vlcInstance.media_player_new()
        self.alsa = alsaaudio.Mixer(alsaaudio.mixers()[0])
        self.alsa.setvolume(self.volume)
        #self.volVLC = vlc.libvlc_audio_get_volume(self.player)  # VLC volume
        #print("Read volume as", self.volVLC)
        self.volVLC = 100
        # Setup Audio Equalizer
        self.eq = vlc.AudioEqualizer()
        bandCount = vlc.libvlc_audio_equalizer_get_band_count()  # Returns: 10
        eqAmps = MY_EQ
        for bandIndex in range(bandCount):
            amp = eqAmps[bandIndex]
            self.eq.set_amp_at_index(amp, bandIndex)
            eqFreqs.append(vlc.libvlc_audio_equalizer_get_band_frequency(bandIndex))
        #print(f'Freq: {" ".join(map(str, eqFreqs))}')
        #print(f'Amp: {" ".join(map(str, eqAmps))}')
        self.changedScreen = False

    def query4Update(self):
        return self.changedScreen

    def clearUpdateFlag(self):
        self.changedScreen = False
        return

    def backup(self, backupAmount):
        mtime = self.player.get_time()
        mtime -= backupAmount
        if mtime < 0:
            mtime = 0
        self.player.set_time( mtime )

    def jumpForward( self, forwardAmount ):
        currentTime = self.player.get_time()
        maxTime = self.player.get_length()
        jumpTo = currentTime + forwardAmount
        if( jumpTo <= (maxTime - 1000) ):
            self.player.set_time( jumpTo )
        return

    def setPlaybackMode(self, pmode):
        self.playbackMode = pmode
        return 1

    def getPlaybackMode(self):
        return self.playbackMode

    def enableEQ(self):
        if self.flagEQ:
            pass   # Do nothing if EQ was already enabled.
        else:
            self.flagEQ = True
            self.player.set_equalizer(self.eq)
            #print("Enable. Setting volume to", self.volVLC)
            vlc.libvlc_audio_set_volume(self.player, 100)
        return 1

    def disableEQ(self):
        if self.flagEQ:
            self.flagEQ = False
            #print("Disable. Setting volume to", self.volVLC-30)
            vlc.libvlc_audio_set_volume(self.player, 70)
            self.player.set_equalizer(None)
        else:
            pass   # Do nothing if EQ was already disabled.
        return 1

    def getStatus(self):
        status = {
            "songLength": self.player.get_length(),
            "currentTime": self.player.get_time(),
            "currentSong": self.playlist[self.currentSongIndex],
            "volume": self.alsa.getvolume()[0],
            "playlist": self.playlist,
            "index": self.currentSongIndex
        }
        return status

    def getSong(self):
        return self.playlist[self.currentSongIndex]

    def loop(self):
        if self.player.get_state() == vlc.State.Ended:
            if( self.playbackMode != "Repeat1" ):
                self.currentSongIndex += 1
                if( self.currentSongIndex == len(self.playlist) ):  # If it's just played final song on playlist, start over.
                    self.currentSongIndex = 0
            self.play()
        return None

    def loadList( self, songList, songIndex ):
        self.playlist = songList
        self.currentSongIndex = songIndex
        self.play()

    def insertList( self, list2Insert ):
        insertPoint = int( self.currentSongIndex + 1 )
        #if( insertPoint >= len( self.playlist ) ):
            #insertPoint = 0
        self.playlist[ insertPoint:insertPoint ] = list2Insert

    def wipePrior(self):
        # Put current song at the top of the playlist
        self.playlist.insert( 0, self.playlist.pop( self.currentSongIndex ) )
        # Keep playing current song, keep displaying the current song on top screen, etc...
        self.currentSongIndex = 0
        # Delete the rest of the playlist, keeping only the current song at the top of the list.
        del self.playlist[1:]
        return

    def updateList(self, newList):
        if self.playlist[0] == ["", "", "", "", "", ""]:
            self.playlist.pop(0)
            self.playlist = list(newList)
            self.currentSongIndex = 0
            self.play()
        else:
            self.currentSongIndex = newList.index(self.playlist[self.currentSongIndex])
            self.playlist = newList

    def play(self):
        self.changedScreen = True    # About to start playing a song, so update the screen.
        self.player.set_media(self.vlcInstance.media_new_path(self.playlist[self.currentSongIndex][0]))
        #print("About to play:", self.playlist[self.currentSongIndex][0] )
        self.player.play()
        # When starting a new song, VLC takes a bit of time to return the proper length.
        count = 0
        temp = self.player.get_length()
        while( (temp == 0) and (count <= 20) ):
            count += 1
            time.sleep( 0.06 )
            temp = self.player.get_length()

    def playAtIndex(self, index):
        self.currentSongIndex = index
        self.player.set_media(self.vlcInstance.media_new_path(self.playlist[self.currentSongIndex][0]))
        self.changedScreen = True    # About to start playing a song, so update the screen.
        self.player.play()

    def playPause(self):
        if self.player.get_state() == vlc.State.Playing:
            self.player.pause()
        elif not self.player.get_state() == vlc.State.Playing:
            self.player.play()

    def shuffle(self):
        # Before shuffling remove the already played songs to make sure these don't get played again
        tempPlaylist = self.playlist[self.currentSongIndex + 1::]
        random.shuffle(tempPlaylist)
        # Add the already played songs to the front again
        self.playlist = self.playlist[:self.currentSongIndex + 1] + tempPlaylist

    def unshuffle(self):
        # Put all songs in the que into alphabetical order.
        tempPlaylist = self.playlist[self.currentSongIndex + 1::]
        tempPlaylist.sort()
        # Add the already played songs to the front again
        self.playlist = self.playlist[:self.currentSongIndex + 1] + tempPlaylist

    def clearQueue(self):
        self.playlist = [["", "", "", "", "", ""]]
        self.currentSongIndex = 0
        #self.player.stop()
        self.changedScreen = True

    def next(self):
        if( self.playbackMode != "Repeat1" ):
            self.currentSongIndex += 1
            if( self.currentSongIndex == len(self.playlist) ):  # If it's just played final song on playlist, start over.
                self.currentSongIndex = 0
        self.play()

    def prev(self):
        if (self.currentSongIndex > 0) and (self.playbackMode != "Repeat1"):
            self.currentSongIndex -= 1
        self.play()

    def volumeUp(self):
        if self.volume <= 95:
            self.volume += 5
            self.alsa.setvolume(self.volume)

    def volumeDown(self):
        if self.volume > 5:
            self.volume -= 5
            self.alsa.setvolume(self.volume)

    def updateLibrary(self):
        self.playPause()
        fileList = []
        musicPath = "/home/pi/Music/"

        for path, dirs, files in os.walk(musicPath):
            for file in files:
                if file.endswith('.mp3') or file.endswith('.MP3') or file.endswith('.Mp3') or \
                    file.endswith('.m4a') or file.endswith('.wav') or file.endswith('.wma') or \
                    file.endswith('.WAV'):
                    fileList.append(os.path.join(path, file))

        file = open("/home/pi/info.csv", "w", newline="")
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        for i in fileList:
            #TODO: .wav files are not handled well(?). Must use metadata derived from filename, only.(?)
            audiofile = taglib.File(i)
            song = audiofile.tags
            if self.UseMeta:  # Metadata source = metadata in the MP3 file.
                # Check to see if the "ARTIST" field is empty, or does not exist.
                #    If does not exist, fill it in with "Not Sure"
                if( 'ARTIST' in song ):
                    if( song['ARTIST'] == [] ):  # Key exists, but points to empty field.
                        self.ArtistEmptyField += 1
                        song['ARTIST'] = ['Unknown ARTIST']  # Found none of these
                    else:
                        pass  # Artist field was filled in. Is legit.
                else:
                    self.ArtistNoKey += 1
                    song['ARTIST'] = ['Unknown ARTIST']   # Found 26 of these

                # Check to see if the "TITLE" field is empty, or does not exist.
                if( 'TITLE' in song ):
                    if( song['TITLE'] == [] ):  # Key exists, but points to empty field.
                        self.TitleEmptyField += 1
                        song['TITLE'] = ['Unknown TITLE']  # Found none of these
                    else:
                        pass  # Album field was filled in. Is legit.
                else:
                    self.TitleNoKey += 1
                    song['TITLE'] = ['Unknown TITLE']   # Found 41 of these

            else:   # Metadata source = the MP3 filename string.
                # MP3 filenames must look exactly like this:
                #    "/home/pi/Music/Thisartist - Thistitle.mp3"
                artist = i.split(" -")
                newartist = artist[0].split("/")
                stringArtist = newartist[4].lstrip()
                song['ARTIST'] = [stringArtist]
                try:
                    title = i.split("- ")
                except:
                    #print("Error splitting!",i)
                    pass
                try:
                    newtitle = title[1].split(".")
                except:
                    #print("Error splitting",i)
                    pass
                stringTitle = newtitle[0].lstrip()
                song['TITLE'] = [stringTitle]

            # Check to see if the "ALBUM" field is empty, or does not exist.
            if( 'ALBUM' in song ):
                if( song['ALBUM'] == [] ):  # Key exists, but points to empty field.
                    self.AlbumEmptyField += 1
                    song['ALBUM'] = ['Unknown ALBUM']  # Found 1635 of these
                else:
                    pass  # Album field was filled in. Is legit.
            else:
                self.AlbumNoKey += 1
                song['ALBUM'] = ['Unknown ALBUM']   # Found 174 of these

            # Check to see if the "GENRE" field is empty, or does not exist.
            if( 'GENRE' in song ):
                if( song['GENRE'] == [] ):  # Key exists, but points to empty field.
                    self.GenreEmptyField += 1
                    song['GENRE'] = ['Unknown GENRE']  # Found 16 of these
                else:
                    pass  # Genre field was filled in. Is legit.
            else:
                self.GenreNoKey += 1
                song['GENRE'] = ['Unknown GENRE']   # Found 52 of these

            # Now do the 'TRACK' information
            if( 'TRACKNUMBER' in song ):
                if( song['TRACKNUMBER'] == [] ):  # Key exists, but points to empty field.
                    self.TrackEmptyField += 1
                    song['TRACKNUMBER'] = ['0']  # Found 2146 of these
                else:
                    #print(song['TRACKNUMBER'] )
                    #if( '/' in str(song['TRACKNUMBER']) ):
                        #print(song['ALBUM'])
                    pass  # Genre field was filled in. Is legit.
            else:
                self.TrackNoKey += 1
                song['TRACKNUMBER'] = ['0']   # Found 158 of these

            # At this point, the following writer call should never fail.
            try:
                writer.writerow( (i, song["ARTIST"][0], song["ALBUM"][0], song["TITLE"][0], song["GENRE"][0], song["TRACKNUMBER"][0]) )
            except:
                print("Unknown write error",i)
                pass
                try:
                    pass
                    #print(song["ARTIST"][0])
                    #print(song["ALBUM"][0])
                    #print(song["TITLE"][0])
                    #print(song["GENRE"][0])
                    #print(song["TRACKNUMBER"][0])
                except:
                    pass
        file.close()
        #print("Done writing metadata file.")
        #print("ArtistNoKey = ", self.ArtistNoKey)
        #print("ArtistEmptyField = ", self.ArtistEmptyField)
        #print("TitleNoKey = ", self.TitleNoKey)
        #print("TitleEmptyField = ", self.TitleEmptyField)
        #print("AlbumNoKey = ", self.AlbumNoKey)
        #print("AlbumEmptyField = ", self.AlbumEmptyField)
        #print("GenreNoKey = ", self.GenreNoKey)
        #print("GenreEmptyField = ", self.GenreEmptyField)
        #print("TrackNoKey = ", self.TrackNoKey)
        #print("TrackEmptyField = ", self.TrackEmptyField)
        return 1
