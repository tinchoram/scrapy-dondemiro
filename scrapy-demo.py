##############################################
# Scrapy Demo - Tinchoram.com/dondemiro
# Version: 1.0.0
# By: @Tinchoram
# CodeSource: https://github.com/tinchoram/scrapy-dondemiro
# Date: 2020-05-17
##############################################

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import time 

############# START FUNCTIONS ####################

###Download web site whit requests library
def downloadWebSite(url):
	try:
		response = requests.get(url)
		soup = BeautifulSoup(response.content,'html.parser')
		print('descarga Ok de: ',str(url))
		return soup
		
	except Exception as e:
		print('Error con descarga: {}'.format(e))
		return None

###get link of each genero and return dictionari key:value = genero:link
def getGenero(url,data):
    try:
        # category = ['action', 'animacion', 'aventure','aventura', 'biography', 
        #             'ciencia-ficcion', 'comedia', 'crimen', 'documental', 
        #             'drama', 'familia', 'fantasia', 'guerra', 'historia', 
        #             'intriga', 'misterio', 'musical','musica', 'terror', 'thriller', 
        #             'romantico', 'western','estrenos','pelicula-de-tv']

        category = ['accion']
        dic_genero = {}

        for genero in category:
            weblinks = data.find_all(href=re.compile('[\/]{}[\/]'.format(genero)),limit=1)

            for link in weblinks:
                linkgenero = link.get('href')
                ln = urljoin(url, str(linkgenero))
                dic_genero[genero] = ln

        
        return dic_genero
    except Exception as e:
        print('Error get genero: {}'.format(e))
        return None

def GetListFilms(url,dic_genero):
    try:
        ##Total page for scrapy
        ##Total de paginas a Scrypear
        totalpage = 2

        ##For each category in dictionary
        for key, value in dic_genero.items():
            for i in range(1,totalpage):
                print('Genero: {} -- Link: {} -- Page: {}'.format(key, value,i))
                page = str(value)+'page/'+str(i)
                print(page)
                souppage = downloadWebSite(page)

                #soup = souppage.find_all(('img','a'))
                soup = souppage.find_all('article' , attrs={'class':'post'} )

                for movie in soup:
                    print('---------------------MOVIE----------------------------')
                    name=movie.find('h2' , attrs={'class':'entry-title'}).text
                    print('---NAME:' + str(name))
                    urlimg=movie.find('img').get('src')
                    print('---URL-IMG:' + str(urlimg))
                    link=movie.find('a').get('href')
                    print('---URL-link:' + str(link))
                    print('-----------------------------------------------------')
                    
                    print('---------------------sleep one-----------------------')
                    #Time sleep between request
                    #Tiempo entre descarga
                    time.sleep(1)

                #print(soup)

    except Exception as e:
        print('Error get genero: {}'.format(e))
        return None


###Function Main Spyder
def scrapyram(url):
    try:
        ###Dowload Website
        ###Descargo Sitio
        data = downloadWebSite(url)

        ###Get All category and links
        ###obtengo todos generos del sitio y su link
        dic_genero = getGenero(url,data)
        print('-----------------GENEROS--------------------------')
        print(dic_genero)
        print('--------------------------------------------------')

        ###Scrapy each category and generate list of films
        ###Escaneo cada genero y creo lista de peliculas
        GetListFilms(url,dic_genero)

    except Exception as e:
        print('Error of Scrapy: {}'.format(e))
        return None

############# END FUNCTIONS ####################


############# MAIN ####################

if __name__ == "__main__":
    
    #URL for Scrapy:
	url = 'https://pelispedia.info/'

	scrapyram(url)