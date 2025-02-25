import mido
import pygame
import time

def create_midi_file(filename):
    """
    Creates a MIDI file for the composition "Mystic Echoes".
    Structure: A-B-A-C, with polyphony in the C section, over 1 minute long.
    """
    mid = mido.MidiFile(ticks_per_beat=480)
    
    # Track 0: Tempo and time signature
    track0 = mido.MidiTrack()
    mid.tracks.append(track0)
    track0.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))  # 120 BPM
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
    
    # Track 4: Bass (Bass Guitar, channel 3)
    track4 = mido.MidiTrack()
    mid.tracks.append(track4)
    track4.append(mido.Message('program_change', channel=3, program=33, time=0))
    
    # Track 5: Percussion (Drums, channel 9)
    track5 = mido.MidiTrack()
    mid.tracks.append(track5)
    track5.append(mido.Message('program_change', channel=9, program=0, time=0))
    
    # Define chord progressions for each section
    # A section: Em - G - C - D | Em - F - G - D
    chords_a = [
        ('Em', [40, 44, 47]),  # E3, G3, B3
        ('G', [43, 47, 50]),   # G3, B3, D4
        ('C', [48, 52, 55]),   # C4, E4, G4
        ('D', [42, 46, 49]),   # D3, F#3, A3
        ('Em', [40, 44, 47]),
        ('F', [41, 45, 48]),   # F3, A3, C4
        ('G', [43, 47, 50]),
        ('D', [42, 46, 49])
    ]
    
    # B section: D - G - Em - C, repeated twice
    chords_b = [
        ('D', [42, 46, 49]),   # D3, F#3, A3
        ('G', [43, 47, 50]),   # G3, B3, D4
        ('Em', [40, 44, 47]),  # E3, G3, B3
        ('C', [48, 52, 55])    # C4, E4, G4
    ] * 2
    
    # C section: Variation of A section with added complexity
    chords_c = [
        ('Em', [40, 44, 47]),  # E3, G3, B3
        ('G', [43, 47, 50]),   # G3, B3, D4
        ('C', [48, 52, 55]),   # C4, E4, G4
        ('D', [42, 46, 49]),   # D3, F#3, A3
        ('Em', [40, 44, 47]),
        ('F', [41, 45, 48]),   # F3, A3, C4
        ('G', [43, 47, 50]),
        ('D', [42, 46, 49])
    ]
    
    # Define melody notes for A section (eighth notes, 240 ticks)
    melody_a_notes = [
        # Bar 1: Em
        64, 67, 72, 67, 72, 67, 72, 67,  # E4, G4, C5, G4, C5, G4, C5, G4
        # Bar 2: G
        67, 72, 76, 72, 76, 72, 76, 72,  # G4, C5, E5, C5, E5, C5, E5, C5
        # Bar 3: C
        72, 76, 81, 76, 81, 76, 81, 76,  # C5, E5, G5, E5, G5, E5, G5, E5
        # Bar 4: D
        69, 74, 77, 74, 77, 74, 77, 74,  # A4, D5, F#5, D5, F#5, D5, F#5, D5
        # Bar 5: Em
        64, 67, 72, 67, 72, 67, 72, 67,
        # Bar 6: F
        65, 69, 72, 69, 72, 69, 72, 69,  # F4, A4, C5, A4, C5, A4, C5, A4
        # Bar 7: G
        67, 72, 76, 72, 76, 72, 76, 72,
        # Bar 8: D
        69, 74, 77, 74, 77, 74, 77, 74
    ]
    melody_a_durations = [240] * 64  # 8 bars * 8 notes/bar
    
    # Define melody notes for B section (quarter notes, 480 ticks)
    melody_b_notes = [
        # Bar 1: D
        69, 74, 77, 74,  # A4, D5, F#5, D5
        # Bar 2: G
        67, 72, 76, 72,  # G4, C5, E5, C5
        # Bar 3: Em
        64, 67, 72, 67,  # E4, G4, C5, G4
        # Bar 4: C
        72, 76, 81, 76,  # C5, E5, G5, E5
        # Bar 5: D
        69, 74, 77, 74,
        # Bar 6: G
        67, 72, 76, 72,
        # Bar 7: Em
        64, 67, 72, 67,
        # Bar 8: C
        72, 76, 81, 76
    ]
    melody_b_durations = [480] * 32  # 8 bars * 4 notes/bar
    
    # Define melody notes for C section (triplet eighth notes, 160 ticks)
    melody_c_notes = [
        # Bar 1: Em
        64, 67, 72, 67, 64, 67, 72, 67, 64, 67, 72, 67,  # E4, G4, C5, G4, E4, G4, C5, G4, E4, G4, C5, G4
        # Bar 2: G
        67, 72, 76, 72, 67, 72, 76, 72, 67, 72, 76, 72,  # G4, C5, E5, C5, G4, C5, E5, C5, G4, C5, E5, C5
        # Bar 3: C
        72, 76, 81, 76, 72, 76, 81, 76, 72, 76, 81, 76,  # C5, E5, G5, E5, C5, E5, G5, E5, C5, E5, G5, E5
        # Bar 4: D
        69, 74, 77, 74, 69, 74, 77, 74, 69, 74, 77, 74,  # A4, D5, F#5, D5, A4, D5, F#5, D5, A4, D5, F#5, D5
        # Bar 5: Em
        64, 67, 72, 67, 64, 67, 72, 67, 64, 67, 72, 67,
        # Bar 6: F
        65, 69, 72, 69, 65, 69, 72, 69, 65, 69, 72, 69,  # F4, A4, C5, A4, F4, A4, C5, A4, F4, A4, C5, A4
        # Bar 7: G
        67, 72, 76, 72, 67, 72, 76, 72, 67, 72, 76, 72,
        # Bar 8: D
        69, 74, 77, 74, 69, 74, 77, 74, 69, 74, 77, 74
    ]
    melody_c_durations = [160] * 96  # 8 bars * 12 notes/bar
    
    # Define bass line for all sections (quarter notes, 480 ticks)
    bass_notes = [
        # A section
        40, 43, 48, 42, 40, 41, 43, 42,
        # B section
        42, 43, 40, 48, 42, 43, 40, 48,
        # A section
        40, 43, 48, 42, 40, 41, 43, 42,
        # C section
        40, 43, 48, 42, 40, 41, 43, 42
    ]
    bass_durations = [480] * 32  # 8 bars * 4 notes/bar
    
    # Define percussion pattern for all sections (sixteenth notes, 120 ticks)
    percussion_notes = [
        # A section
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46,
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46,
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46,
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46,
        # B section
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46,
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46,
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46,
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46,
        # A section
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46,
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46,
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46,
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46,
        # C section
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46,
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46,
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46,
        36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46, 36, 38, 42, 46
    ]
    percussion_durations = [120] * 128  # 32 bars * 4 notes/bar
    
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
    
    # Add bass line to track4
    for note, duration in zip(bass_notes, bass_durations):
        track4.append(mido.Message('note_on', channel=3, note=note, velocity=64, time=0))
        track4.append(mido.Message('note_off', channel=3, note=note, velocity=0, time=duration))
    
    # Add percussion to track5
    for note, duration in zip(percussion_notes, percussion_durations):
        track5.append(mido.Message('note_on', channel=9, note=note, velocity=64, time=0))
        track5.append(mido.Message('note_off', channel=9, note=note, velocity=0, time=duration))
    
    # Save the MIDI file
    mid.save(filename)

# Create and play the MIDI file
create_midi_file('mystic_echoes.mid')
pygame.init()
pygame.mixer.music.load('mystic_echoes.mid')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    time.sleep(1)
print("Song finished playing. MIDI file saved as 'mystic_echoes.mid'.")