def calculer_prix_total(stock_actuel):
    cpt = 0
    for produit in stock_actuel : 
        cpt += int(produit["total_PU"])
    return cpt