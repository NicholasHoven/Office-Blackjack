#Nicholas Hoven 2025
import tkinter as tk
import random
from playsound import playsound
import os

root = tk.Tk()

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def name(self):
        name = str(self.rank) + str(self.suit) + ".gif"
        print(name)
        return(name)
    
class Player:
    def __init__(self):
        self.hand = []

    def score(self):
        score = 0
        for card in self.hand:
            if card.rank == 1: #case Ace
                score += 11
            elif card.rank > 1 and card.rank < 10: #case cards (1-9)
                score += card.rank
            elif card.rank >= 10:
                score += 10    

        if(score == 21):
            score = "BlackJack!"
            return score
        if(int(score) > 21): 
            for card in self.hand:
                if card.rank == 1: #case Ace
                    score -= 10
                    if score == 21:
                        score = "BlackJack!"
                    return score
            if score > 21:
                score = "Bust!"
                return score
        else: 
            score = score
        return score

    def hit(self, deck):
        i = random.randint(0, len(deck)-1)
        self.hand.append(deck[i])
        deck.pop(i)
        img = tk.PhotoImage(file = "DECK/" + self.hand[-1].name()) # Store the PhotoImage in a variable
        label = tk.Label(root, image=img)
        label.image = img #Keep a reference to the image.
        label.place(x = (len(self.hand)*25))
        score_label = tk.Label(root, text="Score: " + str(self.score()))
        score_label.place(x=50,y=250)
        #playsound("SOUNDS/hit.mp3")

    def deal(self, deck):
        self.hit(deck)
        self.hit(deck)

    def play_hand(self):
        clear_menu()
        self.hand.clear()

        root.title("BlackJack!")
        root.geometry("500x500")
        root.configure(bg="#007A33")
        deck = create_deck()
        self.deal(deck)
        play_button = tk.Button(text="Play", command=lambda: self.play_hand())
        play_button.place(x=100,y=200)
        hit_button = tk.Button(text = "Hit", command=lambda: self.hit(deck))
        hit_button.place(x = 200, y = 200)
        stay_button = tk.Button(text = "Stay")
        stay_button.place(x=250, y = 200)
        choice = "" #this is used to represent the players choice for hit or stay
        #while (player.score() != "BlackJack!") and (player.score() != "Bust!") and (choice != "s"):
        
            



    
        
 
def create_deck() -> list[Card]: #if you have a class called card.
    suits = ["c","d","h","s"]
    deck = []
    for r in range(1,14):
       for s in suits:
          deck.append(Card(r,s))
    return deck


def clear_menu(): #this will completely clear the GUI menu
    for widget in root.winfo_children():
        widget.destroy()

  
def display_main_menu():
    clear_menu()
    root.title("BlackJack!")
    root.geometry("500x500")
    root.configure(bg="#007A33")
    nick = Player()
    play_button = tk.Button(text = "Play!", command=lambda:nick.play_hand())
    play_button.place(x=250,y=250)
   



def run_gui():
    display_main_menu()
    root.mainloop()