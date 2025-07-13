from midi.ports import setup_midi_ports
from midi.listener import start_midi_listener
from event_dispatcher import EventDispatcher  # importă clasa nouă

if __name__ == "__main__":
    print("🔌 Inițializare conexiuni MIDI...")
    midi_in, midi_out_apc, midi_out_onyx = setup_midi_ports()

    dispatcher = EventDispatcher(midi_out_apc, midi_out_onyx)

    def midi_callback(event, data=None):
        message, _ = event
        dispatcher.dispatch(message)

    midi_in.set_callback(midi_callback)

    print("🎧 Pornim ascultarea semnalelor MIDI...")
    try:
        while True:
            pass  # Loop principal (poate fi extins ulterior)
    except KeyboardInterrupt:
        print("🛑 Oprire script...")
        midi_in.close_port()
        midi_out_apc.close_port()
        midi_out_onyx.close_port()
