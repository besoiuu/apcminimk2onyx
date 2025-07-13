from controller import apc_handler
from controller.bank_manager import banca_curenta, increment_bank, decrement_bank
from controller.led_memory import get_led_state, set_led_state, clear_led_state

class EventDispatcher:
    def __init__(self, midi_out_apc, midi_out_onyx):
        self.midi_out_apc = midi_out_apc
        self.midi_out_onyx = midi_out_onyx
        self.shift_pressed = False
        self.blackout_state = False

    def dispatch(self, message):
        status, note, velocity = message

        SHIFT_NOTE = 0x7A  # 122
        BLACKOUT_ON_NOTE = 118
        BLACKOUT_OFF_NOTE = 119

        if note == SHIFT_NOTE:
            self.shift_pressed = velocity > 0

        if note == BLACKOUT_ON_NOTE and velocity > 0:
            self.blackout_state = True
        elif note == BLACKOUT_OFF_NOTE and velocity > 0:
            self.blackout_state = False

        # Apelează handler-ul cu stările actualizate
        apc_handler.handle_pad_press(
            note,
            velocity,
            self.midi_out_apc,
            self.midi_out_onyx,
            shift_pressed=self.shift_pressed,
            blackout_state=self.blackout_state
        )
