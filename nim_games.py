#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

"""
Jeu de Nim - Version SIMPLE (21 allumettes) et MARIENBAD (4 tas : 1,3,5,7)
"""

"""
   Demande le mode de jeu voulue (SIMPLE OU MARIENBAD)
   :return: game_mode
"""
def ask_game_mode():
    while True:
        game_mode = input("Tapez SIMPLE (mode classique) ou MARIENBAD : ").strip().upper()
        if game_mode in ("SIMPLE", "MARIENBAD"):
            return game_mode
        else:
            print("Veuillez entrer SIMPLE ou MARIENBAD")


"""
    Demande le type de jeux voulue
    :return: liste de noms des joueurs
"""
def ask_type_of_game():
    while True:
        choice = input("Tapez ORDINATEUR ou JOUEUR : ").strip().upper()
        if choice == "JOUEUR":
            player_name_1 = input("Entrez le nom du joueur 1 : ")
            player_name_2 = input("Entrez le nom du joueur 2 : ")
            return [player_name_1, player_name_2]
        elif choice == "ORDINATEUR":
            player_name_1 = input("Entrez le nom du joueur : ")
            return [player_name_1, "Ordinateur"]
        else:
            print("Choix invalide. Tapez ORDINATEUR ou JOUEUR.")

"""
    Demande au joueur de choisir le nombre d'allumettes qu'il veut enlever dans le mode de jeu simple
    :param name : nom du joueur
    :param matches_remaining : nombre d'allumettes restantes 
    :return: nombre d'allumettes que le joueur souhaite enlever
"""
def player_turn_simple(name, matches_remaining):
    while True:
        try:
            number = int(input(f"{name}, combien d'allumettes voulez-vous prendre ? (1 à 4) : "))
            if 1 <= number <= 4 and number <= matches_remaining:
                return number
        except ValueError:
            pass
        print("Entrée invalide. Essayez encore.")

"""
    Permet à l'ordinateur de choisir le nombre d'allumettes qu'il doit enlever dans le mode de jeu simple
    :param last_choice_player : dernier nombre d'allumettes choisis par le joueur (Nullable)
    :param matches_remaining : nombre d'allumettes restantes 
    :return: liste de noms des joueurs
"""
def computer_turn_simple(last_choice_player, matches_remaining):
    if last_choice_player:
        number = 5 - last_choice_player
    else:
        number = random.randint(1, min(4, matches_remaining))

    number = min(number, matches_remaining)
    print(f"L'ordinateur prend {number} allumette(s).")
    return number

def display_piles(piles):
    print("\nÉtat actuel des tas :")
    for i, pile in enumerate(piles):
        print(f"Tas {i + 1} : {'|' * pile} ({pile})")

def is_game_over_marienbad(piles):
    return all(pile == 0 for pile in piles)

def player_turn_marienbad(player_name, piles):
    while True:
        try:
            pile_index = int(input(f"{player_name}, choisissez un tas (1-4) : ")) - 1
            if pile_index not in range(4):
                print("Choisir un chiffre entre 1 et 4")
            if piles[pile_index] == 0:
                print("Ce tas est vide. Choisissez un autre.")
                continue

            max_take = piles[pile_index]
            count = int(input(f"{player_name}, combien d'allumettes voulez-vous prendre dans le tas ?"))
            if 1 <= count <= max_take:
                return pile_index, count
        except ValueError:
            pass
        print("Entrée invalide. Essayez encore.")

def computer_turn_marienbad(piles):
    non_empty_indices = [i for i, pile in enumerate(piles) if pile > 0]
    pile_index = random.choice(non_empty_indices)
    count = random.randint(1, piles[pile_index])
    print(f"L'ordinateur retire {count} allumette(s) du tas {pile_index + 1}.")
    return pile_index, count


def game_simple(players):
    matches = 21
    actual_player = random.randint(0, 1)
    print(f"\n{players[actual_player]} commence la partie.\n")
    last_choice = None

    while matches > 0:
        print(f"\nAllumettes restantes : {matches}")
        player_name = players[actual_player]

        if player_name == "Ordinateur":
            choice = computer_turn_simple(last_choice, matches)
        else:
            choice = player_turn_simple(player_name, matches)
            last_choice = choice

        matches -= choice

        if matches == 0:
            print(f"\n{player_name} a pris la dernière allumette et perd la partie.")
            print(f"{players[1 - actual_player]} gagne !\n")
            break

        actual_player = 1 - actual_player

def game_marienbad(players):
    piles = [1, 3, 5, 7]
    actual_player = random.randint(0, 1)
    print(f"\n{players[actual_player]} commence la partie.\n")

    while not is_game_over_marienbad(piles):
        display_piles(piles)
        player_name = players[actual_player]

        if player_name == "Ordinateur":
            pile_index, count = computer_turn_marienbad(piles)
        else:
            pile_index, count = player_turn_marienbad(player_name, piles)

        piles[pile_index] -= count
        print(f"{player_name} retire {count} allumette(s) du tas {pile_index + 1}.")

        if is_game_over_marienbad(piles):
            print(f"\n{player_name} a pris la dernière allumette et perd la partie.")
            print(f"{players[1 - actual_player]} gagne !\n")
            break

        actual_player = 1 - actual_player

def main():
    mode = ask_game_mode()

    if mode == "SIMPLE":
        players = ask_type_of_game()
        game_simple(players)

    elif mode == "MARIENBAD":
        players = ask_type_of_game()
        game_marienbad(players)

if __name__ == "__main__":
    main()