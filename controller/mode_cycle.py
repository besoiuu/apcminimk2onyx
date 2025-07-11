# controller/mode_cycle.py

# Memorăm ultima stare pe fiecare note
mode_cycle_per_note = {}

# Ordinea în care ciclăm modurile
mode_order = ["flash", "amber", "aqua", "purple", "off"]

def next_mode(note):
    current_index = mode_cycle_per_note.get(note, -1)
    new_index = (current_index + 1) % len(mode_order)
    mode_cycle_per_note[note] = new_index
    return mode_order[new_index]
