def handle_fader_message(cc, value, midi_out_onyx, osc_client):
    """
    Handlează faderele 1-9 (CC 48-56) de la Akai APC Mini MK2.
    Trimite valoarea MIDI către Onyx și valoarea scalată OSC (0-255).
    """
    if 48 <= cc <= 56:
        # Trimite mesaj MIDI CC raw către Onyx
        midi_out_onyx.send_message([0xB0, cc, value])
        
        # Mapare CC la playback_id (1-based)
        playback_id = cc - 47  # cc=48 -> playback_id=1, cc=56 -> playback_id=9
        
        # Conversie valoare MIDI (0..127) la OSC (0..255)
        level = (value / 127) * 255
        
        # Trimite OSC pentru fader
        osc_client.set_playback_fader(playback_id, level)
