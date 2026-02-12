import csv
import datetime
import os 

#généralisation : 
def charger_fichier(way):
    '''retourne la liste de dictionnaire de tout le fichier CSV
    (False si vide) '''
    liste=[]
    with open(way, 'r',encoding = "UTF-8", newline='') as f : 
        liste = list(csv.DictReader(f, delimiter=';'))
        return liste 


def remplir_fichier(way, colonne, liste): 
    '''remplie une liste de dictionnaire dans un fichier CSV
    (False si vide)'''
    with open(way, 'w',encoding="UTF-8",newline='') as f : 
        writer = csv.DictWriter(f, fieldnames=colonne, delimiter=";")
        writer.writeheader()
        writer.writerows(liste)


def ajouter_fichier(way, colonne, liste): 
    '''ajouter des élément a la fin du fichier sans changer de header'''
    with open(way, 'a',encoding="UTF-8", newline='') as h : 
        writer_2 = csv.DictWriter(h, fieldnames= colonne, delimiter=';')
        if os.path.getsize(way) == 0 : 
            writer_2.writeheader()
        writer_2.writerows(liste)      


def verification(ref, way):
    '''verifie si un produit et disponible dans le ficher
    renvoie un dictionnaire du produit si oui, sinon revoie None'''
    stock_actuel = charger_fichier(way)
    info_produit = None
    for produit in stock_actuel : 
        if produit['referance'] == ref :
            info_produit = produit
            break
    return info_produit

# ---------------------------------------------------------

def recevoire_produit(liste_arrivage, way,colonne): 
    '''reçois les produit ajouter (liste de dictionnaire)
    et les charge dans le fichier stock'''
    #lire le fichier en entier :
    stock_actuel = charger_fichier(way)
    print(f'reception de {len(liste_arrivage)} produit(s)')
     
    #MAJ
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
    remplir_fichier(way,colonne, stock_actuel)
   
          
def vendue(dicto_result, q_vente, way, way_2, colonne_stock, colonne_attente): 
    #1.charger le fichier stock attente
    stock_actuel= charger_fichier(way)
    stock_actuel_att = charger_fichier(way_2)
    
    #2.MAJ Stock
    for produit_1 in stock_actuel : 
        if produit_1['referance'] == dicto_result['referance'] : 
            if int(q_vente) <= int(produit_1['cantité']) : 
                produit_1['cantité'] = str(int(produit_1['cantité']) - int(q_vente))
                produit_1['total_PU']= str(int(produit_1['total_PU']) - int(produit_1['PU']) * int(q_vente))
                  
                #2.1.MAJ attente
                Trouve = False
                for produit_2 in stock_actuel_att : 
                    if produit_2['referance'] == dicto_result['referance'] : 
                        produit_2['cantité'] = str(int(produit_2['cantité']) + int(q_vente))
                        produit_2['total_PU']= str(int(produit_2['total_PU']) + int(produit_2['PU'])*int(q_vente))
                        produit_2['DE'] = str(datetime.date.today() + datetime.timedelta(days=3))
                        Trouve = True
                        break
                if Trouve == False :
                    copy_dicto_result = dicto_result.copy()
                    del copy_dicto_result['DA']
                    copy_dicto_result['cantité'] = q_vente
                    prix_TTPU = str(int(copy_dicto_result['PU']) * int(copy_dicto_result['cantité']))
                    copy_dicto_result['total_PU'] = prix_TTPU
                    copy_dicto_result['DE'] = str(datetime.date.today() + datetime.timedelta(days=3))
                    stock_actuel_att.append(copy_dicto_result)
    
                #2.2.remplir le fichier attente 
                remplir_fichier(way_2, colonne_attente, stock_actuel_att)
                print("produit vendue !")
                
            else : 
                print("cantité indisponible !")
        
    #3.remplire le fichier stock et fermer
    temp = [produit for produit in stock_actuel  if int(produit['cantité'])> 0 ]
    stock_actuel = temp
    remplir_fichier(way, colonne_stock, stock_actuel)
      
      
def retourner(result, q_retourner, way_1, way_2, colonne_1, colonne_2):
    #charger le fichier 
    attente_actuel = charger_fichier(way_1)
    stock_actuel   = charger_fichier(way_2)
    
    
    #MAJ
    ref_cible = result["referance"]
    for produit in attente_actuel : 
        if produit["referance"] == ref_cible : 
            nouvelle_q = str(int(produit['cantité']) - int(q_retourner))
            produit['cantité'] = nouvelle_q
            produit['total_PU']= str(int(nouvelle_q) * int(produit["PU"]))
            break 
        
    trouve_dans_stock = False
    for produit in stock_actuel : 
        if produit['referance'] == ref_cible : 
            nouvelle_q = str(int(produit['cantité']) + int(q_retourner))
            produit["cantité"] = nouvelle_q
            produit["total_PU"]= str(int(nouvelle_q) * int(produit["PU"]))
            trouve_dans_stock = True 
            break 
            
    if not trouve_dans_stock : 
        nouveau_p = result.copy()
        nouveau_p["cantité"] = q_retourner
        nouveau_p["total_PU"]= str(int(q_retourner) * int(nouveau_p["PU"]))
            
        if "DE" in nouveau_p: 
            del nouveau_p["DE"]
            nouveau_p["DA"] = str(datetime.date.today())

        stock_actuel.append(nouveau_p)
            
    #remplire le fichier  
    remplir_fichier(way_2, colonne_2, stock_actuel)
    temp = [p for p in attente_actuel if int(p['cantité'])>0]
    attente_actuel = temp
    remplir_fichier(way_1, colonne_1, attente_actuel) 
    
    print("Retour effectué avec succès !")
    
    
def netoyage_attente(chemain_attente, chemain_historique, colonne_attente, colonne_historique) : 
    #charger le fichier attente
    stock_total  = []
    stock_expire = []
    stock_attente= []
    
    stock_total = charger_fichier(chemain_attente)

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
    temp = [p for p in stock_attente if int(p['cantité'])>0]
    stock_attente = temp
    remplir_fichier(chemain_attente, colonne_attente, stock_attente)
    
    #remplire le fichier historique 
    if stock_expire :
        ajouter_fichier(chemain_historique, colonne_historique, stock_expire) 
 