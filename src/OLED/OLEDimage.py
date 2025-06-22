from OLED import OLED
from PIL import Image
from pathlib import Path

class OLEDimage(OLED):

    def __init__(self, device):
        OLED.__init__(self, device)
        self.full_path = ""
        self.image = None
        self.position = (0, 0)
        self.background = Image.new("RGBA", self.device.size, "white")

    def update_image(self, filename):
        self.full_path = str(Path(__file__).resolve().parent.joinpath(filename))
        self.image = Image.open(self.full_path).convert("RGBA")
        self.position = ((self.device.width - self.image.width) // 2, 0)

    def update(self):
        self.background.paste(self.image, self.position)
        self.device.display(self.background.convert(self.device.mode))
