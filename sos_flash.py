import time
import os

# Define Morse code timing
DOT_DURATION = 0.2   # seconds
DASH_DURATION = DOT_DURATION * 3
SYMBOL_PAUSE = DOT_DURATION
LETTER_PAUSE = DOT_DURATION * 3

# Morse code for SOS: ... --- ...
MORSE_SOS = ['.', '.', '.', '-', '-', '-', '.', '.', '.']

def flash(on: bool):
    os.system(f"termux-torch {'1' if on else '0'}")

def flash_symbol(symbol: str):
    duration = DOT_DURATION if symbol == '.' else DASH_DURATION
    flash(True)
    time.sleep(duration)
    flash(False)
    time.sleep(SYMBOL_PAUSE)

def flash_sos():
    print("Flashing SOS in Morse Code...")
    for symbol in MORSE_SOS:
        flash_symbol(symbol)
    flash(False)
    print("Done.")

if __name__ == "__main__":
    while True:
        flash_sos()
        time.sleep(5)  # Wait 5 seconds before repeating
