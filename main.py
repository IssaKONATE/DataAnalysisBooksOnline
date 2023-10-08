import requests
import csv
from bs4 import BeautifulSoup


# Cette version permet de recuperer les infos de la page catégorie travel 
# ensuite le pro parcourt tous les articles (livres) de cette page
# Pour tous les artcicles de cette catégorie, le programme restittue les informations démandées dans la phase 1 dans un fichiers csv 




root='http://books.toscrape.com/catalogue'
#
homePageUrl = "http://books.toscrape.com/index.html"
#
domaineUrl = "http://books.toscrape.com/"

categorieName = "Travel"

def genererCsvDeArticle(article):
        
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
                

def main():
        travelPage = requests.get(root+"/category/books/travel_2/index.html")
        if travelPage.ok:
                dataSoup = BeautifulSoup(travelPage.text,'lxml')
                title = dataSoup.find('head').find('title').string
                articles = dataSoup.findAll('article')

                headers = ["Product page Url","Tittle","Image Url","Category","UPC","Product type","Price (incl. tax)","Price (excl. tax)","Tax","Number Availability","Number of reviews"]
                csvContent = []
                csvContent.append(headers)

                for article in articles:
                        value = genererCsvDeArticle(article)
                        csvContent.append(value)

                with open("output/"+categorieName+'.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(csvContent)

main()


