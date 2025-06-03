# RMH
Rust in-game Map hider for OBS

Step 1: Download & Install Python 3.12
Download: https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe
Run the installer
IMPORTANT: Check "Add Python to PATH" during installation
Copy the installation path (usually C:\Users[YourName]\AppData\Local\Programs\Python\Python312)
You'll need this path for Step 5

Step 2: Update OBS Python Path
In the Scripts window, click Python Settings
Change the Install Path to your Python 3.12 folder (the path you copied in Step 1)
Click OK

Step 3: Install New Script
Restart OBS completely
Go to Tools → Scripts
Click + and add the new MapHider_v3 script
Setup the scene you would like hidden, the source for the image you wish to use, and set the delay  (recommended 0.35 sec)

Step 4: Configure Hotkeys
Close Scripts window
Go to File → Settings → Hotkeys
Find "RustMap Push To Hide"
Set it to G and Shift+G (or whatever your in-game map key is)
Click Apply → OK

Step 5: Test It Out!
Go to Rust scene and test your map key
The overlay should hide when you hold the key, then reappear after release
