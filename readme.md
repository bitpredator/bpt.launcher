1. Per installare tutte le dipendenze richieste dal tuo progetto apri il terminale integrato in Visual Studio Code (puoi farlo premendo `Ctrl + ` o andando su `Visualizza > Terminale`).

2. Esegui il seguente comando per installare tutte le dipendenze elencate nel file `requirements.txt`:

```bash
pip install -r requirements.txt
```

Questo comando installerà tutte le librerie specificate nel file `requirements.txt`.

Se `tkinter` non viene installato tramite `pip`, è perché è una libreria standard di Python e dovrebbe essere già inclusa nella tua installazione di Python. Se non è presente, potrebbe essere necessario installare un pacchetto specifico per il tuo sistema operativo.

Dopo aver eseguito questi passaggi, tutte le dipendenze richieste dovrebbero essere installate e il tuo progetto dovrebbe funzionare correttamente.

pyinstaller --onefile --windowed --icon=img/ico.ico launcher.py