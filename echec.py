#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 11:23:26 2026

@author: adla309
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 11:23:26 2026

@author: adla309
"""
print("génial ca marche")
class player :
    def __init__(self,name,color):
        self.name=name
        self.color=color
        
    def askMove(self):
        couleur = "Blanc" if self.color == 0 else "Noir"
        print(f"{self.name} ({couleur}), entrez votre coup :")
        print("Format attendu : <pièce><case_depart> <pièce><case_arrivee>")
        print("Exemple : Nb1 Nc3")
        
        while True:
            move = input("Votre coup : ").strip()
            parts = move.split()
            if len(parts) != 2:
                print("Format invalide. Exemple valide : Nb1 Nc3")
                continue

            start, end = parts

            if len(start) != 3 or len(end) != 3:
                print("Format invalide. Exemple valide : Nb1 Nc3")
                continue

            piece_start, piece_end = start[0], end[0]
            pos_start, pos_end = start[1:], end[1:]

            if (pos_start[0] not in "abcdefgh" or pos_end[0] not in "abcdefgh" or
                pos_start[1] not in "12345678" or pos_end[1] not in "12345678"):
                print("Coordonnées invalides.")
                continue

            if piece_start != piece_end:
                print("La pièce doit être la même au départ et à l'arrivée.")
                continue

            return (piece_start, pos_start, pos_end)
        
if __name__ == "__main__":
    player1 = player("Alice", 0)
    coup = player1.askMove()
    print("Coup saisi :", coup)