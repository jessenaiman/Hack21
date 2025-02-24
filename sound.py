import pyfluidsynth
import time

# Initialize FluidSynth
fs = pyfluidsynth.Synth()
fs.start(driver='alsa')  # Use 'coreaudio' for macOS, 'dsound' for Windows

# Load a soundfont (General MIDI, included with fluidsynth on Linux)
sfid = fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")  # Path may vary; check your system
fs.program_select(0, sfid, 0, 0)  # Channel 0, default instrument (Acoustic Grand Piano)

# Function to play a note (MIDI note, velocity, duration in seconds)
def play_note(note, velocity, duration):
    fs.noteon(0, note, velocity)  # Channel 0, note, velocity
    time.sleep(duration)
    fs.noteoff(0, note)

# Tempo (120 BPM, quarter note = 0.5s)
tempo = 0.5

# Loop 1: "Cosmic Journey" (Mysterious, Expansive) - Church Organ (Instrument 19)
def play_cosmic_journey():
    fs.program_select(0, sfid, 0, 19)  # Church Organ
    for _ in range(2):  # 8 bars total (4 bars per cycle)
        # Bar 1-2: A minor arpeggio with bass
        play_note(57, 80, tempo)  # A3 (bass)
        for note in [69, 72, 76, 72]:  # A4, C5, E5, C5
            play_note(note, 100, tempo / 2)  # Eighth notes
        play_note(57, 80, 0)  # Turn off bass

        # Bar 3-4: F major for contrast
        play_note(53, 80, tempo)  # F3 (bass)
        for note in [65, 69, 72, 69]:  # F4, A4, C5, A4
            play_note(note, 90, tempo / 2)
        play_note(53, 80, 0)  # Turn off bass

    # Fade out
    play_note(69, 70, tempo * 2)  # A4, sustained

# Loop 2: "Hero’s Resolve" (Bold, Uplifting) - Bright Acoustic Piano (Instrument 1)
def play_hero_resolve():
    fs.program_select(0, sfid, 0, 1)  # Bright Acoustic Piano
    for _ in range(2):  # 8 bars total
        # Bar 1-2: C major chord stabs
        for _ in range(4):  # Four beats
            chord = [60, 64, 67]  # C4, E4, G4
            for note in chord:
                play_note(note, 110, tempo / 2)  # Staccato
            time.sleep(tempo / 2)

        # Bar 3-4: G major with melody
        play_note(55, 90, tempo)  # G3 (bass)
        for note in [67, 71, 72, 71]:  # G4, B4, C5, B4
            play_note(note, 100, tempo / 2)
        play_note(55, 90, 0)  # Turn off bass

    # Flourish
    for note in [72, 76, 79]:  # C5, E5, G5
        play_note(note, 120, tempo / 2)

# Play one of the loops (uncomment to switch)
play_cosmic_journey()  # Mysterious, expansive
# play_hero_resolve()  # Bold, uplifting

# Clean up
time.sleep(1)  # Let the last notes play
fs.delete()