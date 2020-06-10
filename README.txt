/// QUICK AND DIRTY SETUP ///
0.) Install google chrome, if you don't have it installed already.
1.) Download chromedriver from here: https://chromedriver.chromium.org/downloads.
    MAKE SURE you download a version that supports the version of chrome you have. If you aren't sure what version of chrome you have,
    go here: https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have
2.) Put chromedriver in the same directory as the executable. Running the tool WILL FAIL if it can't find it.
3.) Update the config_template.ini file with your username and password. RENAME THE FILE to "config.ini". I'll eventually change it so the name isn't hardcoded,
    but in the meantime it has to be called "config.ini".
4.) Run the program, either by clicking on it or running through the command prompt. I suggest doing the latter, since it will give you info in case it crashes since
    I don't have it outputting to a log yet. In the event of it failing to open, it's most likely that it couldn't find the config file, or the config file is malfomed.

The first time you run it, it's likely that Windows will give you a popup about allowing the program to run on your network, since it needs access to the internet
in order to run. Just give it access to your private network and (maybe) restart the program.