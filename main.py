import requests
import csv
from bs4 import BeautifulSoup
import os


root='http://books.toscrape.com/catalogue'
homePageUrl = "http://books.toscrape.com/index.html"
domaineUrl = "http://books.toscrape.com/"

#Cette version permet de recuperer les infos de toutes les cathégories 
# Ensuite le programme parcourt one by one chaque catégorie
# Pour tous les artcicles de chaque catégorie, le programme restittue les informations démandées dans la phase 1 dans un fichiers csv 
# Ce programme permet enfin de télécharger et enrégistrer les fichiers images de chaque Page Produit consultées.

def generateFolder(folderName):
        isExist = os.path.exists(folderName)
        if not isExist:
           os.makedirs(folderName)
           


def genererCsvDeArticle(article, categorieName):

        a = article.find('div').find('a',href=True)
        href = a['href']
        link = href.lstrip('../../../')
        productPageUrl = root+'/'+link
        productData = requests.get(productPageUrl)
        dataSoup = BeautifulSoup(productData.text,'lxml')
        descSoup = dataSoup.find(id="product_description")
        description = ""
        if descSoup:
                description = dataSoup.find(id="product_description").find_next("p").string
                
        title = dataSoup.find('h1').string
        img = dataSoup.find("div",{"class":"item active"}).find('img')['src']
        imgUrl = "http://books.toscrape.com/"+img.lstrip('../../../')
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
        
        value.append(description)
        return value

def generateImageFromPage(imageUrl,fileName):
        response = requests.get(imageUrl)
        newFilename = fileName.replace('/','')
        outputFolder = "output/img/"
        
        open(outputFolder+newFilename+".jpg", "wb").write(response.content)


def findAllArticles(dataSoup, myrequest, aProductLink):
        
        articles = (dataSoup.findAll('article'))
        numero = 1

        while dataSoup.find('li',{"class":"next"}) != None:
                numero = numero+1
                page = aProductLink.rstrip("index.html")+"page-"+(str(numero))+".html"

                print(page)
                productData = requests.get(page)
                dataSoup = BeautifulSoup(productData.text,'lxml')
                articles.extend(dataSoup.findAll('article'))


        return articles
                            
        
        
                

def main():

        print("Debut execution du programme")
        generateFolder("output")
        generateFolder("output/img")
        
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
                        #articles = dataSoup.findAll('article')

                        articles = findAllArticles(dataSoup, requests,aProductLink)

                        headers = ["Product page Url","Title","Image Url","Category","UPC","Product type","Price (incl. tax)","Price (excl. tax)","Tax","Number Availability","Number of reviews","Description"]
                        csvContent = []
                        csvContent.append(headers)

                        for article in articles:
                                value = genererCsvDeArticle(article, categorieName)
                                generateImageFromPage(value[2], value[1])
                                csvContent.append(value)

                        
                            
                        with open("output/"+categorieName+'.csv', 'w', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerows(csvContent)
        print("FIN!!!!!!!!!!!!!!!!!!!")

main()
