import json
import csv
import random
import time
import re
import pygame
import numpy as np
import os

MORSE_TO_ALPHA_DICT = 'data\\morse-to-alpha.json'
ALPHA_TO_MORSE_DICT = 'data\\alpha-to-morse.json'
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

cwd = os.getcwd()

def initialize_mixer():
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
        print("Pygame mixer initialized successfully.")
    except pygame.error as e:
        print(f"Failed to initialize mixer: {e}")
        return False
    return True

# Get random quote
def get_quote():
    file_path = os.join(cwd, 'data\\quotes.csv')
    with open(file_path, 'r') as file:
        quotes = list(csv.reader(file))
        return quotes[random.randint(1, len(quotes) - 1)]

def generate_tone(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = 0.5 * np.sin(2 * np.pi * frequency * t)  # Generate sine wave
    audio = (audio * 32767).astype(np.int16)  # Convert to 16-bit PCM
    
    # Reshape to 2D array for compatibility with pygame's Sound mixer
    audio = np.repeat(audio, 2).reshape(-1, 2)
    sound = pygame.sndarray.make_sound(audio)
    return sound

# Play a tone directly from the generated sound object
def play_tone(frequency, duration):
    sound = generate_tone(frequency, duration)
    sound.play()
    time.sleep(duration)  # Wait for the duration of the tone
    sound.stop()

# Morse code playback function with variable WPM
def morse_code_play(message, wpm=20, frequency=700):
    unit = 60 / (50 * wpm)  # Calculate dot duration based on WPM
    with open(ALPHA_TO_MORSE_DICT, 'r') as file:
        morseCode = json.load(file)
        for char in message.upper():
            if char == ' ':
                time.sleep(7 * unit)  # Word space
            elif char in morseCode:
                for symbol in morseCode[char]:
                    if symbol == '.':
                        play_tone(frequency, unit)  # Dot
                    elif symbol == '-':
                        play_tone(frequency, 3 * unit)  # Dash
                    time.sleep(unit)  # Space between symbols
                time.sleep(3 * unit)  # Space between letters

def encode_text(quote):
    with open(ALPHA_TO_MORSE_DICT, 'r') as file:
        morseCode = json.load(file)
        encoded = [morseCode[c.upper()] + '  ' if c != ' ' else '/  ' for c in quote]
        return ''.join(encoded)

def decode(quote):
    with open(MORSE_TO_ALPHA_DICT, 'r') as file:
        morseCode = json.load(file)
        characters = quote.split('  ')
        decoded = [morseCode[c] if c != '/' else ' ' for c in characters]
        return ''.join(decoded)
    
def type_text(quote, text_delay=0.02, cursor_blink_delay=0.25, cursor_duration=1):
    sentences = re.split(r'(?<=[.!?])\s+', quote)
    # text_delay = 0.05
    # cursor_blink_delay = 0.5
    # cursor_duration = 2
    
    for s in sentences:
        # print('\r', end='')
        for c in s:
            print(RED + c, end='', flush=True)
            if c in ['\n', '.', ',', ':', ';', '?', '!']:
                print(' ', end='', flush=True)
                cursor = '_'
                end_time = time.time() + cursor_duration
                while time.time() < end_time:
                    print(cursor, end='', flush=True)  # Show cursor
                    time.sleep(cursor_blink_delay)
                    print('\b \b', end='', flush=True)  # Hide cursor
                    time.sleep(cursor_blink_delay)
            else:
                time.sleep(text_delay)
    print(f'{RESET}\n')

test = 'Hello world'
decodeTest = '''...  ---  --  .  /  .--.  .  ---  .--.  .-..  .  /  ...  .-  -.--  --..--'''
printTest = 'Hello! My name is Morrison. Are you ready to play?'
# print(encode(get_quote()[1]))
# print(decode(decodeTest))
# print(type_text(printTest))
# if initialize_mixer():
#     morse_code_play("I love Lyndsey", wpm=20)
# else:
#     print("Could not initialize the mixer. Please check your audio settings.")
