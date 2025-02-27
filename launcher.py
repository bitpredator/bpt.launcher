import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import json
import os
import time
import requests
from packaging import version
import pyautogui
import psutil
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import uuid
import hashlib

# Percorso del file di configurazione
config_file = "config/launcher_config.json"
current_version = "1.0.4"  # Versione corrente del launcher
repo_url = "https://api.github.com/repos/bitpredator/bpt.launcher/releases/latest"  # URL API GitHub per l'ultima release

def load_config():
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
            return config
    else:
        return {}

def save_config(config):
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    with open(config_file, "w") as f:
        json.dump(config, f)

def is_steam_running():
    """Controlla se Steam è in esecuzione."""
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'steam.exe':
            return True
    return False

def update_convoy_size():
    config_path = os.path.join(os.path.expanduser("~"), "Documents", "Euro Truck Simulator 2", "config.cfg")
    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            lines = file.readlines()
        
        with open(config_path, "w") as file:
            for line in lines:
                if 'uset g_max_convoy_size' in line:
                    file.write('uset g_max_convoy_size "128"\n')
                else:
                    file.write(line)
    else:
        messagebox.showerror("Errore", f"File config.cfg non trovato: {config_path}")

def launch_game():
    if not is_steam_running():
        messagebox.showerror("Errore", "Steam non è avviato. Per favore, avvia Steam prima di avviare il gioco.")
        return

    config = load_config()
    game_path = config.get("game_path")

    if game_path and os.path.exists(game_path):
        try:
            # Aggiorna il parametro del convoglio
            update_convoy_size()
            
            # Avvia il gioco con DirectX 11
            subprocess.Popen([game_path, "-dx11"])
            
            # Attendi che il gioco si avvii (regola il tempo di attesa in base alle tue esigenze)
            time.sleep(30)  # Aumenta il tempo di attesa se necessario
            
            # Chiudi il launcher
            root.destroy()
        except Exception as e:
            messagebox.showerror("Errore", f"Non è stato possibile avviare il gioco: {e}")
    else:
        messagebox.showerror("Errore", "Percorso del gioco non valido. Per favore, seleziona il percorso corretto nelle impostazioni.")

def open_settings():
    def save_settings():
        game_path = path_entry.get()
        if os.path.exists(game_path):
            config = load_config()
            config["game_path"] = game_path
            save_config(config)
            settings_window.destroy()
        else:
            messagebox.showerror("Errore", "Il percorso selezionato non esiste.")

    settings_window = tk.Toplevel(root)
    settings_window.title("Impostazioni")

    tk.Label(settings_window, text="Percorso del gioco:").pack(pady=5)
    path_entry = tk.Entry(settings_window, width=50)
    path_entry.pack(pady=5)

    browse_button = tk.Button(settings_window, text="Sfoglia", command=lambda: path_entry.insert(0, filedialog.askopenfilename()))
    browse_button.pack(pady=5)

    save_button = tk.Button(settings_window, text="Salva", command=save_settings)
    save_button.pack(pady=10)

def check_for_updates():
    try:
        response = requests.get(repo_url)
        response.raise_for_status()
        latest_release = response.json()
        latest_version = latest_release["tag_name"]
        if version.parse(latest_version) > version.parse(current_version):
            download_url = latest_release["assets"][0]["browser_download_url"]
            if messagebox.askyesno("Aggiornamento Disponibile", f"È disponibile una nuova versione ({latest_version}). Vuoi aggiornare?"):
                download_and_install_update(download_url)
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante il controllo degli aggiornamenti: {e}")

def download_and_install_update(download_url):
    try:
        # Rimuovi la versione obsoleta se esiste
        if os.path.exists("launcher.exe"):
            os.remove("launcher.exe")
        
        # Scarica la nuova versione
        response = requests.get(download_url)
        response.raise_for_status()
        with open("launcher.exe", "wb") as f:
            f.write(response.content)
        
        # Verifica se il file scaricato è compatibile
        if not is_compatible_executable("launcher.exe"):
            messagebox.showerror("Errore", "Il file launcher.exe scaricato non è compatibile con il sistema operativo a 64 bit.")
            return
        
        # Avvia l'installazione della nuova versione
        subprocess.Popen(["launcher.exe"])
        root.destroy()
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante il download dell'aggiornamento: {e}")

def is_compatible_executable(file_path):
    # Funzione di esempio per verificare la compatibilità del file eseguibile
    # Nota: Questa funzione è solo un esempio e potrebbe non funzionare correttamente per tutti i file eseguibili
    try:
        with open(file_path, "rb") as f:
            header = f.read(2)
            return header == b'MZ'  # Controlla se il file è un eseguibile Windows
    except Exception:
        return False

def send_discord_message(username):
    """Invia un messaggio al webhook di Discord con l'username."""
    data = {
        "content": f"Camionista {username} ha effettuato la connessione."
    }
    response = requests.post(discord_webhook_url, json=data)
    if response.status_code != 204:
        messagebox.showerror("Errore", "Non è stato possibile inviare il messaggio al webhook di Discord.")

def hash_password(password):
    """Restituisce l'hash SHA-256 della password."""
    return hashlib.sha256(password.encode()).hexdigest()

def center_window(window, width=300, height=300):
    """Centra la finestra sullo schermo."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def set_initial_credentials():
    """Imposta il nickname e la password al primo avvio."""
    config = load_config()
    if "username" in config and "password" in config:
        return

    def save_credentials():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            config["username"] = username
            config["password"] = hash_password(password)
            save_config(config)
            credentials_window.destroy()
            prompt_username()
        else:
            messagebox.showerror("Errore", "Entrambi i campi sono obbligatori.")

    credentials_window = tk.Toplevel(root)
    credentials_window.title("Imposta Credenziali")
    center_window(credentials_window, 300, 300)
    credentials_window.resizable(False, False)

    tk.Label(credentials_window, text="Imposta il tuo nickname e password:").pack(pady=10)
    tk.Label(credentials_window, text="Nickname:").pack(pady=5)
    username_entry = tk.Entry(credentials_window, width=30)
    username_entry.pack(pady=5)
    tk.Label(credentials_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(credentials_window, width=30, show="*")
    password_entry.pack(pady=5)

    save_button = tk.Button(credentials_window, text="Salva", command=save_credentials)
    save_button.pack(pady=10)

def prompt_username():
    config = load_config()
    if "username" not in config or "password" not in config:
        set_initial_credentials()
        return

    def check_credentials():
        username = username_entry.get()
        password = password_entry.get()
        if username == config["username"] and hash_password(password) == config["password"]:
            send_discord_message(username)
            login_window.destroy()
            launch_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Errore", "Nome utente o password errati. Riprova.")

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    center_window(login_window, 300, 300)
    login_window.resizable(False, False)

    tk.Label(login_window, text="Inserisci nome utente e password:").pack(pady=10)
    tk.Label(login_window, text="Nome utente:").pack(pady=5)
    username_entry = tk.Entry(login_window, width=30)
    username_entry.pack(pady=5)
    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, width=30, show="*")
    password_entry.pack(pady=5)

    check_button = tk.Button(login_window, text="Verifica", command=check_credentials)
    check_button.pack(pady=10)

# Crea la finestra principale
root = tk.Tk()
root.title("Launcher Euro Truck Simulator 2")
root.geometry('800x600')  # Imposta la finestra a 800x600 pixel
root.resizable(False, False)  # Blocca il ridimensionamento della finestra

# Carica l'immagine di sfondo
background_image_path = os.path.join(os.path.dirname(__file__), "img", "background.png")
if os.path.exists(background_image_path):
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((800, 600), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
else:
    messagebox.showerror("Errore", f"Immagine di sfondo non trovata: {background_image_path}")
    root.destroy()

# Crea un canvas e aggiungi l'immagine di sfondo
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Imposta l'icona personalizzata
try:
    root.iconbitmap(os.path.join(os.path.dirname(__file__), "img", "ico.ico"))
except tk.TclError:
    print("Icon file not found, using default icon.")

# Aggiungi i pulsanti al canvas
launch_button = tk.Button(root, text="Avvia Gioco", command=launch_game, state=tk.DISABLED)
canvas.create_window(400, 200, window=launch_button)  # Posiziona il pulsante al centro

settings_button = tk.Button(root, text="Impostazioni", command=open_settings)
canvas.create_window(400, 300, window=settings_button)  # Posiziona il pulsante al centro

update_button = tk.Button(root, text="Controlla Aggiornamenti", command=check_for_updates)
canvas.create_window(400, 400, window=update_button)  # Posiziona il pulsante al centro

# Prompt per il nome utente
root.after(100, prompt_username)

root.mainloop()