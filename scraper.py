import requests
from bs4 import BeautifulSoup
import json
#https://teespring.com/new-no-wifi-no-problem?tsmac=store&tsmic=compsci-store&pid=389
url = input("Please enter a valid teespring listing URL: ")
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

pageText = soup.find('div', class_='campaign__column--product')
campaignDict = dict()
campaignDict['title'] = pageText.find('h1', class_='campaign__name display--desktop h2').text.strip()
campaignDescription = pageText.find('div', class_='campaign__description_contents truncated')
for br in campaignDescription.find_all("br"):
    br.replace_with("\n")
campaignDict['description'] = campaignDescription.text.strip()
campaignList = pageText.find_all('option', class_='js-product-option')
campaignDict['baseURL'] = url[:url.rfind("=")+1]
campaignDict['products'] = []
for item in campaignList:
    itemID = item['value']
    productDict = dict()
    productDict['id'] = itemID
    productDict['name'] = item.text.strip()
    productUrl = campaignDict['baseURL'] + itemID
    itemPage = requests.get(productUrl)
    itemSoup = BeautifulSoup(itemPage.content, 'html.parser')
    productDict['imageLink'] = itemSoup.find('img', class_="image_stack__image")['data-zoom']
    campaignDict['products'].append(productDict)

with open('listingData.json', 'w') as fp:
    json.dump(campaignDict, fp,  indent=4)