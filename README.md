## Thanks!

Fisrt, I want to thank Viwyn because I was inspired and I used her repo to create that app.

[Here is her Github page.](https://github.com/Viwyn)

[Here is her Repo page what I used.](https://github.com/Viwyn/Sky-Music-Player)

Thank you so much, Viwyn.


# Sky: COTL Automatic Music Player App for PC

Automatically play music in the game Sky: Children of the Light (*referred to as Sky*) from pre-written music sheets and mimicing key strokes. 


## About

This python app takes the JSON file or skysheet file found in the [Sky Music Nightly](https://specy.github.io/skyMusic/) website and playes the song in game. You can select folder what contains your sheet file.
The script will give you a 3 second window after you have selected a song to tab back into the game before it tabs back for you, it will pause the song if you tab out of Sky so it does not take over your keyboard. The app will automatically end after a song has finished playing.

[Here is the wiki guide to Sky's music](https://sky-children-of-the-light.fandom.com/wiki/Sky_Music_Guide)


## Setup and Installation

1. Download Python from their official [website](https://www.python.org)

2. Clone this repo
    (Click on the green button near the top that says "**<> Code**", then click "**Download ZIP**", then extract the zip anywhere you want)

3. I recommend you use virtual environment (Uhhh I like using venv than global).

4. Install required dependencies `pip install -r requirements.txt`
    (Right click inside the music player folder, then click "Open in Terminal". Then, copy the above code and paste it into the terminal.)


## Usage (Script)

1. Run Sky

2. Run app.py
    (Right click inside the music player folder, then click "Open in Terminal". Then, paste in `py app.py` to run the script.)

3. App's window will appear, you should click to "Detect Sky Window" to push Sky window to top.

4. Click to "Click to choose folder" box, File Explorer appear. You can select a folder which contains your music sheet. Then click to "Select" button.

5. A box below will show you all files in folder. Click to sheet file you want, and choose codec (UTF-8 or UTF-16)

6. Pull out an instrument in Sky

7. Click "Play" button to start. You have 3 second to focus Sky window.

8. If you want to stop current song, you can click "Cancel" button and choose other sheet.


## Usage (App)

1. Run Sky

2. Run SkyAutoMusic.exe

3. App's window will appear, you should click to "Detect Sky Window" to push Sky window to top.

4. Click to "Click to choose folder" box, File Explorer appear. You can select a folder which contains your music sheet. Then click to "Select" button.

5. A box below will show you all files in folder. Click to sheet file you want, and choose codec (UTF-8 or UTF-16)

6. Pull out an instrument in Sky

7. Click "Play" button to start. You have 3 second to focus Sky window.

8. If you want to stop current song, you can click "Cancel" button and choose other sheet.


## Building

1. Open terminal, choose directory to project folder (which contains app.py)

2. Install pyInstaller and pillow with these command (if you don't need icon, you don't need to install pillow)\
    `pip install pillow`\
    `pip install pyinstaller`

3. If you want to use your icon, download image and copy to folder which contains app.py, change extension to .ico.

4. Run this command (if you don't want to use icon, delete `--icon=<your icon file name>`)\
    `pyinstaller --noconsole --onefile --icon=<your icon file name> app.py`

5. File .exe in dist folder, go to it and enjoy your app.


## Downloading Songs

1. Head over to the [Sky Nightly](https://specy.github.io/skyMusic/) website and go to the song library page

2. Search for a song of your choice and download it

Last, I want to thank Viwyn again.