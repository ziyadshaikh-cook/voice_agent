from src.reasoning import parse_tool_call


def test_parse_tool_call_valid_json():
    response = '{"tool": "get_current_time", "argument": ""}'
    tool, arg = parse_tool_call(response)
    assert tool == "get_current_time"
    assert arg == ""


def test_parse_tool_call_calculate_with_argument():
    response = '{"tool": "calculate", "argument": "12 * 8"}'
    tool, arg = parse_tool_call(response)
    assert tool == "calculate"
    assert arg == "12 * 8"


def test_parse_tool_call_plain_text_is_not_a_tool_call():
    response = "The capital of France is Paris."
    tool, arg = parse_tool_call(response)
    assert tool is None
    assert arg is None


def test_parse_tool_call_malformed_json_is_not_a_tool_call():
    response = "{tool: get_current_time}"  # invalid JSON, unquoted keys
    tool, arg = parse_tool_call(response)
    assert tool is None
    assert arg is None


def test_parse_tool_call_json_missing_required_fields():
    response = '{"tool": "get_current_time"}'  # no "argument" field
    tool, arg = parse_tool_call(response)
    assert tool is None
    assert arg is None
