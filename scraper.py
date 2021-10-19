from requests import get 
from bs4 import BeautifulSoup 
from bs4.element import *
import pandas as pd
import itertools
import numpy as np

def one_page_scrapper (response) : 
    # Parser object 

    html_soup=BeautifulSoup(response.text,'html.parser')

    # Div of the announce

    announce = html_soup.find_all('div', class_ = ["annonce","annonce annonce_store"]) 

    # Number of announce in the page 

    NOAFP=len(list(announce))

    # First collumn : id
    for i in range(NOAFP):
        id_=[]
        for i in range(NOAFP):
            a = announce[i].get('id')

            if  a != None :
                id_.append(a)

    # print(id_)
    IDL=len(id_)

    # second collumn : Names of cars 

    carname=[]

    for i in range(NOAFP):
        try:
            carname.append(announce[i].find('h2').text)

        except AttributeError :
            pass



    CNL=len(carname)

    # third collumn : kilometrage 

    vehicule_kilometrage=[]
    for i in range(NOAFP):
        try:
            vehicule_kilometrage.append(announce[i].find('span',class_='vehicule_kilometrage').text)
        except AttributeError :
            pass


    VKL=len(vehicule_kilometrage)

    # from 4 to 9 

    l=[]
    for i in range(NOAFP):
        a=announce[i].find('span',class_='annonce_get_description')
        b=[]
        try:
            for br in a.findAll('br'):
                s = br.previousSibling
                if isinstance(s,NavigableString):
                    c=s
                else:
                    c=s.text 
                b.append(c)

        except AttributeError :
            pass
        l.append(b)

    l.remove([])
    x=list(map(list, itertools.zip_longest(*l, fillvalue=None)))
    LFE=len(x)

    # making the dataframe 

    df = pd.DataFrame({
        'Id_':id_ ,
        'Carname':carname ,
        'Vehicule_kilometrage':vehicule_kilometrage ,
        'Type': x[0],
        'Energie': x[1],
        'Moteur': x[2],
        'Boite': x[3],
        'Couleur': x[4],
        'Licence': x[5]
    })
    return df