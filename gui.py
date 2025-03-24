import tkinter as tk
import random
import pygame
import os

root = tk.Tk()
pygame.mixer.init()

def play_sound(sound_file):
    """Plays a sound file using pygame."""
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

    def score(self):
        score = 0
        if self.score_label:
            self.score_label.config(text="")
        for card in self.hand:
            if card.rank == 1:
                score += 11
            elif card.rank > 1 and card.rank < 10:
                score += card.rank
            elif card.rank >= 10:
                score += 10

        if score == 21:
            return "BlackJack!"
        elif score > 21:
            for card in self.hand:
                if card.rank == 1:
                    score -= 10
                    if score == 21:
                        return "BlackJack!"
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
        self.score_label.config(text="Score: " + str(self.score()))

        if sound:
            play_sound("SOUNDS/hit.mp3")
        else:
            pass


    def deal(self, deck):
        self.hit(deck, False)
        self.hit(deck, False)
        play_sound("SOUNDS/hit.mp3")

    def play_hand(self):
        clear_menu()
        self.hand.clear()
        self.score_label = tk.Label(root, text="Score: ") #create label here
        self.score_label.place(x=250, y=400)

        root.title("BlackJack!")
        root.geometry("500x500")
        root.configure(bg="#007A33")
        deck = create_deck()

        self.deal(deck)
        play_button = tk.Button(text="Play", command=lambda: self.play_hand())
        play_button.place(x=100, y=400)
        hit_button = tk.Button(text="Hit", command=lambda: self.hit(deck, True))
        hit_button.place(x=150, y=400)
        stay_button = tk.Button(text="Stay")
        stay_button.place(x=200, y=400)

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
