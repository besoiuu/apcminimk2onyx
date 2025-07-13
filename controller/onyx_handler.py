from pythonosc import udp_client
import time


class OnyxOSCClient:
    def __init__(self, ip="10.0.0.100", port=8000):
        self.client = udp_client.SimpleUDPClient(ip, port)
        print(f"OSC client initialized for {ip}:{port}")

    def blackout(self, enable=True):
        value = 255.0 if enable else 0.0
        print(f"Sending blackout {'ON' if enable else 'OFF'} with value {value}")
        self.client.send_message("/Mx/fader/2202", value)

    def set_playback_fader(self, playback_id, level):
        if not (1 <= playback_id <= 9):
            raise ValueError("Playback id trebuie să fie între 1 și 9")
        if not (0 <= level <= 255):
            raise ValueError("Level trebuie să fie între 0 și 255")
        address = f"/Mx/fader/{4200 + (playback_id - 1) * 10 + 3}"
        print(f"Setare fader playback {playback_id} la nivel {level}")
        self.client.send_message(address, float(level))

    def select_bank(self, bank_index):
        if not 1 <= bank_index <= 9:
            raise ValueError("Bank index trebuie să fie între 1 și 9")
        address = f"/Mx/button/442{bank_index}/up/down"
        print(f"Selectare playback bank {bank_index}")
        self.client.send_message(address, 1)
        time.sleep(0.1)
        self.client.send_message(address, 0)
