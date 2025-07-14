# APC MINI MK2 ➔ ONYX OSC MIDI Bridge

**Full control and visual feedback for Obsidian Onyx using the Akai APC Mini MK2**  
Python-based integration: fast setup, robust features, custom mapping!

---

## Table of Contents

- [Description](#description)
- [Requirements & Installation](#requirements--installation)
- [loopMIDI & Loopback OSC Setup](#loopmidi--loopback-osc-setup)
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
- **Obsidian ONYX**
- **loopMIDI** (Windows) or an equivalent (IAC, qjackctl) on Mac/Linux
- **python-rtmidi**, **python-osc** and all dependencies from `requirements.txt`

### Quick Install

1. Clone this repo or copy the source files.
2. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up **loopMIDI** and the OSC loopback network adapter (see next section!)
4. Connect your Akai APC Mini mk2 to your computer.

---

## loopMIDI & Loopback OSC Setup

> **⚠️ OSC Loopback Requirement:**  
> For this script to communicate with ONYX on Windows, you must install a loopback network adapter and set IP **`10.0.0.100`** for OSC.  
> ONYX will **not** accept `127.0.0.1` (“localhost”).  
> See instructions below.

### loopMIDI Steps

1. Install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) (free, Windows).
2. Create two virtual MIDI ports:
   - `To Onyx` (output from Python script to Onyx)
   - `From Onyx` (optional: for feedback, not required for basic operation)
3. In ONYX, assign these for MIDI IN/OUT.

### OSC Loopback IP Setup

**Without this, OSC will not work!**

1. Open Device Manager → **Add legacy hardware** → **Microsoft KM-TEST Loopback Adapter**
2. In Network Connections, right-click the new adapter, go to “Properties”, set IPv4 to **`10.0.0.100`** (`255.255.255.0`)
3. In ONYX, go to **Settings > OSC**:
   - Set OSC IP address: **`10.0.0.100`**
   - Set OSC port: **8000** (default in this script)
4. The Python script is preconfigured for this OSC endpoint.
5. At script startup, select the correct **APC MINI IN, OUT, and Onyx** ports.

> If you skip this step, OSC playback, fader, and blackout commands **will NOT work**!

---

## Operating Modes

### FADER MODE (FADERS 1-9 usable)

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

- **In this mode pads are mapped as an 8x8 playback button page in ONYX**

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
  - Double-check the IP/port for Onyx (`10.0.0.100:8000`), and ensure Onyx is listening on that port.
  - Make sure your loopback adapter is set up as above.
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
