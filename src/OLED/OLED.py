
import time
from luma.core.render import canvas


class OLED:
    def __init__(self, device, data: dict, is_dynamic=False):
        self.device = device
        self.data = data
        self.is_dynamic = is_dynamic

    def loading_anim(self):
        self.device.clear()
        with canvas(self.device) as draw:
            draw.point((0, 0), "white")

    def update_data(self, data):
        self.data = data

    def update(self):
        with canvas(self.device) as draw:
            draw.point((0, 0), "white")
