import tkinter as tk
import random
import pygame
import os
import time

root = tk.Tk()
pygame.mixer.init()

def play_sound(sound_file):
    try:
        sound_path = os.path.abspath(sound_file)
        sound = pygame.mixer.Sound(sound_path)
        sound.play()
    except FileNotFoundError:
        print(f"Error: Sound file not found at {sound_path}")
    except pygame.error as e:
        print(f"Error playing sound: {e}")

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def name(self):
        name = str(self.rank) + str(self.suit) + ".gif"
        print(name)
        return name

class Player:
    def __init__(self):
        self.hand = []
        self.dealer_hand = []
        self.score_label = None  # Initialize score_label as None
        self.back_label = None

    def score(self, given_hand):
        score = 0
        if self.score_label:
            self.score_label.config(text="")
        for card in given_hand:
            if card.rank == 1:
                score += 11
            elif card.rank > 1 and card.rank < 10:
                score += card.rank
            elif card.rank >= 10:
                score += 10

        if score == 21:
            return "BlackJack!"
        elif score > 21:
            for card in given_hand:
                if card.rank == 1:
                    score -= 10
                    if score == 21:
                        return "BlackJack!"
                    if score < 21:
                        return score
            if score > 21:
                return "Bust!"
        else:
            return score
        

    def hit(self, deck, sound):
        i = random.randint(0, len(deck) - 1)
        self.hand.append(deck[i])
        deck.pop(i)
        img = tk.PhotoImage(file="DECK/" + self.hand[-1].name())
        label = tk.Label(root, image=img)
        label.image = img
        label.place(x=(len(self.hand) * 25), y=250)
        self.score_label.config(text="Score: " + str(self.score(self.hand)))

        if sound:
            play_sound("SOUNDS/hit.mp3")
        else:
            pass
        
    def init_dealer(self, deck):
        i = random.randint(0, len(deck) - 1)
        self.dealer_hand.append(deck[i])
        deck.pop(i)
        img = tk.PhotoImage(file="DECK/" + self.dealer_hand[-1].name())
        label = tk.Label(root, image=img)
        label.image = img
        label.place(x = 25, y = 25)
        img_back = tk.PhotoImage(file="DECK/b.gif")
        self.back_label= tk.Label(root, image=img_back)
        self.back_label.image = img_back
        self.back_label.place(x = 50, y = 24)

    
    def should_dealer_hit(self):
        if self.score(self.dealer_hand) == "BlackJack!":
            return False
        if self.score(self.dealer_hand) == "Bust!":
            return False
        if int(self.score(self.dealer_hand)) < 17:
            return True
        return False
    
    '''
    def dealer_play(self, deck):
        while self.should_dealer_hit():
            time.sleep(.5)
            play_sound("SOUNDS/hit.mp3")
            self.back_label.destroy()
            i = random.randint(0, len(deck) - 1)
            self.dealer_hand.append(deck[i])
            deck.pop(i)
            img = tk.PhotoImage(file="DECK/" + self.dealer_hand[-1].name())
            label = tk.Label(root, image=img)
            label.image = img
            label.place(x = (len(self.dealer_hand)) * 25, y = 25)"
     '''
    
    def dealer_play(self, deck, root):  # Pass root as an argument
        while self.should_dealer_hit():
            time.sleep(.5)
            play_sound("SOUNDS/hit.mp3")  # Assuming play_sound is defined elsewhere
            if hasattr(self, 'back_label') and self.back_label: #check if back_label exists
                self.back_label.destroy()
                self.back_label = None #prevent multiple destroys.

            i = random.randint(0, len(deck) - 1)
            self.dealer_hand.append(deck[i])
            deck.pop(i)
            img = tk.PhotoImage(file="DECK/" + self.dealer_hand[-1].name())
            label = tk.Label(root, image=img)
            label.image = img
            label.place(x=(len(self.dealer_hand)) * 25, y=25)
            root.update()  # Force the GUI to update
            
                
            
    def deal(self, deck):
        self.hit(deck, False)
        self.hit(deck, False)
        play_sound("SOUNDS/hit.mp3")

    def play_hand(self):
        clear_menu()
        self.hand.clear()
        self.dealer_hand.clear()
        self.score_label = tk.Label(root, text="Score: ") #create label here
        self.score_label.place(x=200, y=400)

        root.title("BlackJack!")
        root.geometry("500x500")
        root.configure(bg="#007A33")
        deck = create_deck()

        
        self.deal(deck)
        self.init_dealer(deck)
        play_button = tk.Button(text="Play", command=lambda: self.play_hand())
        play_button.place(x=50, y=400)
        hit_button = tk.Button(text="Hit", command=lambda: self.hit(deck, True))
        hit_button.place(x=100, y=400)
        stay_button = tk.Button(text="Stay", command=lambda: self.dealer_play(deck, root))
        stay_button.place(x=150, y=400)

def create_deck():
    suits = ["c", "d", "h", "s"]
    deck = []
    for r in range(1, 14):
        for s in suits:
            deck.append(Card(r, s))
    return deck

def clear_menu():
    for widget in root.winfo_children():
        widget.destroy()

def display_main_menu():
    clear_menu()
    root.title("BlackJack!")
    root.geometry("500x500")
    root.configure(bg="#007A33")
    nick = Player()
    play_button = tk.Button(text="Play!", command=lambda: nick.play_hand())
    play_button.place(x=250, y=250)

def run_gui():
    display_main_menu()
    root.mainloop()
