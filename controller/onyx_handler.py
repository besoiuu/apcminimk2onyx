from pythonosc import udp_client

class OnyxOSCClient:
    def __init__(self, ip="10.0.0.100", port=8000):
        self.client = udp_client.SimpleUDPClient(ip, port)
        print(f"OSC client initialized for {ip}:{port}")

    def blackout(self, enable=True):
        # conform documentatiei Onyx, ipotetic /blackout cu param 1 sau 0
        value = 1 if enable else 0
        print(f"Sending blackout {'ON' if enable else 'OFF'}")
        self.client.send_message("/blackout", value)

    def select_bank(self, bank_index):
        # ipotetic mesaj OSC pentru schimbare bank
        print(f"Selecting bank {bank_index}")
        self.client.send_message("/bank/select", bank_index)

    def playback_toggle(self, playback_id, enable=True):
        # ipotetic toggle pentru un playback
        value = 1 if enable else 0
        print(f"Toggling playback {playback_id} {'ON' if enable else 'OFF'}")
        self.client.send_message(f"/playback/{playback_id}/go", value)

# Test simplu
if __name__ == "__main__":
    onyx = OnyxOSCClient(ip="10.0.0.100", port=8000)  # ajustează IP-ul și portul Onyx

    onyx.blackout(True)       # pornește blackout
    onyx.select_bank(2)       # selectează banca 2
    onyx.playback_toggle(1)   # activează playback 1
