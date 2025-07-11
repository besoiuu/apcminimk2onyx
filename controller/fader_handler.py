def handle_fader_message(cc, value, midi_out_onyx):
    """
    Trimite mesajele CC către ONYX fără modificări.
    CC 48–56 sunt fader-ele 1–9.
    """
    if 48 <= cc <= 56:
        print(f"🎚️ Fader CC: {cc}, Value: {value}")
        midi_out_onyx.send_message([0xB0, cc, value])  # B0 = Control Change, Channel 1
