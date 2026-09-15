"""Speech-to-text. Loads faster-whisper once and transcribes wav files.
REQ-STT-1, REQ-STT-2, REQ-STT-3.
"""
from pathlib import Path

from faster_whisper import WhisperModel
from huggingface_hub import snapshot_download

MODEL_REPO = "Systran/faster-whisper-base"


def load_whisper_model(device="cpu", compute_type="int8"):
    """device='cuda', compute_type='float16' if you have an NVIDIA GPU with CUDA."""
    model_path = Path.cwd() / "faster-whisper-base"
    if not model_path.exists():
        snapshot_download(repo_id=MODEL_REPO, local_dir=str(model_path))
    return WhisperModel(str(model_path), device=device, compute_type=compute_type)


def transcribe_audio(model, filename="audio.wav"):
    segments, _info = model.transcribe(filename)
    text = " ".join(segment.text for segment in segments)
    return text.strip()
