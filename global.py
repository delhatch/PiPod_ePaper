import subprocess
p=subprocess.run(["python","/home/drh/PiPod_Zero2W/Sofware/main.py"])
if p.returncode == 1:
  print("FAILED. Re-launching...")
  p=subprocess.run(["python","/home/drh/PiPod_Zero2W/Sofware/main.py"])
