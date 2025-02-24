import pygame.midi
import time
import threading

# Initialize Pygame and MIDI
pygame.init()
pygame.midi.init()

# Choose an output device (usually 0 is the default synthesizer)
midi_out = pygame.midi.Output(0)
midi_out.set_instrument(0)  # 0 = Acoustic Grand Piano, adjust for other sounds

def play_hero_resolve():
    midi_out.set_instrument(1)  # Bright Acoustic Piano
    tempo = 0.5  # 120 BPM
    
    for _ in range(2):  # Repeat twice for 8 bars
        # Bar 1-2: C major chord stabs
        for _ in range(4):  # Four beats
            chord = [60, 64, 67]  # C4, E4, G4
            for note in chord:
                midi_out.note_on(note, 110)
            time.sleep(tempo / 2)  # Staccato
            for note in chord:
                midi_out.note_off(note, 110)
            time.sleep(tempo / 2)

        # Bar 3-4: G major with melody
        midi_out.note_on(55, 90)  # G3 (bass)
        for note in [67, 71, 72, 71]:  # G4, B4, C5, B4
            midi_out.note_on(note, 100)
            time.sleep(tempo / 2)
            midi_out.note_off(note, 100)
        time.sleep(tempo)
        midi_out.note_off(55, 90)

    # End with a flourish
    for note in [72, 76, 79]:  # C5, E5, G5
        midi_out.note_on(note, 120)
        time.sleep(tempo / 2)
        midi_out.note_off(note, 120)

def play_cosmic_journey():
    midi_out.set_instrument(19)  # Church Organ
    tempo = 0.5  # 120 BPM, quarter note = 0.5s
    
    for _ in range(2):  # Repeat twice for 8 bars (4 bars per cycle)
        # Bar 1-2: A minor arpeggio with bass
        midi_out.note_on(57, 80)  # A3 (bass)
        for note in [69, 72, 76, 72]:  # A4, C5, E5, C5
            midi_out.note_on(note, 100)
            time.sleep(tempo / 2)  # Eighth note
            midi_out.note_off(note, 100)
        time.sleep(tempo)  # Hold bass
        midi_out.note_off(57, 80)

        # Bar 3-4: Shift to F major (relative major) for contrast
        midi_out.note_on(53, 80)  # F3 (bass)
        for note in [65, 69, 72, 69]:  # F4, A4, C5, A4
            midi_out.note_on(note, 90)
            time.sleep(tempo / 2)
            midi_out.note_off(note, 90)
        time.sleep(tempo)
        midi_out.note_off(53, 80)

    # Fade out last note
    midi_out.note_on(69, 70)  # A4
    time.sleep(tempo * 2)
    midi_out.note_off(69, 70)

def play_background_music(loop_function):
    def music_thread():
        while True:  # Loop indefinitely
            loop_function()
    thread = threading.Thread(target=music_thread)
    thread.daemon = True  # Stops when main program exits
    thread.start()

# Example game loop
play_background_music(play_cosmic_journey)  # Start music
screen = pygame.display.set_mode((400, 300))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.midi.quit()
pygame.quit()