# APC MINI MK2 ➔ ONYX OSC MIDI Bridge

**Full control and visual feedback for Obsidian Onyx using the Akai APC Mini MK2**  
Python-based integration: fast setup, robust features, custom mapping!

---

## Table of Contents

- [Description](#description)
- [Requirements & Installation](#requirements--installation)
- [loopMIDI Setup](#loopmidi-setup)
- [Operating Modes](#operating-modes)
  - [BUSK Mode](#busk-mode)
  - [KEYBOARD Mode](#keyboard-mode)
- [Main Features](#main-features)
- [Pad & Button Mapping](#pad--button-mapping)
- [LED Feedback & Colors](#led-feedback--colors)
- [Special Commands](#special-commands)
- [Troubleshooting](#troubleshooting)
- [Extending & Customizing](#extending--customizing)
- [Contact](#contact)

---

## Description

This project enables **fast, colorful, and physical control** over Obsidian ONYX using the Akai APC Mini MK2 controller.  
It provides synchronized RGB feedback, mode switching, detailed OSC mapping, quick commands, blackout, bank switching, and full hardware fader support.

---

## Requirements & Installation

- **Windows 10/11** or Linux/Mac with Python 3.8+
- **Akai APC mini mk2** (only mk2 version!)
- **Obsidian ONYX** or any OSC/MIDI compatible software
- **loopMIDI** (Windows) or an equivalent (IAC, qjackctl) on Mac/Linux
- **python-rtmidi**, **python-osc** and all dependencies from `requirements.txt`

### Quick Install

1. Clone this repo or copy the source files.
2. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Install and launch **loopMIDI** (see below).
4. Connect your Akai APC Mini mk2 to your computer.

---

## loopMIDI Setup

1. Install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) (free, Windows).
2. Create **two virtual ports**:
   - `To Onyx` (Output for OSC/MIDI OUT to Onyx)
   - `From Onyx` (Input if you want to receive signals back – optional)
3. In Onyx:  
   - Set up MIDI Input/Output to these ports.
   - Enable OSC, configure IP and port 8000 (default).
4. In the Python script, select the correct APC MINI IN, OUT, and Onyx ports at startup.

---

## Operating Modes

### FADER MODE (FADERS 1-9 are usable)
 
- **Faders can work in either mode**
- **USE PLAYBACK SWAP**

### BUSK Mode (classic grid mode)
- **Default at startup** (or after exiting Keyboard Mode)
- **Visual Feedback:**
    - Grid pads are **off by default**
    - Press pad: **green**
    - Press again: **red**
    - Toggle green/red for GO/RELEASE on playback
- **Track Buttons:** red ON
- **Scene Launch Buttons:** green ON

- **REMEMBER THAT IN THIS MODE PADS ARE AVAILABLE FOR A 8X8 LAYOUT OF A PLAYBACK BUTTON PAGE**
- **REMEMBER THAT IN THIS MODE PADS ARE AVAILABLE FOR A 8X8 LAYOUT OF A PLAYBACK BUTTON PAGE**
- **REMEMBER THAT IN THIS MODE PADS ARE AVAILABLE FOR A 8X8 LAYOUT OF A PLAYBACK BUTTON PAGE**

### KEYBOARD Mode (keypad/command mode)
- **Activate with:** `SHIFT` (Scene Launch 7) + `Scene Launch 1` (top left)
- **Visual Feedback:**
    - All grid pads **blue** by default
    - Pads with OSC mapping (see `keypad_handler.py`): **yellow (amber)**
    - Press mapped OSC button: **green ONHOLD**, returns to amber when released

---

## Main Features

- **Full RGB LED feedback** on pads (blue, green, red, yellow, etc.)
- **OSC** sync with Onyx for fast commands (GO, RELEASE, blackout, bank select)
- **Bank Up/Down support:** quickly switch playback pages
- **Hardware fader support:** instant OSC values when moved
- **Blackout hardware button:** toggle directly from the controller
- **Easy mapping customization** (`keypad_handler.py`)
- **Clear debug/log messages** in the terminal

---

## Pad & Button Mapping

- **8x8 Grid:** Notes 0–63, standard AKAI numbering (rows/columns are inverted for the physical layout)
- **Track Buttons (0x64–0x6B):** red, can be customized
- **Scene Launch (0x70–0x77):** green, used for mode switch, shift, etc.
- **SHIFT:** `0x7A` (Scene Launch 7)
- **BANK UP/DOWN:** `0x75/0x74` (Scene Launch 6/5)
- **Blackout:** Notes 118/119

See `keypad-map.txt` for the full OSC (KEYBOARD) mapping.

---

## LED Feedback & Colors

Colors are set according to AKAI velocity values, see details in `led_memory.py` and the official documentation.  
**Examples:**
- `"green"` (velocity 0x21 or 33) – bright green
- `"red"` (velocity 0x05)
- `"amber"` (velocity 0x09) – yellow/orange
- `"blue"` (velocity 0x29) – standard blue

- **Grid pads:** 0x96 (channel 6), RGB color
- **Track/scene buttons:** 0x90 (channel 0), on/off (green/red)

---

## Special Commands

- **SHIFT + Scene Launch 1:** toggle Keyboard Mode
- **SHIFT:** also used for other custom functions (you can extend this)
- **BANK UP/DOWN:** switch playback pages
- **Blackout:** turns all lights on/off in Onyx

---

## Troubleshooting

- **Controller not found?**  
  - Check that the correct port is selected at script startup.
  - Close Ableton/other DAWs that might block the APC.
- **LEDs not lighting up?**  
  - Make sure you selected the correct OUT port to APC mini mk2 at startup.
- **OSC not working?**  
  - Double-check the IP/port for Onyx (default 8000) and ensure Onyx is listening on that port.
- **Faders not working?**  
  - Verify the correct MIDI ports are selected for Onyx.
- **loopMIDI not transmitting?**  
  - Check connection and correct assignment in Onyx and the script.

---

## Extending & Customizing

- You can modify OSC mapping in `keypad_handler.py`
- Add new modes or custom color schemes in `led_memory.py`
- For advanced feedback (e.g., feedback from Onyx to controller), consult the Onyx OSC documentation
- You can quickly adjust pad behavior to fit your specific project

---

## Contact

Script and documentation by [besoiuuworks].  
For support, questions, or collaboration: [patrickardelean1@gmail.com].

---

Happy programming & enjoy your show!
