import rtmidi
import time

def test_leds(port_index):
    midi_out = rtmidi.MidiOut()
    midi_out.open_port(port_index)
    print(f"Test LED-uri pe portul MIDI OUT: {port_index}")

    # Aprinde LED-urile primelor 8 pad-uri verde (velocity 48)
    for note in range(8):
        midi_out.send_message([0x90, note, 48])
        time.sleep(0.3)

    # Stinge LED-urile
    for note in range(8):
        midi_out.send_message([0x80, note, 0])
        time.sleep(0.1)

    midi_out.close_port()
    print("Test finalizat.")

if __name__ == "__main__":
    PORT_INDEX = 3  # Înlocuiește cu portul tău MIDI OUT pentru APC Mini
    test_leds(PORT_INDEX)
