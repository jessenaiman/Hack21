import mido
import pygame
import time

def create_midi_file(filename):
    """
    Creates a MIDI file for the composition "Echoes of Adventure".
    Structure: A-B-A-C, with polyphony in the C section, over 1 minute long.
    """
    mid = mido.MidiFile(ticks_per_beat=480)

    # Track 0: Tempo and time signature
    track0 = mido.MidiTrack()
    mid.tracks.append(track0)
    # Set tempo to 120 BPM (500,000 microseconds per quarter note)
    track0.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))
    track0.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, time=0))

    # Track 1: Main melody (Piano, channel 0)
    track1 = mido.MidiTrack()
    mid.tracks.append(track1)
    track1.append(mido.Message('program_change', channel=0, program=0, time=0))

    # Track 2: Counter-melody (Flute, channel 1, only in C section)
    track2 = mido.MidiTrack()
    mid.tracks.append(track2)
    track2.append(mido.Message('program_change', channel=1, program=73, time=0))

    # Track 3: Harmony (Strings, channel 2)
    track3 = mido.MidiTrack()
    mid.tracks.append(track3)
    track3.append(mido.Message('program_change', channel=2, program=48, time=0))

    # Define chord progressions for each section
    # A section: Am - F - Dm - E | Am - G - C - E
    chords_a = [
        ('Am', [57, 60, 64]),  # A3, C4, E4
        ('F', [53, 57, 60]),   # F3, A3, C4
        ('Dm', [50, 53, 57]),  # D3, F3, A3
        ('E', [52, 56, 59]),   # E3, G#3, B3
        ('Am', [57, 60, 64]),
        ('G', [55, 59, 62]),   # G3, B3, D4
        ('C', [48, 52, 55]),   # C3, E3, G3
        ('E', [52, 56, 59])
    ]

    # B section: C - G - Am - F, repeated twice
    chords_b = [
        ('C', [48, 52, 55]),   # C3, E3, G3
        ('G', [43, 47, 50]),   # G2, B2, D3
        ('Am', [45, 48, 52]),  # A2, C3, E3
        ('F', [41, 45, 48])    # F2, A2, C3
    ] * 2

    # C section: Same as A for simplicity
    chords_c = chords_a

    # Define melody notes for A section (eighth notes, 240 ticks)
    melody_a_notes = [
        # Bar 1: Am
        69, 76, 72, 76, 81, 76, 72, 76,  # A4, E5, C5, E5, A5, E5, C5, E5
        # Bar 2: F
        65, 72, 69, 72, 77, 72, 69, 72,  # F4, C5, A4, C5, F5, C5, A4, C5
        # Bar 3: Dm
        62, 69, 65, 69, 74, 69, 65, 69,  # D4, A4, F4, A4, D5, A4, F4, A4
        # Bar 4: E
        64, 71, 68, 71, 76, 71, 68, 71,  # E4, B4, G#4, B4, E5, B4, G#4, B4
        # Bar 5: Am
        69, 76, 72, 76, 81, 76, 72, 76,
        # Bar 6: G
        67, 74, 71, 74, 79, 74, 71, 74,  # G4, D5, B4, D5, G5, D5, B4, D5
        # Bar 7: C
        60, 67, 64, 67, 72, 67, 64, 67,  # C4, G4, E4, G4, C5, G4, E4, G4
        # Bar 8: E
        64, 71, 68, 71, 76, 71, 68, 71
    ]
    melody_a_durations = [240] * 64  # 8 bars * 8 notes/bar

    # Define melody notes for B section (quarter notes, 480 ticks)
    melody_b_notes = [
        # Bar 1: C
        60, 64, 67, 72,  # C4, E4, G4, C5
        # Bar 2: G
        55, 59, 62, 67,  # G3, B3, D4, G4
        # Bar 3: Am
        57, 60, 64, 69,  # A4, C5, E5, A5
        # Bar 4: F
        53, 57, 60, 65,  # F4, A4, C5, F5
        # Bar 5: C
        60, 64, 67, 72,
        # Bar 6: G
        55, 59, 62, 67,
        # Bar 7: Am
        57, 60, 64, 69,
        # Bar 8: F
        53, 57, 60, 65
    ]
    melody_b_durations = [480] * 32  # 8 bars * 4 notes/bar

    # Define melody notes for C section (triplet eighth notes, 160 ticks)
    melody_c_notes = [
        # Bar 1: Am
        69, 72, 76, 72, 69, 76, 69, 72, 76, 72, 69, 76,  # A4, C5, E5, repeating
        # Bar 2: F
        65, 69, 72, 69, 65, 72, 65, 69, 72, 69, 65, 72,  # F4, A4, C5
        # Bar 3: Dm
        62, 65, 69, 65, 62, 69, 62, 65, 69, 65, 62, 69,  # D4, F4, A4
        # Bar 4: E
        64, 68, 71, 68, 64, 71, 64, 68, 71, 68, 64, 71,  # E4, G#4, B4
        # Bar 5: Am
        69, 72, 76, 72, 69, 76, 69, 72, 76, 72, 69, 76,
        # Bar 6: G
        67, 71, 74, 71, 67, 74, 67, 71, 74, 71, 67, 74,  # G4, B4, D5
        # Bar 7: C
        60, 64, 67, 64, 60, 67, 60, 64, 67, 64, 60, 67,  # C4, E4, G4
        # Bar 8: E
        64, 68, 71, 68, 64, 71, 64, 68, 71, 68, 64, 71
    ]
    melody_c_durations = [160] * 96  # 8 bars * 12 notes/bar

    # Combine main melody for all sections (A-B-A-C)
    all_melody_notes = melody_a_notes + melody_b_notes + melody_a_notes + melody_c_notes
    all_melody_durations = melody_a_durations + melody_b_durations + melody_a_durations + melody_c_durations

    # Add main melody to track1
    for note, duration in zip(all_melody_notes, all_melody_durations):
        track1.append(mido.Message('note_on', channel=0, note=note, velocity=64, time=0))
        track1.append(mido.Message('note_off', channel=0, note=note, velocity=0, time=duration))

    # Define counter-melody for C section (same as melody_c but delayed by one bar)
    counter_melody_notes = melody_c_notes
    counter_melody_durations = melody_c_durations

    # Calculate start time for counter-melody (start of C section + 1920 ticks)
    t_c = sum(melody_a_durations + melody_b_durations + melody_a_durations)  # Time after A + B + A
    delay = 1920  # One bar
    start_time = t_c + delay

    # Add counter-melody to track2
    track2.append(mido.Message('note_on', channel=1, note=counter_melody_notes[0], velocity=64, time=start_time))
    track2.append(mido.Message('note_off', channel=1, note=counter_melody_notes[0], velocity=0, time=counter_melody_durations[0]))
    for note, duration in zip(counter_melody_notes[1:], counter_melody_durations[1:]):
        track2.append(mido.Message('note_on', channel=1, note=note, velocity=64, time=0))
        track2.append(mido.Message('note_off', channel=1, note=note, velocity=0, time=duration))

    # Define harmony chords for all sections (A + B + A + C)
    all_chords = chords_a + chords_b + chords_a + chords_c

    # Add harmony to track3
    for chord in all_chords:
        chord_notes = chord[1]  # List of MIDI note numbers for the chord
        # Add note_on for all chord notes at the start of the bar
        for note in chord_notes:
            track3.append(mido.Message('note_on', channel=2, note=note, velocity=64, time=0))
        # Add note_off for all chord notes after 1920 ticks
        track3.append(mido.Message('note_off', channel=2, note=chord_notes[0], velocity=0, time=1920))
        for note in chord_notes[1:]:
            track3.append(mido.Message('note_off', channel=2, note=note, velocity=0, time=0))

    # Save the MIDI file
    mid.save(filename)

# Create and play the MIDI file
create_midi_file('echoes_of_adventure.mid')
pygame.init()
pygame.mixer.music.load('echoes_of_adventure.mid')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    time.sleep(1)

print("Song finished playing. MIDI file saved as 'echoes_of_adventure.mid'.")