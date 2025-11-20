import concurrent.futures
import threading

from Website import WebRequestHandler
from http.server import ThreadingHTTPServer
from Database import *

from OLED import OLEDthread, OLEDtext, OLEDtimer


def initialise_database(no_screens):

    # Add screens
    screen_dao = ScreenDAO()
    screen_list = []
    for screen_no in range(1, no_screens + 1):
        screen = Screen(screen_no)
        # If address isn't added, add it
        get_value = screen_dao.get_screen_by_value(screen_no)
        if get_value is None:
            screen = screen_dao.add_screen(screen)
            print(f"Add item {screen_no}")
        else:
            screen = get_value
        screen_list.append(screen)
    print(screen_list)

    # Add default profile.
    profile_dao = ProfileDAO()
    profiles = profile_dao.get_all()
    if len(profiles) <= 1:
        # No profiles exist, add default
        profile = Profile("Default")
        get_value = profile_dao.get_profile_by_value("Default")
        if get_value is None:
            profile = profile_dao.add_profile(profile)
        else:
            profile = get_value
    else:
        # Default first profile
        profile = profiles[0]

    # Add default displays (TEXT type)
    type_dao = DispTypeDAO()
    display_type = type_dao.get_type_by_value(DispTypeList.TEXT.name)
    display_dao = DisplayDAO()
    for screen_no in range(1, no_screens + 1):
        display = Display(
            profile.id,
            screen_list[screen_no-1].id,
            display_type.id,
            {'text': '', 'console': False}
        )
        # If display isn't added, add it
        display_get = display_dao.get_display_by_value(display.profile_id, display.screen_id)
        if display_get is None:
            display_dao.add_display(display)
            print(f"Add display {display.id}")
        else:            # Update OLEDs to show updated display
            display = display_get

        # Get OLED type
        disp_type = DispType("temp")
        disp_type.id = display.type_id
        disp_type = type_dao.get_type(disp_type)
        oled_class = OLEDtext
        if disp_type.name == DispTypeList.TIMER.name:
            oled_class = OLEDtimer
        elif disp_type.name == DispTypeList.IMAGE.name:
            oled_class = None
        elif disp_type.name == DispTypeList.SELECTION.name:
            oled_class = None

        # Update screens
        OLEDthread.change_screen(display.screen_id, oled_class, display.data)
        OLEDthread.threads[display.screen_id - 1].trigger_update()


def setup_oleds():
    # TODO: Reset to previous values
    OLEDthread.change_screen(1, OLEDtext, {"text": "."})
    OLEDthread.set_delay(1, 0.5)

    OLEDthread.change_screen(2, OLEDtext, {"text": "."})
    OLEDthread.set_delay(2, 0.5)

    OLEDthread.change_screen(3, OLEDtext, {"text": "."})
    OLEDthread.set_delay(3, 0.5)

    OLEDthread.change_screen(4, OLEDtext, {"text": "."})
    OLEDthread.set_delay(4, 0.5)


def setup_threads(num, starting_port, address):
    # channel      76543210
    # channel2 = 0b00000100  # channel 2
    OLEDthread.create_threads(num, starting_port, address)


if __name__ == "__main__":
    # Initialise OLEDs
    multiplexer_address = 0x70
    num_screens = 6
    setup_threads(num_screens, 2, multiplexer_address)
    initialise_database(num_screens)

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
            OLEDthread.set_delay(screen_number, 1)


