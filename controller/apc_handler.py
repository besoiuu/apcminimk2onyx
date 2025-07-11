def restore_red_leds_for_bank(midi_out_apc, banca_curenta, get_led_state, set_led_state, update_led):
    for note in range(64):
        mode = get_led_state(banca_curenta, note)
        if mode == "off" or mode is None:
            mode = "standby"  # roșu implicit
            set_led_state(banca_curenta, note, mode)
        update_led(note, mode, midi_out_apc)

def handle_pad_press(note, velocity, midi_out_apc, midi_out_onyx):
    from controller.bank_manager import banca_curenta, increment_bank, decrement_bank
    from controller.led_memory import get_led_state, set_led_state, clear_led_state
    from controller.led_feedback import update_led, restore_leds_for_current_bank

    if velocity == 0:
        return

    BLACKOUT_ON_NOTE = 118
    BLACKOUT_OFF_NOTE = 119
    BANK_UP_NOTE = 0x75    # Scene Launch 6
    BANK_DOWN_NOTE = 0x74  # Scene Launch 5

    blackout_state = getattr(handle_pad_press, "blackout_state", False)

    # Bank down
    if note == BANK_DOWN_NOTE and velocity > 0:
        print("⬅️ Bancă -")
        decrement_bank()
        restore_red_leds_for_bank(midi_out_apc, banca_curenta, get_led_state, set_led_state, update_led)
        return

    # Bank up
    if note == BANK_UP_NOTE and velocity > 0:
        print("➡️ Bancă +")
        increment_bank()
        restore_red_leds_for_bank(midi_out_apc, banca_curenta, get_led_state, set_led_state, update_led)
        return

    if note == BLACKOUT_ON_NOTE and velocity > 0:
        print("⬛ Blackout ON")
        midi_out_onyx.send_message([0x90, BLACKOUT_ON_NOTE, 127])
        update_led(BLACKOUT_ON_NOTE, "red", midi_out_apc)
        handle_pad_press.blackout_state = True
        return

    if note == BLACKOUT_OFF_NOTE and velocity > 0:
        print("⬜ Blackout OFF")
        midi_out_onyx.send_message([0x80, BLACKOUT_ON_NOTE, 0])
        update_led(BLACKOUT_ON_NOTE, "off", midi_out_apc)
        handle_pad_press.blackout_state = False
        return

    if 0 <= note <= 63:
        note_real = note + (banca_curenta * 64)
        current_mode = get_led_state(banca_curenta, note_real)
        next_mode = "standby" if current_mode == "active" else "active"

        midi_out_onyx.send_message([0x90, note_real, velocity])
        update_led(note, next_mode, midi_out_apc)
        set_led_state(banca_curenta, note_real, next_mode)

        print(f"Pad {note_real}: {current_mode} -> {next_mode}")
        return

    return
