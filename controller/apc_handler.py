from controller.bank_manager import banca_curenta, increment_bank, decrement_bank
from controller.led_memory import get_led_state, set_led_state, update_led
from controller.onyx_handler import OnyxOSCClient

osc_client = OnyxOSCClient(ip="10.0.0.100", port=8000)

SHIFT_NOTE = 0x7A
BLACKOUT_ON_NOTE = 118
BLACKOUT_OFF_NOTE = 119
BANK_UP_NOTE = 0x75
BANK_DOWN_NOTE = 0x74

busk_led_state = {}  # note: state ("off", "green", "red")


def clear_busk_grid(midi_out_apc):
    """
    Stinge toate pad-urile din grid (0-63) la intrarea/ieșirea din BUSK.
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
    BUSK mode: Toggle verde/roșu pe grid 0-63. Restul butoanelor gestionează separat.
    """
    if velocity == 0:
        return

    # ======== Funcții speciale ========
    if note == BANK_DOWN_NOTE:
        decrement_bank()
        osc_client.select_bank(banca_curenta)
        clear_busk_grid(midi_out_apc)
        print(f"🔻 Bank - noua bancă: {banca_curenta}")
        return

    if note == BANK_UP_NOTE:
        increment_bank()
        osc_client.select_bank(banca_curenta)
        clear_busk_grid(midi_out_apc)
        print(f"🔺 Bank + noua bancă: {banca_curenta}")
        return

    if note == BLACKOUT_ON_NOTE:
        osc_client.blackout(True)
        print("🕶️ Blackout ON")
        update_led(BLACKOUT_ON_NOTE, "red", midi_out_apc, is_pad=False)
        return

    if note == BLACKOUT_OFF_NOTE:
        osc_client.blackout(False)
        print("🕶️ Blackout OFF")
        update_led(BLACKOUT_ON_NOTE, "off", midi_out_apc, is_pad=False)
        return

    if note == SHIFT_NOTE:
        return

    # ======== BUSK GRID TOGGLE (doar pentru pad-uri 0–63) =====
    if 0 <= note <= 63:
        cur = busk_led_state.get(note, "off")
        if cur in ("off", "red"):
            new = "green"
            osc_action = "go"
        else:
            new = "red"
            osc_action = "release"

        busk_led_state[note] = new
        update_led(note, new, midi_out_apc)

        # OSC logic identic cu ce aveai:
        col = note % 8
        row = note // 8
        logical_note = (7 - row) * 8 + col + 1
        note_real = logical_note + (banca_curenta * 64)
        page_index = banca_curenta + 1
        button_index = logical_note - 1
        osc_client.client.send_message(
            f"/Mx/playback/page{page_index}/{button_index}/{osc_action}", 1
        )
        midi_out_onyx.send_message([0x90, note_real - 1, velocity])

        # print(f"[BUSK] Pad {note}: {cur} -> {new} (LED), OSC: page{page_index} btn{button_index} {osc_action}")
        return

    # ======== Track/Scene Buttons (optional, pentru restul butoanelor) ========
    # Dacă vrei ca Track Buttons (0x64–0x6B) și Scene Launch (0x70–0x77) să fie roșii sau verzi, gestionezi aici separat.
    # Exemplu:
    if 0x64 <= note <= 0x6B:
        # Track buttons: roșu ON
        update_led(note, "red", midi_out_apc, is_pad=False)
        return
    if 0x70 <= note <= 0x77:
        # Scene buttons: verde ON
        update_led(note, "green", midi_out_apc, is_pad=False)
        return


def handle_fader_message(cc, value, midi_out_onyx, osc_client):
    """
    Gestionează mișcarea unui fader: trimite nivelul corespunzător către Onyx.
    """
    if 48 <= cc <= 56:
        scaled_level = int(value * 255 / 127)
        playback_id = cc - 47
        osc_client.set_playback_fader(playback_id=playback_id, level=scaled_level)
        # print(f"[FADER] CC {cc} → poziție {value}, scalat: {scaled_level}, playback: {playback_id}")
