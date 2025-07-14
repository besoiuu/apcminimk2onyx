# led_memory.py
# ===============================
# Control iluminare LED-uri Akai APC Mini MK2 cu velocity conform AKAI Protocol
# ===============================

led_states = {}

def set_led_state(banca, note, mode):
    if banca not in led_states:
        led_states[banca] = {}
    led_states[banca][note] = mode

def get_led_state(banca, note):
    return led_states.get(banca, {}).get(note, "off")

def clear_led_state(banca):
    led_states[banca] = {}

def update_led(note, mode, midi_out_apc):
    color_map = {
        "off": 0x00,
        "amber": 0x09,    # Orange/galben (amber/orange)
        "green": 0x21,    # Verde NORMAL AKAI #00FF00
        "blue": 0x29,     # Albastru AKAI
        "red": 0x05,      # Roșu AKAI
        "white": 0x03,
    }
    velocity = color_map.get(mode, 0x00)
    status = 0x96 if note < 64 else 0x90
    midi_out_apc.send_message([status, note, velocity])
    # print(f"[DEBUG] RGB LED → Note {note}, Velocity {velocity} ({mode})")

