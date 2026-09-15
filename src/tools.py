"""The two tools the agent can call. Pure logic, no I/O — fully unit-testable.
REQ-TOOL-1, REQ-TOOL-2.

calculate() deliberately does NOT use eval()/exec(). It parses the expression
into an AST and only evaluates a small whitelist of safe arithmetic node types,
so it cannot be used to run arbitrary code even if the LLM is manipulated into
passing something malicious as the argument.
"""
import ast
import datetime
import operator

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def get_current_time(_argument=None):
    return datetime.datetime.now().strftime("%I:%M %p")


def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def calculate(argument):
    try:
        tree = ast.parse(argument, mode="eval")
    except SyntaxError as exc:
        # The LLM sometimes passes an incomplete expression (e.g. "7 * 8 -").
        # Treat that the same as an unsupported expression rather than letting
        # a raw SyntaxError escape and crash the whole agent loop.
        raise ValueError(f"Could not parse expression: {argument!r}") from exc
    return _eval_node(tree.body)


TOOLS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
}
