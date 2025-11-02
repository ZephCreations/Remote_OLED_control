import re


def resolve_var(name, context):
    """Resolve dotted variable names like user.name.first"""
    parts = name.split(".")
    value = context
    for p in parts:
        if isinstance(value, dict):
            value = value.get(p)
        else:
            value = getattr(value, p, None)
        if value is None:
            return None
    return value

def eval_condition(expr, context):
    """Evaluate a boolean condition safely using the context."""
    # Replace variable names with Python values
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_.]*", expr)
    safe_locals = {}

    for tok in tokens:
        if tok in {"and", "or", "not", "True", "False", "None"}:
            continue
        val = resolve_var(tok, context)
        safe_locals[tok] = val

    try:
        return bool(eval(expr, {"__builtins__": None}, safe_locals))
    except Exception:
        return False
