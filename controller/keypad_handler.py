from controller.led_memory import update_led

def invert_row(note):
    col = note % 8
    row = note // 8
    inverted_row = 7 - row
    return inverted_row * 8 + col

def reverse_invert(index):
    col = index % 8
    row = index // 8
    inverted_row = 7 - row
    return inverted_row * 8 + col

SCENE_LAUNCH = list(range(0x70, 0x78))
TRACK_BUTTONS = list(range(0x64, 0x6C))

class KeypadHandler:
    def __init__(self, osc_client, midi_out_apc):
        self.osc_client = osc_client
        self.midi_out_apc = midi_out_apc

        self.button_map = {
            0: ("MENU", 2003), 1: ("MACRO", 2001), 2: ("SNAPSHOT", 4331), 3: ("BANK", 4332),
            4: ("PREVIEW", 2002), 5: ("HIGHLIGHT", 0), 8: ("EDIT", 5101), 9: ("EDIT", 5101),
            10: ("UNDO", 5102), 11: ("UNDO", 5102), 12: ("CLEAR", 5103), 13: ("CLEAR", 5103),
            14: ("LAST", 0), 15: ("NEXT", 0), 16: ("COPY", 5104), 17: ("COPY", 5104),
            18: ("MOVE", 5106), 19: ("MOVE", 5106), 20: ("DELETE", 5107), 21: ("DELETE", 5107),
            23: ("FADE", 4321), 24: ("SLASH", 5214), 25: ("MINUS", 5210), 26: ("PLUS", 5211),
            27: ("BACKSPACE", 5215), 28: ("RECORD", 5401), 29: ("RECORD", 5401),
            31: ("DELAY", 4322), 32: ("7", 5207), 33: ("8", 5208), 34: ("9", 5209),
            35: ("THRU", 5302), 36: ("UPDATE", 5402), 37: ("UPDATE", 5402), 39: ("SWAP PROG", 0),
            40: ("4", 5204), 41: ("5", 5205), 42: ("6", 5206), 43: ("FULL", 5301),
            44: ("LOAD", 5411), 45: ("LOAD", 5411), 47: ("LINK", 0), 48: ("1", 5201),
            49: ("2", 5202), 50: ("3", 5203), 51: ("@", 5216), 52: ("GROUP", 5412),
            53: ("GROUP", 5412), 56: ("0", 5200), 57: (".", 5212), 58: ("ENTER", 5213),
            59: ("ENTER", 5213), 60: ("CUE", 5413), 61: ("CUE", 5413)
        }

    def handle_button(self, midi_note, velocity):
        if 0 <= midi_note < 64:
            inverted_note = invert_row(midi_note)
            is_pressed = velocity > 0

            if inverted_note in self.button_map and self.button_map[inverted_note][1] != 0:
                label, osc_id = self.button_map[inverted_note]
                if osc_id:
                    self.osc_client.client.send_message(f"/Mx/button/{osc_id}", int(is_pressed))
                # Pe hold: VERDE NORMAL (21). Pe release: GALBEN (9)
                if is_pressed:
                    update_led(midi_note, "green", self.midi_out_apc)
                else:
                    update_led(midi_note, "amber", self.midi_out_apc)
            else:
                # La pad nemapat: Pe hold: VERDE. Pe release: ALBASTRU
                if is_pressed:
                    update_led(midi_note, "green", self.midi_out_apc)
                else:
                    update_led(midi_note, "blue", self.midi_out_apc)
        elif midi_note in SCENE_LAUNCH:
            update_led(midi_note, "green", self.midi_out_apc)
        elif midi_note in TRACK_BUTTONS:
            update_led(midi_note, "red", self.midi_out_apc)

    def initialize_keyboard_mode(self):
        # Toate grid pads: dacă au mapping OSC → galben, altfel albastru
        for note in range(64):
            inv = invert_row(note)
            if inv in self.button_map and self.button_map[inv][1] != 0:
                update_led(note, "amber", self.midi_out_apc)
            else:
                update_led(note, "blue", self.midi_out_apc)
        for note in SCENE_LAUNCH:
            update_led(note, "green", self.midi_out_apc)
        for note in TRACK_BUTTONS:
            update_led(note, "red", self.midi_out_apc)
