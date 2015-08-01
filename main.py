import requests
from bs4 import BeautifulSoup
from PIL import Image
from StringIO import StringIO

iconListRootDomain = 'http://wow.gamepedia.com/Wowpedia:WoW_Icons/Icon_List'
iconListRootTarget = '$(".mw-content-text ol li a[\'href\']")'
iconSaveDirectory = './icons'

# Side effect: produce list of urls to page that holds icon image
def extractUrlsToIconPage(locationRoot):
  # request get
  print('extracting urls to icon page where icon url will be found')
  r = requests.get(locationRoot)
  soup = BeautifulSoup(r.content, 'html.parser')
  print(soup.prettify())
  listOfIconPageWhereIconFileUrlWillBeFound = []
  return listOfIconPageWhereIconFileUrlWillBeFound

# Side effect: produce a list of urls to icon image
def extractIconUrlFromIconPageUrl(listOfUrls):
  # request get page, extract url to icon file
  print('extracting urls to icon files')
  listOfIconFileUrls = []
  return listOfIconFileUrls

# Side effect: return image from download url
def downloadIconPngImage(iconUrl):
  # Requests go to url and download file
  r = requests.get(iconUrl)
  i = Image.open(StringIO(r.content))
  print('downloading icon image pngs')

# Side effect: save file to directory
def saveFileToDirectory(file, directory):
  # file save this as filename to directory
  print('saving file to directory')

def main():
  listOfIconUrls = extractIconUrlFromIconPageUrl(extractUrlsToIconPage(iconListRootDomain))
  for url in listOfIconUrls:
    print('url in list of icon urls')
    saveFileToDirectory(downloadIconPngImage(url), iconSaveDirectory)
  print('Program complete')

if __name__ == '__main__':
  main()