from controller import apc_handler

class EventDispatcher:
    def __init__(self, midi_out_apc, midi_out_onyx):
        self.midi_out_apc = midi_out_apc
        self.midi_out_onyx = midi_out_onyx
        self.shift_pressed = False
        self.blackout_state = False

    def dispatch(self, message):
        status, note, velocity = message

        print(f"[Dispatcher] Received message: status=0x{status:X}, note={note}, velocity={velocity}")

        # Actualizare stare SHIFT
        SHIFT_NOTE = 0x7A  # 122
        if note == SHIFT_NOTE:
            self.shift_pressed = velocity > 0
            print(f"[Dispatcher] Shift pressed state updated to: {self.shift_pressed}")

        # Actualizare stare BLACKOUT
        BLACKOUT_ON_NOTE = 118
        BLACKOUT_OFF_NOTE = 119
        if note == BLACKOUT_ON_NOTE and velocity > 0:
            self.blackout_state = True
            print(f"[Dispatcher] Blackout state set to ON")
        elif note == BLACKOUT_OFF_NOTE and velocity > 0:
            self.blackout_state = False
            print(f"[Dispatcher] Blackout state set to OFF")

        print(f"[Dispatcher] Forwarding to apc_handler.handle_pad_press with shift_pressed={self.shift_pressed}, blackout_state={self.blackout_state}")
        apc_handler.handle_pad_press(
            note,
            velocity,
            self.midi_out_apc,
            self.midi_out_onyx,
            shift_pressed=self.shift_pressed,
            blackout_state=self.blackout_state
        )
