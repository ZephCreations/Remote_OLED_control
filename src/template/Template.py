import re
from .Node import TextNode, VariableNode, IfNode, ForNode

class Template:
    def __init__(self, template_str):
        self.template_str = template_str
        self._tokens = self._tokenize()
        self._nodes = self._parse()

    def _tokenize(self):
        """
        Splits text into raw text, variables {{ var }}, and tags {% tag %}.
        Removes surrounding line breaks for control tags that appear alone on a line.
        """
        # Remove lines that only contain a control tag (like {% for ... %})
        cleaned = re.sub(
            r'^[ \t]*({%.*?%})[ \t]*\r?\n?',
            r'\1',
            self.template_str,
            flags=re.MULTILINE
        )

        token_re = re.compile(r"({{.*?}}|{%.*?%})")
        parts = token_re.split(cleaned)
        return [p for p in parts if p]

    def _parse(self):
        """
        Converts tokens into node objects.
        """
        root = []
        stack = [root]
        if_stack = [] # To keep track of which IfNode we're inside

        for token in self._tokens:
            if token.startswith("{{") and token.endswith("}}"):
                # Variable
                # Remove {{ }} brackets
                expr = token[2:-2].strip()
                # Add variable node
                stack[-1].append(VariableNode(expr))
            elif token.startswith("{%") and token.endswith("%}"):
                # Tag
                # Remove {% %} brackets
                tag = token[2:-2].strip()

                # Switch case on type
                if tag.startswith("if "):
                    node = IfNode(tag[3:].strip())
                    stack[-1].append(node)
                    if_stack.append(node)
                    stack.append(node.branches[0][1])
                elif tag.startswith("elif "):
                    if not if_stack:
                        raise SyntaxError("{% else %} without matching {% if %}")
                    current_if = if_stack[-1]
                    new_branch = current_if.add_elif(tag[5:].strip())
                    stack.pop()
                    stack.append(new_branch)
                elif tag == "else":
                    if not if_stack:
                        raise SyntaxError("{% else %} without matching {% if %}")
                    current_if = if_stack[-1]
                    new_branch = current_if.add_else()
                    stack.pop()
                    stack.append(new_branch)

                elif tag == "endif":
                    if not if_stack:
                        raise SyntaxError("{% endif %} without matching {% if %}")
                    if_stack.pop()
                    stack.pop()

                elif tag.startswith("for "):
                    # Parse "for x in items"
                    _, var_name, _, iterable = tag.split()
                    node = ForNode(var_name, iterable)
                    stack[-1].append(node)
                    stack.append(node.children)

                elif tag == "endfor":
                    stack.pop()
            else:
                # Regular text
                stack[-1].append(TextNode(token))

        return root

    def render(self, context):
        return "".join(node.render(context) for node in self._nodes)




# # --- Example usage ---
# tpl = Template("""
# Hello {{ name }}!
# {% if admin %}
# You are an admin.
# {% endif %}
#
# Your items:
# {% for x in items %}
#  - {{ x }}
# {% endfor %}
# """)
#
# print(tpl.render({
#     "name": "Sample",
#     "admin": True,
#     "items": ["apple", "banana", "cherry"]
# }))
