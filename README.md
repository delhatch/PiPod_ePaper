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
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/back2.jpg" width="400" /></td>
   <td><img src="https://github.com/delhatch/PiPod_ePaper/blob/main/Pictures/back3.jpg" width="400" /></td>
  </tr>
</table>
<h3>Motivation</h3>
<p>The goal is to see how much power can be conserved by switching from a 2.2" 320x240 LCD screen to a 2.13" 250x122 e-Paper screen (from Waveshare).</p>
<p>This version uses the same 1200 mAh battery and can play music continuously for 4.3 straight hours.</p>
<h3>Project Derivation</h3>
<p>This project is derived from github.com/delhatch/PiPod_Zero2W. I then applied (copied over) the python files from the /PiPod project, because I like that UI better. Then I modified those python files to create the set here. To create this version, clone the PiPod_Zero2W project, then replace the corresponding python files from those in this repository.</p>
<h3>Structural Changes</h3>
<p>I have changed the OS to the "lite" version: 2024-03-15-raspios-bookworm-arm64-lite.img.xz</p>
<p>This change reduces power consumption by ~20 mA, which is a 9% savings, so reasonably significant.</p>
<p>In addition to using an e-paper screen, I also added a headphone amplifier.</p>
<h3>Status</h3>
<p>As of 13 May 2024, I have created a new PCB that hosts the e-Paper screen, and everything works well. The screen software is doing partial-screen updates on the top-level screen, giving flicker-free updates.</p>
<h3>Power Savings</h3>
<p>With the LCD screen, with the backlight on, during playback, the current drawn is 266 mA.</p>
<p>With the LCD screen, with the backlight off, during playback, the current drawn is 220 mA.</p>
<p>With the e-Paper screen, during playback, the current drawn is 210 mA. (Needs to be updated with data from the new PCB.</p>
<p>So the e-Paper screen reduces the current drain from the battery by 10 mA. Over one battery "full-charge play until discharged" cycle this equates to 15 more minutes of playtime. And that assumes the LCD backlight is OFF the entire time (so you cannot ever view the display) which is un-realistic.</p>
<p>So the e-Paper screen is definitely a major improvement in battery life (playback time), and useability.</p>
<h3>Instructions</h3>
<li>I will post PCB files and instructions soon. It basically follows the instructions in PiPod_Zero2W, but with the lite OS, and the need to install the wavershare-epaper libraries.</li>
<h3>Fix the Waveshare Bug</h3>
<p>As part of the git clone of the waveshare-epaper repository, there will be a file in the /python/lib/waveshare-epaper directory called epd2in13_V4.py. This file must be replaced with the file in this repository. There is a single-line bug fix in the ReadBusy(self) method that is corrected in the file located in this repository.</p>
<h3>Wiring the e-Paper screen to the Pi Zero 2 W</h3>
<p>The e-Paper display I am using is sold by Waveshare: 250x122, 2.13inch E-Ink display HAT for Raspberry Pi. SKU: 12915</p>
<p>For any changes to the wiring scheme (moving signals to other GPIO pins, for example), the file "epdconfig.py" must be modified to match. Note: This repository file must be moved to replace the /python/lib/waveshare-epaper/epdconfig.py file. This is similar to replacing the waveshare epd2in13_V4 file, above.</p>
<table>
    <thead>
        <th>e-Paper Desc.</th>
        <th>e-Paper Pin</th>
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



