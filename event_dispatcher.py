from controller import apc_handler
from controller.keypad_handler import KeypadHandler
from controller.onyx_handler import OnyxOSCClient


class EventDispatcher:
    def __init__(self, midi_out_apc, midi_out_onyx):
        self.midi_out_apc = midi_out_apc
        self.midi_out_onyx = midi_out_onyx
        self.shift_pressed = False
        self.blackout_state = False
        self.keyboard_mode = False  # Flag pentru schimbarea între moduri
        self.osc_client = OnyxOSCClient(ip="10.0.0.100", port=8000)
        self.keypad_handler = KeypadHandler(self.osc_client, midi_out_apc)

    def dispatch(self, message):
        status = message[0] & 0xF0
        note = message[1]
        velocity = message[2]

        SHIFT_NOTE = 0x7A  # 122
        SCENE_BTN_1 = 0x70  # Scene Launch Button 1 (Keyboard Mode)
        SCENE_BTN_2 = 0x71  # Scene Launch Button 2 (Busk Mode)

        # Detectează Shift
        if note == SHIFT_NOTE:
            self.shift_pressed = velocity > 0

        # Detectează schimbarea între mode: Keyboard Mode sau Busk Mode
        if note == SCENE_BTN_1 and self.shift_pressed and velocity > 0:
            self.keyboard_mode = True
            print("[Mode Switch] Mod schimbat la: Keyboard Mode")

        if note == SCENE_BTN_2 and self.shift_pressed and velocity > 0:
            self.keyboard_mode = False
            print("[Mode Switch] Mod schimbat la: Busk Mode")

        # Când suntem în Keyboard Mode, procesăm butoanele în KeypadHandler
        if self.keyboard_mode:
            if status == 0x90:  # Note On/Off
                self.keypad_handler.handle_button(note, velocity)

        # Când suntem în Busk Mode, procesăm pad-urile în mod tradițional
        else:
            if status == 0x90:  # Note On/Off -> pad-uri
                apc_handler.handle_pad_press(
                    note,
                    velocity,
                    self.midi_out_apc,
                    self.midi_out_onyx,
                    shift_pressed=self.shift_pressed,
                    blackout_state=self.blackout_state,
                )
            elif status == 0xB0:  # Control Change -> fadere
                apc_handler.handle_fader_message(
                    note,
                    velocity,
                    self.midi_out_onyx,
                    self.osc_client
                )
            else:
                # alte mesaje MIDI pot fi ignorate sau logate
                pass
