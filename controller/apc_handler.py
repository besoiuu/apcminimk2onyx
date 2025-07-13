from controller.bank_manager import banca_curenta, increment_bank, decrement_bank
from controller.led_memory import get_led_state, set_led_state
from controller.onyx_handler import OnyxOSCClient


# Inițializează clientul OSC pentru Onyx
osc_client = OnyxOSCClient(ip="10.0.0.100", port=8000)

COLOR_MAP = {"off": 0, "standby": 5, "active": 48, "flash": 1}

SHIFT_NOTE = 0x7A
BLACKOUT_ON_NOTE = 118
BLACKOUT_OFF_NOTE = 119
BANK_UP_NOTE = 0x75
BANK_DOWN_NOTE = 0x74


class PadColumnGroup:
    def __init__(self, name, pad_notes, softkey_note, fader_cc):
        self.name = name
        self.pad_notes = pad_notes  # Lista note fizice (0x00–0x3F)
        self.softkey_note = softkey_note  # Nota softkey TrackButton
        self.fader_cc = fader_cc  # CC MIDI pentru faderul aferent


def generate_pad_column_inverted_row(col_index):
    # Generează lista de note fizice pentru o coloană inversând rândurile
    return [(7 - row) * 8 + col_index for row in range(8)]


pad_column_groups = [
    PadColumnGroup("Coloana 1", generate_pad_column_inverted_row(0), 0x64, 48),
    PadColumnGroup("Coloana 2", generate_pad_column_inverted_row(1), 0x65, 49),
    PadColumnGroup("Coloana 3", generate_pad_column_inverted_row(2), 0x66, 50),
    PadColumnGroup("Coloana 4", generate_pad_column_inverted_row(3), 0x67, 51),
    PadColumnGroup("Coloana 5", generate_pad_column_inverted_row(4), 0x68, 52),
    PadColumnGroup("Coloana 6", generate_pad_column_inverted_row(5), 0x69, 53),
    PadColumnGroup("Coloana 7", generate_pad_column_inverted_row(6), 0x6A, 54),
    PadColumnGroup("Coloana 8", generate_pad_column_inverted_row(7), 0x6B, 55),
    PadColumnGroup(
        "Scene Launch", [0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77], None, 56
    ),
]


def physical_to_logical_note(physical_note):
    # Conversie nota fizică MIDI (0..63) la nota logică 1..64 cu rândurile inversate
    col = physical_note % 8
    row = physical_note // 8
    inverted_row = 7 - row
    logical_note = inverted_row * 8 + col + 1  # +1 pentru numerotare 1-based
    return logical_note


def find_group_by_note(note):
    for group in pad_column_groups:
        if note in group.pad_notes or note == group.softkey_note:
            return group
    return None


def update_led(note, mode, midi_out_apc, is_pad=True):
    velocity = COLOR_MAP.get(mode, 0)
    if is_pad and 0 <= note <= 63:
        midi_out_apc.send_message([0x90, note, velocity])
    elif not is_pad and 112 <= note <= 119:
        midi_out_apc.send_message([0x90, note, 1 if velocity > 0 else 0])


def restore_red_leds_for_bank(
    midi_out_apc, banca_curenta, get_led_state, set_led_state, update_led_func
):
    for physical_note in range(64):
        logical_note = physical_to_logical_note(physical_note)
        mode = get_led_state(banca_curenta, logical_note)
        if mode not in ("standby", "active"):
            mode = "standby"
            set_led_state(banca_curenta, logical_note, mode)
        update_led_func(physical_note, mode, midi_out_apc)


def handle_pad_press(
    note,
    velocity,
    midi_out_apc,
    midi_out_onyx,
    shift_pressed=False,
    blackout_state=False,
):
    if velocity == 0:
        # Ignoră note off, ca să nu faci dublă procesare
        return

    # Butoane speciale pentru schimbare bancă
    if note == BANK_DOWN_NOTE:
        decrement_bank()
        osc_client.select_bank(banca_curenta)
        restore_red_leds_for_bank(
            midi_out_apc, banca_curenta, get_led_state, set_led_state, update_led
        )
        print(f"Bank decremented: {banca_curenta}")
        return

    if note == BANK_UP_NOTE:
        increment_bank()
        osc_client.select_bank(banca_curenta)
        restore_red_leds_for_bank(
            midi_out_apc, banca_curenta, get_led_state, set_led_state, update_led
        )
        print(f"Bank incremented: {banca_curenta}")
        return

    # Blackout ON/OFF
    if note == BLACKOUT_ON_NOTE:
        osc_client.blackout(True)
        update_led(BLACKOUT_ON_NOTE, "red", midi_out_apc, is_pad=False)
        print("Blackout ON")
        return

    if note == BLACKOUT_OFF_NOTE:
        osc_client.blackout(False)
        update_led(BLACKOUT_ON_NOTE, "off", midi_out_apc, is_pad=False)
        print("Blackout OFF")
        return

    if note == SHIFT_NOTE:
        return  # Shift gestionat separat

    group = find_group_by_note(note)
    if group is None:
        print(f"Nota necunoscută: {note}")
        return

    if 0 <= note <= 63:
        logical_note = physical_to_logical_note(note)
        note_real = logical_note + (banca_curenta * 64)

        page_index = banca_curenta + 1
        button_index = logical_note - 1  # zero-based

        # Citește starea curentă a padului (active/standby)
        current_mode = get_led_state(banca_curenta, note_real)

        if current_mode == "active":
            # Dacă e deja activ, trimite release și setează standby
            osc_action = "release"
            next_mode = "standby"
        else:
            # Dacă e standby sau off, trimite go și setează active
            osc_action = "go"
            next_mode = "active"

        osc_client.client.send_message(
            f"/Mx/playback/page{page_index}/{button_index}/{osc_action}", 1
        )

        set_led_state(banca_curenta, note_real, next_mode)
        update_led(note, next_mode, midi_out_apc, is_pad=True)
        midi_out_onyx.send_message([0x90, note_real - 1, velocity])  # Onyx e 0-based

        print(
            f"[{group.name}] Pad fizic {note} -> logic {logical_note}, OSC: page {page_index} button {button_index} {osc_action}"
        )
        return

    # Similar pentru softkey TrackButton și Scene Launch - doar toggle la apăsare:
    if group.softkey_note is not None and note == group.softkey_note:
        current_mode = get_led_state(banca_curenta, note)
        next_mode = "standby" if current_mode == "active" else "active"
        update_led(note, next_mode, midi_out_apc, is_pad=False)
        set_led_state(banca_curenta, note, next_mode)
        print(
            f"[{group.name}] Softkey TrackButton {note}: {current_mode} -> {next_mode}"
        )
        return

    if group.name == "Scene Launch" and note in group.pad_notes:
        current_mode = get_led_state(banca_curenta, note)
        next_mode = "standby" if current_mode == "active" else "active"
        update_led(note, next_mode, midi_out_apc, is_pad=False)
        set_led_state(banca_curenta, note, next_mode)
        print(f"[Scene Launch] Button {note}: {current_mode} -> {next_mode}")
        return


def handle_fader_message(cc, value, midi_out_onyx, osc_client):
    if 48 <= cc <= 56:
        scaled_level = int(value * 255 / 127)
        playback_id = cc - 47
        print(
            f"Fader CC {cc} poziție: {value} scaled to {scaled_level}, playback_id: {playback_id}"
        )
        osc_client.set_playback_fader(playback_id=playback_id, level=scaled_level)
