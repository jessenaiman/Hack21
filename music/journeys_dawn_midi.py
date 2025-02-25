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
    Creates a MIDI file for the composition "Journey's Dawn".
    Structure: A-B-A-C, with polyphony in the C section, over 1 minute long.
    Designed as theme music for an RPG game similar to Final Fantasy 1.
    """
    # Create a MidiFile object with 480 ticks per beat for precise timing
    mid = mido.MidiFile(ticks_per_beat=480)

    # Track 0: Tempo and time signature
    track0 = mido.MidiTrack()
    mid.tracks.append(track0)
    # Set tempo to 120 BPM (500,000 microseconds per quarter note)
    track0.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))
    # Set time signature to 4/4
    track0.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))

    # Track 1: Main melody (Trumpet, channel 0, program 56)
    track1 = mido.MidiTrack()
    mid.tracks.append(track1)
    track1.append(mido.Message('program_change', channel=0, program=56, time=0))

    # Track 2: Counter-melody (Flute, channel 1, program 73, only in C section)
    track2 = mido.MidiTrack()
    mid.tracks.append(track2)
    track2.append(mido.Message('program_change', channel=1, program=73, time=0))

    # Track 3: Harmony (String Ensemble, channel 2, program 48)
    track3 = mido.MidiTrack()
    mid.tracks.append(track3)
    track3.append(mido.Message('program_change', channel=2, program=48, time=0))

    # Define chord progressions for each section
    # Section A: Am - F - G - C | Am - F - G - E (8 bars)
    chords_a = [
        ('Am', [45, 48, 52]),  # A2, C3, E3
        ('F', [41, 45, 48]),   # F2, A2, C3
        ('G', [43, 47, 50]),   # G2, B2, D3
        ('C', [36, 40, 43]),   # C2, E2, G2
        ('Am', [45, 48, 52]),  # A2, C3, E3
        ('F', [41, 45, 48]),   # F2, A2, C3
        ('G', [43, 47, 50]),   # G2, B2, D3
        ('E', [40, 44, 47])    # E2, G#2, B2
    ]

    # Section B: C - G - Am - Em | F - C - G - C (8 bars)
    chords_b = [
        ('C', [36, 40, 43]),   # C2, E2, G2
        ('G', [43, 47, 50]),   # G2, B2, D3
        ('Am', [45, 48, 52]),  # A2, C3, E3
        ('Em', [40, 43, 47]),  # E2, G2, B2
        ('F', [41, 45, 48]),   # F2, A2, C3
        ('C', [36, 40, 43]),   # C2, E2, G2
        ('G', [43, 47, 50]),   # G2, B2, D3
        ('C', [36, 40, 43])    # C2, E2, G2
    ]

    # Section C: C - F - G - C | Am - F - G - C (8 bars)
    chords_c = [
        ('C', [36, 40, 43]),   # C2, E2, G2
        ('F', [41, 45, 48]),   # F2, A2, C3
        ('G', [43, 47, 50]),   # G2, B2, D3
        ('C', [36, 40, 43]),   # C2, E2, G2
        ('Am', [45, 48, 52]),  # A2, C3, E3
        ('F', [41, 45, 48]),   # F2, A2, C3
        ('G', [43, 47, 50]),   # G2, B2, D3
        ('C', [36, 40, 43])    # C2, E2, G2
    ]

    # Define main melody for Section A (quarter notes, 480 ticks)
    # 8 bars, 4 notes per bar, total 32 notes
    melody_a_notes = [
        # Bar 1: Am
        69, 72, 76, 81,  # A4, C5, E5, A5
        # Bar 2: F
        77, 72, 69, 65,  # F5, C5, A4, F4
        # Bar 3: G
        67, 71, 74, 79,  # G4, B4, D5, G5
        # Bar 4: C
        72, 76, 79, 84,  # C5, E5, G5, C6
        # Bar 5: Am
        81, 76, 72, 69,  # A5, E5, C5, A4
        # Bar 6: F
        65, 69, 72, 77,  # F4, A4, C5, F5
        # Bar 7: G
        79, 74, 71, 67,  # G5, D5, B4, G4
        # Bar 8: E
        64, 68, 71, 76   # E4, G#4, B4, E5
    ]
    melody_a_durations = [480] * 32

    # Define main melody for Section B (quarter notes, 480 ticks)
    # 8 bars, 4 notes per bar, total 32 notes
    melody_b_notes = [
        # Bar 1: C
        72, 67, 64, 60,  # C5, G4, E4, C4
        # Bar 2: G
        71, 74, 79, 74,  # B4, D5, G5, D5
        # Bar 3: Am
        69, 72, 76, 72,  # A4, C5, E5, C5
        # Bar 4: Em
        67, 71, 74, 71,  # G4, B4, D5, B4
        # Bar 5: F
        65, 69, 72, 77,  # F4, A4, C5, F5
        # Bar 6: C
        72, 76, 79, 84,  # C5, E5, G5, C6
        # Bar 7: G
        79, 74, 71, 67,  # G5, D5, B4, G4
        # Bar 8: C
        72, 67, 64, 60   # C5, G4, E4, C4
    ]
    melody_b_durations = [480] * 32

    # Define main melody for Section C (triplet eighth notes, 160 ticks)
    # 8 bars, 12 notes per bar, total 96 notes
    melody_c_notes = []
    for chord in chords_c:
        # Define arpeggio patterns for each chord
        if chord[0] == 'C':
            # C4, E4, G4, C5, E5, G5, C6, G5, E5, C5, G4, E4
            notes = [60, 64, 67, 72, 76, 79, 84, 79, 76, 72, 67, 64]
        elif chord[0] == 'F':
            # F4, A4, C5, F5, A5, C6, F6, C6, A5, F5, C5, A4
            notes = [65, 69, 72, 77, 81, 84, 89, 84, 81, 77, 72, 69]
        elif chord[0] == 'G':
            # G4, B4, D5, G5, B5, D6, G6, D6, B5, G5, D5, B4
            notes = [67, 71, 74, 79, 83, 86, 91, 86, 83, 79, 74, 71]
        elif chord[0] == 'Am':
            # A4, C5, E5, A5, C6, E6, A6, E6, C6, A5, E5, C5
            notes = [69, 72, 76, 81, 84, 88, 93, 88, 84, 81, 76, 72]
        else:
            # Default to C chord pattern
            notes = [60, 64, 67, 72, 76, 79, 84, 79, 76, 72, 67, 64]
        melody_c_notes.extend(notes)
    melody_c_durations = [160] * 96

    # Combine main melody for all sections (A-B-A-C)
    all_melody_notes = melody_a_notes + melody_b_notes + melody_a_notes + melody_c_notes
    all_melody_durations = melody_a_durations + melody_b_durations + melody_a_durations + melody_c_durations

    # Add main melody to track1 (Trumpet, channel 0)
    for note, duration in zip(all_melody_notes, all_melody_durations):
        track1.append(mido.Message('note_on', channel=0, note=note, velocity=64, time=0))
        track1.append(mido.Message('note_off', channel=0, note=note, velocity=0, time=duration))

    # Define counter-melody for Section C (whole notes, root of each chord)
    # Transpose root notes up one octave for clarity
    counter_melody_notes = [chord[1][0] + 12 for chord in chords_c]
    counter_melody_durations = [1920] * 8  # One whole note per bar

    # Calculate start time for counter-melody (start of Section C)
    t_c = sum(melody_a_durations + melody_b_durations + melody_a_durations)  # Time after A + B + A
    # Add counter-melody to track2 (Flute, channel 1)
    for i, (note, duration) in enumerate(zip(counter_melody_notes, counter_melody_durations)):
        track2.append(mido.Message('note_on', channel=1, note=note, velocity=64, time=t_c if i == 0 else 0))
        track2.append(mido.Message('note_off', channel=1, note=note, velocity=0, time=duration))
        t_c = 0  # Subsequent notes start immediately after the previous one

    # Combine all chords for harmony tracks (A + B + A + C)
    all_chords = chords_a + chords_b + chords_a + chords_c

    # Add harmony to track3 (String Ensemble, channel 2)
    for chord in all_chords:
        chord_notes = chord[1]  # List of MIDI note numbers for the chord
        # Add note_on for all chord notes at the start of the bar
        for note in chord_notes:
            track3.append(mido.Message('note_on', channel=2, note=note, velocity=64, time=0))
        # Add note_off for all chord notes after one bar (1920 ticks)
        track3.append(mido.Message('note_off', channel=2, note=chord_notes[0], velocity=0, time=1920))
        for note in chord_notes[1:]:
            track3.append(mido.Message('note_off', channel=2, note=note, velocity=0, time=0))

    # Save the MIDI file in the specified song directory
    filepath = os.path.join(SONG_DIR, filename)
    mid.save(filepath)
    return filepath

# Create and play the MIDI file
midi_file = create_midi_file('journeys_dawn.mid')
pygame.init()
pygame.mixer.music.load(midi_file)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    time.sleep(1)

print(f"Song finished playing. MIDI file saved as '{midi_file}'.")