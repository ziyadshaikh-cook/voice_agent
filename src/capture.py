"""Voice input capture. Pure I/O — records from the microphone and writes a wav file.
Kept deliberately free of any reasoning logic so it can be swapped for a fake
recorder in tests without touching anything else. REQ-CAP-1, REQ-CAP-2, REQ-CAP-3.
"""
import sounddevice as sd
from scipy.io.wavfile import write

SAMPLE_RATE = 16000


def record_audio(filename="audio.wav", duration=5, sample_rate=SAMPLE_RATE):
    print("Listening...")
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
    )
    sd.wait()
    write(filename, sample_rate, audio)
    print("Recording complete.")
    return filename
