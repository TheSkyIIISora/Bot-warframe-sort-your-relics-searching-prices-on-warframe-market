from lxml import html, etree
import requests
import asyncio
import discord
from selenium.webdriver import Firefox
import time

def html_tree(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree

def recherche(nom):         #to get the price of items
    driver.get("https://warframe.market/items/"+nom)
    time.sleep(1)
    prix = driver.find_element_by_class_name("price").text

    return prix

def liste(reliques):        #add relics to a list
    global liste_reliques,relique,fin
    if (reliques == '14'):
        fin=1
        print("end\nIt'll take "+str(14*len(liste_reliques))+' seconds')
    else:
        liste_reliques = liste_reliques + [reliques]
        
driver = Firefox(executable_path=r'C:/tmp/git/Bot-warframe-sort-your-relics-searching-prices-on-warframe-market/geckodriver.exe')
relique = ''

while (True):
        
    liste_reliques = []
    ordre=[]
    u_prix=[]
    b=0
    fin = 0

    
    print("what's your relics ? (enter '14' to end) ")      #asking to get relics


    while (True):
        if (fin == 1):
            break
        relique = input()
        relique = relique.replace(' ','_')
        liste(relique)

    

    compteur1 = 0
    while (len(liste_reliques) != compteur1):

        tree = html_tree('https://warframe.fandom.com/wiki/'+liste_reliques[compteur1])     #search for items in relics
        a = (tree.xpath('//table[@class="emodtable"]/tr/td/a/text()'))

        
        compteur = 0
        while (len(a) != compteur):
            if (a[compteur] != "Forma Blueprint"):          #forma can't be found on warframe.market
                if (a[compteur]=="Kavasa Prime Collar"):        #exception
                    a[compteur]="Kavasa Prime KUBROW Collar Blueprint" 
                item = a[compteur].replace(' ','_') 
                item = item.replace('&','and')
                item = item.lower()
                prix=recherche(item)
                
                pair=compteur1*3
                pair2=pair+1
                pair3=pair+2
                if (len(ordre) < pair3):
                    ordre=ordre+[a[compteur]]
                    ordre=ordre+[prix]
                    ordre=ordre+[liste_reliques[compteur1]]
                else:
                    if (int(prix) > b):
                        b = int(prix)
                        ordre[pair]=a[compteur]
                        ordre[pair2]=prix
                        ordre[pair3]=liste_reliques[compteur1]
                
                compteur = compteur + 1
                
            else:
                compteur = compteur + 1

        compteur1 = compteur1 + 1
        b=0

    u_prix = ordre[1::3]
    u_prix2 = u_prix
    comparateur3=0
    
    while (len(u_prix) != comparateur3):        #price > str to int
        u_prix[comparateur3]=int(u_prix[comparateur3])
        comparateur3=comparateur3+1
        
    u_prix = sorted(u_prix)         #sort only price

    rangement=0
    rangement2=0
    u_final=[]
    while (len(u_final)!= len(ordre)):      #sort all
        if (u_prix[rangement] == u_prix2[rangement2]):
            u_prix2[rangement2]=0
            rangement2=rangement2+1
            u_final = u_final+ordre[rangement2*3-3:rangement2*3]
            rangement=rangement+1
            rangement2=0
        else:
            rangement2=rangement2+1

    u_final.reverse()

    fini=2
    classement=1
    while (len(u_final)+2 != fini):     #print result
        print(str(classement)+' | '+'relique '+u_final[fini-2]+' '+u_final[fini]+' '+u_final[fini-1]+'\n')
        classement=classement+1
        fini=fini+3
        
