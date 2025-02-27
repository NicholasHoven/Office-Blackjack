#Nicholas Hoven 2025
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pathlib import Path
from cards import *

root = tk.Tk()
data_path = str(Path(__file__).parent).replace("\\src", "\\data")
root.configure(bg="#007A33") #menu color

def clear_menu(): #this will completely clear the GUI menu
    for widget in root.winfo_children():
        widget.destroy()

def display_main_menu():
    clear_menu()
    root.title("Office BlackJack")
    root.geometry("400x400")
    card_path = str(data_path) + str("\\deck\\1c.gif")
    print(card_path)
    image = tk.PhotoImage(file = card_path) # Change to your GIF file name

# Create a label to display the image
    label = tk.Label(root, image=image)
    label.image = image  # Keep a reference to the image
    label.place(x=5)

def run_gui():
    display_main_menu()
    root.mainloop()