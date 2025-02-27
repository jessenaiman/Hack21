import mido
from music_theory import get_chord_notes, get_scale_notes

def transpose_notes(notes, semitones):
    """
    Transpose a list of notes by a number of semitones.
    
    Args:
        notes (list): List of MIDI note numbers.
        semitones (int): Number of semitones to transpose.
    
    Returns:
        list: Transposed MIDI note numbers.
    """
    return [note + semitones for note in notes]

def generate_arpeggio(chord, duration, repeats):
    """
    Generate an arpeggio pattern from a chord.
    
    Args:
        chord (list): List of MIDI note numbers for the chord.
        duration (int): Duration parameter (not used in current implementation).
        repeats (int): Number of times to repeat the pattern.
    
    Returns:
        list: Arpeggio pattern as MIDI note numbers.
    """
    # Simple arpeggio: play chord notes plus middle note again (e.g., C, E, G, E)
    pattern = chord + [chord[1]]
    return pattern * repeats

def generate_chord_progression(root_note, progression, chord_octave=4):
    """
    Generate a chord progression based on a root note and chord specifications.
    
    Args:
        root_note (str): Root note of the key (e.g., 'C').
        progression (list): List of tuples (root, chord_type) (e.g., [('C', 'major'), ('G', 'major')]).
        chord_octave (int): Octave for the root notes (default 4).
    
    Returns:
        list: List of chord MIDI note lists.
    """
    chord_notes_list = []
    for chord_root, chord_type in progression:
        # Construct the root note name at the specified octave
        root_note_name = f"{chord_root}{chord_octave}"
        chord_notes = get_chord_notes(root_note_name, chord_type)
        chord_notes_list.append(chord_notes)
    return chord_notes_list

def generate_drum_pattern(ticks_per_beat=480):
    """
    Generate a basic drum pattern for one bar (4 beats in 4/4 time).
    
    Args:
        ticks_per_beat (int): MIDI ticks per beat (default 480).
    
    Returns:
        list: List of MIDI messages for the drum pattern arranged with correct delta times.
    """
    # One bar is 4 beats
    bar_duration = ticks_per_beat * 4  # e.g., 1920 ticks for 480 ticks_per_beat
    
    # List to store (absolute_time, message) tuples
    messages = []
    
    # Kick drum (C1, MIDI note 36) on beats 1 and 3
    messages.append((0, mido.Message('note_on', channel=9, note=36, velocity=80)))
    messages.append((ticks_per_beat, mido.Message('note_off', channel=9, note=36, velocity=0)))
    messages.append((ticks_per_beat * 2, mido.Message('note_on', channel=9, note=36, velocity=80)))
    messages.append((ticks_per_beat * 3, mido.Message('note_off', channel=9, note=36, velocity=0)))
    
    # Snare drum (D1, MIDI note 38) on beats 2 and 4
    messages.append((ticks_per_beat * 1, mido.Message('note_on', channel=9, note=38, velocity=64)))
    messages.append((ticks_per_beat * 2, mido.Message('note_off', channel=9, note=38, velocity=0)))
    messages.append((ticks_per_beat * 3, mido.Message('note_on', channel=9, note=38, velocity=64)))
    messages.append((ticks_per_beat * 4, mido.Message('note_off', channel=9, note=38, velocity=0)))
    
    # Closed hi-hat (F#1, MIDI note 42) every eighth note (every half beat)
    for i in range(8):
        start_time = i * (ticks_per_beat // 2)  # 240 ticks for 480 ticks_per_beat
        messages.append((start_time, mido.Message('note_on', channel=9, note=42, velocity=32)))
        messages.append((start_time + ticks_per_beat // 4, mido.Message('note_off', channel=9, note=42, velocity=0)))
    
    # Sort messages by absolute time
    messages.sort(key=lambda x: x[0])
    
    # Convert absolute times to delta times
    pattern = []
    last_time = 0
    for time, msg in messages:
        delta = time - last_time
        msg.time = delta
        pattern.append(msg)
        last_time = time
    
    return pattern

def generate_scale(key, mode='major', octave=4, octaves=1):
    """
    Generate a scale based on the key, mode, and octave.
    
    Args:
        key (str): Root note of the scale (e.g., 'C').
        mode (str): Scale mode (e.g., 'major', 'natural_minor').
        octave (int): Starting octave (default 4).
        octaves (int): Number of octaves to generate (default 1).
    
    Returns:
        list: MIDI note numbers for the scale.
    """
    root_note = f"{key}{octave}"
    return get_scale_notes(root_note, mode, octaves)