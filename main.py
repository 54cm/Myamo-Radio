import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter
import vlc
import os

# --- Dossiers ---
CACHE_DIR = "cache"
AUDIO_DIR = "audio"

# --- Récitateurs et sourates ---
RECITATORS = {
    "Mishary Alafasy": {
        "img": "mishary.png",
        "tracks": {
            "Al-Fatiha": "mishary_alafasy_001.mp3",
            "Al-Baqara": "mishary_alafasy_002.mp3"
        }
    },
    "Yasir Al-Dawsari": {
        "img": "yasir.png",
        "tracks": {
            "Al-Fatiha": "yasir_001.mp3",
            "Al-Baqara": "yasir_002.mp3"
        }
    }
}

# --- Variables globales ---
player = None
current_track = None
selected_reciter = None

# --- Fonctions VLC ---
def play():
    global player, current_track
    if not current_track:
        status_label.config(text="⚠ Sélectionnez une sourate")
        return

    file_path = os.path.join(AUDIO_DIR, current_track)
    if not os.path.exists(file_path):
        status_label.config(text=f"⚠ Introuvable : {file_path}")
        return

    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(file_path)
    player.set_media(media)
    player.play()
    status_label.config(text=f"▶ Lecture : {current_track}")

def stop():
    global player
    if player:
        player.stop()
        status_label.config(text="⏹ Arrêté")

def set_volume(val):
    global player
    if player:
        volume = int(val)
        player.audio_set_volume(volume)

def on_sourate_select(event):
    global current_track, selected_reciter
    sourate = sourate_var.get()
    current_track = RECITATORS[selected_reciter]["tracks"][sourate]
    status_label.config(text=f"Sélectionné : {sourate}")

# --- Navigation ---
def open_selection():
    frame_welcome.pack_forget()
    frame_selection.pack(fill="both", expand=True)

def open_player(reciter):
    global selected_reciter
    selected_reciter = reciter

    frame_selection.pack_forget()
    frame_player.pack(fill="both", expand=True)

    sourate_menu['values'] = list(RECITATORS[reciter]["tracks"].keys())
    sourate_var.set("")
    status_label.config(text=f"🎙 {reciter} sélectionné")

# --- Interface ---
app = tk.Tk()
app.title("Myamo Radio Halal")
app.geometry("800x600")
app.resizable(False, False)

# --- Fond flouté ---
bg_path = os.path.join(CACHE_DIR, "mosquee.png")
bg_img = Image.open(bg_path).resize((800, 600)).filter(ImageFilter.GaussianBlur(4))
bg_tk = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(app, image=bg_tk)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# --- Couleurs thème Myamo (chien marron/noir) ---
BG_FRAME = "#2B1B0E"   # marron foncé
FG_TEXT = "#F5E1C0"    # beige clair
BTN_PLAY = "#A0522D"   # brun
BTN_STOP = "#8B0000"   # rouge foncé
BTN_NEXT = "#D2691E"   # orange brun

# --- Frame accueil ---
frame_welcome = tk.Frame(app, bg=BG_FRAME)
frame_welcome.pack(fill="both", expand=True)

welcome_label = tk.Label(
    frame_welcome,
    text="🌙 Bienvenue sur Myamo Radio 🌙",
    font=("Arial", 24, "bold"),
    fg=FG_TEXT,
    bg=BG_FRAME
)
welcome_label.pack(expand=True)

app.after(3000, open_selection)

# --- Frame sélection récitateurs ---
frame_selection = tk.Frame(app, bg=BG_FRAME)

# Logo Myamo en haut
myamo_path = os.path.join(CACHE_DIR, "myamo.png")
if os.path.exists(myamo_path):
    logo_img = Image.open(myamo_path).resize((100, 100))
    logo_tk = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(frame_selection, image=logo_tk, bg=BG_FRAME)
    logo_label.image = logo_tk
    logo_label.pack(pady=10)

title_sel = tk.Label(
    frame_selection,
    text="Sélectionnez un réciteur",
    font=("Arial", 20, "bold"),
    fg=FG_TEXT,
    bg=BG_FRAME
)
title_sel.pack(pady=10)

reciters_frame = tk.Frame(frame_selection, bg=BG_FRAME)
reciters_frame.pack(pady=15)

for i, reciter in enumerate(RECITATORS.keys()):
    img_path = os.path.join(CACHE_DIR, RECITATORS[reciter]["img"])
    if os.path.exists(img_path):
        img = Image.open(img_path).resize((140, 140))
        img_tk = ImageTk.PhotoImage(img)
        btn = tk.Button(
            reciters_frame,
            image=img_tk,
            command=lambda r=reciter: open_player(r),
            bd=0, relief="flat",
            bg=BG_FRAME,
            activebackground=BG_FRAME
        )
        btn.image = img_tk
        btn.grid(row=0, column=i, padx=20)

# --- Frame lecteur ---
frame_player = tk.Frame(app, bg=BG_FRAME)

status_label = tk.Label(frame_player, text="🎵 Prêt", font=("Arial", 14), fg=FG_TEXT, bg=BG_FRAME)
status_label.pack(pady=10)

sourate_var = tk.StringVar()
sourate_menu = ttk.Combobox(frame_player, textvariable=sourate_var, state="readonly")
sourate_menu.bind("<<ComboboxSelected>>", on_sourate_select)
sourate_menu.pack(pady=10)

controls = tk.Frame(frame_player, bg=BG_FRAME)
controls.pack(pady=10)

btn_play = tk.Button(controls, text="▶ Play", command=play, width=10, bg=BTN_PLAY, fg=FG_TEXT)
btn_play.grid(row=0, column=0, padx=10)

btn_stop = tk.Button(controls, text="⏹ Stop", command=stop, width=10, bg=BTN_STOP, fg=FG_TEXT)
btn_stop.grid(row=0, column=1, padx=10)

btn_next = tk.Button(controls, text="⏭ Next", command=lambda: None, width=10, bg=BTN_NEXT, fg=FG_TEXT)
btn_next.grid(row=0, column=2, padx=10)

volume_label = tk.Label(frame_player, text="🔊 Volume", fg=FG_TEXT, bg=BG_FRAME)
volume_label.pack()
volume_slider = tk.Scale(frame_player, from_=0, to=100, orient="horizontal", command=set_volume, bg=BG_FRAME, fg=FG_TEXT, troughcolor="#654321")
volume_slider.set(70)
volume_slider.pack(pady=5)

# --- Lancement ---
app.mainloop()
