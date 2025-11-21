from OLED import OLED

from luma.core.render import canvas

from textwrap import wrap


class OLEDtext(OLED):

    def __init__(self, device, data: dict):
        OLED.__init__(self, device, data)
        self.items = []
        self.text = ""
        self.update_data(data)

    def update_data(self, data):
        super().update_data(data)
        self.items = data.get("items") # format [(str, bool), (str, bool)]
        self.text = self.join_text(self.items)

    def update(self):
        with canvas(self.device) as draw:
            # Legacy draw for monospace
            # text(draw, (0, 0), f"{self.text}", font=CP437_FONT, fill="white")

            # Modern draw with Pillow
            draw.text((0, 0), f"{self.text}", fill="white", font_size=12)


    @staticmethod
    def join_text(items):
        return "\n".join(
            f"{'[x]' if checked else '[]'} {text}"
            for text, checked in items
        ),

