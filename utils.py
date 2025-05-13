import pygame
import os
import tkinter as tk


root = tk.Tk()
pygame.mixer.init()
green = "#007A33" #casino colors

def play_sound(sound_file):
    try:
        sound_path = os.path.abspath(sound_file)
        sound = pygame.mixer.Sound(sound_path)
        sound.play()
    except FileNotFoundError:
        print(f"Error: Sound file not found at {sound_path}")
    except pygame.error as e:
        print(f"Error playing sound: {e}")


def clear_menu():
    for widget in root.winfo_children():
        widget.destroy()