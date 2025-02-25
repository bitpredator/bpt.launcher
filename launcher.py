import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import json
import os
import time
import requests
from packaging import version
import pyautogui

# Percorso del file di configurazione
config_file = "config/launcher_config.json"
current_version = "1.0.2"  # Versione corrente del launcher
repo_url = "https://api.github.com/repos/bitpredator/bpt.launcher/releases/latest"  # URL API GitHub per l'ultima release
server_id = "85568392932298269/101"  # ID del server

def load_config():
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    else:
        return {}

def save_config(config):
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    with open(config_file, "w") as f:
        json.dump(config, f)

def launch_game():
    config = load_config()
    game_path = config.get("game_path")
    if game_path and os.path.exists(game_path):
        try:
            # Avvia il gioco con DirectX 11
            subprocess.Popen([game_path, "-dx11"])
            
            # Attendi che il gioco si avvii (regola il tempo di attesa in base alle tue esigenze)
            time.sleep(30)  # Aumenta il tempo di attesa se necessario
            
            # Simula l'interazione con l'interfaccia utente per cercare il server
            search_server(server_id)
            
            # Chiudi il launcher
            root.destroy()
        except Exception as e:
            messagebox.showerror("Errore", f"Non è stato possibile avviare il gioco: {e}")
    else:
        messagebox.showerror("Errore", "Percorso del gioco non valido. Per favore, seleziona il percorso corretto nelle impostazioni.")

def search_server(server_id):
    # Simula i tasti per aprire il menu di connessione (modifica in base al gioco)
    pyautogui.press('-')
    time.sleep(1)
    
    # Simula la digitazione dell'ID del server
    pyautogui.typewrite(server_id)
    time.sleep(1)
    
    # Simula il tasto Invio per confermare la connessione
    pyautogui.press('enter')

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
        if os.path.exists("update.exe"):
            os.remove("update.exe")
        
        # Scarica la nuova versione
        response = requests.get(download_url)
        response.raise_for_status()
        with open("update.exe", "wb") as f:
            f.write(response.content)
        
        # Avvia l'installazione della nuova versione
        subprocess.Popen(["update.exe"])
        root.destroy()
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante il download dell'aggiornamento: {e}")

root = tk.Tk()
root.title("Launcher Euro Truck Simulator 2")

# Imposta l'icona personalizzata
try:
    root.iconbitmap("img/ico.ico")
except tk.TclError:
    print("Icon file not found, using default icon.")

launch_button = tk.Button(root, text="Avvia Gioco", command=launch_game)
launch_button.pack(pady=10)

settings_button = tk.Button(root, text="Impostazioni", command=open_settings)
settings_button.pack(pady=10)

update_button = tk.Button(root, text="Controlla Aggiornamenti", command=check_for_updates)
update_button.pack(pady=10)

root.mainloop()