from controller import apc_handler
from controller.keypad_handler import KeypadHandler
from controller.onyx_handler import OnyxOSCClient
from controller.lighting_modes import LightingManager
from controller.mode_cycle import next_track_mode, track_mode_order

class EventDispatcher:
    def __init__(self, midi_out_apc, midi_out_onyx):
        self.midi_out_apc = midi_out_apc
        self.midi_out_onyx = midi_out_onyx
        self.shift_pressed = False
        self.blackout_state = False
        self.keyboard_mode = False

        self.osc_client = OnyxOSCClient(ip="10.0.0.100", port=8000)
        self.keypad_handler = KeypadHandler(self.osc_client, midi_out_apc)

        # Manager RGB
        self.lighting = LightingManager(midi_out_apc)

        # Track buttons 0x64–0x6B
        self.track_notes = list(range(0x64, 0x6C))

        # DEBUG: apăsând acest note code vei rula debug_palette()
        self.DEBUG_NOTE = 0x6A

    def dispatch(self, message):
        status = message[0] & 0xF0
        note   = message[1]
        velo   = message[2]

        # 1) Debug palette
        if note == self.DEBUG_NOTE and velo > 0:
            print("[DEBUG] Palette test start")
            self.lighting.debug_palette()
            print("[DEBUG] Palette test end")
            return

        SHIFT_NOTE   = 0x7A
        SCENE_BTN_1  = 0x70

        # 2) SHIFT down/up
        if note == SHIFT_NOTE:
            self.shift_pressed = velo > 0
            return

        # 3) Toggle Keyboard Mode: SHIFT + SceneBtn1
        if note == SCENE_BTN_1 and self.shift_pressed and velo > 0:
            self.keyboard_mode = not self.keyboard_mode
            print(f"[Mode Switch] {'Keyboard' if self.keyboard_mode else 'Busk'} mode")
            if self.keyboard_mode:
                # stop RGB threads + clear grid
                self.lighting.set_mode(8)
                self.lighting.off()
                self.keypad_handler.initialize_keyboard_mode()
            else:
                apc_handler.clear_busk_grid(self.midi_out_apc)
            return

        # 4) SHIFT + Track0 => cycle lighting modes
        if self.shift_pressed and note == self.track_notes[0] and velo > 0 and not self.keyboard_mode:
            mode_name  = next_track_mode(note)
            mode_index = track_mode_order.index(mode_name) + 1
            print(f"[LIGHT MODE] -> {mode_index} ({mode_name})")
            self.lighting.set_mode(mode_index)
            return

        # 5) Fader messages always pass through
        if status == 0xB0:
            apc_handler.handle_fader_message(
                note, velo, self.midi_out_onyx, self.osc_client
            )
            return

        # 6) Keyboard Mode button handling
        if self.keyboard_mode:
            if status == 0x90 and velo > 0:
                self.keypad_handler.handle_button(note, velo)
            elif status in (0x80, 0x90) and velo == 0:
                self.keypad_handler.handle_button(note, 0)
            return

        # 7) Busk Mode pad presses
        if status == 0x90:
            apc_handler.handle_pad_press(
                note,
                velo,
                self.midi_out_apc,
                self.midi_out_onyx,
                shift_pressed=self.shift_pressed,
                blackout_state=self.blackout_state,
            )
            return
