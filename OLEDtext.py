from OLED import OLED

from luma.core.render import canvas
from luma.core.virtual import terminal


class OLEDtext(OLED):

    def __init__(self, device, text="", display_console=False):
        OLED.__init__(self, device)
        self.text = text
        self.display_console = display_console

    def update_text(self, text):
        self.text = text

    def update(self):
        if self.display_console:
            term = terminal(self.device)
            term.println(self.text)
        else:
            with canvas(self.device) as draw:
                draw.text((0, 0), f"{self.text}", fill="white", font_size=12)
