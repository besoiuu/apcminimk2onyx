import time
from midi.ports import setup_midi_ports
from event_dispatcher import EventDispatcher

def main():
    print("🔌 Configurare porturi MIDI...")
    midi_in, midi_out_apc, midi_out_onyx = setup_midi_ports()

    dispatcher = EventDispatcher(midi_out_apc, midi_out_onyx)

    def midi_callback(message, data=None):
        # message e de forma ([status, note, velocity], timestamp)
        midi_message = message[0]
        dispatcher.dispatch(midi_message)

    midi_in.set_callback(midi_callback)

    print("🎧 Ascultare mesaje MIDI. Apasă Ctrl+C pentru oprire.")
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("🛑 Închidere porturi MIDI...")
        midi_in.close_port()
        midi_out_apc.close_port()
        midi_out_onyx.close_port()
        print("Program terminat.")

if __name__ == "__main__":
    main()
