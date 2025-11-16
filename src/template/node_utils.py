import re


def resolve_var(name, context):
    """
    Resolve dotted and indexed variable names like:
    - top.next.last
    - items[0]
    - items[1].top.next
    """
    # Split by dots, keep possible index parts []
    parts = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\[\d+]", name)
    value = context

    for part in parts:
        if part.startswith('[') and part.endswith(']'):
            # Handle list/tuple indexing
            index = int(part[1:-1])
            try:
                value = value[index]
            except (IndexError, TypeError, KeyError):
                return None
        else:
            # Handle attribute or dict key
            if isinstance(value, dict):
                value = value.get(part)
            else:
                value = getattr(value, part, None)

        if value is None:
            return None
    return value

def eval_condition(expr, context):
    """Evaluate a boolean condition safely using the context."""
    # Replace variable names with Python values
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_.\[\]]*", expr)
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
