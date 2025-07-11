from event_dispatcher import EventDispatcher

def start_midi_listener(midi_in, midi_out_apc, midi_out_onyx):
    dispatcher = EventDispatcher(midi_out_apc, midi_out_onyx)

    def midi_callback(event, data=None):
        message, _ = event
        status, note, velocity = message
        print(f"[MIDI] Status: {status:#04x}, Note: {note}, Velocity: {velocity}")
        dispatcher.dispatch(message)

    midi_in.set_callback(midi_callback)
