# Local Voice AI Agent

Offline voice assistant: record -> transcribe (faster-whisper) -> reason and
optionally call a tool (Ollama, llama3.2) -> speak (Piper) -> play back.

See `SRS_Local_Voice_AI_Agent.docx` for the full requirements this code
implements, and the REQ-IDs referenced in each module's docstring.

## Setup

```bash
conda env create -f environment.yml
conda activate voice-agent
```

You also need, separately from the Python packages above:

1. **Ollama** — install from ollama.com, then:
   ```bash
   ollama pull llama3.2
   ollama serve
   ```
   Leave `ollama serve` running in its own terminal.

2. **Piper voice model** — download `en_US-lessac-medium.onnx` and its matching
   `.onnx.json` file from the Piper voices repository on Hugging Face, and
   place both in this project's root folder.

3. Confirm your Piper install supports the flags this code uses:
   ```bash
   piper --help
   ```
   If `--output_file` isn't listed, tell me what options it does show — the
   command in `src/speak.py` will need adjusting for your build.

## Run the tests

```bash
pytest
```

These test the tool-call parser and the calculator only — no microphone,
speakers, or running services required. They should pass on any machine.

## Run the agent

```bash
python main.py
```

First run downloads the whisper-base model (needs internet, one time only).
After that it runs fully offline as long as Ollama is running locally.
