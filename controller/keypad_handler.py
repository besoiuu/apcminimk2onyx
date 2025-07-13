# keypad_handler.py

def invert_row(note):
    """
    Inversează rândul pentru matricea 8x8. 
    Notele vin 0-63, coloanele rămân aceleași, rândurile se inversează vertical.
    """
    col = note % 8
    row = note // 8
    inverted_row = 7 - row
    return inverted_row * 8 + col


class KeypadHandler:
    def __init__(self, osc_client, midi_out_apc):
        self.osc_client = osc_client
        self.midi_out_apc = midi_out_apc

        # Mapare completă: nota MIDI (logică după invert_row) -> (nume buton, OSC button ID)
        self.button_map = {
            0: ("MENU", 2003),
            1: ("MACRO", 2001),
            2: ("SNAPSHOT", 4331),
            3: ("BANK", 4332),
            4: ("PREVIEW", 2002),
            5: ("HIGHLIGHT", 0),
            8: ("EDIT", 5101),
            9: ("EDIT", 5101),
            10: ("UNDO", 5102),
            11: ("UNDO", 5102),
            12: ("CLEAR", 5103),
            13: ("CLEAR", 5103),
            14: ("LAST", 0),
            15: ("NEXT", 0),
            16: ("COPY", 5104),
            17: ("COPY", 5104),
            18: ("MOVE", 5106),
            19: ("MOVE", 5106),
            20: ("DELETE", 5107),
            21: ("DELETE", 5107),
            23: ("FADE", 4321),
            24: ("SLASH", 5214),
            25: ("MINUS", 5210),
            26: ("PLUS", 5211),
            27: ("BACKSPACE", 5215),
            28: ("RECORD", 5401),
            29: ("RECORD", 5401),
            31: ("DELAY", 4322),
            32: ("7", 5207),
            33: ("8", 5208),
            34: ("9", 5209),
            35: ("THRU", 5302),
            36: ("UPDATE", 5402),
            37: ("UPDATE", 5402),
            39: ("SWAP PROG", 0),
            40: ("4", 5204),
            41: ("5", 5205),
            42: ("6", 5206),
            43: ("FULL", 5301),
            45: ("LOAD", 5411),
            46: ("LOAD", 5411),
            47: ("LINK", 0),
            48: ("1", 5201),
            49: ("2", 5202),
            50: ("3", 5203),
            51: ("@", 5216),
            52: ("GROUP", 5412),
            53: ("GROUP", 5412),
            56: ("0", 5200),
            57: (".", 5212),
            58: ("ENTER", 5213),
            59: ("ENTER", 5213),
            60: ("CUE", 5413),
            61: ("CUE", 5413),
        }

    def handle_button(self, midi_note, velocity):
        # Aplică invertirea rândului pentru nota fizică primită
        midi_note_inverted = invert_row(midi_note)
        if midi_note_inverted not in self.button_map:
            print(f"[KeypadHandler] Nota MIDI necunoscută: {midi_note} (invertită: {midi_note_inverted})")
            return

        btn_name, osc_id = self.button_map[midi_note_inverted]
        state = 1 if velocity > 0 else 0

        if osc_id == 0:
            print(f"[KeypadHandler] Butonul {btn_name} ({midi_note}) nu are mapping OSC definit.")
            return

        # Trimite OSC mesaj apăsare/eliberare — fără segmentul /up/down în adresă
        osc_address = f"/Mx/button/{osc_id}"
        print(f"[KeypadHandler] Trimit OSC {osc_address} cu valoarea {state}")
        self.osc_client.client.send_message(osc_address, state)

        # # Actualizează LED
        # led_address = f"/Mx/button/{osc_id}/led"
        # self.osc_client.client.send_message(led_address, state)

        print(f"[KeypadHandler] {btn_name} ({midi_note} inversat: {midi_note_inverted}) - {'pressed' if state else 'released'}")
