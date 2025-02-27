# Instrument names mapped to MIDI program numbers (0-127) based on General MIDI standard
instruments = {
    # Pianos
    'acoustic_grand_piano': 0,
    'bright_acoustic_piano': 1,
    'electric_grand_piano': 2,
    'honky_tonk_piano': 3,
    'electric_piano_1': 4,
    'electric_piano_2': 5,
    'harpsichord': 6,  # Added for the composition
    
    # Chromatic Percussion
    'celesta': 8,
    'glockenspiel': 9,
    'music_box': 10,
    'vibraphone': 11,
    'marimba': 12,
    
    # Strings
    'violin': 40,
    'viola': 41,
    'cello': 42,
    'contrabass': 43,
    'tremolo_strings': 44,
    'pizzicato_strings': 45,
    'orchestral_harp': 46,
    'timpani': 47,
    'string_ensemble_1': 48,
    'string_ensemble_2': 49,
    
    # Woodwinds
    'flute': 73,
    'piccolo': 72,
    'oboe': 68,
    'english_horn': 69,
    'bassoon': 70,
    'clarinet': 71,
    'bass_clarinet': 71,  # Note: GM does not distinguish bass clarinet; using clarinet
    'recorder': 74,
    
    # Brass
    'trumpet': 56,
    'trombone': 57,
    'tuba': 58,
    'muted_trumpet': 59,
    'french_horn': 60,
    'brass_section': 61,
    
    # Guitars
    'acoustic_guitar_nylon': 24,
    'acoustic_guitar_steel': 25,
    'electric_guitar_jazz': 26,
    'electric_guitar_clean': 27,
    'electric_guitar_muted': 28,
    'overdriven_guitar': 29,
    'distortion_guitar': 30,
    
    # Basses
    'acoustic_bass': 32,
    'electric_bass_finger': 33,
    'electric_bass_pick': 34,
    'fretless_bass': 35,
    'slap_bass_1': 36,
    'slap_bass_2': 37,
    
    # Percussion
    'drums': 0,  # Standard drum kit, typically on channel 9 (program irrelevant)
    
    # Others
    'sitar': 104,
    'banjo': 105,
    'shamisen': 106,
    'koto': 107,
    
    # Add more instruments as needed
}