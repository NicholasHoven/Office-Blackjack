import tkinter as tk
import random
import time
from utils import *


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def name(self):
        name = str(self.rank) + str(self.suit) + ".gif"
        return name
    

def create_deck():
    suits = ["c", "d", "h", "s"]
    deck = []
    for r in range(1, 14):
        for s in suits:
            deck.append(Card(r, s))
    return deck


class Player:
    def __init__(self):
        self.hand = []
        self.dealer_hand = []
        self.score_label = None
        self.back_label = None
        self.dealer_score_label = None
        self.outcome = "unknown"
        self.outcome_label = None
        self.balance = 500
        self.balance_label = None
        self.bet = 0
        self.wager_textbox = None
        self.wager_label = None
        self.first_run = True
        self.can_bet = True
        self.hit_count = 0
        self.play_Status = "not started"
        self.stay_staus = "not started"
        self.play_again_status = False


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
            return "Blackjack!"
        elif score > 21:
            for card in given_hand:
                if card.rank == 1:
                    score -= 10
                    if score == 21:
                        return "Blackjack!"
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
        if self.score(self.dealer_hand) == "Blackjack!":
            return False
        if self.score(self.dealer_hand) == "Bust!":
            return False
        if isinstance(self.score(self.dealer_hand), int) and self.score(self.dealer_hand) < 17:
            return True
        return False
    
    
    def play_again(self):
        self.hand = []
        self.dealer_hand = []
        self.score_label = None
        self.back_label = None
        self.dealer_score_label = None
        self.outcome = "unknown"
        self.outcome_label = None
        self.balance = 500
        self.balance_label = None
        self.bet = 0
        self.wager_textbox = None
        self.wager_label = None
        self.first_run = True
        self.can_bet = True
        self.play_Status = "not started"
        self.stay_staus = "not started"
        self.play_again_status = True
        self.play_hand(self.bet)

    
    def determine_winner(self):
        self.can_bet = True
        self.play_Status = "not started"
        if self.score(self.hand) == "Bust!":
            self.balance -= self.bet
            self.balance_label.config(text = "Balance: $" + str(self.balance))
            root.update()
            time.sleep(.3)
            if self.balance < 10:
                play_sound("SOUNDS/lose_horn.mp3")
                play_again_button = tk.Button(text = "Play Again?", command=lambda: self.play_again())
                play_again_button.place(x=425, y = 200)
                return "The House Always Wins!"
            else:
                play_sound("SOUNDS/dealer_win.mp3")
                self.outcome = "Dealer Wins!"
            return "Dealer Wins!"
        elif self.score(self.hand) == "Blackjack!" and self.score(self.dealer_hand) != "Blackjack!":
            self.balance += (1.5 * self.bet)
            self.balance_label.config(text = "Balance: $" + str(self.balance))
            root.update()
            time.sleep(.3)
            play_sound("SOUNDS/win_sound.mp3")
            self.outcome = "You Win!"
            return "You Win!"
        elif self.score(self.dealer_hand) == "Blackjack!" and self.score(self.hand) != "Blackjack!":
            self.balance -= self.bet
            self.balance_label.config(text = "Balance: $" + str(self.balance))
            root.update()
            time.sleep(.3)
            if self.balance == 0:
                play_sound("SOUNDS/lose_horn.mp3")
                play_again_button = tk.Button(text = "Play Again?", command=lambda: self.play_again())
                play_again_button.place(x=450, y = 200)
                return "The House Always Wins!"
            else:
                play_sound("SOUNDS/dealer_win.mp3")
                self.outcome = "Dealer Wins!"
            return "Dealer Wins!"
        elif self.score(self.dealer_hand) == "Bust!":
            self.balance += self.bet
            self.balance_label.config(text = "Balance: $" + str(self.balance))
            root.update()
            time.sleep(.3)
            play_sound("SOUNDS/win_sound.mp3")
            self.outcome = "You Win!"
            return "You Win!"
        elif self.score(self.hand) == self.score(self.dealer_hand):
            self.outcome = "Push!"
            return "Push!"
        elif int(self.score(self.hand)) < int(self.score(self.dealer_hand)):
            self.balance -= self.bet
            self.balance_label.config(text = "Balance: $" + str(self.balance))
            root.update()
            time.sleep(.3)
            if self.balance == 0:
                play_sound("SOUNDS/lose_horn.mp3")
                play_again_button = tk.Button(text = "Play Again?", command=lambda: self.play_again())
                play_again_button.place(x=450, y = 200)
                return "The House Always Wins!"
            else:
                play_sound("SOUNDS/dealer_win.mp3")
                self.outcome = "Dealer Wins!"
            return "Dealer Wins!"
        elif int(self.score(self.hand)) > int(self.score(self.dealer_hand)):
            self.balance += self.bet
            self.balance_label.config(text = "Balance: $" + str(self.balance))
            root.update()
            time.sleep(.3)
            play_sound("SOUNDS/win_sound.mp3")
            self.outcome = "You Win!"
            return "You Win!"


    def dealer_play(self, deck, root):
        if self.outcome_label == "undetermined":
            if self.stay_staus == "not started":
                self.stay_staus = "started"
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
                self.outcome_label.place(x=245, y = 200)
            self.bet = 0
            self.wager_label.config(text = "Bet: $" + str(self.bet))


    def hit(self, deck, sound, on_deal):
        if self.outcome == "unknown":
            if self.score(self.hand) != "Bust!" and self.score(self.hand) != "Blackjack!":
                self.hit_count += 1
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
                    self.outcome_label.place(x=245, y = 200)
                    self.bet = 0
                    self.wager_label.config(text = "Bet: $" + str(self.bet))
                if self.score(self.hand) == "Blackjack!":
                    root.after(500, self.dealer_play, deck, root)


    def deal(self, deck):
        self.hit(deck, False, True)
        self.hit(deck, False, True)
        play_sound("SOUNDS/hit.mp3")


    def increase_bet(self, amount):
        if (amount == -1) and (self.can_bet == True): #case clear
            self.bet = 0
            self.wager_label.config(text = "Bet: $" + str(self.bet))
        elif ((self.bet + amount) <= self.balance) and (self.can_bet == True):
            play_sound("SOUNDS/money_click.mp3")
            self.bet += amount
            self.wager_label.config(text = "Bet: $" + str(self.bet))


    def place_bets(self):
        self.wager_label = tk.Label(text = "Bet: $" + str(self.bet))
        self.wager_label.place(x = 180, y = 420)
        one_img_v = tk.PhotoImage(file="CURRENCY/100_135v.png")
        one_button = tk.Button(root, image=one_img_v, borderwidth=0, command=lambda: self.increase_bet(100))
        one_button.image = one_img_v
        one_button.place(x = 280, y = 350)
        one_img_v = tk.PhotoImage(file="CURRENCY/50_135v.png")
        one_button = tk.Button(root, image=one_img_v, borderwidth=0, command=lambda: self.increase_bet(50))
        one_button.image = one_img_v
        one_button.place(x = 350, y = 350)
        one_img_v = tk.PhotoImage(file="CURRENCY/20_135v.png")
        one_button = tk.Button(root, image=one_img_v, borderwidth=0, command=lambda: self.increase_bet(20))
        one_button.image = one_img_v
        one_button.place(x = 420, y = 350)
        one_img_v = tk.PhotoImage(file="CURRENCY/10_135v.png")
        one_button = tk.Button(root, image=one_img_v, borderwidth=0, command=lambda: self.increase_bet(10))
        one_button.image = one_img_v
        one_button.place(x = 490, y = 350)
        clear_bet_button = tk.Button(root, text="Clear", command=lambda: self.increase_bet(-1))
        clear_bet_button.place(x=180, y = 470)

    def play_music(self):
        music_image = tk.PhotoImage(file="ASSETS/music_label.png")
        sound_button = tk.Button(root, image=music_image, borderwidth=0, bg="#007A33", command=lambda: toggle_music("SOUNDS/game_music.mp3"))
        sound_button.image = music_image
        sound_button.place(x = 538, y = 2)


    def play_hand(self, wager):
        if self.first_run == True: #initial case
            if self.play_again_status == False:
                toggle_music("SOUNDS/game_music.mp3")
            self.first_run = False
            clear_menu()
            self.play_music()
            self.outcome = "unknown"
            self.place_bets()
            play_button = tk.Button(text="Play", command=lambda: self.play_hand(self.bet))
            play_button.place(x=25, y=450)
            hit_button = tk.Button(text="Hit", command=lambda: self.hit(deck, True, False))
            hit_button.place(x=75, y=450)
            stay_button = tk.Button(text="Stay", command=lambda: self.dealer_play(deck, root))
            stay_button.place(x=125, y=450)
            self.balance_label = tk.Label(text = "Balance: $" + str(self.balance))
            self.balance_label.place(x = 180, y = 445)
        elif wager != 0:
            if self.play_Status != "in progress":
                self.play_Status = "in progress"
                self.stay_staus = "not started"
                clear_menu()
                self.play_music()
                self.hit_count = 0
                self.can_bet = False
                self.outcome = "unknown"
                self.place_bets()
                self.hand.clear()
                self.dealer_hand.clear()
                self.outcome_label = "undetermined"
                self.bet = int(wager)
                print("BET: "+ str(self.bet))
                self.score_label = tk.Label(root, text="Score: " + str(self.score(self.hand))) #create label here and set player score.
                self.score_label.place(x=50, y=360)
                self.dealer_score_label = tk.Label(root, text="Score: " + str(self.score(self.dealer_hand)))
                self.dealer_score_label.place(x=50, y=135)
                root.title("Blackjack!")
                root.geometry("568x500")
                root.configure(bg="#007A33")
                deck = create_deck()
                self.deal(deck)
                self.init_dealer(deck)
                play_button = tk.Button(text="Play", command=lambda: self.play_hand(self.bet))
                play_button.place(x=25, y=450)
                hit_button = tk.Button(text="Hit", command=lambda: self.hit(deck, True, False))
                hit_button.place(x=75, y=450)
                stay_button = tk.Button(text="Stay", command=lambda: self.dealer_play(deck, root))
                stay_button.place(x=125, y=450)
                self.balance_label = tk.Label(text = "Balance: $" + str(self.balance))
                self.balance_label.place(x = 180, y = 445)