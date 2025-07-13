# controller/mode_cycle.py

# Memorăm ultima stare pe fiecare note
mode_cycle_per_note = {}

# Ordinea în care ciclăm modurile
# În Keyboard Mode: Ciclăm între mov (flash), galben (yellow) și verde (green)
# În Busk Mode: Ciclăm între verde (green) și roșu (standby)
mode_order_keyboard = ["flash", "yellow", "green", "off"]
mode_order_busk = ["green", "standby", "off"]

def next_mode(note, keyboard_mode):
    if keyboard_mode:
        # În Keyboard Mode, ciclăm între mov (flash), galben (yellow), și verde (green)
        current_index = mode_cycle_per_note.get(note, -1)
        new_index = (current_index + 1) % len(mode_order_keyboard)
        mode_cycle_per_note[note] = new_index
        return mode_order_keyboard[new_index]
    else:
        # În Busk Mode, doar verde (green) pentru "active" și roșu (standby) pentru "standby"
        if mode_cycle_per_note.get(note, "off") == "off":
            mode_cycle_per_note[note] = "active"
            return "active"
        elif mode_cycle_per_note.get(note) == "active":
            mode_cycle_per_note[note] = "standby"
            return "standby"
        else:
            mode_cycle_per_note[note] = "off"
            return "off"
