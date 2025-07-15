# controller/mode_cycle.py

# --- Stări memorate pentru fiecare tip de ciclare și note ------------------
mode_cycle_per_note = {}
track_mode_cycle_per_note = {}

# --- Ordinea modurilor existente (Keyboard / Busk) -----------------------
mode_order_keyboard = ["flash", "yellow", "green", "off"]
mode_order_busk    = ["green", "standby", "off"]

# --- Ordinea celor 8 moduri dinamice de lumină --------------------------
track_mode_order = [
    "rainbow_breath",   # 1
    "expanding_square", # 2
    "ripple",           # 3
    "snake_game",       # 4
    "sparkle",          # 5
    "fireworks",        # 6
    "theater_chase",    # 7
    "off"               # 8
]


def next_mode(note, keyboard_mode):
    """
    Ciclare a modurilor pentru PAD-uri:
    - În Keyboard Mode: flash (mov), yellow (galben), green (verde), off
    - În Busk Mode: green (active), standby (roșu), off

    Returnează numele modului următor pentru `note`.
    """
    if keyboard_mode:
        current_index = mode_cycle_per_note.get(note, -1)
        new_index = (current_index + 1) % len(mode_order_keyboard)
        mode_cycle_per_note[note] = new_index
        return mode_order_keyboard[new_index]
    else:
        state = mode_cycle_per_note.get(note, "off")
        if state == "off":
            mode_cycle_per_note[note] = "green"
            return "green"
        elif state == "green":
            mode_cycle_per_note[note] = "standby"
            return "standby"
        else:
            mode_cycle_per_note[note] = "off"
            return "off"


def next_track_mode(note):
    """
    Ciclare a celor 8 moduri dinamice de iluminare (track buttons):
    rainbow_breath → expanding_square → ripple → snake_game → sparkle → fireworks → theater_chase → off

    Returnează numele modului următor pentru `note`.
    """
    current = track_mode_cycle_per_note.get(note, -1)
    new = (current + 1) % len(track_mode_order)
    track_mode_cycle_per_note[note] = new
    return track_mode_order[new]
