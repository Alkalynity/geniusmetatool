# -*- coding: UTF-8 -*-
import requests
import sys
import os.path
import configparser
import string
import time
from lxml import html
from selenium import webdriver
from selenium.webdriver.support.ui import Select

config = configparser.ConfigParser()
config.read('config.ini')


# read username and password from config
# DO NOT include config.ini in git repo unless you wanna your account stolen
my_username = config.get('LOGIN', 'username').strip('"')
my_password = config.get('LOGIN', 'password').strip('"')

disable_headless = config.get('GENERAL', 'headless') == 'False'
# debug will slow things down and give us better log info
debug = config.get('GENERAL', 'debug') == 'True'

if 'win' in sys.platform:
    pathname = os.path.join(os.getcwd() + '\\')
else:
    pathname = os.path.join(os.getcwd() + '/')


# this is mostly for testing purposes, ideally we'll read in the metadata from a json file or something
def cli_get_input():
    url_verified = False
    album_url = ''
    # get the album URL and verify that it's on Genius before we go further
    while not url_verified:
        album_url = input("Enter Genius album URL: ").strip()
        if genius_album_exists(album_url):
            url_verified = True
        else:
            print("Error: album does not exist. Please check the URL and that the album page exists on Genius.")

    done = False
    # field : value
    meta_dict = {}

    # get the metadata
    while not done:
        user_input = input("Enter metadata to update for album (type 'usage' for help): ").strip()
        if user_input == "usage":
            print_usage()
        else:
            meta_dict = process_cli_input(user_input, album_url)
            if meta_dict:
                done = True

    return album_url, meta_dict


def process_cli_input(user_input, album_url):
    meta_dict = {}
    ok = True
    tokenized = user_input.split()
    for token in tokenized:
        try:
            field, values = token.split('=')
        except ValueError:
            print_usage()
            return {}

        # just to save me some headaches later
        field = field.lower().replace('_', ' ')
        values = values.replace('_', ' ')

        # adjust for variations on common fields
        # this is to make finding the correct input box easier when we're updating the metadata
        if "producer" == field or "producers" == field:
            field = "produced by"
        if "primary" == field:
            field = "primary tag"
        if "writer" == field:
            field = "written by"
        if "date" == field:
            field = "release date"

        # check to make sure value isn't empty
        if not values:
            print('Error: value for "' + field + '" cannot be empty.')
            return {}

        values = values.split(',')

        # TODO: I'm using capwords here because we search case-insensitively when updating the metadata...this is dumb
        meta_dict.update({string.capwords(field): values})

    print("Album URL: " + album_url + "\n"
                                            "Metadata: " + str(meta_dict))
    print("Is this OK? (y/n)")
    answer = input().lower()
    if 'y' not in answer:
        print("Clearing metadata.")
        meta_dict = {}

    return meta_dict


def print_usage():
    print("usage: \n"
                 "Date: date=<MM/DD/YYYY>\n"
                 "All other fields: <field>=<value1>,<value2>,...\n")
    print("FIELDS are CASE-INSENSITIVE; VALUES are CASE-SENSITIVE\n")
    print("Separate all FIELDS by SPACES and VALUES by COMMAS; if you need to use spaces in a field or value,"
                 " use '_'\n"
                 "EXAMPLE: produced_by=Abraham_Lincoln,George_Washington\n"
                 "This will enter 'Abraham Lincoln' and 'George Washington' as the producers "
                 "for every song on the album.\n"
                 "\n"
                 "NOTE: entering the following will automatically update the relevant fields on Genius,\n"
                 "OTHERWISE they will be entered under 'Additional Credits' (slashes indicate that either "
                 "can be used:\n"
                 "'Album', 'Date', 'Recorded at', 'Tags', 'Primary Tag/Primary', "
                 "'Written By/Writer', 'Produced by/Producer'\n")


# check if an album exists on genius already, returns true if it does
def genius_album_exists(url):
    request = requests.get(url.strip())
    if request.status_code == 200:
        return True
    return False


# given the URL of an album, get the song page URLs so we can update their metadata
# returns a list of links
def get_song_urls_from_album(album_url):
    debug_print("getting songs from album url: " + album_url)
    response = requests.get(album_url)
    tree = html.fromstring(response.content)
    links = tree.xpath('//*[@class="u-display_block"]/@href')
    return links


def startup():
    options = webdriver.ChromeOptions()
    if not disable_headless:
        options.add_argument("--headless")
    driverpath = 'chromedriver.exe'
    if 'win' not in sys.platform:
        driverpath = '/usr/lib/chromium-browser/chromedriver'
    driver = webdriver.Chrome(executable_path=driverpath, options=options)
    driver.maximize_window()
    driver.get("https://genius.com/signup_or_login")
    return driver


def login(driver):
    debug_print("logging in...")
    login_box = driver.find_element_by_xpath("//*[@class='last_button apply_hover_on_active ']")
    login_box.click()

    username = driver.find_element_by_id("user_session_login")
    username.send_keys(my_username)

    password = driver.find_element_by_id("user_session_password")
    password.send_keys(my_password)

    submit = driver.find_element_by_id("user_session_submit")
    submit.click()


# this opens the four metadata tabs in the editor
# I'm not sure if it's necessary to open them, but until I test it this is fine
def open_meta_tabs(driver):
    debug_print("opening meta tabs")
    if debug:
        time.sleep(1)
    title_and_artist_tab = driver.find_element_by_xpath("//div[contains(text(),'Title and Artists')]")
    title_and_artist_tab.click()

    if debug:
        time.sleep(1)
    avi_tab = driver.find_element_by_xpath("//div[contains(text(),'Audio, Video & Images')]")
    avi_tab.click()

    if debug:
        time.sleep(1)
    adlt_tab = driver.find_element_by_xpath("//div[contains(text(),'Albums, Date, Location & Tags')]")
    adlt_tab.click()

    if debug:
        time.sleep(1)
    song_relationship_tab = driver.find_element_by_xpath("//div[contains(text(),'Song Relationships')]")
    song_relationship_tab.click()
    debug_print("tabs opened.")


# if debug is True in config, print string
def debug_print(string):
    debug_string = "DEBUG: " + string
    if debug:
        print(debug_string)


# TODO: finish this
def check_if_tracklist_set(album_url, num_songs):
    response = requests.get(album_url)
    tree = html.fromstring(response.content)
    tracklist_number_elements = [e for e in tree.xpath(
        "//span[contains(@class, 'chart_row-number_container-number chart_row-number_container-number--gray')]/span") if e.text]
    if len(tracklist_number_elements) == num_songs:
        return True
    else:
        return False


def update_song_metadata(driver, link, meta_dict, song_num):
    debug_print("getting link: %s" % link)
    driver.get(link)
    if debug:
        time.sleep(5)

    # find the edit button and click it
    debug_print("Finding and clicking edit_button...")
    edit_button = driver.find_element_by_class_name("tiny_edit_button-svg")
    edit_button.click()

    # let it think for a second or two
    debug_print("edit_button clicked.")
    if debug:
        time.sleep(5)
    else:
        time.sleep(1)

    # now update the metadata
    # open all four metadata tabs, just to be safe
    open_meta_tabs(driver)

    # get all the input boxes
    input_boxes = driver.find_elements_by_xpath("//div[contains(@class, 'square_form-input_and_label')]")
    for field, value in meta_dict.items():
        # extract track info from field, if it exists
        field_track_list = field.split('|')
        track_nums = []
        # check if we have track info
        if len(field_track_list) > 1:
            debug_print("Track numbers detected. checking if current song is in track_nums...")
            field = field_track_list[0]
            track_nums = field_track_list[1].replace(' ', '').split(',')
            # convert list of strings to ints
            track_nums = [int(i) for i in track_nums]
            if song_num not in track_nums:
                debug_print("role %s is not set for track number %d. skipping" % (field, song_num))
                continue
            else:
                debug_print("song is in track_nums. will update")

        # otherwise, carry on
        else:
            field = field_track_list[0]
        if debug:
            time.sleep(1)
        # need to handle date separately
        if "release date" == field.lower():
            debug_print("adding release date")
            # date is currently a list
            update_date(driver, value)
            continue
        elif "primary tag" == field.lower():
            debug_print("adding primary tag")
            combo_box = Select(driver.find_element_by_xpath("//select[@ng-model='song.primary_tag']"))
            combo_box.select_by_visible_text(value)
            continue

        # TODO: find a way to case-insensitively match labels
        # try to find the corresponding input box
        # sigh
        box = driver.find_elements_by_xpath(
            "//div[contains(@class, 'square_form-input_and_label') and contains(@label,'" + field + "')]")
        # if we found it, cool
        if box:
            debug_print("adding 'generic'")
            # "box" is a list right now
            box = box[0]
            values_box = box.find_element_by_xpath('.//input')
            # don't try to click anything or find the suggestion if it's the recording location
            # the .join is because it's a list (sometimes a list of strings by accident...)
            if "recorded at" in field.lower():
                debug_print("adding recorded at")
                values_box.clear()
                values_box.send_keys(', '.join(value))
            else:
                for v in value:
                    find_and_click_suggestion(driver, values_box, v.strip())

        # otherwise, we stick it under "Additional Credits"
        else:
            add_additional_artist(driver, field, value)

    # click save
    save_button = driver.find_element_by_xpath("//button[@class='modal_window-save_button square_button square_button--purple u-small_vertical_margins']")
    save_button.click()

    # give it time to process
    time.sleep(5)

    song_title = driver.find_element_by_xpath("//h1[@class='header_with_cover_art-primary_info-title']").text
    print("%s successfully updated." % song_title)

    return song_title


# update the date, given the date as a list in the form of [month, day, year]
# TODO: should be a tuple
def update_date(driver, date_as_list):
    month = date_as_list[0]
    day = date_as_list[1]
    year = date_as_list[2]

    select_year = Select(driver.find_element_by_xpath("//select[contains(@ng-model, 'ngModel.year')]"))
    select_year.select_by_visible_text(str(year))

    # select by index since we don't have the name of the month, just the number
    select_month = Select(driver.find_element_by_xpath("//select[contains(@ng-model, 'ngModel.month')]"))
    select_month.select_by_index(int(month))

    # strip any leading 0's, which would cause the select to fail
    select_day = Select(driver.find_element_by_xpath("//select[contains(@ng-model, 'ngModel.day')]"))
    select_day.select_by_visible_text(str(day).lstrip('0'))


def add_additional_artist(driver, field, values):
    # TODO: this is shit. don't match by text...I'm just doing it for PoC
    add_additional_button = driver.find_element_by_xpath("//span[contains(text(), '+ Add Additional Credits')]")
    # add new box
    add_additional_button.click()
    # get list of additional role boxes (need to do this every time so it's refreshed)
    # ...ugly
    addit_role_boxes = driver.find_elements_by_xpath(
        '//div[contains(@class, "square_form-sub_section") and contains(@ng-repeat, "customPerformanceRole in customPerformanceRoles")]')
    # the last one in this list is always the new one we made
    new_box_elem = addit_role_boxes[-1]
    # get the input boxes
    # if we put in a duplicate field, genius will filter it out automatically
    field_box, values_box = new_box_elem.find_elements_by_xpath('.//input')[0], \
                            new_box_elem.find_elements_by_xpath('.//input')[1]
    # input field
    field_box.send_keys(field)
    # input values
    for v in values:
        find_and_click_suggestion(driver, values_box, v)


def find_and_click_suggestion(driver, values_box, v):
    debug_print("trying to find and click suggestion...")
    found = False
    # TODO: this doesn't clear boxes that can have multiple artists...it will just append instead of overwriting
    values_box.clear()
    # add zero-width space just in case
    values_box.send_keys('\u200b' + v)
    # give the website a chance to load the suggestions first
    time.sleep(2)
    # check if one of the autocomplete suggestions match
    suggestions_list = driver.find_elements_by_class_name("suggestion-item")
    for s in suggestions_list:
        suggestion = s.find_element_by_xpath(".//ng-include")
        s_text = suggestion.text.lower()
        # if we found it, click
        # the second half of the conditional is if we hit the "create new" suggestion, which means we couldn't find
        # an existing artist and have to create a new one.
        if v.lower() == s_text or 'create new' in s_text:
            suggestion.click()
            found = True
            debug_print("found suggestion and successfully clicked!")
            break

    # TODO: idk, do something?
    if not found:
        debug_print("Value %s not found." % v)


def main():
    # get dictionary of metadata to update from either user or (eventually) json
    album_url, meta_dict = cli_get_input()

    # get the driver going and login
    driver = startup()
    login(driver)
    song_links = get_song_urls_from_album(album_url)
    for link in song_links:
        update_song_metadata(driver, link, meta_dict)
    get_song_urls_from_album(album_url)

    return 0


if __name__ == '__main__':
    main()
