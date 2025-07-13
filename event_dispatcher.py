from controller import apc_handler
from controller.keypad_handler import KeypadHandler
from controller.onyx_handler import OnyxOSCClient


class EventDispatcher:
    def __init__(self, midi_out_apc, midi_out_onyx):
        self.midi_out_apc = midi_out_apc
        self.midi_out_onyx = midi_out_onyx
        self.shift_pressed = False
        self.blackout_state = False
        self.keyboard_mode = False  # Flag mod tastatură
        self.osc_client = OnyxOSCClient(ip="10.0.0.100", port=8000)
        self.keypad_handler = KeypadHandler(self.osc_client, midi_out_apc)

    def dispatch(self, message):
        status = message[0] & 0xF0
        note = message[1]
        velocity = message[2]

        SHIFT_NOTE = 0x7A
        SCENE_BTN_1 = 0x70

        BLACKOUT_ON_NOTE = 118
        BLACKOUT_OFF_NOTE = 119

        # Detectare shift
        if note == SHIFT_NOTE:
            self.shift_pressed = velocity > 0

        # Toggle mod tastatură cu SHIFT + Scene Button 1
        if note == SCENE_BTN_1 and self.shift_pressed and velocity > 0:
            self.keyboard_mode = not self.keyboard_mode
            print(
                f"[Mode Switch] Modul schimbat în: {'Keyboard' if self.keyboard_mode else 'Busk'}"
            )

        if self.keyboard_mode:
            if status == 0x90:  # Note On/Off
                self.keypad_handler.handle_button(note, velocity)
        else:
            if status == 0x90:
                apc_handler.handle_pad_press(
                    note,
                    velocity,
                    self.midi_out_apc,
                    self.midi_out_onyx,
                    shift_pressed=self.shift_pressed,
                    blackout_state=self.blackout_state,
                )
            elif status == 0xB0:
                apc_handler.handle_fader_message(
                    note, velocity, self.midi_out_onyx, self.osc_client
                )
