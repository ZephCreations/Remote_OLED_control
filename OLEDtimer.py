from time import time
from datetime import timedelta
from OLED import OLED
from luma.core.render import canvas


class OLEDtimer(OLED):
    def __init__(self, device, name="Timer"):
        OLED.__init__(self, device)
        self.name = name
        self.paused = False
        self.starting_time = time()
        self.value = 0

    def update(self):
        with canvas(self.device) as draw:
            draw.text((0, 0), f"{self.name}:", fill="white", font_size=14)
            draw.text((0, 20), f"{self._format_time()}:", fill="white", font_size=14)
            if not self.paused:
                self.value = time() - self.starting_time

    def pause(self):
        self.paused = not self.paused

    def reset(self):
        self.starting_time = time()
        self.value = 0

    def _format_time(self):
        m, s = divmod(self.value, 60)
        h, m = divmod(m, 60)
        return f"{int(h):d}:{int(m):02d}:{s:.02f}"

