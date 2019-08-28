###############################################################################################
# Author:	Anastasios Monachos (secuid0) - [anastasiosm(at)gmail(dot)com]
# Usage: 	python screenshots.py -f urls.txt -t 5
# Purpose: 	Simple script that goes through a given list of urls and takes screenshots of their content
# Dependencies: Chromium webdriver get it from https://sites.google.com/a/chromium.org/chromedriver/home
# and extract in the same folder as this script.
# Version: 	0.1
################################################################################################
import os
import datetime
import concurrent.futures
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

SCREENSHOTS_PATH = './screenshots/'
CHROMEDRIVER_PATH = os.getcwd()+'/chromedriver'
NUMBER_OF_THREADS = 3;

def open_file(file):
    openedfile = open(file, "r")
    counter = 1
    print("Started: ", str(datetime.datetime.now().time()), " with ", str(NUMBER_OF_THREADS), " threads.")

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_THREADS) as executor:
        to_do = []
        for aline in openedfile:
            future = executor.submit(take_screenshot, aline, counter)
            to_do.append(future)
            counter += 1

    openedfile.close()
    print("Ended: ", str(datetime.datetime.now().time()))



def take_screenshot(url,counter):
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--test-type')
    options.add_argument('--headless')

    driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
    driver.get("http://"+url)
    driver.set_window_size(1024, 1080)
    driver.save_screenshot(SCREENSHOTS_PATH+"url_"+str(counter)+".png")
    print ("At ", str(datetime.datetime.now().time()), " the screenshot of ",url, " was taken ")
    driver.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='[i] Feed it with a file (full of urls, one at each line) and the number of threads (default is 3')
    parser.add_argument('-f',
                        metavar='file',
                        help='Filename with URLs to take screenshots',
                        required=True)
    parser.add_argument('-t',
                        metavar='threads',
                        help='Number of threads/workers, default is 3',
                        type=int,
                        default=3,
                        required=False)
    try:
        results = parser.parse_args()
        file_to_open = results.f
        NUMBER_OF_THREADS = results.t

    except IOError, msg:
        parser.error(str(msg))

    if not os.path.exists(SCREENSHOTS_PATH):
        os.mkdir(SCREENSHOTS_PATH)
        print("Directory ", SCREENSHOTS_PATH, " OK (created) ")
    else:
        print("Directory ", SCREENSHOTS_PATH, " OK (already exists)")

    open_file(file_to_open)
