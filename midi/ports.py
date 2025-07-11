import rtmidi

def setup_midi_ports():
    midi_in = rtmidi.MidiIn()
    midi_out_apc = rtmidi.MidiOut()
    midi_out_onyx = rtmidi.MidiOut()

    # Afișăm porturile disponibile
    print("🎛️ Porturi MIDI disponibile (Input):")
    for i, name in enumerate(midi_in.get_ports()):
        print(f"{i}: {name}")
    
    print("\n🎚️ Porturi MIDI disponibile (Output):")
    for i, name in enumerate(midi_out_apc.get_ports()):
        print(f"{i}: {name}")

    # Alegem porturi (poți adapta cu indexuri fixe)
    apc_in_port = int(input("Selectează indexul pentru APC MINI IN: "))
    onyx_out_port = int(input("Selectează indexul pentru ONYX MIDI OUT: "))
    apc_out_port = int(input("Selectează indexul pentru APC MINI OUT: "))

    midi_in.open_port(apc_in_port)
    midi_out_apc.open_port(apc_out_port)
    midi_out_onyx.open_port(onyx_out_port)

    return midi_in, midi_out_apc, midi_out_onyx
