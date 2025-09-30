import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
import os

# --- Initialisation ---
pygame.mixer.init()

AUDIO_DIR = "audio"

# Récitateurs et fichiers MP3
RECITATORS = {
    "Mishary Alafasy": ["mishary_alafasy_001.mp3", "mishary_alafasy_002.mp3"],
    # tu peux ajouter d'autres récitateurs ici
}

current_index = 0
current_playlist = []

def play():
    global current_playlist, current_index
    if not current_playlist:
        recitateur = reciter_var.get()
        current_playlist = RECITATORS[recitateur]
        current_index = 0
    file_path = os.path.join(AUDIO_DIR, current_playlist[current_index])
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    status_label.config(text=f"▶ Lecture : {current_playlist[current_index]}")

def next_track():
    global current_index
    if current_playlist:
        current_index = (current_index + 1) % len(current_playlist)
        play()

def stop():
    pygame.mixer.music.stop()
    status_label.config(text="⏹ Arrêté")

# --- Interface ---
app = tk.Tk()
app.title("Myamo Radio")
app.geometry("500x400")
app.configure(bg="#fdf6e3")

# Image Myamo
img = Image.open("myamo.png").resize((150,150))
img_tk = ImageTk.PhotoImage(img)
label_img = tk.Label(app, image=img_tk, bg="#fdf6e3")
label_img.pack(pady=10)

# Message de bienvenue
welcome_label = tk.Label(app, text="🌙 Bienvenue sur Myamo Radio Halal 🌙", font=("Arial", 14), bg="#fdf6e3")
welcome_label.pack(pady=5)

# Sélecteur récitateur
reciter_var = tk.StringVar()
reciter_var.set(list(RECITATORS.keys())[0])
reciter_menu = ttk.Combobox(app, textvariable=reciter_var, values=list(RECITATORS.keys()), state="readonly", width=30)
reciter_menu.pack(pady=10)

# Boutons
frame_btn = tk.Frame(app, bg="#fdf6e3")
frame_btn.pack(pady=10)

btn_play = tk.Button(frame_btn, text="▶️ Play", command=play, width=10)
btn_play.grid(row=0, column=0, padx=5)

btn_next = tk.Button(frame_btn, text="⏭ Next", command=next_track, width=10)
btn_next.grid(row=0, column=1, padx=5)

btn_stop = tk.Button(frame_btn, text="⏹ Stop", command=stop, width=10)
btn_stop.grid(row=0, column=2, padx=5)

# Statut
status_label = tk.Label(app, text="Prêt 🎧", bg="#fdf6e3")
status_label.pack(pady=10)

app.mainloop()
