import mido
import pygame
import time
import os

# Define the directory where MIDI files will be saved
SONG_DIR = "songs"

# Ensure the song directory exists
if not os.path.exists(SONG_DIR):
    os.makedirs(SONG_DIR)

def create_midi_file(filename):
    """
    Creates a MIDI file for an original composition: "Whispers of the Eldergrove".
    Inspired by Baroque composers like J.S. Bach, featuring polyphony and ornamentation.
    Designed for a mystical forest biome in an RPG game, over 1 minute long.
    Structure: A (8 bars) - B (8 bars) - A' (8 bars) - Coda (8 bars with polyphony).
    """
    # Initialize MidiFile with 480 ticks per beat for precise timing
    mid = mido.MidiFile(ticks_per_beat=480)

    # **Track 0: Tempo and Time Signature**
    track0 = mido.MidiTrack()
    mid.tracks.append(track0)
    # Set tempo to 85 BPM (705,882 microseconds per quarter note)
    track0.append(mido.MetaMessage('set_tempo', tempo=705882, time=0))
    # Set time signature to 3/4, reflecting a Baroque dance-like feel
    track0.append(mido.MetaMessage('time_signature', numerator=3, denominator=4, time=0))

    # **Track 1: Main Melody (Flute, channel 0, program 73)**
    track1 = mido.MidiTrack()
    mid.tracks.append(track1)
    track1.append(mido.Message('program_change', channel=0, program=73, time=0))

    # **Track 2: Counter-Melody (Flute, channel 1, program 73, in Coda)**
    track2 = mido.MidiTrack()
    mid.tracks.append(track2)
    track2.append(mido.Message('program_change', channel=1, program=73, time=0))

    # **Track 3: Harp (channel 2, program 46)**
    track3 = mido.MidiTrack()
    mid.tracks.append(track3)
    track3.append(mido.Message('program_change', channel=2, program=46, time=0))

    # **Track 4: Strings (channel 3, program 48)**
    track4 = mido.MidiTrack()
    mid.tracks.append(track4)
    track4.append(mido.Message('program_change', channel=3, program=48, time=0))

    # Define chord progressions in F# minor (Aeolian mode) for a mystical, somber tone
    chords = [
        # Section A (bars 1-8): F#m - E - D - Bm | F#m - E - D - E
        ('F#m', [54, 57, 61]), ('E', [52, 56, 61]), ('D', [50, 54, 57]), ('Bm', [47, 50, 54]),
        ('F#m', [54, 57, 61]), ('E', [52, 56, 61]), ('D', [50, 54, 57]), ('E', [52, 56, 61]),
        # Section B (bars 9-16): A - E - F#m - D | A - E - F#m - E
        ('A', [57, 61, 64]), ('E', [52, 56, 61]), ('F#m', [54, 57, 61]), ('D', [50, 54, 57]),
        ('A', [57, 61, 64]), ('E', [52, 56, 61]), ('F#m', [54, 57, 61]), ('E', [52, 56, 61]),
        # Section A' (bars 17-24): Same as A
        ('F#m', [54, 57, 61]), ('E', [52, 56, 61]), ('D', [50, 54, 57]), ('Bm', [47, 50, 54]),
        ('F#m', [54, 57, 61]), ('E', [52, 56, 61]), ('D', [50, 54, 57]), ('E', [52, 56, 61]),
        # Coda (bars 25-32): F#m - E - D - Bm | F#m - E - D - F#m
        ('F#m', [54, 57, 61]), ('E', [52, 56, 61]), ('D', [50, 54, 57]), ('Bm', [47, 50, 54]),
        ('F#m', [54, 57, 61]), ('E', [52, 56, 61]), ('D', [50, 54, 57]), ('F#m', [54, 57, 61])
    ]

    # **Main Melody (Track 1)**
    # In 3/4 time, one bar = 1440 ticks (480 ticks per quarter note * 3 beats)

    # --- Section A ---
    # Bar 1: F#4 dotted quarter, G#4 eighth, A4 quarter
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=720))
    track1.append(mido.Message('note_on', channel=0, note=68, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=68, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=480))

    # Bar 2: B4 quarter, A4 eighth, G#4 eighth, F#4 quarter
    track1.append(mido.Message('note_on', channel=0, note=71, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=71, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=68, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=68, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=480))

    # Bar 3: A4 dotted quarter, F#4 eighth, E4 quarter
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=720))
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=64, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=64, velocity=0, time=480))

    # Bar 4: D4 quarter, E4 quarter, F#4 quarter
    track1.append(mido.Message('note_on', channel=0, note=62, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=62, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=64, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=64, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=480))

    # Bar 5: F#4 dotted quarter, A4 eighth, B4 quarter
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=720))
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=71, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=71, velocity=0, time=480))

    # Bar 6: C#5 quarter, B4 eighth, A4 eighth, G#4 quarter
    track1.append(mido.Message('note_on', channel=0, note=73, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=73, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=71, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=71, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=68, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=68, velocity=0, time=480))

    # Bar 7: F#4 quarter, E4 quarter, D4 quarter
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=64, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=64, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=62, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=62, velocity=0, time=480))

    # Bar 8: E4 dotted quarter, F#4 eighth, G#4 quarter
    track1.append(mido.Message('note_on', channel=0, note=64, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=64, velocity=0, time=720))
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=68, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=68, velocity=0, time=480))

    # --- Section B ---
    # Bar 9: A4 half, C#5 quarter
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=960))
    track1.append(mido.Message('note_on', channel=0, note=73, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=73, velocity=0, time=480))

    # Bar 10: E5 quarter, D5 quarter, B4 quarter
    track1.append(mido.Message('note_on', channel=0, note=76, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=76, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=74, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=74, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=71, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=71, velocity=0, time=480))

    # Bar 11: A4 dotted quarter, F#4 eighth, E4 quarter
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=720))
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=64, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=64, velocity=0, time=480))

    # Bar 12: D5 quarter, C#5 quarter, A4 quarter
    track1.append(mido.Message('note_on', channel=0, note=74, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=74, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=73, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=73, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=480))

    # Bar 13: A4 half, B4 quarter
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=960))
    track1.append(mido.Message('note_on', channel=0, note=71, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=71, velocity=0, time=480))

    # Bar 14: C#5 quarter, D5 quarter, E5 quarter
    track1.append(mido.Message('note_on', channel=0, note=73, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=73, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=74, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=74, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=76, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=76, velocity=0, time=480))

    # Bar 15: F#5 dotted quarter, E5 eighth, D5 quarter
    track1.append(mido.Message('note_on', channel=0, note=78, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=78, velocity=0, time=720))
    track1.append(mido.Message('note_on', channel=0, note=76, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=76, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=74, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=74, velocity=0, time=480))

    # Bar 16: E5 half, F#5 quarter
    track1.append(mido.Message('note_on', channel=0, note=76, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=76, velocity=0, time=960))
    track1.append(mido.Message('note_on', channel=0, note=78, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=78, velocity=0, time=480))

    # --- Section A' (Bars 17-24) ---
    # Repeat Section A with slight ornamentation for variety
    # Bar 17: F#4 dotted quarter, G#4 eighth (trill to A4), A4 quarter
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=720))
    track1.append(mido.Message('note_on', channel=0, note=68, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=68, velocity=0, time=120))
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=120))
    track1.append(mido.Message('note_on', channel=0, note=68, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=68, velocity=0, time=120))
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=480))

    # Bar 18: B4 quarter, A4 eighth, G#4 eighth, F#4 quarter
    track1.append(mido.Message('note_on', channel=0, note=71, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=71, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=68, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=68, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=480))

    # Bar 19: A4 dotted quarter, F#4 eighth, E4 quarter
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=720))
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=64, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=64, velocity=0, time=480))

    # Bar 20: D4 quarter, E4 quarter, F#4 quarter
    track1.append(mido.Message('note_on', channel=0, note=62, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=62, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=64, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=64, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=480))

    # Bar 21: F#4 dotted quarter, A4 eighth, B4 quarter
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=720))
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=71, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=71, velocity=0, time=480))

    # Bar 22: C#5 quarter, B4 eighth, A4 eighth, G#4 quarter
    track1.append(mido.Message('note_on', channel=0, note=73, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=73, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=71, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=71, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=68, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=68, velocity=0, time=480))

    # Bar 23: F#4 quarter, E4 quarter, D4 quarter
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=64, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=64, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=62, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=62, velocity=0, time=480))

    # Bar 24: E4 dotted quarter, F#4 eighth, G#4 quarter
    track1.append(mido.Message('note_on', channel=0, note=64, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=64, velocity=0, time=720))
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=68, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=68, velocity=0, time=480))

    # --- Coda (Bars 25-32) ---
    # Polyphonic section with counter-melody
    # Repeat melody from Section A, bars 1-8
    # Bar 25
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=720))
    track1.append(mido.Message('note_on', channel=0, note=68, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=68, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=480))

    # Bar 26
    track1.append(mido.Message('note_on', channel=0, note=71, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=71, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=68, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=68, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=480))

    # Bar 27
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=720))
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=64, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=64, velocity=0, time=480))

    # Bar 28
    track1.append(mido.Message('note_on', channel=0, note=62, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=62, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=64, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=64, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=480))

    # Bar 29
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=720))
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=71, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=71, velocity=0, time=480))

    # Bar 30
    track1.append(mido.Message('note_on', channel=0, note=73, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=73, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=71, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=71, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=69, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=69, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=68, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=68, velocity=0, time=480))

    # Bar 31
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=64, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=64, velocity=0, time=480))
    track1.append(mido.Message('note_on', channel=0, note=62, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=62, velocity=0, time=480))

    # Bar 32
    track1.append(mido.Message('note_on', channel=0, note=64, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=64, velocity=0, time=720))
    track1.append(mido.Message('note_on', channel=0, note=66, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=66, velocity=0, time=240))
    track1.append(mido.Message('note_on', channel=0, note=68, velocity=80, time=0))
    track1.append(mido.Message('note_off', channel=0, note=68, velocity=0, time=480))

    # **Counter-Melody (Track 2) for Coda**
    # Starts 3 bars into the Coda (bar 28), delayed by 3 * 1440 = 4320 ticks
    counter_start = 27 * 1440  # After 24 bars (A+B+A') + 3 bars into Coda
    # Bar 28 of counter-melody (same as bar 1 of main melody)
    track2.append(mido.Message('note_on', channel=1, note=66, velocity=60, time=counter_start))
    track2.append(mido.Message('note_off', channel=1, note=66, velocity=0, time=720))
    track2.append(mido.Message('note_on', channel=1, note=68, velocity=60, time=0))
    track2.append(mido.Message('note_off', channel=1, note=68, velocity=0, time=240))
    track2.append(mido.Message('note_on', channel=1, note=69, velocity=60, time=0))
    track2.append(mido.Message('note_off', channel=1, note=69, velocity=0, time=480))

    # Bar 29
    track2.append(mido.Message('note_on', channel=1, note=71, velocity=60, time=0))
    track2.append(mido.Message('note_off', channel=1, note=71, velocity=0, time=480))
    track2.append(mido.Message('note_on', channel=1, note=69, velocity=60, time=0))
    track2.append(mido.Message('note_off', channel=1, note=69, velocity=0, time=240))
    track2.append(mido.Message('note_on', channel=1, note=68, velocity=60, time=0))
    track2.append(mido.Message('note_off', channel=1, note=68, velocity=0, time=240))
    track2.append(mido.Message('note_on', channel=1, note=66, velocity=60, time=0))
    track2.append(mido.Message('note_off', channel=1, note=66, velocity=0, time=480))

    # Bar 30
    track2.append(mido.Message('note_on', channel=1, note=69, velocity=60, time=0))
    track2.append(mido.Message('note_off', channel=1, note=69, velocity=0, time=720))
    track2.append(mido.Message('note_on', channel=1, note=66, velocity=60, time=0))
    track2.append(mido.Message('note_off', channel=1, note=66, velocity=0, time=240))
    track2.append(mido.Message('note_on', channel=1, note=64, velocity=60, time=0))
    track2.append(mido.Message('note_off', channel=1, note=64, velocity=0, time=480))

    # Bar 31
    track2.append(mido.Message('note_on', channel=1, note=62, velocity=60, time=0))
    track2.append(mido.Message('note_off', channel=1, note=62, velocity=0, time=480))
    track2.append(mido.Message('note_on', channel=1, note=64, velocity=60, time=0))
    track2.append(mido.Message('note_off', channel=1, note=64, velocity=0, time=480))
    track2.append(mido.Message('note_on', channel=1, note=66, velocity=60, time=0))
    track2.append(mido.Message('note_off', channel=1, note=66, velocity=0, time=480))

    # Bar 32
    track2.append(mido.Message('note_on', channel=1, note=66, velocity=60, time=0))
    track2.append(mido.Message('note_off', channel=1, note=66, velocity=0, time=720))
    track2.append(mido.Message('note_on', channel=1, note=69, velocity=60, time=0))
    track2.append(mido.Message('note_off', channel=1, note=69, velocity=0, time=240))
    track2.append(mido.Message('note_on', channel=1, note=71, velocity=60, time=0))
    track2.append(mido.Message('note_off', channel=1, note=71, velocity=0, time=480))

    # **Harp Arpeggios (Track 3)**
    # Each bar has 6 eighth notes (1440 ticks total)
    for chord in chords:
        root, third, fifth = chord[1]
        arpeggio = [root, third, fifth, root, third, fifth]
        for note in arpeggio:
            track3.append(mido.Message('note_on', channel=2, note=note, velocity=50, time=0))
            track3.append(mido.Message('note_off', channel=2, note=note, velocity=0, time=240))

    # **String Harmonies (Track 4)**
    # Each chord sustains for one bar (1440 ticks)
    for chord in chords:
        chord_notes = chord[1]
        for note in chord_notes:
            track4.append(mido.Message('note_on', channel=3, note=note, velocity=50, time=0))
        track4.append(mido.Message('note_off', channel=3, note=chord_notes[0], velocity=0, time=1440))
        for note in chord_notes[1:]:
            track4.append(mido.Message('note_off', channel=3, note=note, velocity=0, time=0))

    # Save the MIDI file
    filepath = os.path.join(SONG_DIR, filename)
    mid.save(filepath)
    return filepath

# Create and play the MIDI file
midi_file = create_midi_file('whispers_of_the_eldergrove.mid')
pygame.init()
pygame.mixer.music.load(midi_file)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    time.sleep(1)

print(f"Song finished playing. MIDI file saved as '{midi_file}'.")