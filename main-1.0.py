import requests
from bs4 import BeautifulSoup
from PIL import Image
from StringIO import StringIO
import os

iconListRootDomainIconList = 'http://wow.gamepedia.com/Wowpedia:WoW_Icons/Icon_List'
iconListRootDomain = 'http://wow.gamepedia.com'
iconListRootTarget = '$(".mw-content-text ol li a[\'href\']")'  # jQuery psuedo code selection
iconListRootTargetId = 'mw-content-text'
iconSaveDirectory = './output/icons'

# Side effect: produce list of urls to page that holds icon image
def extractUrlsToIconPage(locationRoot):
  # request get base page
  print('extracting urls to icon page where icon url will be found')
  r = requests.get(locationRoot)
  soup = BeautifulSoup(r.content, 'html.parser')
  # print(soup.find(id = iconListRootTargetId).find_all('li').find('a'))  # current stopping point
  listOfIconPageUrlWhereIconFileUrlWillBeFound = []
  # for a in soup.find(id = iconListRootTargetId).find_all('a', href=True):
  for a in soup.select('#' + iconListRootTargetId + ' ol li a'):
    # print(a['href'])
    listOfIconPageUrlWhereIconFileUrlWillBeFound.append(iconListRootDomain + a['href'])
  return listOfIconPageUrlWhereIconFileUrlWillBeFound

# Side effect: produce a list of urls to icon image
def extractIconUrlFromIconPageUrl(listOfUrls):
  # request get page, extract url to icon file
  print('extracting urls to icon files')
  listOfIconFileUrls = []
  for url in listOfUrls:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    for a in soup.select('.fullMedia a'):
      print(url)
      print(a['href'])
      listOfIconFileUrls.append(a['href'])
  return listOfIconFileUrls

# Side effect: return image from download url
def downloadIconPngImage(iconUrl):
  print('downloading icon image pngs')
  # Requests go to url and download file
  r = requests.get(iconUrl)
  i = Image.open(StringIO(r.content))
  print(i)

# Side effect: save file to directory
def saveFileToDirectory(file, directory):
  # file save this as filename to directory
  print('saving file to directory')

def main():
  listOfIconUrls = extractIconUrlFromIconPageUrl(extractUrlsToIconPage(iconListRootDomainIconList))
  for url in listOfIconUrls:
    print('url in list of icon urls')
    saveFileToDirectory(downloadIconPngImage(url), iconSaveDirectory)
  print('Program complete')

if __name__ == '__main__':
  main()