from Website.requestHandler import WebRequestHandler
from http.server import ThreadingHTTPServer
from Database import *

Address = ("0.0.0.0", 8000)


def initialise_database(no_screens):
    get_value = None

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
    # TODO: Add restore to previous settings (like previous profiles etc.)
    profile_dao = ProfileDAO()
    profile = Profile("Default")
    get_value = profile_dao.get_profile_by_value("Default")
    if get_value is None:
        profile = profile_dao.add_profile(profile)
    else:
        profile = get_value

    # Add default displays (TEXT type)
    type_dao = DispTypeDAO()
    display_type = type_dao.get_type_by_value(DispTypeList.TEXT.name)
    display_dao = DisplayDAO()
    for screen_no in range(1, no_screens + 1):
        display = Display(profile.id, screen_list[screen_no-1].id, display_type.id, "")
        # If display isn't added, add it
        display_get = display_dao.get_display_by_value(display.profile_id, display.screen_id, display.type_id)
        if display_get is None:
            display_dao.add_display(display)
            print(f"Add display {display.id}")
        else:
            display = display_get




if __name__ == "__main__":
    initialise_database(6)
    server = ThreadingHTTPServer(Address, WebRequestHandler)
    print(f"Server running on address {Address}")
    server.serve_forever()
