from composition import Composition, Instrument, Melody, Note
from instruments import PIANO

# Define pitches for Voice A: 32 quarter notes in C major with harmonic progression
voice_a_pitches = [
    60, 62, 64, 65,  # Bar 1: C4 D4 E4 F4 (C major)
    67, 69, 71, 72,  # Bar 2: G4 A4 B4 C5 (C major)
    69, 67, 65, 64,  # Bar 3: A4 G4 F4 E4 (A minor)
    65, 67, 69, 71,  # Bar 4: F4 G4 A4 B4 (F major)
    67, 65, 64, 62,  # Bar 5: G4 F4 E4 D4 (G major)
    60, 62, 64, 65,  # Bar 6: C4 D4 E4 F4 (C major)
    62, 64, 65, 67,  # Bar 7: D4 E4 F4 G4 (D minor)
    67, 65, 64, 62   # Bar 8: G4 F4 E4 D4 (G to C)
]

# Define pitches for Voice B: 128 16th notes, C major scale up and down
scale_up = [48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72]  # C3 to C5
scale_down = [71, 69, 67, 65, 64, 62, 60, 59, 57, 55, 53, 52, 50, 48]  # B4 to C3
full_scale = scale_up + scale_down  # 29 notes per cycle
voice_b_pitches = (full_scale * 5)[:128]  # Repeat 5 times, take first 128 notes

# Create composition
comp = Composition()

# Create instruments (both piano, different channels)
instrument_a = Instrument("Piano A", channel=0, program=PIANO)
instrument_b = Instrument("Piano B", channel=1, program=PIANO)

# Create melodies with durations: 480 ticks (quarter), 120 ticks (16th)
melody_a = Melody([Note(pitch, 480) for pitch in voice_a_pitches])
melody_b = Melody([Note(pitch, 120) for pitch in voice_b_pitches])

# Add melodies to instruments
instrument_a.add_element(melody_a)
instrument_b.add_element(melody_b)

# Add instruments to composition
comp.add_instrument(instrument_a)
comp.add_instrument(instrument_b)

# Save as MIDI file
comp.save('bach_invention_inspired.mid')