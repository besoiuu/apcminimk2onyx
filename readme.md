# apcminimk2onyx

Integrare completă între controller-ul MIDI **Akai APC Mini MK2** și software-ul de control lumini **Obsidian Onyx** folosind protocoale MIDI și OSC.

---

## Descriere

Acest proiect este dedicat inginerilor și operatorilor de lumini care doresc să folosească Akai APC Mini MK2 ca interfață hardware pentru controlul direct al consolei de lumini Obsidian Onyx. Prin interpretarea mesajelor MIDI de la controller și trimiterea lor în format OSC către Onyx, proiectul permite controlul în timp real al fadere-lor, pad-urilor, butoanelor speciale (blackout, schimbare bancă), precum și feedback vizual pe controller prin LED-uri.

---

## Funcționalități implementate

### 1. Gestionare completă a mesajelor MIDI de la Akai APC Mini MK2

- Recepționarea și interpretarea mesajelor **Note On/Off** pentru pad-uri și butoane
- Recepționarea și interpretarea mesajelor **Control Change (CC)** pentru fadere (CC 48-56 corespunzător fadere 1-9)

### 2. Control feedback LED pe controller

- Actualizarea LED-urilor pad-urilor în funcție de starea lor internă (standby, activ, flash)
- Control simplu al LED-urilor butoanelor speciale (ex. blackout ON/OFF)
- Sincronizarea LED-urilor cu schimbările de bancă și stările fade-lor

### 3. Control OSC către Obsidian Onyx

- Trimiterea mesajelor OSC conform protocolului oficial Onyx pentru:
  - Setarea nivelului fadere-lor (`/Mx/fader/<id>`) cu valori scalate 0-255
  - Activarea/dezactivarea blackout-ului (`/Mx/fader/2202`)
  - Schimbarea bancilor de playback prin comenzi `/Mx/button/442x/up/down`

### 4. Schimbare dinamică a bancilor pe controller și pe Onyx

- Butoane dedicate pentru incrementarea/decrementarea bancilor pe controller
- Actualizarea corespunzătoare a feedback-ului vizual și a OSC-ului pentru bancă

### 5. Mod Shift și alte funcții speciale

- Implementarea unui buton Shift pentru extinderea funcționalităților
- Gestionarea stării blackout prin două butoane dedicate
- Alte facilități de management intern al stării

### 6. Structură modulară și clară a codului

- `onyx_handler.py` — clasa pentru comunicare OSC către Onyx
- `fader_handler.py` — handler pentru fadere
- `apc_handler.py` — handler pentru pad-uri, butoane și funcții speciale
- `event_dispatcher.py` — dispatcher-ul mesajelor MIDI către handler-ele corespunzătoare
- `main.py` — scriptul principal pentru inițializarea porturilor și pornirea ascultării MIDI

---

## Structura proiectului

```bash
apcminimk2onyx/
├── controller/
│   ├── apc_handler.py        # Gestionează logica de procesare a pad-urilor și butoanelor de pe controller-ul Akai APC Mini MK2.
│   ├── fader_handler.py      # Gestionează interpretarea mesajelor MIDI CC pentru fadere și transmiterea valorilor către Obsidian Onyx.
│   ├── onyx_handler.py       # Implementarea clasei client OSC pentru comunicarea și controlul consolei Obsidian Onyx.
│   ├── bank_manager.py       # Gestionarea internă a stării și schimbărilor bancilor de playback (incrementare, decrementare, starea curentă).
│   ├── led_memory.py         # Stocarea și gestionarea stărilor LED-urilor de pe controller pentru sincronizarea feedback-ului vizual.
│   ├── mode_cycle.py         # Logica pentru ciclul și modificarea modurilor LED-urilor, inclusiv animații sau schimbări de stare ciclice.
├── midi/
│   ├── listener.py           # Clasa responsabilă pentru ascultarea porturilor MIDI și recepționarea mesajelor hardware.
│   ├── ports.py              # Configurarea și managementul porturilor MIDI de input și output utilizate în aplicație.
├── event_dispatcher.py       # Dispatcher-ul principal care primește mesajele MIDI și le direcționează către handler-ele corespunzătoare (pad-uri, fadere).
├── main.py                   # Scriptul principal de inițializare și rulare a aplicației, configurează porturile MIDI și pornește ascultarea.
├── requirements.txt          # Lista dependențelor Python necesare pentru rularea corectă a proiectului.
└── README.md                 # Documentația proiectului, descriere, instrucțiuni de instalare și utilizare.

```

---

## Instalare

1. Clonează repository-ul:

```bash
git clone https://github.com/besoiuu/apcminimk2onyx.git
cd apcminimk2onyx
```

2. Instalează dependențele:

---

```bash
pip install -r requirements.txt
```

3. Configurează porturile MIDI în main.py conform configurației sistemului tău (listă porturi MIDI disponibile).

4. Asigură-te că IP-ul și portul pentru OnyxOSCClient corespund setărilor Onyx-ului tău (implicit 10.0.0.100:8000).

## Utilizare

Rulează scriptul principal:

```bash
python main.py
```

## Cerințe

Python 3.7+

python-rtmidi

python-osc

Controller Akai APC Mini MK2 conectat la PC

Obsidian Onyx configurat pentru a primi mesaje OSC pe portul configurat

## Dezvoltare și contribuții

Codul este structurat modular pentru a facilita extinderea și modificarea

Sunt binevenite sugestiile și pull request-urile pentru adăugarea de funcționalități noi sau corectarea bug-urilor

Pentru orice problemă deschide un issue în repository

## Autor

besoiuu

## Licență

MIT License
