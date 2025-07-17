from controller.bank_manager import banca_curenta, increment_bank, decrement_bank
from controller.led_memory import update_led
from controller.onyx_handler import OnyxOSCClient

# OSC client pentru comenzi la Onyx
osc_client = OnyxOSCClient(ip="10.0.0.100", port=8000)

# Note speciale de la APC
SHIFT_NOTE       = 0x7A
BLACKOUT_ON_NOTE = 118
BLACKOUT_OFF_NOTE= 119
BANK_UP_NOTE     = 0x75
BANK_DOWN_NOTE   = 0x74

# Starea LED-urilor pentru pad-urile Busk (0–63)
busk_led_state = {}

def clear_busk_grid(midi_out_apc):
    """
    Resetează toate pad-urile Busk (0–63) la starea "off".
    """
    for pad in range(64):
        busk_led_state[pad] = "off"
        update_led(pad, "off", midi_out_apc)


def handle_pad_press(
    note,
    velocity,
    midi_out_apc,
    midi_out_onyx,
    shift_pressed=False,
    blackout_state=False,
):
    """
    Busk Mode: toggle GO/RELEASE pe grid (0–63) și tratează butoane speciale.
    """
    # Ignoră evenimente de release
    if velocity == 0:
        return

    # Navigare bancă
    if note == BANK_DOWN_NOTE:
        decrement_bank()
        # select_bank așteaptă index 1-based
        osc_client.select_bank(banca_curenta + 1)
        clear_busk_grid(midi_out_apc)
        print(f"🔻 Bank - noua bancă: {banca_curenta}")
        return

    if note == BANK_UP_NOTE:
        increment_bank()
        osc_client.select_bank(banca_curenta + 1)
        clear_busk_grid(midi_out_apc)
        print(f"🔺 Bank + noua bancă: {banca_curenta}")
        return

    # Control blackout Onyx
    if note == BLACKOUT_ON_NOTE:
        osc_client.blackout(True)
        print("🕶️ Blackout ON")
        update_led(BLACKOUT_ON_NOTE, "red", midi_out_apc)
        return

    if note == BLACKOUT_OFF_NOTE:
        osc_client.blackout(False)
        print("🕶️ Blackout OFF")
        update_led(BLACKOUT_ON_NOTE, "off", midi_out_apc)
        return

    # SHIFT simplu: nu face nimic
    if note == SHIFT_NOTE:
        return

    # Toggle grid pad (Busk Mode)
    if 0 <= note <= 63:
        current = busk_led_state.get(note, "off")
        if current in ("off", "red"):
            new_state = "green"
            action = "go"
        else:
            new_state = "red"
            action = "release"

        busk_led_state[note] = new_state
        update_led(note, new_state, midi_out_apc)

        # Calculare index logical (0-based) și pagină
        col = note % 8
        row = note // 8
        logical = (7 - row) * 8 + col
        page = banca_curenta + 1
        # Trimite OSC pentru go/release pe pagina curentă
        osc_client.client.send_message(
            f"/Mx/playback/page{page}/{logical}/{action}", 1
        )
        # Feedback LED Onyx (via MIDI) simultan
        midi_out_onyx.send_message([0x90, note, 127 if action == "go" else 0])
        print(f"[BUSK] Pad {note} -> {action} on page {page}, btn {logical}")
        return


def handle_fader_message(cc, value, midi_out_onyx, osc_client):
    """
    Gestionează mișcarea fader-elor: scalează și trimite OSC către Onyx.
    """
    # Fadere playback 1–9 (CC48–CC56)
    if 48 <= cc <= 56:
        scaled = int(value * 255 / 127)
        playback_id = cc - 47  # CC48->1, ..., CC56->9
        osc_client.set_playback_fader(playback_id=playback_id, level=scaled)
        print(f"[FADER] CC {cc} -> nivel {scaled}, playback {playback_id}")
    # Fader 10 (Master/Bank Swap) – CC57
    elif cc == 57:
        scaled = int(value * 255 / 127)
        playback_id = 10
        osc_client.set_playback_fader(playback_id=playback_id, level=scaled)
        print(f"[FADER] CC {cc} -> nivel {scaled}, playback {playback_id}")
