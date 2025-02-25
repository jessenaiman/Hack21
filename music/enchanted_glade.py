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
    Creates a MIDI file for the composition "Whispers of the Enchanted Glade".
    Structure: A-B-A-C, with polyphony in the C section, over 1 minute long.
    Designed for a mystical forest biome in an RPG game.
    """
    # Create a MidiFile object with 480 ticks per beat for precise timing
    mid = mido.MidiFile(ticks_per_beat=480)

    # Track 0: Tempo and time signature
    track0 = mido.MidiTrack()
    mid.tracks.append(track0)
    # Set tempo to 90 BPM (666,667 microseconds per quarter note)
    track0.append(mido.MetaMessage('set_tempo', tempo=666667, time=0))
    # Set time signature to 4/4
    track0.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))

    # Track 1: Main melody (Flute, channel 0, program 73)
    track1 = mido.MidiTrack()
    mid.tracks.append(track1)
    track1.append(mido.Message('program_change', channel=0, program=73, time=0))

    # Track 2: Counter-melody (Flute, channel 1, program 73, only in C section)
    track2 = mido.MidiTrack()
    mid.tracks.append(track2)
    track2.append(mido.Message('program_change', channel=1, program=73, time=0))

    # Track 3: Harp (channel 2, program 46)
    track3 = mido.MidiTrack()
    mid.tracks.append(track3)
    track3.append(mido.Message('program_change', channel=2, program=46, time=0))

    # Track 4: Strings (channel 3, program 48)
    track4 = mido.MidiTrack()
    mid.tracks.append(track4)
    track4.append(mido.Message('program_change', channel=3, program=48, time=0))

    # Define chord progressions for each section
    # Section A and C: Am - G - F - E | Am - G - F - E (8 bars)
    # Section B: Dm - Am - E - Am | Dm - Am - E - Am (8 bars)
    chords = [
        # Section A (bars 1-8)
        ('Am', [45, 48, 52]), ('G', [43, 47, 50]), ('F', [41, 45, 48]), ('E', [40, 44, 47]),
        ('Am', [45, 48, 52]), ('G', [43, 47, 50]), ('F', [41, 45, 48]), ('E', [40, 44, 47]),
        # Section B (bars 9-16)
        ('Dm', [38, 41, 45]), ('Am', [45, 48, 52]), ('E', [40, 44, 47]), ('Am', [45, 48, 52]),
        ('Dm', [38, 41, 45]), ('Am', [45, 48, 52]), ('E', [40, 44, 47]), ('Am', [45, 48, 52]),
        # Section A' (bars 17-24)
        ('Am', [45, 48, 52]), ('G', [43, 47, 50]), ('F', [41, 45, 48]), ('E', [40, 44, 47]),
        ('Am', [45, 48, 52]), ('G', [43, 47, 50]), ('F', [41, 45, 48]), ('E', [40, 44, 47]),
        # Section C (bars 25-32)
        ('Am', [45, 48, 52]), ('G', [43, 47, 50]), ('F', [41, 45, 48]), ('E', [40, 44, 47]),
        ('Am', [45, 48, 52]), ('G', [43, 47, 50]), ('F', [41, 45, 48]), ('E', [40, 44, 47])
    ]

    # Define main melody for Section A (quarter notes, 480 ticks)
    # 8 bars, 4 notes per bar, total 32 notes
    melody_a_notes = [
        # Bar 1: Am
        69, 72, 76, 72,  # A4, C5, E5, C5
        # Bar 2: G
        67, 71, 74, 71,  # G4, B4, D5, B4
        # Bar 3: F
        65, 69, 72, 69,  # F4, A4, C5, A4
        # Bar 4: E
        64, 68, 71, 68,  # E4, G#4, B4, G#4
        # Bar 5: Am
        69, 72, 76, 72,
        # Bar 6: G
        67, 71, 74, 71,
        # Bar 7: F
        65, 69, 72, 69,
        # Bar 8: E
        64, 68, 71, 68
    ]
    melody_a_durations = [480] * 32

    # Define main melody for Section B (quarter notes, 480 ticks)
    # 8 bars, 4 notes per bar, total 32 notes
    melody_b_notes = [
        # Bar 9: Dm
        74, 77, 81, 77,  # D5, F5, A5, F5
        # Bar 10: Am
        72, 76, 81, 76,  # C5, E5, A5, E5
        # Bar 11: E
        71, 68, 64, 68,  # B4, G#4, E4, G#4
        # Bar 12: Am
        69, 72, 76, 72,  # A4, C5, E5, C5
        # Bar 13: Dm
        74, 77, 81, 77,
        # Bar 14: Am
        72, 76, 81, 76,
        # Bar 15: E
        71, 68, 64, 68,
        # Bar 16: Am
        69, 72, 76, 72
    ]
    melody_b_durations = [480] * 32

    # Combine main melody for all sections (A-B-A-C)
    all_melody_notes = melody_a_notes + melody_b_notes + melody_a_notes + melody_a_notes
    all_melody_durations = melody_a_durations + melody_b_durations + melody_a_durations + melody_a_durations

    # Add main melody to track1 (Flute, channel 0)
    for note, duration in zip(all_melody_notes, all_melody_durations):
        track1.append(mido.Message('note_on', channel=0, note=note, velocity=64, time=0))
        track1.append(mido.Message('note_off', channel=0, note=note, velocity=0, time=duration))

    # Define counter-melody for Section C (same as melody_a_notes, delayed by 2 bars)
    counter_melody_notes = melody_a_notes
    counter_melody_durations = melody_a_durations
    start_time = 26 * 1920  # Start after 26 bars (sections A-B-A + 2 bars into C)

    # Add counter-melody to track2 (Flute, channel 1)
    track2.append(mido.Message('note_on', channel=1, note=counter_melody_notes[0], velocity=64, time=start_time))
    track2.append(mido.Message('note_off', channel=1, note=counter_melody_notes[0], velocity=0, time=counter_melody_durations[0]))
    for note, duration in zip(counter_melody_notes[1:], counter_melody_durations[1:]):
        track2.append(mido.Message('note_on', channel=1, note=note, velocity=64, time=0))
        track2.append(mido.Message('note_off', channel=1, note=note, velocity=0, time=duration))

    # Add harp arpeggios to track3 (Harp, channel 2)
    for chord in chords:
        # Define arpeggio pattern: root (octave 3), fifth (octave 4), third (octave 4), fifth (octave 4), repeat
        root = chord[1][0] + 12  # Root in octave 3
        third = chord[1][1] + 12  # Third in octave 4
        fifth = chord[1][2] + 12  # Fifth in octave 4
        harp_notes = [root, fifth, third, fifth] * 2  # 8 eighth notes per bar
        for note in harp_notes:
            track3.append(mido.Message('note_on', channel=2, note=note, velocity=64, time=0))
            track3.append(mido.Message('note_off', channel=2, note=note, velocity=0, time=240))

    # Add string harmonies to track4 (Strings, channel 3)
    for chord in chords:
        chord_notes = chord[1]  # Notes for the chord (e.g., [45, 48, 52] for Am)
        # Add note_on for all chord notes at the start of the bar
        for note in chord_notes:
            track4.append(mido.Message('note_on', channel=3, note=note, velocity=64, time=0))
        # Add note_off for all chord notes after 1920 ticks (one bar)
        track4.append(mido.Message('note_off', channel=3, note=chord_notes[0], velocity=0, time=1920))
        for note in chord_notes[1:]:
            track4.append(mido.Message('note_off', channel=3, note=note, velocity=0, time=0))

    # Save the MIDI file in the specified song directory
    filepath = os.path.join(SONG_DIR, filename)
    mid.save(filepath)
    return filepath

# Create and play the MIDI file
midi_file = create_midi_file('whispers_of_the_enchanted_glade.mid')
pygame.init()
pygame.mixer.music.load(midi_file)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    time.sleep(1)

print(f"Song finished playing. MIDI file saved as '{midi_file}'.")