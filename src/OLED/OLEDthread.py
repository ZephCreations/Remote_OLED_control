import time
from time import sleep
from threading import Event

from smbus2 import SMBus
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

from OLED import OLED


class OLEDthread:
    start_port = 2
    threads = []

    def __init__(self, address, screen_no):
        self.address = address
        self.screen_no = screen_no
        self.port = 1 << (OLEDthread.start_port + self.screen_no - 1)
        print(bin(self.port))

        # Increase array to ensure right size and add instance to array
        while len(OLEDthread.threads) < self.screen_no:
            OLEDthread.threads.append(None)
        OLEDthread.threads[self.screen_no - 1] = self

        # Initialise BUS and setup I2C communication
        self.bus = SMBus(1)
        self.bus.write_byte(self.address, self.port)
        serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(serial)

        # Add OLED and setup variables for updating
        self.oled = OLED(self.device)
        self.update_event = Event()
        self.dynamic_mode = False
        self.delay = 1

    def trigger_update(self):
        """External force-update (interrupt, used by web requests)"""
        self.update_event.set()

    def set_dynamic(self, state: bool):
        """Enable/disable dynamic auto-updating (e.g. timers)"""
        self.dynamic_mode = state
        if state:
            self.update_event.set() # wake if sleeping

    def set_delay(self, delay):
        self.delay = delay

    def update(self, lock, stop_event):
        while not stop_event.is_set():
            # Wait loop
            if not self.dynamic_mode:
                # Sleep until either forced update or shutdown
                self.update_event.wait()
                self.update_event.clear()

            # Perform screen update
            with lock:
                self.bus.write_byte(0x70, self.port)
                self.oled.update()
                print(f"Updated OLED {self.port}")

            # If thread is told to stop
            if stop_event.is_set():
                return

            # If dynamic delay, wait for time
            if self.dynamic_mode:
                self.update_event.wait(self.delay)
                self.update_event.clear()

    @staticmethod
    def update_delay(screen_no, delay):
        try:
            OLEDthread.threads[screen_no - 1].set_delay(delay)
        except IndexError:
            pass

    @staticmethod
    def change_screen(screen_no, function, *args, **kwargs):
        try:
            old = OLEDthread.threads[screen_no - 1]
            old.oled = function(old.device, *args, **kwargs)
        except IndexError:
            print("Can't change")

    @classmethod
    def get_oled(cls, screen_no):
        try:
            return OLEDthread.threads[screen_no - 1].oled
        except IndexError:
            return None

    @classmethod
    def create_threads(cls, no_threads, starting_port, address):
        cls.start_port = starting_port
        cls.threads.clear()
        for oled_no in range(1, no_threads + 1):
            cls.threads.append(cls(address, oled_no))





