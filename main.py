from tabulate import tabulate
import os 

import gestion_stock 
import finance


liste_produit = []
caract_produit = ('nom','referance','cantité','PU','PV')

def nettoyer():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

while True : 
    nettoyer() #ici
    print(10*"==")
    print(" 1.ajouter un produit")
    print(" 2.vendre un produit")
    print(" 3.stock")
    print(" 4.finance")
    print(" 5.quitter")
    print(10*"==") 
    choix = int(input("entrer votre choix : "))
    nettoyer() #ici
    
    if  choix == 1 : 
        while True : 
            produit = {}
            for CP in caract_produit : 
                produit[CP] = str(input(f"veuillez entrer le {CP} : "))
            liste_produit.append(produit)
            choix= input('ajouter un nouveau produit ? (O/N) : ') 
            if choix.upper() == 'O'  : 
                pass 
            else : 
                break
        nettoyer() #ici
        gestion_stock.recevoire_produit(liste_produit)
        input("\cliqur sur [ENTRER] pour revenir au menue")

    elif choix == 2 : 
        #donnée du produit
        ref = input("entrer la reférance du produit a vendre : ")
        result=gestion_stock.verification(ref)
        
        #recherche du produit
        if result == None : 
            print("produit indisponible !")
            input("\cliquer sur [ENTRER] pour revenir au menu")
        else : 
            
            #afficher le produit 
            print(tabulate([result], headers="keys", tablefmt="fancy_grid"))
            q_vente = int(input("saisisz la quantité a vendre : "))
            nettoyer() #ici
            
            #vendre la cantité 
            gestion_stock.vendue(result, q_vente)
            input("\cliqur sur [ENTRER] pour revenir au menue")       
                
    elif choix == 3 :  
        total_stock = gestion_stock.afficher_tableu()
        if total_stock != None :
            print(tabulate(total_stock, headers="keys", tablefmt="fancy_grid")) 
        else : 
            print("stock vide !")
        input("\cliqur sur [ENTRER] pour revenir au menue")

    elif choix == 4 : 
        total_stock = gestion_stock.afficher_tableu()
        prix_total = finance.calculer_prix_total(total_stock)
        nettoyer() #ici
        print(f"l'argent dorment est  : {prix_total} DA")
        input("\ckiquer sur [ENTRER] pour revenir au menue ")
    
    elif choix == 5 : 
        print("au revoire !")
        break

        
        



    
            

