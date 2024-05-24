# PiPod_ePaper
This project takes the github.com/delhatch/PiPod project (which was derived from github.com/BramRausch/PiPod) and replaces the LCD screen with an e-Paper screen.
<table border="1">
  <tr>
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/front_quarter_playing.jpg" width="500" /></td>
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/front_led.jpg" width="500" /></td>
  </tr>
  <tr>
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/front_playing.jpg" width="400" /></td>
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/back1.jpg" width="400" /></td>
  </tr>
  <tr>
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/back_bare.jpg" width="400" /></td>
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/back3.jpg" width="400" /></td>
  </tr>
</table>
<h3>Motivation</h3>
<p>The goal of this project was to extend the battery run-time by switching from a 2.2" 320x240 LCD screen to a 2.13" 250x122 e-Paper screen (from Waveshare).</p>
<p>Using the project's standard 1200 mAh battery, the continuous play time is now <b>4 hours, 48 minutes</b>.</p>
<p>In addition to using an e-paper screen, I also added a headphone amplifier based on the TP6113 IC. Note: This amplifier is rated at 40 mW, which does not sound like a lot of power, but even with inefficient headphones this equates to 108 dBSPL (equivalent to a gas lawn mower at 1m), which is far too loud for sustained listening. Watch your volume setting!</p>
<h3>Project Derivation</h3>
<p>This project is derived from github.com/delhatch/PiPod_Zero2W. This repository has changes to use the e-Paper screen, along with other minor bug fixes.</p>
<h3>Structural Changes</h3>
<p>I have changed the OS to the "lite" version: 2024-03-15-raspios-bookworm-arm64-lite.img.xz This change reduces power consumption by ~20 mA, which is a 9% savings, so reasonably significant.</p>
<p>Also moved from Pygame to Pillow for the screen graphics.</p>
<p>Then I got rid of Pygame completely, since I was only using it for the key stroke buffer, and the Python keypad library was already taking care of that. Eliminating Pygame reduced power consumption by 9.2% when idle, and by 5.2% when playing music.</p>
<h3>Status</h3>
<p>As of 24 May 2024, I have created a new PCB that hosts the e-Paper screen, and everything works well (see Known Bugs). The case parts are now being fabricated -- there will probably be fixes needed and I will update the case files in the future.</p>
<h3>Power Savings</h3>
<p>With the LCD screen, with the backlight on, during playback, the current draw is <b>266 mA</b>.</p>
<p>With the LCD screen, with the backlight off, during playback, the current draw is <b>220 mA</b>.</p>
<p>With the e-Paper screen, during playback, the current draw is <b>175 mA</b>.</p>
<p>Having eliminated Pygame, the current draw is down to only <b>166 mA</b>.</p>
<p>So the e-Paper screen is definitely a major improvement in battery life (playback time), and also useability because there is no anxiety about leaving an LCD backlight on.</p>
<h3>Known Bugs</h3>
<p>The locations of C28 and C29 interfere with the push-buttons. Fix: Solder one end of the caps directly to the headphone jack terminal, and use a short jumper wire (28-30 gauge wire) on the other end of the capacitor to connect it to the (now unused) pad of C29.</p>
<h3>Instructions</h3>
<p>The bare PC board can be ordered via this link at <a href="https://www.pcbway.com/project/shareproject/ePaper_PiPod_MP3_music_player_a6adf3e1.html">PCBWay</a>. The BoM is part of this repository, under "Hardware." The case parts can also be ordered via that same link. I specified printing in Nylon: PA-12 with 35% glass fill.</p>
<ul>
  <li>Download the OS file "2024-03-15-raspios-bookworm-arm64-lite.img.xz" or newer.</li>
  <li>Using rufus-3.22.exe (or similar), burn the image to a 128GB micro-SD card.</li>
  <li>Assuming you have a fully-assembled PiPod hardware: Connect an HDMI monitor to the Pi Zero 2 W. Also connect a USB expander hub such as the SmartQ H302S to the Pi Zero usb connector. Connect a USB keyboard and mouse to the hub.</li>
  <li>Apply power (from a plug-in USB power supply) to the USB connector at the bottom of the PiPod.</li>
  <li>Power-up and go through the configuration screens. Create the user "pi" with a password of your choosing. Reboot and log in.</li>
  <li>At the prompt: sudo raspi-config
    <ul>
      <li>Go into Menu Item #1. Enter the SSID and passphrase for your wi-fi.</li>
      <li>Select menu item #1, then select S5 (Boot/Auto-login) select and enable "Console Autologin", then select "Back"</li>
      <li>From top menu, select #3 "Interface Options" the select and enable I1 "Enable SSH".</li>
      <li>Then select and enable I4 "Enable I2C".</li>
      <li>Select "Back" to top screen, then "Finish" and then reboot.</li>
    </ul></li>
  <li>Type sudo nano /boot/firmware/config.txt and make the following changes:
    <ul>
      <li>If necessary, un-comment dtparam=spi=on (to turn on the SPI port)</li>
      <li>comment-out the "dtparam=audio=on" line</li>
      <li>If necessary, un-comment out the line dtparam=12c_arm=on</li>
      <li>At the end of the file, add a line: dtoverlay=hifiberry-dac</li>
  </ul>
</li>
  <li>sudo reboot</li>
  <li>Enter the following lines to install the required packages:
  <ul>
    <li>sudo apt install python3</li>
    <li>sudo apt install build-essential python3-dev python3-smbus -y</li>
    <li>sudo apt install git -y</li>
    <li>sudo apt install python3-vlc -y</li>
    <li>sudo apt install python3-alsaaudio -y</li>
    <li>sudo apt install pulseaudio -y</li>
    <li>sudo apt install python3-taglib -y</li>
    <li>sudo apt install python3-spidev -y</li>
    <li>sudo apt install python3-gpiozero -y</li>
    <li>sudo apt install python3-pip -y</li>
    <li>sudo apt install python3-pil -y</li>
    <li>sudo apt install python3-numpy -y</li>
  </ul>
</li>
<li>sudo reboot</li>
<li>Verify that the audio is working. Plug headphones into the PiPod and type:
  <ul>
    <li>sudo raspi-config</li>
    <li>Select line #1, then #2 "Audio"
    <li>Select snd_rpi_hifiberry_dac then Finish</li>
    <li>type: amixer set Master 50%</li>
    <li>type: speaker-test -c2</li>
    <li>Verify that audio is coming from the headphones and not the HDMI monitor.</li>
  </ul>
</li>
<li>Install the Adafruit_GPIO library:
  <ul>
    <li>from the home directory (~/) type: git clone https://github&#46;com/adafruit/Adafruit_Python_GPIO.git</li>
    <li>cd Adafruit_Python_GPIO</li>
    <li>sudo python3 setup.py install</li>
  </ul>
<li>Install the Adafruit Blinka library:
  <ul>
    <li>cd ~/ </li>
    <li>sudo pip3 install --break-system-packages Adafruit-Blinka</li>
  </ul>
</li>
<li>Install the waveshare e-Paper libraries:
  <ul>
    <li>cd ~/</li>
    <li>git clone https://github&#46;com/waveshare/e-Paper.git</li>
    <li>sudo pip install --break-system-packages waveshare-epaper epd-library</li>
  </ul></li>
<li>sudo reboot</li>
<li>Now fetch the e-Paper MP3 player software from this repository:
  <ul>
    <li>Clone this repository: cd ~/ then type: git clone https://github&#46;com/delhatch/PiPod_ePaper.git</li>
    <li>cd PiPod_ePaper</li>
    <li>mv launch.sh ~/.</li>
    <li>cd ~/</li>
    <li>chmod 777 launch.sh</li>
    <li>mkdir .config</li>
    <li>mkdir .config/systemd</li>
    <li>mkdir .config/systemd/user</li>
    <li>cd PiPod_ePaper</li>
    <li>mv pipod.service ~/.config/systemd/user/.</li>
    <li>mv -f epd2in13_V4.py ~/e-Paper/RaspberryPi_JetsonNano/python/lib/waveshare_epd/.</li>
    <li>mv -f epdconfig.py ~/e-Paper/RaspberryPi_JetsonNano/python/lib/waveshare_epd/.</li>
  </ul>
</li>
<li>Create the directory ~/Music</li>
<li>Move your music files into this Music directory. You can do this two ways:
  <ul>
    <li>Method 1: Insert a USB Flash stick into the USB hub, and cp the files over.
      <ul>
        <li>sudo mount /dev/sda1 /mnt/usb (You'll need to sudo mkdir the /mnt/usb directory)</li>
        <li>After copying, sudo umount /mnt/usb then remove the USB stick.</li>
      </ul>
    </li>
    <li>Method 2 (this is easiest): Type "ifconfig" (no quotes) and note the IP address. Use the application WinSCP, and use the SFTP protocol, to copy media files from a Windows computer to the PiPod.</li>
  </ul>
</li>
<li>You should now be able to launch the PiPod software, with everything working.
  <ul>
    <li>cd into the directory ~/PiPod_ePaper/Software</li>
    <li>Type: python3 main.py</li>
    <li>Note that when launching for the first time, it will scan the music files and create an index file. This may take a minute or two.</li>
  </ul>
</li>
<li>To have the PiPod automatically run the player automatically on power-on:
  <ul>
    <li>To activate the pipod.service file, at the prompt, type: systemctl --user enable pipod.service </li>
    <li>Reboot. If there are problems, type: systemctl --user status pipod.service to see if the service launched.</li>
  </ul>
</li>
  <li>At this point, you probably want to disable wifi, bluetooth, and reduce the CPU speed to save power.</li>
  <li>To do this you can just use the config.txt file I use, which provided in this repository:
    <ul>
      <li>cd ~/PiPod_ePaper</li>
      <li>Note that the next line will over-write your config.txt file. If you want to make a backup copy, do so now.</li>
      <li>sudo mv -f config.txt /boot/firmware/.</li>
    </ul></li>
</ul>
<h3>Wiring the e-Paper screen to the Pi Zero 2 W</h3>
<p>The e-Paper display I am using is sold by Waveshare: 250x122, 2.13inch E-Ink display. SKU: 12672</p>
<p>Waveshare's epdconfig.py file defines how the Raspi Pi I/O pins are connected to the e-paper screen. I made to the wiring scheme (moving signals to other GPIO pins, for example), so the file "epdconfig.py" was modified to match. Therefore, this github repository file must be moved to replace the /python/lib/waveshare-epaper/epdconfig.py file. Doing this is part of the instructions above.</p>
<p>The table below shows how the Raspi Pi was connected to the waveshare e-paper screen module. This is not important because the PCB incorporates all necessary circuitry and connections. See the schematics in the /Hardware folder.</p>
<p>I am keeping this table in the Readme.md for reference purposes, in case it is useful.</p>
<table>
    <thead>
        <th>e-Paper Desc.</th>
        <th>e-Paper Module Pin</th>
        <th>Pi BCM NAME</th>
        <th>Pi Connector Pin #</th>
    </thead>
    <tbody>
        <tr>
            <td>VCC</td>
            <td>1</td>
            <td>3.3V</td>
            <td>1</td>
        </tr>
        <tr>
            <td>GND</td>
            <td>2</td>
            <td>GND</td>
            <td>6</td>
        </tr>
        <tr>
            <td>DIN / MOSI</td>
            <td>3</td>
            <td>MOSI / GPIO10</td>
            <td>19</td>
        </tr>
        <tr>
            <td>SPI CLK</td>
            <td>4</td>
            <td>SCLK / GPIO11</td>
            <td>23</td>
        </tr>
        <tr>
            <td>CS</td>
            <td>5</td>
            <td>GPIO4</td>
            <td>7</td>
        </tr>
        <tr>
            <td>DC</td>
            <td>6</td>
            <td>GPIO15</td>
            <td>10</td>
        </tr>
        <tr>
            <td>RST</td>
            <td>7</td>
            <td>GPIO16</td>
            <td>36</td>
        </tr>
        <tr>
            <td>BUSY</td>
            <td>8</td>
            <td>GPIO14</td>
            <td>8</td>
        </tr>
    </tbody>
</table>



