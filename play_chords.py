# Copyright (c) 2026 Genavive Ramirez. All rights reserved.

import os
import math
import struct
import time

BPM = 50
BEAT_DURATION = 60.0 / BPM
CHORD_HOLD_TIME = 1.0
STRUM_DELAY = 0.04
TOTAL_BEAT_TIME = BEAT_DURATION
REST_TIME = TOTAL_BEAT_TIME - CHORD_HOLD_TIME

ROOT_FREQS = [261.63, 196.00, 220.00, 164.81, 261.63, 196.00, 146.83, 220.00]
NAMES = ["C", "G", "A", "E", "C", "G", "D", "A"]
CHORD_TYPE = "minor chords"

SEQUENCE = ['Cm', 'Gm', 'Am', 'Em', 'Cm', 'Gm', 'Dm', 'Am']


def generate_minor_chord_wav(root_freq, filename="temp_chord.wav"):
    sample_rate = 22050
    duration = CHORD_HOLD_TIME
    num_samples = int(sample_rate * duration)

    f1, f2, f3 = root_freq, root_freq * 1.1892, root_freq * 1.4983

    with open(filename, "wb") as f:
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + num_samples * 2))
        f.write(b"WAVEfmt ")
        f.write(struct.pack("<IHHIIHH", 16, 1, 1, sample_rate, sample_rate * 2, 2, 16))
        f.write(b"data")
        f.write(struct.pack("<I", num_samples * 2))

        for sample_num in range(num_samples):
            t = sample_num / sample_rate
            envelope = 1.0 if t < 0.8 else (1.0 - (t - 0.8) / 0.2)

            signal = math.sin(2 * math.pi * f1 * t) + math.sin(2 * math.pi * f2 * t) + math.sin(2 * math.pi * f3 * t)
            val = int((signal / 3.0) * 16383 * envelope)
            f.write(struct.pack("<h", val))


def main():
    print("=" * 60)
    print(" MAC NATIVE PROGRESSION PLAYER (Zero-Dependency)")
    print(f" Grid Blueprint: {BPM} BPM | Play Target: {CHORD_HOLD_TIME}s")
    print("=" * 60)
    print("© 2026 Genavive Ramirez. All rights reserved.\n")
    print("Playing loop... Press Ctrl+C to STOP\n")

    try:
        while True:
            for index, freq in enumerate(ROOT_FREQS):
                print(f"🎵 Playing: {NAMES[index]} {CHORD_TYPE} (Ringing 1.0s)")

                generate_minor_chord_wav(freq)
                os.system("afplay temp_chord.wav &")

                time.sleep(CHORD_HOLD_TIME)

                os.system("killall afplay > /dev/null 2>&1")
                time.sleep(REST_TIME)

    except KeyboardInterrupt:
        print("\nPlayback stopped.")
    finally:
        if os.path.exists("temp_chord.wav"):
            os.remove("temp_chord.wav")


if __name__ == "__main__":
    main()
