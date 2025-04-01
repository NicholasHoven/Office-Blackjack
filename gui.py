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
        return name

class Player:
    def __init__(self):
        self.hand = []
        self.dealer_hand = []
        self.score_label = None
        self.back_label = None
        self.dealer_score_label = None
        self.outcome_label = None
        self.balance = 500

    def score(self, given_hand):
        score = 0
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
        

    def init_dealer(self, deck):
        i = random.randint(0, len(deck) - 1)
        self.dealer_hand.append(deck[i])
        deck.pop(i)
        img = tk.PhotoImage(file="DECK/" + self.dealer_hand[-1].name())
        label = tk.Label(root, image=img)
        label.image = img
        label.place(x=25, y=25)
        img_back = tk.PhotoImage(file="DECK/b.gif")
        self.back_label = tk.Label(root, image=img_back)
        self.back_label.image = img_back
        self.back_label.place(x=50, y=24)
        self.dealer_score_label.config(text="Score: " + str(self.score(self.dealer_hand)))

    def should_dealer_hit(self):
        if self.score(self.dealer_hand) == "BlackJack!":
            return False
        if self.score(self.dealer_hand) == "Bust!":
            return False
        if isinstance(self.score(self.dealer_hand), int) and self.score(self.dealer_hand) < 17:
            return True
        return False
    
    def determine_winner(self):
        if self.score(self.hand) == "Bust!":
            time.sleep(.3)
            play_sound("SOUNDS/dealer_win.mp3")
            return "Dealer Wins!"
        elif self.score(self.dealer_hand) == "Bust!":
            time.sleep(.3)
            play_sound("SOUNDS/win_sound.mp3")
            return "You Win!"
        elif self.score(self.dealer_hand) == "BlackJack!" and self.score(self.hand) != "BlackJack!":
            time.sleep(.3)
            play_sound("SOUNDS/dealer_win.mp3")
            return "Dealer Wins!"
        elif self.score(self.hand) == "BlackJack!" and self.score(self.dealer_hand) != "BlackJack!":
            time.sleep(.3)
            play_sound("SOUNDS/win_sound.mp3")
            return "You Win!"
        elif self.score(self.hand) == self.score(self.dealer_hand):
            return "Push!"
        elif int(self.score(self.hand)) < int(self.score(self.dealer_hand)):
            time.sleep(.3)
            play_sound("SOUNDS/dealer_win.mp3")
            return "Dealer Wins!"
        elif int(self.score(self.hand)) > int(self.score(self.dealer_hand)):
            time.sleep(.3)
            play_sound("SOUNDS/win_sound.mp3")
            return "You Win!"


    def dealer_play(self, deck, root):
        while self.should_dealer_hit():
            time.sleep(.5)
            play_sound("SOUNDS/hit.mp3")
            if hasattr(self, 'back_label') and self.back_label:
                self.back_label.destroy()
                self.back_label = None

            i = random.randint(0, len(deck) - 1)
            self.dealer_hand.append(deck[i])
            deck.pop(i)
            img = tk.PhotoImage(file="DECK/" + self.dealer_hand[-1].name())
            label = tk.Label(root, image=img)
            label.image = img
            label.place(x=(len(self.dealer_hand)) * 25, y=25)
            self.dealer_score_label.config(text="Score: " + str(self.score(self.dealer_hand)))
            root.update()
        self.outcome_label = tk.Label(text=self.determine_winner())
        self.outcome_label.place(x=150, y = 200)

    def hit(self, deck, sound, on_deal):
        if self.score(self.hand) != "Bust!" and self.score(self.hand) != "BlackJack!":
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
            if self.score(self.hand) == "Bust!":
                self.outcome_label = tk.Label(text=self.determine_winner())
                self.outcome_label.place(x=150, y = 200)
                #time.sleep(.2)
                #play_sound("SOUNDS/lose_horn.mp3")  
            if on_deal == False and self.score(self.hand) == "BlackJack!":
                time.sleep(1)
                self.dealer_play(deck, root)
                self.outcome_label = tk.Label(text=self.determine_winner())
                self.outcome_label.place(x=150, y = 200)
                

    def deal(self, deck):
        self.hit(deck, False, True)
        self.hit(deck, False, True)
        play_sound("SOUNDS/hit.mp3")

    
    def play_hand(self):
        clear_menu()
        self.hand.clear()
        self.dealer_hand.clear()
        self.score_label = tk.Label(root, text="Score: " + str(self.score(self.hand))) #create label here and set player score.
        self.score_label.place(x=200, y=400)
        self.dealer_score_label = tk.Label(root, text="Score: " + str(self.score(self.dealer_hand)))
        self.dealer_score_label.place(x=50, y=200)
        

        root.title("BlackJack!")
        root.geometry("500x500")
        root.configure(bg="#007A33")
        deck = create_deck()

        self.deal(deck)
        if self.score(self.hand) == "BlackJack!":
            self.init_dealer(deck)
            self.dealer_play(deck, root)
            self.outcome_label = tk.Label(text=self.determine_winner())
            self.outcome_label.place(x=150, y = 200)
        else:
            self.init_dealer(deck)
        play_button = tk.Button(text="Play", command=lambda: self.play_hand())
        play_button.place(x=50, y=400)
        hit_button = tk.Button(text="Hit", command=lambda: self.hit(deck, True, False))
        hit_button.place(x=100, y=400)
        stay_button = tk.Button(text="Stay", command=lambda: self.dealer_play(deck, root))
        stay_button.place(x=150, y=400)
        balance_label = tk.Label(text = "Balance: $" + str(self.balance))
        balance_label.place(x = 75, y = 450)
        wager_label = tk.Label(text = "Wager:")
        wager_label.place(x = 175, y = 450)
        wager_textbox = tk.Entry(root, width=5)
        wager_textbox.place(x = 225, y = 450)

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
