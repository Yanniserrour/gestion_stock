import csv

#DATA
colonne = ['nom','referance','cantité','PU','PV']
chemain_stock = r'C:\CODE\code python\projet-gestion-stock.-py\stock.csv'


def recevoire_produit(liste_arrivage): 
    stock_actuel = []
    print(f'reception de {len(liste_arrivage)} produit(s)')
    #lire le fichier en entier : 
    with open(chemain_stock, 'r', encoding = 'UTF-8',newline='') as f : 
            stock_actuel=list(csv.DictReader(f,delimiter=';'))
    
    #MAJ de la liste
    for nv_produit in liste_arrivage : 
        trouve = False 
        for ac_produit in stock_actuel : 
            if nv_produit['referance'] == ac_produit['referance'] : 
                total = int(ac_produit['cantité']) + int(nv_produit['cantité'])
                ac_produit['cantité'] = str(total)
                trouve = True
                break
        if trouve == False : 
            stock_actuel.append(nv_produit)
    
    #remplire le fichier 
    with open(chemain_stock, 'w', encoding='UTF-8',newline='') as f : 
        scripteur = csv.DictWriter(f, fieldnames=colonne, delimiter=';') #l'ordre 
        scripteur.writeheader() #ecire l'entete
        scripteur.writerows(stock_actuel) #deposer le fichier
        
        
        

def verification(ref):
    stock_actuel =[]
    with open (chemain_stock, 'r', encoding = "UTF-8",newline='') as f :
        stock_actuel = list(csv.DictReader(f, delimiter=';'))
        info_produit = None
        for produit in stock_actuel : 
            if produit['referance'] == ref :
                info_produit = produit
                break
        return info_produit
        
def vendue(dicto_result): 
    stock_actuel=[]
    with open(chemain_stock, 'r', encoding="UTF-8", newline= '') as f : 
        stock_actuel = list(csv.DictReader(f,delimiter=';'))
    
    for produit in stock_actuel :
        if produit['referance'] == dicto_result['referance'] : 
            produit['cantité'] = dicto_result['cantité']
            break
    
    
    with open(chemain_stock, 'w', encoding = 'UTF-8', newline='') as f : 
        writer = csv.DictWriter(f, fieldnames= colonne , delimiter= ';')
        writer.writeheader()
        writer.writerows(stock_actuel)
    
def afficher_tableu():
    stock_actuel=[]
    with open(chemain_stock, 'r', encoding = "UTF-8", newline='') as f : 
        stock_actuel = list(csv.DictReader(f, delimiter=';'))
        return stock_actuel 
        
        
        
    