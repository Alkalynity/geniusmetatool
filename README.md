# Genius metatool, by alkalynity

## I. INTRODUCTION: WHAT DOES THIS TOOL DO?

The process of updating song metadata on Genius is tedious. Updating song metadata for *every song on an album* - when each song has almost exactly the same metadata items - is even more so, since for whatever reason Genius hasn't added a means of adding metadata album-wide. That's why I wrote this, because fuck it, why not ¯\\_(ツ)_/¯

This tool does not create additional song pages, it ONLY updates metadata for song pages on an *existing* album. The tool checks if the album exists before attempting to update the song pages.

*THIS IS CURRENTLY WINDOWS-ONLY.* I have no plans to officially support mac due to their draconian app notarization that rolled out with Catalina (10.15). However, in theory it should still work if you built it yourself and ran it, but I haven't tested it on \*nix so YMMV.

It's currently still *very* buggy. It doesn't handle errors from Genius very well, particularly when it (Genius) fails to update the song metadata (for reasons I still don't understand yet). The GUI in particular is a big CF, mostly because I suck at GUI development and (admittedly) don't care enough to improve it beyond being usable. That being said, if it's a big enough problem that it hinders people from being able to use it properly, I'll try to fix it the best I can. I wanted to get a release out so other people can test it and give me feedback.

I also have a no-GUI version that operates strictly from the command line (which I prefer, but I can understand why it's harder to use in general). If there's enough interest I can put out the GUI-less version for people to use as well.

## II. QUICK AND DIRTY SETUP
0. Install google chrome, if you don't have it installed already. Next, check your date/time format. If the year is only two digits (e.g. `20` instead of `2020`), go to `Control Panel -> Change date, time, or number formats` and change your short date format to a format with four digits. This is to work around a PyQt issue where only supplying two digits defaults to `19XX` instead of `20XX`.
1. Download chromedriver from here: https://chromedriver.chromium.org/downloads. MAKE SURE you download a version that supports the version of chrome you have. If you aren't sure what version of chrome you have, go here: https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have
2. Put chromedriver in the same directory as the metatool executable. Running the tool WILL FAIL if it can't find it.
3. Update the config_template.ini file with your username and password. RENAME THE FILE to "config.ini". I'll eventually change it so the name isn't hardcoded, but in the meantime it has to be called "config.ini".
4. Run the program, either by clicking on it or running through the command prompt. I suggest doing the latter, since it will give you info in case it crashes since I don't have it outputting to a log yet. In the event of it failing to open, it's most likely that it couldn't find the config file, or the config file is malformed.

The first time you run it, it's likely that Windows will give you a popup about allowing the program to run on your network, since it needs access to the internet in order to run. Just give it access to your private network and (maybe) restart the program.

**IMPORTANT:** There's a [known issue](https://github.com/Alkalynity/geniusmetatool/issues/1) where the tool will fail to click a certain element when it's running. The fix for this is to set `headless = False` in the config file and run the tool until it hits the error, go into the browser and click "accept" on the banner at the top of the page. The issue is that the banner blocks the tool from clicking on the metadata dialog. I'm working on fixing this in an upcoming release, but this is the easiest way to work around it in the meantime.

## III. USAGE

Either double-click on the executable or run it from the command line:
```sh
metatool1.0.exe
```

## IV. CONFIG FILE
**NOTE: the config file must be located in the SAME directory as the executable.**

[LOGIN]
* username: (str) your Genius username.
* password: (str) your Genius password.

[GENERAL]
* headless: (bool) Runs the browser in headless mode. Setting to False means the browser will open as a separate window and you can watch it update the metadata yourself. This can be useful for debugging or if you're bored and want to watch it zip around the website :^) True by default.
* debug: (bool) Runs the tool in debug mode. This will slow the tool down and print more debug info in the console. If you're hitting problems, set this to `True` and send me the log output, a screenshot of the browser (if `headless = False`) and a screenshot of the input you used in the GUI.

## V. PLANNED FEATURES/KNOWN ISSUES
* Linux support
* Add a track number column for "additional roles" to only add roles for specific tracks
* fix table formatting
* "delete additional artist" button
* Comptuters with the date format as `DD-MM-YY` will be interpreted as `19YY` instead of `20YY`. For now, changing the computer's localization settings to a four-digit year will fix the issue.
* the aforementioned issue with the banner blocking the metadata dialog.
* ...

## VI. CONTACT INFO
either message me on [Genius](https://genius.com/Alkalynity) or on slack, idk

If you hit a bug, set `debug = True` in the config file and send me the log output, a screenshot of the browser (if `headless = False`) and a screenshot of the input you used in the GUI. I'll try to get back to you as soon as I'm able.
