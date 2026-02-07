import csv
import datetime

#DATA
colonne = ['nom','referance','cantité','PU','PV']
colonne_attente = ['nom','referance','cantité','PU','PV','DV']
chemain_stock   = r'C:\CODE\code python\projet-gestion-stock.-py\stock.csv'
chemain_attente = r'C:\CODE\code python\projet-gestion-stock.-py\attente.csv'


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
        
def vendue(dicto_result): #probléme de logieque pour la liste d'attente
    stock_actuel=[]
    with open(chemain_stock, 'r', encoding="UTF-8", newline= '') as f : 
        stock_actuel = list(csv.DictReader(f,delimiter=';')) #sortie du stock
    
    for produit in stock_actuel : #maj
        if produit['referance'] == dicto_result['referance'] : 
            dif = int(produit['cantité']) - int(dicto_result['cantité'])
            temp_dicto = produit.copy()
            temp_dicto['cantité'] = str(dif)
            produit['cantité'] = dicto_result['cantité']
            
            try :
                with open(chemain_attente, 'r', encoding = 'UTF-8', newline='') as g : 
                    stock_actuel_att = list(csv.DictReader(g, delimiter=';'))
            except : 
                pass
                
            Trouve = False
            for produit_2 in stock_actuel_att : 
                if produit_2['referance'] == temp_dicto['referance'] : 
                    produit_2['cantité'] = temp_dicto['cantité']
                    produit_2['DV'] = datetime.date.today()
                    Trouve = True
                    break
            if Trouve == False :
                temp_dicto['DV'] = datetime.date.today()
                stock_actuel_att.append(temp_dicto)
   
            
            with open(chemain_attente, 'w', encoding= 'UTF-8', newline='') as g : 
                writer_2 = csv.DictWriter(g, fieldnames = colonne_attente ,delimiter=';')
                writer_2.writeheader()
                writer_2.writerows(stock_actuel_att)
            break
    
    
    with open(chemain_stock, 'w', encoding = 'UTF-8', newline='') as f : #metre dans le stock
        writer = csv.DictWriter(f, fieldnames= colonne , delimiter= ';')
        writer.writeheader()
        writer.writerows(stock_actuel)
    
def afficher_tableu():
    stock_actuel=[]
    with open(chemain_stock, 'r', encoding = "UTF-8", newline='') as f : 
        stock_actuel = list(csv.DictReader(f, delimiter=';'))
        return stock_actuel 
        
        
        
    