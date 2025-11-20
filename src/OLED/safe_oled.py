from utils import is_pi

if is_pi():
    from luma.core.interface.serial import i2c
    from luma.oled.device import ssd1306
else:
    # Mock OLED on Windows
    class MockSerial:
        def __init__(self, *args, **kwargs):
            print("[Mock OLED] Serial initialised")

    class MockSSD1306:
        width = 128
        height = 64
        mode = "1"
        size = (width, height)

        def __init__(self, serial):
            print("[Mock OLED] SSD1306 mock created")

        def display(self, image):
            print("[Mock OLED] Display update")

        def clear(self):
            print("[Mock OLED] Clear")

        def show(self):
            print("[Mock OLED] Show called")

    def i2c(**kwargs):
        return MockSerial()

    def ssd1306(serial):
        return MockSSD1306(serial)
