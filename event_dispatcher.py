from controller import apc_handler
from controller.keypad_handler import KeypadHandler
from controller.onyx_handler import OnyxOSCClient
from controller.lighting_modes import LightingManager
from controller.mode_cycle import next_track_mode, track_mode_order
from controller.bank_manager import get_banca_curenta


class EventDispatcher:
    def __init__(self, midi_out_apc, midi_out_onyx):
        self.midi_out_apc = midi_out_apc
        self.midi_out_onyx = midi_out_onyx
        self.shift_pressed = False
        self.keyboard_mode = False

        self.osc_client = OnyxOSCClient(ip="10.0.0.100", port=8000)
        self.keypad_handler = KeypadHandler(self.osc_client, midi_out_apc)
        self.lighting = LightingManager(midi_out_apc)
        # Track Buttons 1–9 notes (0x64–0x6C)
        self.track_notes = list(range(0x64, 0x6D))

    def dispatch(self, message):
        # Parse MIDI message
        status = message[0] & 0xF0
        note = message[1]
        velo = message[2]

        SHIFT_NOTE = 0x7A
        SCENE_BTN_1 = 0x70

        # 1) Handle SHIFT press/release
        if note == SHIFT_NOTE:
            self.shift_pressed = velo > 0
            return

        # 2) Toggle Keyboard Mode (SHIFT + Scene Launch 1)
        if note == SCENE_BTN_1 and self.shift_pressed and velo > 0:
            self.keyboard_mode = not self.keyboard_mode
            mode = 'Keyboard' if self.keyboard_mode else 'Busk'
            print(f"[Mode Switch] {mode} mode")
            if self.keyboard_mode:
                self.lighting.set_mode(8)
                self.lighting.off()
                self.keypad_handler.initialize_keyboard_mode()
            else:
                apc_handler.clear_busk_grid(self.midi_out_apc)
            return

        # 3) Cycle lighting modes (SHIFT + Track Button 1)
        if (self.shift_pressed and note == self.track_notes[0]
                and velo > 0 and not self.keyboard_mode):
            mode_name = next_track_mode(note)
            mode_index = track_mode_order.index(mode_name) + 1
            print(f"[LIGHT MODE] -> {mode_index} ({mode_name})")
            self.lighting.set_mode(mode_index)
            return

        # 4) Track Buttons 1–9 ⇒ full-level toggle for playback faders 1–9
        if note in self.track_notes and not self.shift_pressed and not self.keyboard_mode:
            idx = self.track_notes.index(note)  # 0–8 for faders 1–9
            playback_id = idx + 1
            # Press → full level (255)
            if status == 0x90 and velo > 0:
                # LED feedback: green on
                self.midi_out_apc.send_message([0x90, note, 0x21])
                # Set fader to max
                self.osc_client.set_playback_fader(playback_id, 255)
                return
            # Release → zero level
            elif (status in (0x80, 0x90)) and velo == 0:
                # LED feedback: red on
                self.midi_out_apc.send_message([0x90, note, 0x05])
                # Set fader to zero
                self.osc_client.set_playback_fader(playback_id, 0)
                return
            # otherwise ignore
            return

        # 5) Fader CC messages passthrough Fader CC messages passthrough
        if status == 0xB0:
            apc_handler.handle_fader_message(
                note, velo, self.midi_out_onyx, self.osc_client
            )
            return

        # 6) Keyboard Mode: delegate to keypad_handler
        if self.keyboard_mode:
            if status == 0x90 and velo > 0:
                self.keypad_handler.handle_button(note, velo)
            elif (status in (0x80, 0x90)) and velo == 0:
                self.keypad_handler.handle_button(note, 0)
            return

        # 7) Busk Mode pad presses
        if status == 0x90 and not self.keyboard_mode:
            apc_handler.handle_pad_press(
                note,
                velo,
                self.midi_out_apc,
                self.midi_out_onyx,
                shift_pressed=self.shift_pressed,
            )
            return
