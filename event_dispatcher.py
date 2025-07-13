from controller import apc_handler, fader_handler
from controller.onyx_handler import OnyxOSCClient


class EventDispatcher:
    def __init__(self, midi_out_apc, midi_out_onyx):
        self.midi_out_apc = midi_out_apc
        self.midi_out_onyx = midi_out_onyx
        self.shift_pressed = False
        self.blackout_state = False
        self.osc_client = OnyxOSCClient(ip="10.0.0.100", port=8000)

    def dispatch(self, message):
        status = message[0] & 0xF0
        note = message[1]
        velocity = message[2]

        SHIFT_NOTE = 0x7A  # 122
        BLACKOUT_ON_NOTE = 118
        BLACKOUT_OFF_NOTE = 119

        if note == SHIFT_NOTE:
            self.shift_pressed = velocity > 0

        if note == BLACKOUT_ON_NOTE and velocity > 0:
            self.blackout_state = True
        elif note == BLACKOUT_OFF_NOTE and velocity > 0:
            self.blackout_state = False

        if status == 0x90:  # Note On -> pad-uri
            apc_handler.handle_pad_press(
                note,
                velocity,
                self.midi_out_apc,
                self.midi_out_onyx,
                shift_pressed=self.shift_pressed,
                blackout_state=self.blackout_state,
            )
        elif status == 0xB0:  # Control Change -> fadere
            fader_handler.handle_fader_message(
                note, velocity, self.midi_out_onyx, self.osc_client
            )

        else:
            # alte mesaje MIDI, ignoră sau loghează
            pass
