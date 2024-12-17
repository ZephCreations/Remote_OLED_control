from OLED import OLED

from luma.core.render import canvas


class OLEDtimer(OLED):
    def __init__(self, device):
        OLED.__init__(self, device)


    def update(self):
        with canvas(self.device) as draw:
            draw.text((0, 0), f"Timer:", fill="white", font_size=12)

