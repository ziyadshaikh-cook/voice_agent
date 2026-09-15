"""LLM reasoning. ask_llm() is the one function that touches the network
(localhost Ollama). parse_tool_call() is pure logic with zero I/O — this is
the function the SRS flags as REQ-LLM-3, and it's the one to test hardest.
"""
import json
import re

import ollama

TOOLS_DESCRIPTION = """Available tools:
- get_current_time: use this when the user asks for the current time.
- calculate: use this for mathematical calculations. Argument is a plain
  arithmetic expression, e.g. "2 + 2".

If a tool is required, respond ONLY with JSON:
{"tool": "tool_name", "argument": "tool_argument"}

If no tool is required, respond normally.
"""

# Matches the outermost {...} in a response, even if there's other text
# around it (small local models often add a sentence before/after the JSON).
_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def ask_llm(user_text, model="llama3.2"):
    prompt = f"""You are a helpful Voice AI Agent.

{TOOLS_DESCRIPTION}

User request:
{user_text}
"""
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]


def parse_tool_call(llm_response):
    """Returns (tool_name, argument) if llm_response contains a recognizable
    tool-call JSON object, otherwise returns (None, None) so the caller
    treats the response as a plain-text answer.

    llama3.2 does not reliably produce strict JSON (trailing commas, a
    missing "argument" field, or extra text around the object are all
    observed in practice), so this is deliberately more forgiving than a
    plain json.loads() call: it extracts the {...} fragment first, then
    strips a trailing comma before the closing brace, before attempting to
    parse it.
    """
    if not isinstance(llm_response, str):
        return None, None

    match = _JSON_OBJECT_RE.search(llm_response)
    if not match:
        return None, None

    candidate = match.group(0)
    candidate = re.sub(r",\s*\}", "}", candidate)  # drop a trailing comma

    try:
        data = json.loads(candidate)
    except json.JSONDecodeError:
        return None, None

    if not isinstance(data, dict) or "tool" not in data:
        return None, None

    return data["tool"], data.get("argument", "")

