import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import json
import os
import pyautogui
import time

# Percorso del file di configurazione
config_file = "launcher_config.json"
server_id = "85568392932298269/101"

def load_config():
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    else:
        return {}

def save_config(config):
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
            time.sleep(10)
            
            # Simula l'interazione con l'interfaccia utente per connettersi al server
            connect_to_server(server_id)
            
            # Chiudi il launcher
            root.destroy()
        except Exception as e:
            messagebox.showerror("Errore", f"Non è stato possibile avviare il gioco: {e}")
    else:
        messagebox.showerror("Errore", "Percorso del gioco non valido. Per favore, seleziona il percorso corretto nelle impostazioni.")

def connect_to_server(server_id):
    # Simula i tasti per aprire il menu di connessione (modifica in base al gioco)
    pyautogui.press('esc')
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

root = tk.Tk()
root.title("Launcher Euro Truck Simulator 2")

launch_button = tk.Button(root, text="Avvia Gioco", command=launch_game)
launch_button.pack(pady=10)

settings_button = tk.Button(root, text="Impostazioni", command=open_settings)
settings_button.pack(pady=10)

update_button = tk.Button(root, text="Controlla Aggiornamenti", command=lambda: messagebox.showinfo("Aggiornamenti", "Nessun aggiornamento disponibile."))
update_button.pack(pady=10)

root.mainloop()