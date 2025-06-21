from OLED import OLED

from luma.core.render import canvas
from luma.core.virtual import terminal


class OLEDtext(OLED):

    def __init__(self, device, text="", display_console=False):
        OLED.__init__(self, device)

        # Setup text
        self.text = text
        self._add_line_breaks()

        # Other variables
        self.display_console = display_console

    def _add_line_breaks(self, every=20):
        lines = []
        for i in range(0, len(self.text), every):
            lines.append(self.text[i:i + every])
        self.text = '\n'.join(lines)

    def update(self):
        if self.display_console:
            term = terminal(self.device)
            term.println(self.text)
        else:
            with canvas(self.device) as draw:
                draw.text((0, 0), f"{self.text}", fill="white", font_size=12)
