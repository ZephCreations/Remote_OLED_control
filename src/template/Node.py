from .node_utils import eval_condition, resolve_var


class TemplateNode:
    def render(self, context):
        raise NotImplementedError


class TextNode(TemplateNode):
    def __init__(self, text):
        self.text = text

    def render(self, context):
        return self.text


class VariableNode(TemplateNode):
    def __init__(self, var):
        self.var = var

    def render(self, context):
        val = resolve_var(self.var, context)
        return "" if val is None else str(val)


class IfNode(TemplateNode):
    def __init__(self, condition):
        # Holds tuples: (condition_expr or None, [child_nodes])
        self.branches = [(condition, [])]

    def add_elif(self, condition):
        self.branches.append((condition, []))

    def add_else(self):
        self.branches.append((None, []))
        return self.branches[-1][1] # return the new branch list

    def render(self, context):
        for condition, branch in self.branches:
            if condition is None or eval_condition(condition, context):
                return "".join(child.render(context) for child in branch)
        return ""


class ForNode(TemplateNode):
    def __init__(self, var_name, iterable_name):
        self.var_name = var_name
        self.iterable_name = iterable_name
        self.children = []

    def render(self, context):
        iterable = resolve_var(self.iterable_name, context)
        if iterable is None:
            iterable = context.get(self.iterable_name, [])

        # Try to make it iterable
        try:
            iterable = list(iterable)
        except TypeError:
            iterable = []

        output = []
        total = len(iterable)

        for i, item in enumerate(iterable):
            # Each iteration has its own copy of context
            local_context = context.copy()
            local_context[self.var_name] = item

            # Add forloop context
            local_context["forloop"] = {
                "counter": i + 1, # 1-based
                "counter0": i,    # 0-based
                "first": (i == 0),
                "last": (i == total - 1),
            }

            # Render all children with the new context
            rendered = "".join(child.render(local_context) for child in self.children)
            output.append(rendered)
        return "".join(output)