import tkinter as tk
from tkinter import *
from blackjack import *

def display_main_menu():
    clear_menu()
    root.title("Blackjack!")
    root.geometry("568x500")
    root.configure(bg="#007A33")
    nick = Player()
    play_button = tk.Button(text="Play!", command=lambda: nick.play_hand(nick.bet))
    play_button.place(x=250, y=250)
    

def run_gui():
    display_main_menu()
    root.mainloop()

run_gui()