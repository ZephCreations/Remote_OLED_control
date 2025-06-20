import concurrent.futures
import threading
import time

from requestHandler import WebRequestHandler
from http.server import ThreadingHTTPServer

from OLEDthread import OLEDthread
from OLED import OLED
from OLEDtext import OLEDtext
from OLEDimage import OLEDimage
from OLEDtimer import OLEDtimer


def setup_oleds():
    OLEDthread.change_screen(1, OLEDtext)
    OLEDthread.update_delay(1, 0.5)

    OLEDthread.change_screen(2, OLEDtext)
    OLEDthread.update_delay(2, 0.5)

    OLEDthread.change_screen(3, OLEDimage)
    OLEDthread.update_delay(3, 10)
    OLEDthread.get_oled(3).update_image("files/Axalotl.jpg")

    OLEDthread.change_screen(4, OLEDtimer)
    OLEDthread.update_delay(4, 1)


def setup_threads(num, starting_port, address):
    # channel      76543210
    # channel2 = 0b00000100  # channel 2
    OLEDthread.create_threads(num, starting_port, address)


if __name__ == "__main__":
    # Initialise OLEDs
    multiplexer_address = 0x70
    num_screens = 6
    setup_threads(num_screens, 2, multiplexer_address)
    setup_oleds()

    stop_event = threading.Event()
    oled_port_lock = threading.Lock()

    # Start Webserver
    server = ThreadingHTTPServer(("0.0.0.0", 8000), WebRequestHandler)

    # Keep threads going
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        executor.submit(server.serve_forever)

        for oled_thread in OLEDthread.threads:
            executor.submit(oled_thread.update, oled_port_lock, stop_event)

        # Set delay and start looping
        for screen_number in range(1, num_screens+1):
            OLEDthread.update_delay(screen_number, 1)


