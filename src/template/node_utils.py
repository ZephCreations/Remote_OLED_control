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
    """Evaluate a boolean condition safely using the context.
    Replaces dotted/indexed tokens with safe placeholder then evaluates with a restricted locals dict."""

    # Tokens that look like variable references
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_.\[\]]*", expr)

    # keywords to avoid
    keywords = {"and", "or", "not", "True", "False", "None"}

    # Keep unique tokens in order of decreasing length to avoid partial replacements
    unique_tokens = []
    for t in tokens:
        if t not in unique_tokens:
            unique_tokens.append(t)
    unique_tokens.sort(key=len, reverse=True)

    safe_locals = {}
    expr_mod = expr

    var_idx = 0
    for tok in unique_tokens:
        if tok in keywords:
            continue

        # Resolve token to a Python value using resolver
        val = resolve_var(tok, context)

        # Create a safe placeholder name
        placeholder = f"__var{var_idx}"
        var_idx += 1

        # Replace all "whole" occurrences of the token with the placeholder
        # Use negative/positive lookarounds to avoid replacing parts of longer names
        pattern = r'(?<![A-Za-z0-9_])' + re.escape(tok) + r'(?![A-Za-z0-9_])'
        expr_mod = re.sub(pattern, placeholder, expr_mod)

        # Bind the placeholder to the resolved value
        safe_locals[placeholder] = val

    try:
        return bool(eval(expr_mod, {"__builtins__": None}, safe_locals))
    except Exception:
        return False
