from midi.ports import setup_midi_ports
from midi.listener import start_midi_listener

if __name__ == "__main__":
    print("🔌 Inițializare conexiuni MIDI...")
    midi_in, midi_out_apc, midi_out_onyx = setup_midi_ports()

    print("🎧 Pornim ascultarea semnalelor MIDI...")
    start_midi_listener(midi_in, midi_out_apc, midi_out_onyx)

    try:
        while True:
            pass  # Loop principal (poate fi extins ulterior)
    except KeyboardInterrupt:
        print("🛑 Oprire script...")
        midi_in.close_port()
        midi_out_apc.close_port()
        midi_out_onyx.close_port()
