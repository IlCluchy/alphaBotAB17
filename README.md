# AlphaBot17

Come inziare a controllare e progettare un AlphaBot tramite **Raspberry Pi**

## Requisiti:
**Hardware:**
- AlphaBot (con motori, sensori, e scheda base)
- batterie per alimentazione
- scheda micro SD

**Software:**
- Raspberry Pi OS
- Python 3

## Connessione SSH
Per stabilire una connessione SSH tra un AlphaBot e un computer è necessario che entrambi siano connessi alla stessa rete Wi-Fi. 

Nel nostro caso:

SSID -> AI-FAI-4AROB 2.4GHz

Volendo è possibile usare Putty altrimenti da riga di comando:

### Linux
```shell
computer@utente:~$ ssh pi@AB17.local
pi@ab17.local's password:
pi@AB17:~ $ 
```

### Windows
```shell
C:\Users\Utente> ssh pi@AB17.local
pi@ab17.local's password:
pi@AB17:~ $
```

Stabilita la connessione è possibile visionere la struttare della directory

## Primi programmi
Per iniziare a far muovere un Alphabot si può utilizzare la libreria [Alphabot.py](./libreries/Alphabot.py).

Ecco un esempio di codice Python che faccia andare avanti l'Alphabot [forward.py](forward.py).

Per caricare il programma sull'Alphabot basta eseguirlo con python nella connessione SSH:
```shell
pi@AB17:~ $ python3 forward.py
```
## WinSCP
Uno strumento che può essere utile allo sviluppo di codice per Alèphabot è **WinSCP** che consente di spostare dei file dal PC locale alla SSD dell'Alphabot. Questo consente di utilizzare un editor di testo [VSC, Sublime] al posto di nano.

### Installazione di WinSCP
## Linux

WinSCP non è disponibile nativamente per Linux, ma puoi usarlo tramite **Wine** o installare un’alternativa compatibile come **FileZilla**.

**Wine**
```bash
sudo apt update
sudo apt install wine
wget https://winscp.net/download/WinSCP-6.3.4-Setup.exe
wine WinSCP-6.3.4-Setup.exe
```
## Windows

1. Vai al sito ufficiale: [https://winscp.net/eng/download.php](https://winscp.net/eng/download.php)
2. Clicca su **Download WinSCP Installer**.
3. Esegui il file `.exe` scaricato e segui le istruzioni di installazione.
4. Avvia WinSCP dal menu Start.

