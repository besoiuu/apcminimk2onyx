# controller/led_feedback.py

from controller.led_memory import get_led_state
from controller.bank_manager import banca_curenta

COLOR_MAP = {
    "off": 0,
    "flash": 1,     # albastru puls
    "active": 21,   # verde solid
    "standby": 5,   # roșu
    "amber": 9,
    "purple": 13,
    "aqua": 45
}

def update_led(note, mode, midi_out_apc, is_pad=True):
    """
    Trimite un mesaj MIDI pentru a actualiza culoarea LED-ului.
    """
    velocity = COLOR_MAP.get(mode, 0)

    if is_pad and 0 <= note <= 63:
        # LED pe pad (canal 7 - 0x96)
        midi_out_apc.send_message([0x96, note, velocity])
    elif not is_pad and 112 <= note <= 119:
        # Soft keys Scene Launch (canal 0 - 0x90)
        midi_out_apc.send_message([0x90, note, 1 if velocity > 0 else 0])

def restore_leds_for_current_bank(midi_out_apc):
    """
    Restaurează toate LED-urile din banca curentă.
    """
    print(f"♻️ Restaurăm LED-urile pentru banca {banca_curenta}")
    for note in range(64):
        mode = get_led_state(banca_curenta, note)
        update_led(note, mode, midi_out_apc, is_pad=True)
