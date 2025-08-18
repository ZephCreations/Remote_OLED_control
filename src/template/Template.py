import re
from Node import TextNode, VariableNode, IfNode, EndIfNode, ForNode, EndForNode

class Template:
    def __init__(self, template_str):
        self.template_str = template_str
        self._tokens = self._tokenize()
        self._nodes = self._parse()

    def _tokenize(self):
        """
        Splits text into raw text, variables {{ var }}, and tags {% tag %}
        """
        token_re = re.compile(r"({{.*?}}|{%.*?%})")
        parts = token_re.split(self.template_str)
        return [p for p in parts if p]

    def _parse(self):
        """
        Converts tokens into node objects.
        """
        nodes = []
        for token in self._tokens:
            if token.startswith("{{") and token.endswith("}}"):
                # Variable
                # Remove {{ }} brackets
                expr = token[2:-2].strip()

                # Add variable node
                nodes.append(VariableNode(expr))
            elif token.startswith("{%") and token.endswith("%}"):
                # Tag
                # Remove {{ }} brackets
                tag = token[2:-2].strip()

                # Switch case on type
                if tag.startswith("if "):
                    nodes.append(IfNode(tag[3:].strip()))
                elif tag == "endif":
                    nodes.append(EndIfNode())
                elif tag.startswith("for "):
                    # TODO Add loops
                    pass
            else:
                # Regular text
                nodes.append(TextNode(token))
        return nodes

    def render(self, context):
        """
        Walk nodes and render into a string.
        """
        output = []

        # Check to see whether to skip over a block of code or not
        skip = False
        loop = False
        for node in self._nodes:
            # Check node type
            if isinstance(node, IfNode):
                # Skip over block if context variable with the name of node.var is FALSE
                # Defaults to FALSE if no context var is provided
                skip = not context.get(node.var, False)
            elif isinstance(node, EndIfNode):
                # Stop skipping content (nodes) when endif is reached.
                skip = False
            elif isinstance(node, ForNode):
                pass
            elif isinstance(node, EndForNode):
                pass
                loop = False
            elif not skip:
                # Insert node content (variable or text) if it is not being skipped.
                output.append(node.render(context))
        # End of for loop

        return "".join(output)




# --- Example usage ---
tpl = Template("Hello {{ name }}! {% if admin %}You are an admin.{% endif %}")
print(tpl._nodes)
print(tpl.render({"name": "Sample", "admin": True}))

print(tpl.render({"name": "Sample", "admin": False}))
