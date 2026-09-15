"""Plays a wav file through the default audio output device. REQ-PLAY-1, REQ-PLAY-2.
This was the missing piece from the original screenshots — generating speech
and playing it back are separate steps, and this module is the second one.
"""
import sounddevice as sd
import soundfile as sf


def play_audio(filename="response.wav"):
    data, samplerate = sf.read(filename)
    sd.play(data, samplerate)
    sd.wait()
