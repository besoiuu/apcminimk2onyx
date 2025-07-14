# onyx_handler.py
# ===============================
# Client OSC pentru comunicarea cu Obsidian Onyx
# Permite trimiterea de comenzi către fader-e, blackout și schimbare de bank.
# ===============================

from pythonosc import udp_client
import time

class OnyxOSCClient:
    def __init__(self, ip="10.0.0.100", port=8000):
        """
        Inițializează clientul OSC care trimite mesaje către Onyx.

        Args:
            ip (str): Adresa IP a PC-ului cu Onyx (default: 10.0.0.100).
            port (int): Portul OSC setat în Onyx (default: 8000).
        """
        self.client = udp_client.SimpleUDPClient(ip, port)
        print(f"[OSC] Client inițializat pentru {ip}:{port}")

    def blackout(self, enable=True):
        """
        Activează sau dezactivează blackout-ul general din Onyx.

        Args:
            enable (bool): True → blackout ON (valoare 255.0), False → OFF (0.0)
        """
        value = 255.0 if enable else 0.0
        # print(f"[OSC] Trimit blackout {'ON' if enable else 'OFF'} → valoare: {value}")
        self.client.send_message("/Mx/fader/2202", value)

    def set_playback_fader(self, playback_id, level):
        """
        Trimite valoarea unui fader playback specific către Onyx.

        Args:
            playback_id (int): Număr între 1–9, corespunzător unui fader de playback.
            level (int): Nivelul faderului (0–255). Se scalează extern din MIDI [0–127].

        Exemple adresă OSC:
            /Mx/fader/4203 (pentru playback_id=1)
            /Mx/fader/4213 (pentru playback_id=2)
        """
        if not (1 <= playback_id <= 9):
            raise ValueError("Playback ID trebuie să fie între 1 și 9")
        if not (0 <= level <= 255):
            raise ValueError("Level trebuie să fie între 0 și 255")

        address = f"/Mx/fader/{4200 + (playback_id - 1) * 10 + 3}"
        # print(f"[OSC] Set playback {playback_id} → nivel {level} → {address}")
        self.client.send_message(address, float(level))

    def select_bank(self, bank_index):
        """
        Trimite o comandă OSC pentru a selecta banca de playback curentă în Onyx.

        Args:
            bank_index (int): Valori acceptate 1–9 (coincide cu butoanele /Mx/button/442X/up/down)
        """
        if not (1 <= bank_index <= 9):
            raise ValueError("Bank index trebuie să fie între 1 și 9")

        address = f"/Mx/button/442{bank_index}/up/down"
        # print(f"[OSC] Selectare bancă playback: {bank_index} → {address}")
        self.client.send_message(address, 1)
        time.sleep(0.1)
        self.client.send_message(address, 0)
