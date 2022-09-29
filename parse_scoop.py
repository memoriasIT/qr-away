import requests
from bs4 import BeautifulSoup

def parseHtml():
    r = requests.get(
        'https://scoop.pinch.nl/?page=app-detail&hash=e09e1ddb325632953fbc107d3de7741d&version=114')
    soup = BeautifulSoup(r.text, "html.parser")

    downloadAppLogo(soup)
    downloadUrl = getUrlFromButtonWithId("download", soup)
    installUrl = getUrlFromButtonWithId("install", soup)


def downloadAppLogo(soup: BeautifulSoup, output_filename: str="appLogo.png"):
    """Downloads the app icon to the img folder

    Args:
        soup (BeautifulSoup): The parsed html from the scoop link
        output_filename (str): The output filename of the image
    """    
    appIcon = soup.find("img", {"class": "app-icon"})
    appIconUrl = appIcon['src']

    with open(f"img/{output_filename}", "wb") as f:
        f.write(requests.get(appIconUrl).content)


def getUrlFromButtonWithId(text: str, soup: BeautifulSoup):
    for EachPart in soup.select(f'div[id*="{text}-button"]'):
        print(EachPart.get_text().strip())
        print(EachPart.find("a").get("href"))


if __name__ == '__main__':
    parseHtml()


# <div class="navbar-header"><a class="navbar-brand" href="#"></a><div class="navbar-pinch-logo"></div> </div>
# </nav>
# </div>
# <ol class="breadcrumb"><li class="active"></li></ol><div class="app-details-container">
# <section class="app-main-info-section">
# <div class="app-icon-container"><img alt="" class="app-icon" src="https://scoop.pinch.nl/?page=icon&amp;hash=e09e1ddb325632953fbc107d3de7741d&amp;version=114"/></div>
# <div class="app-main-info">
# <div class="app-title">Qmusic</div>
# <div class="app-platform">
# <span><i aria-hidden="true" class="fa fa-apple platform-icon"></i>
#                     iOS 8.0 or later</span>
# </div>
# </div>
# </section>
# <section class="download-row-section">
# <div class="download-button" id="download-button">
# <a class="btn btn-primary" href="https://scoop.pinch.nl/?page=download&amp;hash=e09e1ddb325632953fbc107d3de7741d&amp;version=114" role="button">Download</a>
# </div>
# <div class="download-button" id="install-button">
# <a class="btn btn-primary" href="itms-services://?action=download-manifest&amp;url=https%3A%2F%2Fscoop.pinch.nl%2F%3Fpage%3Ddownload-plist%26hash%3De09e1ddb325632953fbc107d3de7741d%26version%3D114" role="button">Install</a>
# </div>
