# controller/led_memory.py

# Memorie LED-uri: {banca: {note: mode (ex: "active", "flash", "yellow", "green", "off")}}
led_states = {}


def set_led_state(banca, note, mode):
    """
    Setează starea LED-ului pentru o bancă și o notă specifică.
    """
    if banca not in led_states:
        led_states[banca] = {}
    led_states[banca][note] = mode


def get_led_state(banca, note):
    """
    Obține starea LED-ului pentru o bancă și o notă specifică.
    """
    return led_states.get(banca, {}).get(note, "off")


def clear_led_state(banca):
    """
    Resetează toate LED-urile pentru o anumită bancă.
    """
    led_states[banca] = {}
