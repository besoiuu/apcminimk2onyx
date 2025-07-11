# Memorie LED-uri: {banca: {note: mode (ex: "active", "flash", ...)}}
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
        "off": 0,
        "flash": 1,      # Albastru intermitent
        "active": 48,    # Verde
        "standby": 5,    # Roșu
        "red": 5,
        "amber": 9,
        "aqua": 25,
        "purple": 13,
        "green": 48,
        "blue": 41,
        "white": 3,
        "pink": 20
    }
    velocity = color_map.get(mode, 0)
    midi_out_apc.send_message([0x90, note, velocity])

