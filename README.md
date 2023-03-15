# PulseStream
 A streaming addon for Pulsus. This addon comes with two parts:
 
 **The Javascript Side**: A browser extension that injects a small .js file into the webpage, which starts a websocket to send data to the other half.
 **The Python Side**: A tkinter window that displays the data retrieved from the websocket, with theming capabilities included.
 
# How to run
 1. If you are using a browser, download the .zip file titled `PulseStream_Extension.zip` from the releases. On Chrome you have to extract the .zip, then 
 click the three dots in the top right, click `Settings`, go to `Extensions,` and click `Load unpacked`. On Firefox, you go to `about:addons`, click the 
 gear, then `Install addon from file` (don't unzip it!). On the electron app, idk :( but if you want to try to get it working you probably have to mess around with the `.asar` file.
 2. Now download the `PulseStream_Python.zip` file, and extract it. Open that folder, and open a terminal of your choice in that folder (for those on Windows,
 just type `cmd` in the directory path). Then type `python3 main.py`, and it should open. I'm working on making it an executable. For some reason the pyinstaller package that I want to
 use to do that isn't installing or something :(