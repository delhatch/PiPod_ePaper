import subprocess
import os

p=subprocess.run(["python","/home/pi/PiPod_ePaper/Software/main.py"])
#if p.returncode == 1:
  #print("FAILED. Re-launching...")
  #p=subprocess.run(["python","/home/pi/PiPod_ePaper/Software/main.py"])
#os.system("sudo shutdown now")
