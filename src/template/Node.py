
class TemplateNode:
    def __init__(self, var=None):
        self.var = var

    def render(self, content):
        pass


class TextNode(TemplateNode):
    def __init__(self, text):
        super().__init__(text)

    def render(self, context):
        return self.var


class VariableNode(TemplateNode):
    def __init__(self, var):
        super().__init__(var)

    def render(self, context):
        return str(context.get(self.var, ""))


class IfNode(TemplateNode):
    def __init__(self, var):
        super().__init__(var)


class EndIfNode(TemplateNode):
    pass


class ForNode(TemplateNode):
    pass


class EndForNode(TemplateNode):
    pass
