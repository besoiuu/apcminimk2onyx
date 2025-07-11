from controller.apc_handler import handle_pad_press
from controller.fader_handler import handle_fader_message


def start_midi_listener(midi_in, midi_out_apc, midi_out_onyx):
    def midi_callback(event, data=None):
        message, _ = event
        status, note, velocity = message

        print(f"[MIDI] Status: {status:#04x}, Note: {note}, Velocity: {velocity}")

        if status == 0x90 and velocity > 0:
            # Note On → pad apăsat
            handle_pad_press(note, velocity, midi_out_apc, midi_out_onyx)

        elif status == 0xB0:
            # Control Change (CC) → fader mișcat
            cc = note        # în acest context, "note" e numărul de control
            value = velocity
            handle_fader_message(cc, value, midi_out_onyx)

    midi_in.set_callback(midi_callback)
