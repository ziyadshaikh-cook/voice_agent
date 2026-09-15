"""Text-to-speech via Piper. REQ-TTS-1, REQ-TTS-2.
Run `piper --help` on your machine first — if --output_file isn't listed as
an option for your install, this command needs adjusting (see README).
"""
import subprocess

PIPER_MODEL = "en_US-lessac-medium.onnx"


def synthesize_speech(text, output_file="response.wav", model=PIPER_MODEL):
    command = ["piper", "--model", model, "--output_file", output_file]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, text=True)
    process.communicate(text)
    return output_file
