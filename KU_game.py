# Tātad, šis ir diezgan labs pamats, tam ko mēs taisīsim. GPT 4o uzcookoja, nemelošu. 
# No visiem mūsu dotajiem uzdevumiem:
# Ir:
#   ✅ Spēles loģika ir pilnībā realizēta
#   ✅ Dators spēlē pret cilvēku
#   ✅ Punktu skaitīšana un noteikumi ievēroti
#   ✅ Minimaksa algoritms ir realizēts
#   ✅ Dators veic stratēģiskus gājienus
#   ✅ Datu struktūra spēles stāvokļa apstrādei ir izveidota (ar funkcijām, kas aprēķina spēles stāvokli)
# Nav:
#   🔲 Alfa-beta algoritms nav ieviests
#   🔲 Nav GUI (grafiskā lietotāja saskarne)
#   🔲 Nav iespējas izvēlēties, kurš sāk spēli (cilvēks vai dators)
#   🔲 Nav eksperimentu ar algoritmu efektivitāti
#
# Principā atliek pievienot to kā vēl nav un viss. Vēl var izdarīt šos pāris soļus, lai uzlabotu algoritmu. (jo pagaidām, tas ir diezgan stulbs un bieži zaudē)
#   Uzlabot heuristikas funkciju, lai dators labāk analizētu savas uzvaras iespējas.
#   Izmēģināt dažādus depth līmeņus minimaksa algoritmam (piemēram, 6-7 līmeņi).

import random

def get_initial_stones():
    while True:
        try:
            stones = int(input("Ievadiet akmentiņu skaitu (50-70): "))
            if 50 <= stones <= 70:
                return stones
            else:
                print("Lūdzu, ievadiet skaitli no 50 līdz 70!")
        except ValueError:
            print("Lūdzu, ievadiet skaitli!")

def evaluate_state(stones, player_stones, player_points):
    if stones % 2 == 0:
        return player_points + 2
    else:
        return player_points - 2

def minimax(stones, depth, is_maximizing, player_stones, player_points):
    if stones == 0:
        return player_points + player_stones
    if depth == 0:
        return evaluate_state(stones, player_stones, player_points)
    
    if is_maximizing:
        best_score = float('-inf')
        for move in [2, 3]:
            if stones >= move:
                score = minimax(stones - move, depth - 1, False, player_stones + move, player_points)
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for move in [2, 3]:
            if stones >= move:
                score = minimax(stones - move, depth - 1, True, player_stones, player_points)
                best_score = min(best_score, score)
        return best_score

def ai_move(stones, player_stones, player_points):
    best_move = None
    best_score = float('-inf')
    
    for move in [2, 3]:
        if stones >= move:
            score = minimax(stones - move, 5, False, player_stones + move, player_points)
            if score > best_score:
                best_score = score
                best_move = move
    
    return best_move if best_move is not None else 2  # Ja best_move ir None, paņem 2

def play_game():
    stones = get_initial_stones()
    human_stones, ai_stones = 0, 0
    human_points, ai_points = 0, 0
    turn = random.choice(["cilvēks", "dators"])
    
    while stones > 0:
        print(f"\nAtlikušie akmentiņi: {stones}")
        print(f"Jūsu punkti: {human_points}, Datora punkti: {ai_points}")
        
        if turn == "cilvēks":
            if stones < 2:  # Ja paliek mazāk par 2 akmentiņiem, spēle beidzas
                break
            while True:
                try:
                    move = int(input("Jūsu gājiens! Paņemiet 2 vai 3 akmentiņus: "))
                    if move in [2, 3] and move <= stones:
                        break
                    else:
                        print("Nederīga izvēle!")
                except ValueError:
                    print("Ievadiet skaitli 2 vai 3!")
            
            stones -= move
            human_stones += move
            human_points = evaluate_state(stones, human_stones, human_points)
            turn = "dators"
        else:
            print("Dators domā...")
            move = ai_move(stones, ai_stones, ai_points)
            print(f"Dators paņēma {move} akmentiņus.")
            stones -= move
            ai_stones += move
            ai_points = evaluate_state(stones, ai_stones, ai_points)
            turn = "cilvēks"
    
    print("\nSpēle beigusies!")
    human_points += human_stones
    ai_points += ai_stones
    
    print(f"Jūsu punkti: {human_points}, Datora punkti: {ai_points}")
    if human_points > ai_points:
        print("Jūs uzvarējāt!")
    elif human_points < ai_points:
        print("Dators uzvarēja!")
    else:
        print("Neizšķirts!")

if __name__ == "__main__":
    play_game()
