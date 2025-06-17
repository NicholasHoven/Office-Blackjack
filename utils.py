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


def toggle_music(sound_file):
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        print("Music stopped.")
    else:
        try:
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.set_volume(0.15)
            pygame.mixer.music.play(-1) # Play indefinitely
            print(f"Playing: {os.path.basename(sound_file)}")
        except pygame.error as e:
            print(f"Error starting music: {e}")


def clear_menu():
    for widget in root.winfo_children():
        widget.destroy()