import re

# Chord types with interval patterns (relative to root note in semitones)
chord_types = {
    'major': [0, 4, 7],          # e.g., C major: C, E, G
    'minor': [0, 3, 7],          # e.g., C minor: C, Eb, G
    'diminished': [0, 3, 6],     # e.g., C diminished: C, Eb, Gb
    'augmented': [0, 4, 8],      # e.g., C augmented: C, E, G#
    'major7': [0, 4, 7, 11],     # e.g., Cmaj7: C, E, G, B
    'minor7': [0, 3, 7, 10],     # e.g., Cm7: C, Eb, G, Bb
    'dominant7': [0, 4, 7, 10],  # e.g., C7: C, E, G, Bb
    'sus4': [0, 5, 7],           # e.g., Csus4: C, F, G
    'sus2': [0, 2, 7],           # e.g., Csus2: C, D, G
    # Add more chord types as needed
}

# Scale types with interval patterns (relative to root note in semitones)
scale_types = {
    'major': [0, 2, 4, 5, 7, 9, 11],              # e.g., C major: C, D, E, F, G, A, B
    'natural_minor': [0, 2, 3, 5, 7, 8, 10],      # e.g., C natural minor: C, D, Eb, F, G, Ab, Bb
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],     # e.g., C harmonic minor: C, D, Eb, F, G, Ab, B
    'melodic_minor': [0, 2, 3, 5, 7, 9, 11],      # e.g., C melodic minor: C, D, Eb, F, G, A, B
    'dorian': [0, 2, 3, 5, 7, 9, 10],             # e.g., C dorian: C, D, Eb, F, G, A, Bb
    'phrygian': [0, 1, 3, 5, 7, 8, 10],           # e.g., C phrygian: C, Db, Eb, F, G, Ab, Bb
    'lydian': [0, 2, 4, 6, 7, 9, 11],             # e.g., C lydian: C, D, E, F#, G, A, B
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],         # e.g., C mixolydian: C, D, E, F, G, A, Bb
    'locrian': [0, 1, 3, 5, 6, 8, 10],            # e.g., C locrian: C, Db, Eb, F, Gb, Ab, Bb
    # Add more scales as needed
}

def note_name_to_midi(note_name):
    """
    Convert a note name (e.g., 'C4', 'C#4', 'Bb3') to MIDI note number.
    
    Args:
        note_name (str): Note name to convert.
    
    Returns:
        int: MIDI note number.
    
    Raises:
        ValueError: If the note name is invalid.
    """
    match = re.match(r'([A-G])([#b])?(\d+)', note_name)
    if not match:
        raise ValueError("Invalid note name")
    
    letter, accidental, octave = match.groups()
    octave = int(octave)
    
    # Base offsets for natural notes (C4 = 60)
    note_offsets = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    offset = note_offsets[letter]
    
    # Adjust for accidental
    if accidental == '#':
        offset += 1
    elif accidental == 'b':
        offset -= 1
    
    # Calculate MIDI note number: (octave + 1) * 12 + offset
    # Since C-1 is MIDI note 0, C4 is MIDI note 60
    note_number = (octave + 1) * 12 + offset
    return note_number

def get_chord_notes(root, chord_type):
    """
    Generate MIDI note numbers for a chord based on root note and chord type.
    
    Args:
        root (str or int): Root note (e.g., 'C4' or MIDI number 60).
        chord_type (str): Type of chord (e.g., 'major', 'minor7').
    
    Returns:
        list: MIDI note numbers for the chord.
    
    Raises:
        ValueError: If the chord type is unknown.
    """
    if isinstance(root, str):
        root = note_name_to_midi(root)
    
    intervals = chord_types.get(chord_type, [])
    if not intervals:
        raise ValueError(f"Unknown chord type: {chord_type}")
    
    return [root + interval for interval in intervals]

def get_scale_notes(root, scale_type, octaves=1):
    """
    Generate MIDI note numbers for a scale based on root note and scale type.
    
    Args:
        root (str or int): Root note (e.g., 'C4' or MIDI number 60).
        scale_type (str): Type of scale (e.g., 'major', 'natural_minor').
        octaves (int): Number of octaves to generate (default 1).
    
    Returns:
        list: MIDI note numbers for the scale.
    
    Raises:
        ValueError: If the scale type is unknown.
    """
    if isinstance(root, str):
        root = note_name_to_midi(root)
    
    intervals = scale_types.get(scale_type, [])
    if not intervals:
        raise ValueError(f"Unknown scale type: {scale_type}")
    
    scale_notes = []
    for octave in range(octaves):
        for interval in intervals:
            scale_notes.append(root + interval + (octave * 12))
    return scale_notes