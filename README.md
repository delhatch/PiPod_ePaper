# PiPod_ePaper
This project takes the github.com/delhatch/PiPod project (which was derived from github.com/BramRausch/PiPod) and replaces the LCD screen with an e-Paper screen.
<table border="1">
  <tr>
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/case1.jpg" width="500" /></td>
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/case2.jpg" width="500" /></td>
  </tr>
  <tr>
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/front_quarter_playing.jpg" width="500" /></td>
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/front_led.jpg" width="500" /></td>
  </tr>
  <tr>
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/PCB_parts_top.JPG" width="500" /></td>
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/back1.jpg" width="400" /></td>
  </tr>
  <tr>
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/back_bare.jpg" width="400" /></td>
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/back3.jpg" width="400" /></td>
  </tr>
</table>
<h3>Motivation</h3>
<p>The goal of this project was switching from a 2.2" 320x240 LCD screen to a 2.13" 250x122 e-Paper screen (from Waveshare) in order to extend the battery run-time.</p>
<p>Using the project's standard 1200 mAh battery, the continuous play time is now <b>4 hours, 48 minutes</b>.</p>
<p>In addition to using an e-paper screen, I also added a headphone amplifier based on the TP6113 IC. Note: This amplifier is rated at 40 mW, which does not sound like a lot of power, but even with inefficient headphones this equates to 108 dBSPL (equivalent to a gas lawn mower at 1m), which is far too loud for sustained listening. Watch your volume setting!</p>
<h3>Project Derivation</h3>
<p>This project is derived from github.com/delhatch/PiPod_Zero2W. This repository has changes to impliment the use of the e-Paper screen, along with other minor bug fixes.</p>
<h3>Structural Changes</h3>
<p>I have changed the OS to the "lite" version: 2024-03-15-raspios-bookworm-arm64-lite.img.xz This change reduces power consumption by ~20 mA, which is a 9% savings, so reasonably significant.</p>
<p>Also moved from Pygame to Pillow for the screen graphics.</p>
<p>Then I got rid of Pygame completely, since I was only using it for the key stroke buffer, and the Python keypad library was already taking care of that. Eliminating Pygame reduced power consumption by 9.2% when idle, and by 5.2% when playing music.</p>
<h3>Status</h3>
<p>31 May 2024: I built a unit with the Rev1 parts (see pics). It works great now, but required pysically re-locating two 220uF capacitors on the PCB (clash with left-arrow navigation push-button), and some minor filing of the case parts so that some of the side buttons moved more easily. The Rev2 files are now in this github repository, and I am fabricating those right now, but have not received them yet.</p>
<h3>Power Savings</h3>
<p>With the LCD screen, with the backlight on, during playback, the current draw is <b>266 mA</b>.</p>
<p>With the LCD screen, with the backlight off, during playback, the current draw is <b>220 mA</b>.</p>
<p>With the e-Paper screen, during playback, the current draw is <b>175 mA</b>.</p>
<p>Having eliminated Pygame, the current draw is down to only <b>166 mA</b>.</p>
<p>So the e-Paper screen is definitely a major improvement in battery life (playback time), and also useability because there is no anxiety about leaving an LCD backlight on.</p>
<h3>Known Bugs</h3>
<ul>
<li>None.</li>
</ul>
<h3>Features TODO</h3>
<ul>
  <li>Eliminate flashing screen on sub-menus.</li>
</ul>
<h3>Instructions</h3>
<p>Completion of these instructions takes about 40 minutes, not including the time transferring the music files.</p>
<p>The bare PC board and case parts can be ordered via this link at <a href="https://www.pcbway.com/project/shareproject/ePaper_PiPod_MP3_music_player_a6adf3e1.html">PCBWay</a>. For the case parts (top, bottom and frame parts) I specified 3D printing in Nylon: PA-12 with 35% glass fill. For the navigation and side buttons, any cheap white plastic will do.</p>
<a href="https://www.pcbway.com/project/shareproject/ePaper_PiPod_MP3_music_player_a6adf3e1.html"><img src="https://www.pcbway.com/project/img/images/frompcbway-1220.png" alt="PCB from PCBWay" /></a>
<p>Instructions:</p>
<ul>
  <li>Download the OS file "2024-03-15-raspios-bookworm-arm64-lite.img.xz" or newer.</li>
  <li>Using rufus-3.22.exe (or similar), burn the image to a 128GB micro-SD card.</li>
  <li>Assuming you have a fully-assembled PiPod hardware: Connect an HDMI monitor to the Pi Zero 2 W. Also connect a USB expander hub such as the SmartQ H302S to the Pi Zero usb connector. Connect a USB keyboard and mouse to the hub.</li>
  <li>Insert the SD card into the Pi Zero 2 W slot.</li>
  <li>Apply power (from a plug-in USB power supply) to the USB connector at the bottom of the PiPod.</li>
  <li>Power-up and go through the configuration screens. Create the user "pi" with a password of your choosing. Reboot and log in.</li>
  <li>At the prompt: <code>sudo raspi-config</code>
    <ul>
      <li>Go into Menu Item #1, then select S1. Enter the SSID and passphrase for your wi-fi.</li>
      <li>Select menu item #1, then select S5 (Boot/Auto-login) select and enable "Console Autologin".</li>
      <li>From the top menu, select #3 "Interface Options" then select and enable I1 "Enable SSH".</li>
      <li>From the top menu, select #3 "Interface Options" then select and enable I4 "Enable I2C".</li>
      <li>Select "Back" to top screen, then "Finish" and then reboot.</li>
    </ul></li>
  <li>Type: <code>sudo nano /boot/firmware/config.txt</code> and make the following changes:
    <ul>
      <li>If necessary, un-comment <tt>dtparam=spi=on</tt> (to turn on the SPI port)</li>
      <li>comment-out the <tt>dtparam=audio=on</tt> line</li>
      <li>If necessary, un-comment out the line <tt>dtparam=12c_arm=on</tt></li>
      <li>At the end of the file, add a line: <tt>dtoverlay=hifiberry-dac</tt></li>
      <li><tt>CTRL-O</tt> and <tt>ENTER</tt> and <tt>CTRL-X</tt> to save and exit.</li>
  </ul>
</li>
  <li><code>sudo reboot</code></li>
  <li>Enter the following lines to install the required packages:
  <ul>
    <li><code>sudo apt install python3</code></li>
    <li><code>sudo apt install build-essential python3-dev python3-smbus -y</code></li>
    <li><code>sudo apt install git -y</code></li>
    <li><code>sudo apt install python3-vlc -y</code></li>
    <li><code>sudo apt install python3-alsaaudio -y</code></li>
    <li><code>sudo apt install pulseaudio -y</code></li>
    <li><code>sudo apt install python3-taglib -y</code></li>
    <li><code>sudo apt install python3-spidev -y</code></li>
    <li><code>sudo apt install python3-gpiozero -y</code></li>
    <li><code>sudo apt install python3-pip -y</code></li>
    <li><code>sudo apt install python3-pil -y</code></li>
    <li><code>sudo apt install python3-numpy -y</code></li>
  </ul>
</li>
<li><code>sudo reboot</code></li>
<li>Verify that the audio is working. Plug headphones into the PiPod and type:
  <ul>
    <li><code>sudo raspi-config</code></li>
    <li>Select line #1, then #2 "Audio"
    <li>Select snd_rpi_hifiberry_dac then Finish</li>
    <li>type: <code>amixer set Master 50%</code></li>
    <li>type: <code>speaker-test -c2</code></li>
    <li>Verify that audio is coming from the headphones and not the HDMI monitor.</li>
    <li><tt>CTRL-C</tt> to finish and quit.</li>
  </ul>
</li>
<li>Install the Adafruit_GPIO library:
  <ul>
    <li>from the home directory (<code>~/</code>) type: <code>git clone https://github&#46;com/adafruit/Adafruit_Python_GPIO.git</code></li>
    <li><code>cd Adafruit_Python_GPIO</code></li>
    <li><code>sudo python3 setup.py install</code></li>
  </ul>
<li>Install the Adafruit Blinka library:
  <ul>
    <li><code>cd ~/</code></li>
    <li><code>sudo pip3 install --break-system-packages Adafruit-Blinka</code></li>
  </ul>
</li>
<li>Install the waveshare e-Paper libraries:
  <ul>
    <li><code>cd ~/</code></li>
    <li><code>git clone https://github&#46;com/waveshare/e-Paper.git</code></li>
    <li><code>sudo pip3 install --break-system-packages waveshare-epaper epd-library</code></li>
  </ul></li>
<li><code>sudo reboot</code></li>
<li>Now fetch the e-Paper MP3 player software from this repository:
  <ul>
    <li><code>cd ~/</code> then type: <code>git clone https://github&#46;com/delhatch/PiPod_ePaper.git</code></li>
    <li><code>cd PiPod_ePaper</code></li>
    <li><code>mv launch.sh ~/.</code></li>
    <li><code>cd ~/</code></li>
    <li><code>chmod 777 launch.sh</code></li>
    <li><code>mkdir .config/systemd</code></li>
    <li><code>mkdir .config/systemd/user</code></li>
    <li><code>cd PiPod_ePaper</code></li>
    <li><code>mv pipod.service ~/.config/systemd/user/.</code></li>
    <li><code>mv -f epd2in13_V4.py ~/e-Paper/RaspberryPi_JetsonNano/python/lib/waveshare_epd/.</code></li>
    <li><code>mv -f epdconfig.py ~/e-Paper/RaspberryPi_JetsonNano/python/lib/waveshare_epd/.</code></li>
  </ul>
</li>
<li>Create the directory: <code>mkdir ~/Music</code></li>
<li>Move your music files into this Music directory. You can do this two ways:
  <ul>
    <li>Method 1: Insert a USB Flash stick into the USB hub, and cp the files over.
      <ul>
        <li><code>sudo mount /dev/sda1 /mnt/usb</code> (You'll need to sudo mkdir the /mnt/usb directory)</li>
        <li>After copying, <code>sudo umount /mnt/usb</code> then remove the USB stick.</li>
      </ul>
    </li>
    <li>Method 2 (this is easiest): Type: <code>ifconfig</code> and note the IP address. Use the application WinSCP, and use the SFTP protocol, to copy media files from a Windows computer to the PiPod.</li>
  </ul>
</li>
<li>You should now be able to launch the PiPod software, with everything working.
  <ul>
    <li>cd into the directory: <code>cd ~/PiPod_ePaper/Software</code></li>
    <li>Type: <code>python3 main.py</code></li>
    <li>Note that when launching for the first time, it will scan the music files and create an index file. This may take a minute or two.</li>
  </ul>
</li>
<li>To have the PiPod automatically run the player automatically on power-on:
  <ul>
    <li>To activate the pipod.service file, at the prompt, type: <code>systemctl --user enable pipod.service</code></li>
    <li>Reboot. If there are problems, type: <code>systemctl --user status pipod.service</code> to see if the service launched.</li>
  </ul>
</li>
  <li>At this point, you probably want to disable wifi, bluetooth, and reduce the CPU speed to save power. To do this you can just use the config.txt file I use, which I provide in this repository:
    <ul>
      <li>Note that the next line will over-write your /boot/firmware/config.txt file. If you want to make a backup copy, do so now.</li>
      <li><code>cd ~/PiPod_ePaper</code></li>
      <li><code>sudo mv -f config.txt /boot/firmware/.</code></li>
    </ul></li>
  <li>Or make those changes manually:
  <ul>
    <li><code>sudo nano /boot/firmware/config.txt</code></li>
    <li>After the line "dtparam=spi=on add these new lines:
    <ul>
      <li><code>dtoverlay=disable-wifi</code></li>
      <li><code>dtoverlay=disable-bt</code></li>
    </ul></li>
    <li>Under the line "Enable DRM VC4 V3D driver", comment out the 2 lines that follow.</li>
    <li>Comment out the line <code>display_auto_detect=1</code></li>
    <li>Under the line "Run as fast as firmware board allows"
      <ul>
        <li>comment out <code>arm_boost=1</code></li>
        <li>add the lines:
          <ul>
            <li><code>arm_freq=150</code></li>
            <li><code>core_freq=150</code></li>
            <li><code>over_voltage=-4</code></li>
          </ul></li></li>
      </ul>
  </li>
</ul>
<h3>Operating Procedure</h3>
<p>To charge the battery, slide the top power switch to the left. Connect a USB power supply to the USB jack at the bottom of the PiPod. Applying power will start charging the battery, and will also boot the PiPod.</p>
<p>To shutdown the PiPod, press the up arrow to get into the menu tree. Press the down arrow to "Shutdown". Press the middle button.</p>
<p>To operate from battery power, slide the top power switch to the right. Wait for it to boot.</p>
<p>While operating from battery power, you can plug (and unplug) the bottom USB jack into a power source to charge the battery.</p>
<p>To shutdown from battery power, find and press the "Shutdown" command as above. After 5 seconds (and with the bottom USB jack <b>NOT</b> connected to a power source), slide the top power switch to the left.</p>
