import os
from enum import Enum
import logging, sys

import requests
from bs4 import BeautifulSoup


class AppPlatform(Enum):
    ANDROID = 1
    IOS = 2
    UNKNOWN = 3


class ScoopData:
    def __init__(self, soup: BeautifulSoup):
        self.app_title = getAppTitle(soup)
        self.app_platform = getPlatform(soup)
        self.app_logo_path = downloadAppLogo(soup, output_path=f"{self.app_title}/{self.app_platform.name}")
        self.download_url = getUrlFromButtonWithId("download", soup)
        self.install_url = getUrlFromButtonWithId("install", soup)
    
    def __str__(self):
        return f"{self.app_title} - {self.app_platform}"

    

def parseHtml(url: str):
    """Parses the HTML of a scoop link to produce a [ScoopData] class, containing all necessary info.

    Args:
        url (str): url from scoop to parse

    Returns:
        ScoopData: All the parsed data from the html
    """    
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        return ScoopData(soup)
    except:
        logging.debug("Could not parse soup from html.")
        raise
    


def downloadAppLogo(soup: BeautifulSoup, output_path: str = "img/app_icon.png"):
    """Downloads the app icon to the img folder

    Args:
        soup (BeautifulSoup): The parsed html from the scoop link
        output_filename (str): The output filename of the image
    Returns:
        str: Path with file
    """
    # Make dirs for the app logo
    try:
        full_output_path = f"img/{output_path}"
        path_with_file = f"{full_output_path}/app_icon.png"
        path_exist = os.path.exists(full_output_path)
        if not path_exist:
            os.makedirs(full_output_path)
    except:
        path_with_file = f"img/app_icon.png"

    # Download image from scoop and save to dir
    try:
        appIcon = soup.find("img", {"class": "app-icon"})
        appIconUrl = appIcon['src']
        with open(path_with_file, "wb") as f:
            f.write(requests.get(appIconUrl).content)
            print(f"Saved app_icon to {full_output_path}/app_icon.png")
    except:
        logging.debug("Could not save app icon to file, maybe it's non-existant?")
        logging.debug("Using default app_icon.png")
        path_with_file = f"img/default_app_icon.png"
    
    return path_with_file


def getUrlFromButtonWithId(text: str, soup: BeautifulSoup):
    """This method allows to get the URL of the button given a id

    Args:
        text (str): _description_
        soup (BeautifulSoup): _description_
    Returns:
        Url of the button requested
    """    
    button_div = soup.select_one(f'div[id*="{text}-button"]')
    button_url = button_div.find("a").get("href")

    if (button_url is None):
        logging.debug(f"Could not find the button url with id: {text}-button. Returning ''")
        return ""
    else:
        return button_url


def getAppTitle(soup: BeautifulSoup) -> str:
    """Parses App Title from the soup

    Args:
        soup (BeautifulSoup): parsed HTML in form of Soup

    Returns:
        str: App title
    """    
    title_div = soup.select_one(selector=f'div[class*="app-title"]')

    if (title_div is None):
        logging.debug(f"Could not find the title div with class: app-title. Returning ''")
        return ""
    else:
        return title_div.get_text().strip()


def getPlatform(soup: BeautifulSoup) -> AppPlatform:
    app_platform_div = soup.select_one(selector=f'div[class*="app-platform"]')
    apple_icon = soup.select_one(selector=f'i[class*="fa-apple"]')
    android_icon = soup.select_one(selector=f'i[class*="fa-android"]')

    if apple_icon is not None:
        return AppPlatform.IOS
    elif android_icon is not None:
        return AppPlatform.ANDROID
    else:
        return AppPlatform.UNKNOWN


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    # Demo URL
    parseHtml(url="https://scoop.pinch.nl/?page=app-detail&hash=e09e1ddb325632953fbc107d3de7741d&version=114")
