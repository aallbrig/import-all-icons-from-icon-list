import requests
from bs4 import BeautifulSoup
from PIL import Image
from StringIO import StringIO
import os
# Async requests libs
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor
# Download image libs
import shutil
# Debug
from pprint import pprint

iconListRootDomain = 'http://wow.gamepedia.com'
iconListRootDomainIconList = 'http://wow.gamepedia.com/Wowpedia:WoW_Icons/Icon_List'
iconSaveDirectory = './output/icons'

# # Side effect: produce a list of urls to icon image
def extractIconUrlFromIconPageUrl(url):
  print('Extracting page URLs')
  html = requests.get(url).content
  selection = '#mw-content-text ol li a'
  listOfATags = BeautifulSoup(html, "html.parser").select(selection)
  listOfImageFilePageUrls = []
  for a in listOfATags:
    pageUrl = (iconListRootDomain + a['href']).strip()
    listOfImageFilePageUrls.append(str(pageUrl))
  return listOfImageFilePageUrls

# # Side effect: return image from download url
def downloadIconPngImage(response):
  print(response.url)
  iconFileName = response.url.split('/')[-1]
  print(iconFileName)
  with open(iconSaveDirectory + '/' + iconFileName, 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)

def main():
  # get the list of URLs to vist
  listOfImageFilePageUrls = extractIconUrlFromIconPageUrl(iconListRootDomainIconList)
  # TODO: Replace logic below with something nicer
  filteredListOfAbilityIcons = []
  for pageUrl in listOfImageFilePageUrls:
    imageName = pageUrl.split('/')[-1]
    if ('Ability_' in imageName or 'Spell_' in imageName):
      filteredListOfAbilityIcons.append(pageUrl)
  session = FuturesSession(executor=ThreadPoolExecutor(max_workers=10))
  futuresOfPageHtml = []
  for u in filteredListOfAbilityIcons:
    futuresOfPageHtml.append(session.get(u))

  # TODO: Replace below with thread pool and queue
  iconFileImageUrls = []
  for f in futuresOfPageHtml:
    result = f.result()
    html = result.content
    selection = '#mw-content-text .fullMedia a'
    listOfATags = BeautifulSoup(html, "html.parser").select(selection)
    for a in listOfATags:
      pageUrl = (a['href']).strip()
      print(pageUrl)
      iconFileImageUrls.append(pageUrl)

  # TODO: Replace below with thread pool and queue
  futuresOfPageHtml = []
  for u in iconFileImageUrls:
    futuresOfPageHtml.append(session.get(u, stream=True))

  for f in futuresOfPageHtml:
    result = f.result()
    iconImage = downloadIconPngImage(result)
  print('Program complete')

if __name__ == '__main__':
  main()