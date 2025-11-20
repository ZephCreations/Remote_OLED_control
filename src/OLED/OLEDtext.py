from OLED import OLED

from luma.core.render import canvas
from luma.core.virtual import terminal

from textwrap import wrap


class OLEDtext(OLED):

    def __init__(self, device, data: dict):
        OLED.__init__(self, device, data)
        self.text = self.wrap_text(self.data.get("text"))
        self.display_console = self.data.get("console") or False


    def update(self):
        if self.display_console:
            term = terminal(self.device)
            term.println(self.text)
        else:
            with canvas(self.device) as draw:
                draw.text((0, 0), f"{self.text}", fill="white", font_size=12)


    @staticmethod
    def wrap_text(text):
        lines = []

        for line in text.splitlines():
            if line.strip != '':
                wrapped = wrap(line, 20, break_long_words=False, replace_whitespace=False)
                lines.append('\n'.join(wrapped))

        return '\n'.join(lines)

