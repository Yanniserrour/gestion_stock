import csv
import datetime

#DATA
colonne = ['nom','referance','cantité','PU','PV']
colonne_attente = ['nom','referance','cantité','PU','PV','DV']
chemain_stock   = r'C:\CODE\code python\projet-gestion-stock.-py\stock.csv'
chemain_attente = r'C:\CODE\code python\projet-gestion-stock.-py\attente.csv'




def recevoire_produit(liste_arrivage): 
    '''reçois les produit ajouter (liste de dictionnaire)
    et les charge dans le fichier stock'''
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
        scripteur = csv.DictWriter(f, fieldnames=colonne, delimiter=';') 
        scripteur.writeheader() 
        scripteur.writerows(stock_actuel) 
        
        
        
        
        
        

def verification(ref):
    '''verifie si un produit et disponible dans le ficher
    renvoie un dictionnaire du produit si oui, sinon revoie None'''
    stock_actuel =[]
    with open (chemain_stock, 'r', encoding = "UTF-8",newline='') as f :
        stock_actuel = list(csv.DictReader(f, delimiter=';'))
        info_produit = None
        for produit in stock_actuel : 
            if produit['referance'] == ref :
                info_produit = produit
                break
        return info_produit


        
def vendue(dicto_result, q_vente): 
    
    stock_actuel=[]
    #1.charger du fichier stock
    with open(chemain_stock, 'r', encoding="UTF-8", newline= '') as f : 
        stock_actuel = list(csv.DictReader(f,delimiter=';')) 
    
    #2.MAJ stock
    stock_actuel_att=[]
    for produit_1 in stock_actuel : 
        if produit_1['referance'] == dicto_result['referance'] : 
            if q_vente <= int(produit_1['cantité']) : 
                produit_1['cantité'] = str(int(produit_1['cantité']) - q_vente)
                
                #2.1.charger du fichier attente
                try :
                    with open(chemain_attente, 'r', encoding = 'UTF-8', newline='') as g : 
                        stock_actuel_att = list(csv.DictReader(g, delimiter=';'))
                except : 
                    pass
                    
                #2.2.MAJ attente
                Trouve = False
                for produit_2 in stock_actuel_att : 
                    if produit_2['referance'] == dicto_result['referance'] : 
                        produit_2['cantité'] = str(int(produit_2['cantité']) + q_vente)
                        produit_2['DV'] = datetime.date.today()
                        Trouve = True
                        break
                if Trouve == False :
                    dicto_result['DV'] = datetime.date.today()
                    stock_actuel_att.append(dicto_result)
    
                
                #2.3.remplir le fichier attente et fermer
                with open(chemain_attente, 'w', encoding= 'UTF-8', newline='') as g : 
                    writer_2 = csv.DictWriter(g, fieldnames = colonne_attente ,delimiter=';')
                    writer_2.writeheader()
                    writer_2.writerows(stock_actuel_att)
                print("produit vendue !")
                
            else : 
                print("cantité indisponible !")
        
    
    
    #3.remplire le fichier stock et fermer
    with open(chemain_stock, 'w', encoding = 'UTF-8', newline='') as f : 
        writer = csv.DictWriter(f, fieldnames= colonne , delimiter= ';')
        writer.writeheader()
        writer.writerows(stock_actuel)
        

def afficher_tableu():
    '''retourne la liste de dictionnaire de tout le fichier CSV'''
    stock_actuel=[]
    with open(chemain_stock, 'r', encoding = "UTF-8", newline='') as f : 
        stock_actuel = list(csv.DictReader(f, delimiter=';'))
        return stock_actuel 
        
def verification_stock_attente():
    today = datetime.date.today()
    
    stock_actuel=[]
    with open(chemain_attente , 'r' , encoding= "UTF-8", newline='') as a : 
        stock_actuel = csv.DictReader(a , delimiter=';')
    
    for produit in stock_actuel : 
        if produit['DV'] == today  : 
            pass
            
        
    