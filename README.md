# PiPod_ePaper
This project takes the github.com/delhatch/PiPod project and replaces the LCD screen with an e-Paper screen.
<h3>Motivation</h3>
<p>The goal is to see how much power can be conserved by switching from a 2.2" 320x240 LCD screen to a 2.13" 255x122 e-Paper screen.</p>
<p>The LCD-based PiPod player, even with various power savings such as wi-fi off, bluetooth off, and lowering the CPU clock speed to 200 MHz, still has a power draw during playback (with the LCD backlight off) averaging 220 mA. So a 1200 mAh battery would run for 5.45 hours, at most.</p>
<h3>Project Derivation</h3>
<p>This project is derived from github.com/delhatch/PiPod_Zero2W. I then applied (copied over) the python files from the /PiPod project, because I like that UI better. Then I modified those python files to create the set here. To create this version, clone the PiPod_Zero2W project, then replace the corresponding python files from those in this repository.</p>
<h3>Status</h3>
<p>As of 5 April 2024, the player runs with an e-Paper screen, but barely. The screen flickers a lot, and the keys are not very responsive. I will be working both of those issues tomorrow.</p>
