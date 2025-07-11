from controller import apc_handler
from controller.bank_manager import banca_curenta, increment_bank, decrement_bank
from controller.led_memory import get_led_state, set_led_state, clear_led_state

class EventDispatcher:
    def __init__(self, midi_out_apc, midi_out_onyx):
        self.midi_out_apc = midi_out_apc
        self.midi_out_onyx = midi_out_onyx
        self.shift_pressed = False  # Poți adăuga gestiunea shift aici, dacă dorești
        self.blackout_state = False

    def dispatch(self, message):
        status, note, velocity = message
        print(f"[Dispatcher] Received message: status=0x{status:X}, note={note}, velocity={velocity}")

        # Trimite evenimentul către handler-ul din apc_handler.py
        apc_handler.handle_pad_press(
            note,
            velocity,
            self.midi_out_apc,
            self.midi_out_onyx
            # Folosește funcțiile interne din apc_handler, fără alte modificări aici
        )
