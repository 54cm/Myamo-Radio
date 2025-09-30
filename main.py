import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import vlc

# --- Dossiers ---
CACHE_DIR = "cache"
AUDIO_DIR = "audio"

# --- Récitateurs et sourates ---
RECITATORS = {
    "Mishary Alafasy": {
        "img": "mishary.png",
        "tracks": {
            "Al-Fatiha": "Mishary_alafasy_001.wav",
            "Al-Baqara": "Mishary_alafasy_002.wav",
            "Al-Ikhlas": "Mishary_alafasy_003.wav"
        }
    },
    "Yasir Al-Dawsari": {
        "img": "yasir.png",
        "tracks": {
            "Al-Fatiha": "Yasir_001.wav",
            "Al-Baqara": "Yasir_002.wav",
            "Al-Kawthar": "Yasir_003.wav"
        }
    },
    "Saad Al-Ghamdi": {
        "img": "saad.png",
        "tracks": {
            "Al-Fatiha": "Saad_001.wav",
            "Al-Baqara": "Saad_002.wav",
            "Al-Asr": "Saad_003.wav"
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

def next_track():
    global current_track, selected_reciter
    tracks = list(RECITATORS[selected_reciter]["tracks"].values())
    if current_track in tracks:
        idx = tracks.index(current_track)
        idx = (idx + 1) % len(tracks)
        current_track = tracks[idx]
        play()

def set_volume(val):
    global player
    if player:
        player.audio_set_volume(int(val))

def on_sourate_select(event):
    global current_track
    sourate = sourate_var.get()
    current_track = RECITATORS[selected_reciter]["tracks"][sourate]
    status_label.config(text=f"Sélectionné : {sourate}")

# --- Navigation ---
def open_selection():
    frame_welcome.pack_forget()
    frame_player.pack_forget()
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
app.geometry("900x650")
app.resizable(False, False)

# --- Fond mosquée ---
bg_path = os.path.join(CACHE_DIR, "mosquee.png")
if os.path.exists(bg_path):
    bg_img = Image.open(bg_path).resize((900, 650))
    bg_tk = ImageTk.PhotoImage(bg_img)
    bg_label = tk.Label(app, image=bg_tk)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# --- Frame accueil ---
frame_welcome = tk.Frame(app, bg="#000000")  # overlay sombre
frame_welcome.pack(fill="both", expand=True)

# Logo Myamo
myamo_path = os.path.join(CACHE_DIR, "myamo.png")
if os.path.exists(myamo_path):
    logo_img = Image.open(myamo_path).resize((120, 120))
    logo_tk = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(frame_welcome, image=logo_tk, bg="#000000")
    logo_label.image = logo_tk
    logo_label.pack(pady=20)

welcome_label1 = tk.Label(frame_welcome, text="🌙 Bienvenue sur Myamo Radio Halal 🌙",
                          font=("Arial", 28, "bold"), fg="white", bg="#000000")
welcome_label1.pack(pady=10)

welcome_label2 = tk.Label(frame_welcome, text="Welcome to Myamo Halal Radio 🤙",
                          font=("Arial", 20, "italic"), fg="white", bg="#000000")
welcome_label2.pack(pady=10)

app.after(3000, open_selection)  # animation 3 sec

# --- Header permanent ---
header = tk.Frame(app, bg="#3e2723", height=60)
header.pack(fill="x")
header.pack_propagate(False)

if os.path.exists(myamo_path):
    logo_img2 = Image.open(myamo_path).resize((50, 50))
    logo_tk2 = ImageTk.PhotoImage(logo_img2)
    logo_label2 = tk.Label(header, image=logo_tk2, bg="#3e2723")
    logo_label2.image = logo_tk2
    logo_label2.pack(side="left", padx=10)

palestine_path = os.path.join(CACHE_DIR, "palestine.png")
if os.path.exists(palestine_path):
    pal_img = Image.open(palestine_path).resize((50, 30))
    pal_tk = ImageTk.PhotoImage(pal_img)
    pal_label = tk.Label(header, image=pal_tk, bg="#3e2723")
    pal_label.image = pal_tk
    pal_label.pack(side="right", padx=10)
    text_pal = tk.Label(header, text="Free Palestine", font=("Arial", 16, "bold"), fg="white", bg="#3e2723")
    text_pal.pack(side="right", padx=5)

# --- Frame sélection récitateurs ---
frame_selection = tk.Frame(app, bg="#5d4037")
title_sel = tk.Label(frame_selection, text="Choisissez un réciteur", font=("Arial", 22, "bold"), fg="white", bg="#5d4037")
title_sel.pack(pady=20)

reciters_frame = tk.Frame(frame_selection, bg="#5d4037")
reciters_frame.pack(pady=10)

for i, reciter in enumerate(RECITATORS.keys()):
    img_path = os.path.join(CACHE_DIR, RECITATORS[reciter]["img"])
    if os.path.exists(img_path):
        img = Image.open(img_path).resize((130, 130))
        img_tk = ImageTk.PhotoImage(img)
        btn = tk.Button(
            reciters_frame,
            image=img_tk,
            command=lambda r=reciter: open_player(r),
            bd=0, relief="flat",
            bg="#5d4037",
            activebackground="#3e2723"
        )
        btn.image = img_tk
        btn.grid(row=0, column=i, padx=15, pady=5)
        # Nom du réciteur sous la photo
        name_label = tk.Label(reciters_frame, text=reciter, fg="white", bg="#5d4037", font=("Arial", 12, "bold"))
        name_label.grid(row=1, column=i, pady=(0, 15))

# --- Frame lecteur ---
frame_player = tk.Frame(app, bg="#5d4037")

btn_back = tk.Button(frame_player, text="← Retour", command=open_selection, bg="#3e2723", fg="white")
btn_back.pack(anchor="nw", padx=10, pady=10)

status_label = tk.Label(frame_player, text="🎵 Prêt", font=("Arial", 14), fg="white", bg="#5d4037")
status_label.pack(pady=10)

# --- Combobox sourates stylée ---
style = ttk.Style()
style.theme_use('clam')
style.configure('TCombobox',
                fieldbackground='#3e2723',
                background='#3e2723',
                foreground='white',
                arrowcolor='white',
                borderwidth=0)
style.map('TCombobox',
          fieldbackground=[('readonly', '#3e2723')],
          background=[('readonly', '#3e2723')],
          foreground=[('readonly', 'white')])

sourate_var = tk.StringVar()
sourate_menu = ttk.Combobox(frame_player, textvariable=sourate_var, state="readonly", width=30, style='TCombobox')
sourate_menu.bind("<<ComboboxSelected>>", on_sourate_select)
sourate_menu.pack(pady=10)

# --- Contrôles ---
controls = tk.Frame(frame_player, bg="#5d4037")
controls.pack(pady=10)

btn_play = tk.Button(controls, text="▶ Play", command=play, width=10, bg="#4caf50", fg="white")
btn_play.grid(row=0, column=0, padx=10)

btn_stop = tk.Button(controls, text="⏹ Stop", command=stop, width=10, bg="#f44336", fg="white")
btn_stop.grid(row=0, column=1, padx=10)

btn_next = tk.Button(controls, text="⏭ Next", command=next_track, width=10, bg="#2196f3", fg="white")
btn_next.grid(row=0, column=2, padx=10)

# --- Slider volume modernisé ---
volume_frame = tk.Frame(frame_player, bg="#5d4037")
volume_frame.pack(pady=10)

volume_label = tk.Label(volume_frame, text="🔊 Volume", fg="white", bg="#5d4037", font=("Arial", 12, "bold"))
volume_label.pack(side="left", padx=5)

volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient="horizontal", command=set_volume,
                         bg="#5d4037", fg="white", troughcolor="#2196f3", highlightthickness=0, bd=0,
                         length=200)
volume_slider.set(70)
volume_slider.pack(side="left", padx=5)

# --- Lancement ---
app.mainloop()
