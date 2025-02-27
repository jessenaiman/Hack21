import mido
import pygame
import time

# Function to create the MIDI file
def create_midi_file(filename):
    """
    Generates a MIDI file for "Whispers of the Forest" with a serene yet adventurous feel.
    Structure: A-B-C-D, with a seamless looping ending.
    """
    mid = mido.MidiFile(ticks_per_beat=480)

    # Track 0: Tempo and time signature
    track0 = mido.MidiTrack()
    mid.tracks.append(track0)
    # Set tempo to 100 BPM (600,000 microseconds per quarter note)
    track0.append(mido.MetaMessage('set_tempo', tempo=600000, time=0))
    track0.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))

    # Track 1: Main melody (Acoustic Guitar, channel 0)
    track1 = mido.MidiTrack()
    mid.tracks.append(track1)
    track1.append(mido.Message('program_change', channel=0, program=24, time=0))  # Nylon Guitar

    # Track 2: Harmony and counter-melody (Harp, channel 1)
    track2 = mido.MidiTrack()
    mid.tracks.append(track2)
    track2.append(mido.Message('program_change', channel=1, program=46, time=0))  # Harp

    # Track 3: Bass (Cello, channel 2)
    track3 = mido.MidiTrack()
    mid.tracks.append(track3)
    track3.append(mido.Message('program_change', channel=2, program=42, time=0))  # Cello

    # Define chord progressions for each section
    chords_a = [
        ('G', [43, 47, 50, 55]),  # G2, B2, D3, G3
        ('C', [48, 52, 55, 60]),  # C3, E3, G3, C4
        ('D', [50, 54, 57, 62]),  # D3, F#3, A3, D4
        ('Em', [51, 55, 58, 63]),  # E3, G3, B3, E4
        ('G', [43, 47, 50, 55]),
        ('Am', [45, 48, 52, 57]),  # A2, C3, E3, A3
        ('Bm', [47, 50, 54, 59]),  # B2, D3, F#3, B3
        ('C', [48, 52, 55, 60])
    ]
    chords_b = [
        ('Em', [51, 55, 58, 63]),
        ('Bm', [47, 50, 54, 59]),
        ('C', [48, 52, 55, 60]),
        ('G', [43, 47, 50, 55]),
        ('Em', [51, 55, 58, 63]),
        ('Am', [45, 48, 52, 57]),
        ('D', [50, 54, 57, 62]),
        ('G', [43, 47, 50, 55])
    ]
    chords_c = [
        ('G', [43, 47, 50, 55]),
        ('D', [50, 54, 57, 62]),
        ('Em', [51, 55, 58, 63]),
        ('C', [48, 52, 55, 60]),
        ('G', [43, 47, 50, 55]),
        ('Am', [45, 48, 52, 57]),
        ('Bm', [47, 50, 54, 59]),
        ('D', [50, 54, 57, 62])
    ]
    chords_d = [
        ('G', [43, 47, 50, 55]),
        ('C', [48, 52, 55, 60]),
        ('D', [50, 54, 57, 62]),
        ('G', [43, 47, 50, 55])
    ]

    # Define melody for A section (quarter and half notes)
    melody_a_notes = [
        # Bar 1: G
        67, 71, 74, 79,  # G4, B4, D5, G5 (quarter notes)
        # Bar 2: C
        72, 76, 79, 84,  # C5, E5, G5, C6
        # Bar 3: D
        74, 78, 81, 86,  # D5, F#5, A5, D6
        # Bar 4: Em
        75, 79, 82, 87,  # E5, G5, B5, E6
        # Bar 5: G
        67, 71, 74, 79,
        # Bar 6: Am
        69, 72, 76, 81,  # A4, C5, E5, A5
        # Bar 7: Bm
        71, 74, 78, 83,  # B4, D5, F#5, B5
        # Bar 8: C
        72, 76, 79, 84
    ]
    melody_a_durations = [480] * 32  # Quarter notes (480 ticks)

    # Define melody for B section (eighth notes with syncopation)
    melody_b_notes = [
        # Bar 1: Em
        75, 76, 75, 74, 75, 76, 75, 74,  # E5, F5, E5, D5, etc.
        # Bar 2: Bm
        71, 72, 71, 70, 71, 72, 71, 70,  # B4, C5, B4, A4, etc.
        # Bar 3: C
        72, 73, 72, 71, 72, 73, 72, 71,  # C5, D5, C5, B4, etc.
        # Bar 4: G
        67, 68, 67, 66, 67, 68, 67, 66,  # G4, A4, G4, F#4, etc.
        # Bar 5: Em
        75, 76, 75, 74, 75, 76, 75, 74,
        # Bar 6: Am
        69, 70, 69, 68, 69, 70, 69, 68,  # A4, B4, A4, G4, etc.
        # Bar 7: D
        74, 75, 74, 73, 74, 75, 74, 73,  # D5, E5, D5, C5, etc.
        # Bar 8: G
        67, 68, 67, 66, 67, 68, 67, 66
    ]
    melody_b_durations = [240] * 64  # Eighth notes (240 ticks)

    # Define melody for C section (mixed rhythms, including sixteenths)
    melody_c_notes = [
        # Bar 1: G
        67, 71, 74, 79, 74, 71, 67, 71,  # G4, B4, D5, G5, D5, B4, G4, B4
        # Bar 2: D
        74, 78, 81, 86, 81, 78, 74, 78,  # D5, F#5, A5, D6, A5, F#5, D5, F#5
        # Bar 3: Em
        75, 79, 82, 87, 82, 79, 75, 79,  # E5, G5, B5, E6, B5, G5, E5, G5
        # Bar 4: C
        72, 76, 79, 84, 79, 76, 72, 76,  # C5, E5, G5, C6, G5, E5, C5, E5
        # Bar 5: G
        67, 71, 74, 79, 74, 71, 67, 71,
        # Bar 6: Am
        69, 72, 76, 81, 76, 72, 69, 72,  # A4, C5, E5, A5, E5, C5, A4, C5
        # Bar 7: Bm
        71, 74, 78, 83, 78, 74, 71, 74,  # B4, D5, F#5, B5, F#5, D5, B4, D5
        # Bar 8: D
        74, 78, 81, 86, 81, 78, 74, 78
    ]
    melody_c_durations = [240] * 64  # Eighth notes

    # Define melody for D section (simplified A section)
    melody_d_notes = [
        # Bar 1: G
        67, 71, 74,  # G4, B4, D5
        # Bar 2: C
        72, 76, 79,  # C5, E5, G5
        # Bar 3: D
        74, 78, 81,  # D5, F#5, A5
        # Bar 4: G
        79, 74, 71, 67  # G5, D5, B4, G4
    ]
    melody_d_durations = [480] * 12  # Quarter notes

    # Combine melody for all sections
    all_melody_notes = melody_a_notes + melody_b_notes + melody_c_notes + melody_d_notes
    all_melody_durations = melody_a_durations + melody_b_durations + melody_c_durations + melody_d_durations

    # Add main melody to track1
    for note, duration in zip(all_melody_notes, all_melody_durations):
        track1.append(mido.Message('note_on', channel=0, note=note, velocity=64, time=0))
        track1.append(mido.Message('note_off', channel=0, note=note, velocity=0, time=duration))

    # Define harmony (harp) for A section (arpeggios)
    harmony_a = []
    for chord in chords_a:
        root, third, fifth, octave = chord[1]
        harmony_a.extend([root, third, fifth, octave] * 2)  # Eighth notes
    harmony_a_durations = [240] * len(harmony_a)

    # Define harmony for B section (broken chords)
    harmony_b = []
    for chord in chords_b:
        root, third, fifth, octave = chord[1]
        harmony_b.extend([root, fifth, third, octave])  # Quarter notes
    harmony_b_durations = [480] * len(harmony_b)

    # Define harmony for C section (counter-melody)
    counter_melody_c_notes = [
        55, 57, 59, 60, 62, 64, 65, 67,  # G3 to G4
        62, 64, 65, 67, 69, 71, 72, 74,  # D4 to D5
        60, 62, 64, 65, 67, 69, 71, 72,  # Em scale
        59, 60, 62, 64, 65, 67, 69, 71,  # C scale
        55, 57, 59, 60, 62, 64, 65, 67,
        57, 59, 60, 62, 64, 65, 67, 69,
        59, 60, 62, 64, 65, 67, 69, 71,
        62, 64, 65, 67, 69, 71, 72, 74
    ]
    counter_melody_c_durations = [240] * 64  # Eighth notes

    # Define harmony for D section (whole note chords)
    harmony_d = [chord[1] for chord in chords_d]  # List of chords
    harmony_d_durations = [1920] * 4  # Whole notes

    # Add harmony to track2
    # A section: arpeggios
    for note, duration in zip(harmony_a, harmony_a_durations):
        track2.append(mido.Message('note_on', channel=1, note=note, velocity=64, time=0))
        track2.append(mido.Message('note_off', channel=1, note=note, velocity=0, time=duration))
    # B section: broken chords
    for note, duration in zip(harmony_b, harmony_b_durations):
        track2.append(mido.Message('note_on', channel=1, note=note, velocity=64, time=0))
        track2.append(mido.Message('note_off', channel=1, note=note, velocity=0, time=duration))
    # C section: counter-melody
    for note, duration in zip(counter_melody_c_notes, counter_melody_c_durations):
        track2.append(mido.Message('note_on', channel=1, note=note, velocity=64, time=0))
        track2.append(mido.Message('note_off', channel=1, note=note, velocity=0, time=duration))
    # D section: whole note chords
    for chord, duration in zip(harmony_d, harmony_d_durations):
        for note in chord:
            track2.append(mido.Message('note_on', channel=1, note=note, velocity=64, time=0))
        track2.append(mido.Message('note_off', channel=1, note=chord[0], velocity=0, time=duration))
        for note in chord[1:]:
            track2.append(mido.Message('note_off', channel=1, note=note, velocity=0, time=0))

    # Define bass for all sections (simple root notes)
    bass_notes = [chord[1][0] for chord in (chords_a + chords_b + chords_c + chords_d)]  # Root of each chord
    bass_durations = [1920] * len(bass_notes)  # Whole notes

    # Add bass to track3
    for note, duration in zip(bass_notes, bass_durations):
        track3.append(mido.Message('note_on', channel=2, note=note, velocity=64, time=0))
        track3.append(mido.Message('note_off', channel=2, note=note, velocity=0, time=duration))

    # Save the MIDI file
    mid.save(filename)

# Create and play the MIDI file
create_midi_file('whispers_of_the_forest.mid')

# Initialize Pygame and play the MIDI file
pygame.init()
pygame.mixer.music.load('whispers_of_the_forest.mid')
pygame.mixer.music.play()

# Keep the script running while the music plays
while pygame.mixer.music.get_busy():
    time.sleep(1)

print("Song finished playing. MIDI file saved as 'whispers_of_the_forest.mid'.")