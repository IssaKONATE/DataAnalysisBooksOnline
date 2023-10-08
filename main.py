import requests
import csv
from bs4 import BeautifulSoup



# Cette version permet de recuperer les infos de toutes les cathégories 
# Ensuite le programme parcourt one by one chaque catégorie
# Pour tous les artcicles de chaque catégorie, le programme restittue les informations démandées dans la phase 1 dans un fichiers csv 
# Ce programme permet enfin de télécharger et enrégistrer les fichiers images de chaque Page Produit consultées.

root='http://books.toscrape.com/catalogue'
#
homePageUrl = "http://books.toscrape.com/index.html"
#
domaineUrl = "http://books.toscrape.com/"


def genererCsvDeArticle(article, categorieName):
        
        a = article.find('div').find('a',href=True)
        href = a['href']
        link = href.lstrip('../../../')
        productPageUrl = root+'/'+link
        productData = requests.get(productPageUrl)
        dataSoup = BeautifulSoup(productData.text,'lxml')
        title = dataSoup.find('head').find('title').string
        imgUrl = dataSoup.find("div",{"class":"item active"}).find('img')['src']
        value = []
        tables = dataSoup.findChildren('table')
        my_table = tables[0]
        rows = my_table.findChildren(['tr'])
        value.append(productPageUrl)
        value.append(title)
        value.append(imgUrl)
        value.append(categorieName)
        for row in rows:
                th = row.find('th').string
                td = row.find('td').string
                value.append(td)
        
        return value

def generateImageFromPage(imageUrl,fileName):
        response = requests.get(imageUrl)
        open("output/img/"+fileName+".ico", "wb").write(response.content)
                

def main():
        homePageUrlResponse = requests.get(homePageUrl)
        if homePageUrlResponse.ok:
                soup = BeautifulSoup(homePageUrlResponse.text, 'lxml')
                allCategories = soup.find('ul', {"class":"nav nav-list"}).find('li').find('ul').findAll('li')
                for categorie in allCategories:
                        aHref= categorie.find('a')
                        categorieName = " ".join(aHref.string.split())
                        linkA = aHref['href']	
                        aProductLink = domaineUrl+linkA
                        productData = requests.get(aProductLink)
                        dataSoup = BeautifulSoup(productData.text,'lxml')
                        #title = dataSoup.find('head').find('title').string
                        articles = dataSoup.findAll('article')

                        headers = ["Product page Url","Title","Image Url","Category","UPC","Product type","Price (incl. tax)","Price (excl. tax)","Tax","Number Availability","Number of reviews"]
                        csvContent = []
                        csvContent.append(headers)

                        for article in articles:
                                value = genererCsvDeArticle(article, categorieName)
                                imgUrl = "http://books.toscrape.com/"+value[2].lstrip('../../../')
                                generateImageFromPage(imgUrl, value[1])
                                csvContent.append(value)

                        with open("output/"+categorieName+'.csv', 'w', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerows(csvContent)

main()
