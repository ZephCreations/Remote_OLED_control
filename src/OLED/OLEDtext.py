from PIL.ImageFont import ImageFont

from OLED import OLED

from luma.core.render import canvas
from luma.core.virtual import terminal
from luma.core.legacy.font import CP437_FONT
from luma.core.legacy import text

from textwrap import wrap


class OLEDtext(OLED):

    def __init__(self, device, data: dict):
        OLED.__init__(self, device, data)
        self.text = ""
        self.display_console = False
        self.update_data(data)

    def update_data(self, data):
        super().update_data(data)
        self.text = self.wrap_text(self.data.get("text") or "")
        self.display_console = self.data.get("console")

    def update(self):
        if self.display_console:
            print("Console mode")
            term = terminal(self.device)
            term.println(self.text)
        else:
            with canvas(self.device) as draw:
                # Legacy draw for monospace
                text(draw, (0, 0), f"{self.text}", font=CP437_FONT, fill="white")

                # Modern draw with Pillow
                # draw.text((0, 0), f"{self.text}", font=TINY_FONT, fill="white", font_size=12)


    @staticmethod
    def wrap_text(text):
        lines = []

        for line in text.splitlines():
            if line.strip != '':
                wrapped = wrap(line, 20, break_long_words=False, replace_whitespace=False)
                lines.append('\n'.join(wrapped))

        return '\n'.join(lines)

