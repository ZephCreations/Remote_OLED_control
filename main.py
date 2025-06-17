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


if __name__ == "__main__":
    address = 0x70
    # channel      76543210
    # channel2 = 0b00000100  # channel 2

    OLEDthread.create_threads(6, 2, address)
    setup_oleds()

    text = "Zeph is the best"
    text_split = text.split()
    text2 = "Lola is also cool"
    text2_splot = text2.split()

    stop_event = threading.Event()
    oled_port_lock = threading.Lock()

    server = ThreadingHTTPServer(("0.0.0.0", 8000), WebRequestHandler)

    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        executor.submit(server.serve_forever)

        for oled_thread in OLEDthread.threads:
            executor.submit(oled_thread.update, oled_port_lock, stop_event)
#         for i in range(0, len(text_split)):
#             OLEDthread.get_oled(1).update_text(text_split[i])
#             OLEDthread.get_oled(2).update_text(text2_splot[i])
#             time.sleep(1)
#
#         time.sleep(1)

        OLEDthread.update_delay(1, 1)
        OLEDthread.update_delay(2, 1)
        OLEDthread.update_delay(3, 1)
        OLEDthread.update_delay(4, 1)
        OLEDthread.update_delay(5, 1)
        OLEDthread.update_delay(6, 1)


