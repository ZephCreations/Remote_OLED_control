from time import sleep
from threading import Event

# from smbus2 import SMBus
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

from OLED import OLED


class OLEDthread:
    start_port = 2
    oleds = []

    def __init__(self, id, address, screen):
        self.id = id
        self.address = address
        self.screen = screen
        self.port = 1 << (OLEDthread.start_port + self.screen - 1)
        print(bin(self.port))

        # Increase array to ensure right size
        while len(OLEDthread.oleds) < screen:
            OLEDthread.oleds.append(None)

        OLEDthread.oleds[screen - 1] = self

        self.bus = SMBus(1)
        self.bus.write_byte(self.address, self.port)
        serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(serial)

        self.oled = OLED(self.device)

        self.delay = 1
        self.interrupt_event = Event()

    def _set_delay(self, delay):
        self.delay = delay

    def interrupt(self):
        self.interrupt_event.set()

    def _handle_interrupt(self, lock):
        with lock:
            self.interrupt_event.clear()

    def update(self, lock, stop_event):
        while not stop_event.is_set():
            if self.interrupt_event.is_set():
                self._handle_interrupt(lock)
                break
            with lock:
                print(f"Start OLED {self.port}")
                self.bus.write_byte(0x70, self.port)
                self.oled.update()
                print(f"Updated OLED {self.port}")
            sleep(self.delay)

    @staticmethod
    def update_delay(screen, delay):
        try:
            OLEDthread.oleds[screen - 1]._set_delay(delay)
        except IndexError:
            pass

    @staticmethod
    def change_screen(screen, function, *args, **kwargs):
        try:
            old = OLEDthread.oleds[screen - 1]
            old.oled = function(old.device, *args, **kwargs)
        except IndexError:
            print("Can't change")
            pass

    @classmethod
    def get_oled(cls, screen):
        try:
            return OLEDthread.oleds[screen - 1].oled
        except IndexError:
            return None

    @classmethod
    def create_threads(cls, num, starting_port, address):
        cls.start_port = starting_port
        cls.oleds.clear()
        for oled in range(1, num + 1):
            cls.oleds.append(cls(oled, address, oled))




