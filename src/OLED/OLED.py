
import time
from luma.core.render import canvas


class OLED:
    def __init__(self, device):
        self.device = device
        self._loading()

    def _loading(self):
        self.device.clear()
        with canvas(self.device) as draw:
            draw.point((0, 0), "white")

    def update(self):
        with canvas(self.device) as draw:
            draw.point((0, 0), "white")
