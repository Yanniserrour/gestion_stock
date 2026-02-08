from tabulate import tabulate
import os 

import gestion_stock 
import finance


'''
a faire : 
    ajouter l'acces des fichier dans main  /done 
    netoyyer les nom de fonctions et de varialbes /done
    ajouter les colonnes comme effectifs  /done
    ameliorer la logique de vente stock -> attente -> historique /done
    améliorer la logique de produit arriver /done
    imbriquer les choix d'acces au stock (ajouter des options)  /done
    imbriquer la possibilité de calculer l'argent de historique, attente dans finance /done
    rendre les produit retourner dans le stock
    supprimer les produits completement vide du fichier 
    travailler sur le passage par copie du dictionnaire
'''


#DATA
colonne_stock      = ['nom','referance','cantité','PU','PV']
colonne_attente    = ['nom','referance','cantité','PU','PV','DE']
colonne_historique = ['nom','referance','cantité','PU','PV','DE']

#Way
chemain_stock      = r'C:\CODE\code python\projet-gestion-stock.-py\stock.csv'
chemain_attente    = r'C:\CODE\code python\projet-gestion-stock.-py\attente.csv'
chemain_historique = r'C:\CODE\code python\projet-gestion-stock.-py\historique.csv'



def nettoyer():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

gestion_stock.netoyage_attente(chemain_attente, chemain_historique , colonne_attente, colonne_historique)
while True : 
    nettoyer() 
    print(10*"==")
    print(" 1.ajouter un produit")
    print(" 2.vendre un produit")
    print(" 3.stock")
    print(" 4.finance")
    print(" 5.quitter")
    print(10*"==") 
    choix = int(input("entrer votre choix : "))
    nettoyer() 
    
    
    if  choix == 1 : 
        liste_produit = []
        while True : 
            produit = {}
            for CP in colonne_stock : 
                produit[CP] = str(input(f"veuillez entrer le {CP} : "))
            liste_produit.append(produit)
            choix= input('ajouter un nouveau produit ? (O/N) : ') 
            if choix.upper() == 'O'  : 
                pass 
            else : 
                break
        nettoyer() 
        gestion_stock.recevoire_produit(liste_produit, chemain_stock,colonne_stock)
        input("\cliqur sur [ENTRER] pour revenir au menue")


    elif choix == 2 : 
        #donnée du produit
        ref = input("entrer la reférance du produit a vendre : ")
        result=gestion_stock.verification(ref, chemain_stock)
        
        #recherche du produit
        if result == None : 
            print("produit indisponible !")
            input("\cliquer sur [ENTRER] pour revenir au menu")
        else : 
            
            #afficher le produit 
            print(tabulate([result], headers="keys", tablefmt="fancy_grid"))
            q_vente = input("saisisz la quantité a vendre : ")
            nettoyer() 
            
            #vendre la cantité 
            gestion_stock.vendue(result, q_vente, chemain_stock, chemain_attente , colonne_stock, colonne_attente)
            input("\cliqur sur [ENTRER] pour revenir au menue")       
        
                
    elif choix == 3 :  
        while True : 
            print(10*"==")
            print(" 1.afficher le stock")
            print(" 2.afficher les produits en attente")
            print(" 3.afficher les produits vendue ")
            print(" 4.sortir")
            print(10*"==")
            choix_3 = int(input('entrez votre choix : '))
            if  choix_3 == 1 : 
                total_stock = gestion_stock.charger_tableu(chemain_stock)
                if total_stock != None :
                    print(tabulate(total_stock, headers="keys", tablefmt="fancy_grid")) 
                else : 
                    print("stock vide !")
                input("\cliqur sur [ENTRER] pour revenir au menue")
                nettoyer()
            elif choix_3 == 2 : 
                total_stock = gestion_stock.charger_tableu(chemain_attente)
                if total_stock != None : 
                    print(tabulate(total_stock, headers="keys", tablefmt="fancy_grid"))
                else : 
                    print("attente vide !")
                input("\cliqur sur [ENTRER] pour revenir au menue")
                nettoyer()
            elif choix_3 == 3 : 
                total_stock = gestion_stock.charger_tableu(chemain_historique)
                if total_stock != False : 
                    print(tabulate(total_stock, headers="keys", tablefmt="fancy_grid"))
                else : 
                    print("historique vide !")
                input("\cliqur sur [ENTRER] pour revenir au menue")
                nettoyer()
            elif choix_3 == 4 : 
                break

    elif choix == 4 :
        while True :  
            print(10*"==")
            print(" 1.acceder a l'argent du stock")
            print(" 2.acceder a l'argent de l'attente")
            print(" 3.acceder a l'argent de l'historique")
            print(" 4.sortir")
            print(10*"==")
            choix_4 = int(input("entrer votre choix : "))
            if  choix_4 == 1 : 
                total_stock = gestion_stock.charger_tableu(chemain_stock)
                prix_total = finance.calculer_prix_total(total_stock)
                nettoyer() 
                print(f"la somme total est  : {prix_total} DA")
                input("\ckiquer sur [ENTRER] pour revenir au menue ")
                nettoyer()
            elif choix_4 == 2 : 
                total_stock = gestion_stock.charger_tableu(chemain_attente)
                prix_total = finance.calculer_prix_total(total_stock)
                nettoyer()
                print(f"la somme total est {prix_total} DA")
                input("\ckiquer sur [ENTRER] pour revenir au menue ")
                nettoyer()
            elif choix_4 == 3 : 
                total_stock = gestion_stock.charger_tableu(chemain_historique)
                prix_total = finance.calculer_prix_total(total_stock)
                nettoyer()
                print(f"la somme total est {prix_total} DA")
                input("\ckiquer sur [ENTRER] pour revenir au menue ")
                nettoyer()
            elif choix_4 == 4 : 
                break
            
    elif choix == 5 : 
        print("au revoire !")
        break

