# controller/apc_handler.py

from controller.bank_manager import banca_curenta, increment_bank, decrement_bank
from controller.led_memory import get_led_state, set_led_state, clear_led_state
from controller.onyx_handler import OnyxOSCClient

# Inițializează clientul OSC pentru Onyx (IP și port să fie corecte)
osc_client = OnyxOSCClient(ip="10.0.0.100", port=8000)

COLOR_MAP = {
    "off": 0,
    "standby": 5,    # roșu (implicit)
    "active": 48,    # verde
    "flash": 1       # albastru puls
}

def update_led(note, mode, midi_out_apc, is_pad=True):
    """
    Trimite mesaj MIDI pentru a actualiza culoarea LED-ului pe controller.
    """
    velocity = COLOR_MAP.get(mode, 0)
    if is_pad and 0 <= note <= 63:
        # Pad-uri pe canal 0x90
        midi_out_apc.send_message([0x90, note, velocity])
    elif not is_pad and 112 <= note <= 119:
        # Softkeys (Scene Launch) - simplu ON/OFF
        midi_out_apc.send_message([0x90, note, 1 if velocity > 0 else 0])

def restore_red_leds_for_bank(midi_out_apc, banca_curenta, get_led_state, set_led_state, update_led_func):
    """
    Aprinde LED-urile roșii (standby) pe pad-urile care sunt inactive sau necunoscute.
    """
    for note in range(64):
        mode = get_led_state(banca_curenta, note)
        if mode not in ("standby", "active"):
            mode = "standby"
            set_led_state(banca_curenta, note, mode)
        update_led_func(note, mode, midi_out_apc)

def handle_pad_press(note, velocity, midi_out_apc, midi_out_onyx,
                     shift_pressed=False, blackout_state=False):
    """
    Gestionează apăsările pe pad-uri și butoane, cu integrare MIDI și OSC.
    """
    if velocity == 0:
        return  # ignoră mesajele Note Off

    BLACKOUT_ON_NOTE = 118
    BLACKOUT_OFF_NOTE = 119
    BANK_UP_NOTE = 0x75    # Scene Launch 6
    BANK_DOWN_NOTE = 0x74  # Scene Launch 5

    # Control schimbare bancă
    if note == BANK_DOWN_NOTE and velocity > 0:
        print("⬅️ Bancă -")
        decrement_bank()
        osc_client.select_bank(banca_curenta)
        restore_red_leds_for_bank(midi_out_apc, banca_curenta, get_led_state, set_led_state, update_led)
        return

    if note == BANK_UP_NOTE and velocity > 0:
        print("➡️ Bancă +")
        increment_bank()
        osc_client.select_bank(banca_curenta)
        restore_red_leds_for_bank(midi_out_apc, banca_curenta, get_led_state, set_led_state, update_led)
        return

    # Blackout ON
    if note == BLACKOUT_ON_NOTE and velocity > 0:
        print("⬛ Blackout ON")
        osc_client.blackout(True)
        update_led(BLACKOUT_ON_NOTE, "red", midi_out_apc, is_pad=False)
        handle_pad_press.blackout_state = True
        return

    # Blackout OFF
    if note == BLACKOUT_OFF_NOTE and velocity > 0:
        print("⬜ Blackout OFF")
        osc_client.blackout(False)
        update_led(BLACKOUT_ON_NOTE, "off", midi_out_apc, is_pad=False)
        handle_pad_press.blackout_state = False
        return

    # Toggle LED pe pad-uri 0–63
    if 0 <= note <= 63:
        note_real = note + (banca_curenta * 64)
        current_mode = get_led_state(banca_curenta, note_real)
        next_mode = "standby" if current_mode == "active" else "active"

        midi_out_onyx.send_message([0x90, note_real, velocity])  # Trimite nota reală către Onyx (dacă e nevoie)
        update_led(note, next_mode, midi_out_apc, is_pad=True)
        set_led_state(banca_curenta, note_real, next_mode)

        print(f"Pad {note_real}: {current_mode} -> {next_mode}")
        return

    # Alte comenzi ignorate
    return
