from time import time
from datetime import timedelta
from OLED import OLED
from luma.core.render import canvas


class OLEDtimer(OLED):
    def __init__(self, device, data: dict):
        OLED.__init__(self, device, data, True)
        self.name = self.data.get("name")
        self.paused = False
        self.starting_time = time()
        self.paused_since = None
        self.pause_total = 0.0
        self.value = 0.0

    def update(self):
        with canvas(self.device) as draw:
            draw.text((0, 0), f"{self.name}:", fill="white", font_size=14)
            draw.text((0, 20), f"{self._format_time()}:", fill="white", font_size=14)
            if not self.paused:
                self.value = time() - self.starting_time - self.pause_total

    def pause(self):
        if not self.paused:
            # Just paused
            self.paused_since = time()
            self.paused = True
        else:
            # Resumed
            self.pause_total += time() - self.paused_since
            self.paused_since = None
            self.paused = False

    def reset(self):
        self.starting_time = time()
        self.value = 0
        self.pause_total = 0.0
        if self.paused:
            self.paused_since = time()
        else:
            self.paused_since = None
            self.pause_total = 0.0

    def _format_time(self):
        m, s = divmod(self.value, 60)
        h, m = divmod(m, 60)
        return f"{int(h):d}:{int(m):02d}:{s:.02f}"

    @staticmethod
    def format_time(value):
        m, s = divmod(value, 60)
        h, m = divmod(m, 60)
        return f"{int(h):d}:{int(m):02d}:{s:.02f}"

