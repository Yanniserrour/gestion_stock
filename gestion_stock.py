import csv
import datetime
import os 

#Tools : 
def charger_tableu(way):
    '''retourne la liste de dictionnaire de tout le fichier CSV
    (False si vide) '''
    stock_actuel=[]
    with open(way, 'r', encoding = "UTF-8", newline='') as f : 
        stock_actuel = list(csv.DictReader(f, delimiter=';'))
        return stock_actuel 
    

def verification(ref, way):
    '''verifie si un produit et disponible dans le ficher
    renvoie un dictionnaire du produit si oui, sinon revoie None'''
    stock_actuel =[]
    with open (way, 'r', encoding = "UTF-8",newline='') as f :
        stock_actuel = list(csv.DictReader(f, delimiter=';'))
        info_produit = None
        for produit in stock_actuel : 
            if produit['referance'] == ref :
                info_produit = produit
                break
        return info_produit




def recevoire_produit(liste_arrivage, way,colonne): 
    '''reçois les produit ajouter (liste de dictionnaire)
    et les charge dans le fichier stock'''
    stock_actuel = []
    print(f'reception de {len(liste_arrivage)} produit(s)')
    #lire le fichier en entier : 
    with open(way, 'r', encoding = 'UTF-8',newline='') as f : 
            stock_actuel=list(csv.DictReader(f,delimiter=';'))
    
    #MAJ de la liste
    for nv_produit in liste_arrivage : 
        trouve = False 
        for ac_produit in stock_actuel : 
            if nv_produit['referance'] == ac_produit['referance'] : 
                total = int(ac_produit['cantité']) + int(nv_produit['cantité'])
                ac_produit['cantité'] = str(total)
                ac_produit['PU'] = nv_produit['PU']
                ac_produit['PV'] = nv_produit['PV']
                ac_produit['DA'] = nv_produit['DA']
                trouve = True
                break
        if trouve == False : 
            stock_actuel.append(nv_produit)
    
    #remplire le fichier 
    with open(way, 'w', encoding='UTF-8',newline='') as f : 
        scripteur = csv.DictWriter(f, fieldnames=colonne, delimiter=';') 
        scripteur.writeheader() 
        scripteur.writerows(stock_actuel) 
        
             
def vendue(dicto_result, q_vente, way, way_2, colonne_stock, colonne_attente): 
    
    stock_actuel=[]
    #1.charger du fichier stock
    with open(way, 'r', encoding="UTF-8", newline= '') as f : 
        stock_actuel = list(csv.DictReader(f,delimiter=';')) 
    
    #2.MAJ stock
    stock_actuel_att=[]
    for produit_1 in stock_actuel : 
        if produit_1['referance'] == dicto_result['referance'] : 
            if int(q_vente) <= int(produit_1['cantité']) : 
                produit_1['cantité'] = str(int(produit_1['cantité']) - int(q_vente))
                produit_1['total_PU']= str(int(produit_1['total_PU']) - int(produit_1['PU']) * int(q_vente))
                
                #2.1.charger du fichier attente
                try :
                    with open(way_2, 'r', encoding = 'UTF-8', newline='') as g : 
                        stock_actuel_att = list(csv.DictReader(g, delimiter=';'))
                except : 
                    pass
                    
                #2.2.MAJ attente
                Trouve = False
                for produit_2 in stock_actuel_att : 
                    if produit_2['referance'] == dicto_result['referance'] : 
                        produit_2['cantité'] = str(int(produit_2['cantité']) + int(q_vente))
                        produit_2['total_PU']= str(int(produit_2['total_PU']) + int(produit_2['PU'])*int(q_vente))
                        produit_2['DE'] = datetime.date.today() + datetime.timedelta(days=3)
                        Trouve = True
                        break
                if Trouve == False :
                    copy_dicto_result = dicto_result.copy()
                    del copy_dicto_result['DA']
                    copy_dicto_result['cantité'] = q_vente
                    prix_TTPU = str(int(copy_dicto_result['PU']) * int(copy_dicto_result['cantité']))
                    copy_dicto_result['total_PU'] = prix_TTPU
                    copy_dicto_result['DE'] = datetime.date.today() + datetime.timedelta(days=3)
                    stock_actuel_att.append(copy_dicto_result)
    
                #2.3.remplir le fichier attente et fermer
                with open(way_2, 'w', encoding= 'UTF-8', newline='') as g : 
                    writer_2 = csv.DictWriter(g, fieldnames = colonne_attente ,delimiter=';')
                    writer_2.writeheader()
                    writer_2.writerows(stock_actuel_att)
                print("produit vendue !")
                
            else : 
                print("cantité indisponible !")
        
    #3.remplire le fichier stock et fermer
    with open(way, 'w', encoding = 'UTF-8', newline='') as f : 
        writer = csv.DictWriter(f, fieldnames= colonne_stock , delimiter= ';')
        writer.writeheader()
        writer.writerows(stock_actuel)
        
      
def netoyage_attente(chemain_attente, chemain_historique, colonne_attente, colonne_historique) : 
    #charger les données du fichier attente
    stock_total  = []
    stock_expire = []
    stock_attente= []
    try : 
        with open(chemain_attente, 'r', encoding='UTF-8', newline='') as a : 
            stock_total = list(csv.DictReader(a, delimiter=';'))
    except :
        pass
        
    #MAJ
    for produit in stock_total : 
        
        today = datetime.date.today()
        date_verifier = produit["DE"]
        date_verifier = datetime.date.fromisoformat(date_verifier)
        
        if today >= date_verifier : 
            stock_expire.append(produit)
        else : 
            stock_attente.append(produit)
    
    
    #remplire le fichier attente
    with open(chemain_attente,   'w',encoding="UTF-8", newline='') as a : 
        writer  = csv.DictWriter(a,  fieldnames=colonne_attente,   delimiter=';')
        writer.writeheader()
        writer.writerows(stock_attente)
        
    #remplire le fichier historique 
    if stock_expire : 
        with open(chemain_historique, 'a',encoding="UTF-8", newline='') as h : 
            writer_2 = csv.DictWriter(h, fieldnames= colonne_historique, delimiter=';')
            if os.path.getsize(chemain_historique) == 0 : 
                writer_2.writeheader()
            writer_2.writerows(stock_expire)
    
