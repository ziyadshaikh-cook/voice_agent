"""The main loop: record -> transcribe -> reason -> (tool?) -> speak -> play.
This is the piece that was missing entirely from the original screenshots —
individual functions existed, but nothing tied them into a running agent.
"""
from src.capture import record_audio
from src.playback import play_audio
from src.reasoning import ask_llm, parse_tool_call
from src.speak import synthesize_speech
from src.tools import TOOLS
from src.transcribe import load_whisper_model, transcribe_audio


def run(duration=5):
    print("Loading Whisper model...")
    whisper_model = load_whisper_model()
    print("Voice agent ready. Press Ctrl+C to stop.\n")

    while True:
        record_audio(duration=duration)
        user_text = transcribe_audio(whisper_model)
        print(f"You said: {user_text}")

        if not user_text:
            continue

        llm_response = ask_llm(user_text)
        tool_name, argument = parse_tool_call(llm_response)

        if tool_name and tool_name in TOOLS:
            try:
                tool_result = TOOLS[tool_name](argument)
            except ValueError:
                # A bad or incomplete expression from the LLM shouldn't take
                # down the whole session, tell the user and move on.
                final_text = "Sorry, I couldn't work that out. Could you repeat the question?"
            else:
                follow_up = (
                    f"The {tool_name} tool returned: {tool_result}. "
                    "Give the user a short spoken answer using this result."
                )
                final_text = ask_llm(follow_up)
        else:
            final_text = llm_response

        print(f"Agent: {final_text}\n")
        synthesize_speech(final_text)
        play_audio()


if __name__ == "__main__":
    run()
