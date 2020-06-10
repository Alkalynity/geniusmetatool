# Genius metatool, by alkalynity

## I. INTRODUCTION: WHAT DOES THIS TOOL DO?

The process of updating song metadata on Genius is tedious. Updating song metadata for *every song on an album* - when each song has almost exactly the same metadata items - is even more so, since for whatever reason Genius hasn't added a means of adding metadata album-wide. That's why I wrote this, because fuck it, why not ¯\\_(ツ)_/¯

This tool does not create additional song pages, it ONLY updates metadata for song pages on an *existing* album. The tool checks if the album exists before attempting to update the song pages.

## II. QUICK AND DIRTY SETUP
0. Install google chrome, if you don't have it installed already.
1. Download chromedriver from here: https://chromedriver.chromium.org/downloads. MAKE SURE you download a version that supports the version of chrome you have. If you aren't sure what version of chrome you have, go here: https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have
2. Put chromedriver in the same directory as the executable. Running the tool WILL FAIL if it can't find it.
3. Update the config_template.ini file with your username and password. RENAME THE FILE to "config.ini". I'll eventually change it so the name isn't hardcoded, but in the meantime it has to be called "config.ini".
4. Run the program, either by clicking on it or running through the command prompt. I suggest doing the latter, since it will give you info in case it crashes since I don't have it outputting to a log yet. In the event of it failing to open, it's most likely that it couldn't find the config file, or the config file is malfomed.

The first time you run it, it's likely that Windows will give you a popup about allowing the program to run on your network, since it needs access to the internet in order to run. Just give it access to your private network and (maybe) restart the program.

## III. USAGE

Either double-click on the executable or run it from the command line:
```sh
metatoolv1.0.exe
```

## IV. PLANNED FEATURES
will fill out later

## V. CONTACT INFO
either message me on [Genius](https://genius.com/Alkalynity) or on slack, idk
