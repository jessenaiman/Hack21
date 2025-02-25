import mido
import pygame
import time
import random

def create_dynamic_midi(filename):
    mid = mido.MidiFile(ticks_per_beat=480)
    tracks = []
    
    # ======== TRACK CONFIGURATION ========
    instruments = [
        (0, 0, "Heroic Violins"),   # Program 0: Piano -> 40: Violin
        (1, 56, "Trumpet Call"),     # Program 56: Trumpet
        (2, 48, "Epic Strings"),     # Program 48: String Ensemble 1
        (3, 24, "Nylon Guitar"),     # Program 24: Nylon Guitar
        (4, 73, "Mystic Flute"),     # Program 73: Flute
        (9, 0, "Cinematic Percussion") # Channel 9 (Drums)
    ]
    
    for ch, prog, _ in instruments:
        track = mido.MidiTrack()
        if ch != 9:
            track.append(mido.Message('program_change', channel=ch, program=prog, time=0))
        tracks.append(track)
    mid.tracks.extend(tracks)
    
    # ======== MUSICAL PARAMETERS ========
    harmonic_field = {
        'main_theme': [60, 63, 67, 70],  # C Eb G Bb (C minor/major7 hybrid)
        'combat': [58, 62, 65, 69],       # Bb D F A
        'mystery': [61, 64, 67, 72]       # C# E G C
    }
    
    # ======== GENERATIVE ELEMENTS ========
    def generate_ostinato(base_note, intensity):
        """Creates evolving rhythmic patterns"""
        return [(base_note + random.choice([0,2,3,5,7]), 120 + intensity*10) 
                for _ in range(8 + intensity*2)]
    
    def modal_interchange(root, quality):
        """Generates chords with modal mixture"""
        chords = {
            'major': [0,4,7,11],
            'minor': [0,3,7,10],
            'lydian': [0,4,7,11,6],
            'phrygian': [0,1,5,8]
        }
        return [root + interval for interval in random.choice(list(chords.values()))]
    
    # ======== MAIN COMPOSITION ========
    sections = {
        'Prologue': {'tempo': 80, 'time': (7, 4), 'intensity': 1},  # Use tuple (numerator, denominator)
        'Exploration': {'tempo': 110, 'time': (4, 4), 'intensity': 3},
        'Conflict': {'tempo': 140, 'time': (5, 8), 'intensity': 7},
        'Resolution': {'tempo': 100, 'time': (3, 4), 'intensity': 2}
    }

    current_time = 0
    for section_name, params in sections.items():
        # Section Setup
        tracks[0].append(mido.MetaMessage(
            'set_tempo', tempo=int(600000 / params['tempo']), time=current_time))
        tracks[0].append(mido.MetaMessage(
            'time_signature',
            numerator=params['time'][0],   # Access numerator from the tuple
            denominator=params['time'][1], # Access denominator from the tuple
            time=0))
        
        # Generate Musical Elements
        harmonic_base = modal_interchange(60 + params['intensity']*2, 'phrygian')
        melody_notes = [n + 12 * random.randint(0,1) for n in harmonic_base]
        
        # Add to Tracks
        for i, note in enumerate(melody_notes):
            duration = 480 // (i%3 +1)
            tracks[1].append(mido.Message('note_on', note=note, velocity=50+params['intensity']*10, 
                                         time=i*120))
            tracks[1].append(mido.Message('note_off', note=note, time=duration))
        
        # Percussion Layers
        if params['intensity'] > 1:
            drum_pattern = [(36, 240), (38, 120), (42, 60)] * params['intensity']
            for note, dur in drum_pattern:
                tracks[5].append(mido.Message('note_on', note=note, velocity=90, time=current_time))
                tracks[5].append(mido.Message('note_off', note=note, time=dur))
                current_time += dur
    
    # ======== DYNAMIC MIXING ========
    for track in tracks[1:4]:
        track.append(mido.Message('control_change', control=7, value=80, time=0))  # Volume
        track.append(mido.Message('control_change', control=10, value=64, time=0)) # Pan
    
    # ======== FINAL EXPORT ========
    mid.save(filename)
    return mid

# Generate and play
create_dynamic_midi('horizons_unbound.mid')

pygame.init()
pygame.mixer.music.load('horizons_unbound.mid')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    time.sleep(1)
print("Epic composition complete! MIDI file saved.")
