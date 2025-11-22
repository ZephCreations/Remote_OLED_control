import json
from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl
from pathlib import Path

from utils import get_project_root
from OLED import OLEDthread, OLEDtext, OLEDtimer, OLEDchecklist
from template import TemplateLoader
from Database import *

loader = TemplateLoader()
ASSETS_DIR = get_project_root() / 'assets'

class WebRequestHandler(BaseHTTPRequestHandler):
    active_profile_id = None
    active_screen_id = None

    @cached_property
    def display_dao(self):
        return DisplayDAO()

    @cached_property
    def profile_dao(self):
        return ProfileDAO()

    @cached_property
    def type_dao(self):
        return DispTypeDAO()

    @cached_property
    def screen_dao(self):
        return ScreenDAO()

    @cached_property
    def default_profile(self):
        profile = self.profile_dao.get_profile_by_value("Default")
        if profile is None:
            profile = self.profile_dao.add_profile(Profile("Default"))
        return profile

    # -----------------------------------------------------------
    # Cached properties for request parsing
    # -----------------------------------------------------------
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def cookies(self):
        return SimpleCookie(self.headers.get("Cookie"))

    # -----------------------------------------------------------
    # HTTP GET
    # -----------------------------------------------------------
    def do_GET(self):
        if self.path == '/':
            # Get current profile/display
            current_profile = self.get_current_profile()
            current_screen = self.get_current_screen()
            print(f"Active: profile {current_profile.name}, screen {current_screen.id}")

            # Get all profiles
            profiles = self.profile_dao.get_all()
            if len(profiles) == 0:
                # No default, create
                self.profile_dao.add_profile(Profile("Default"))

            # Get all displays
            displays = self.display_dao.get_all_by_profile_id(current_profile)
            current_display = displays[current_screen.id - 1]

            # Get type
            disp_type = DispType("temp")
            disp_type.id = current_display.type_id
            disp_type = self.type_dao.get_type(disp_type)

            # Get checklist (if relavent)
            items = []
            if disp_type.name == "CHECKLIST":
                # Pad or slice existing list to exactly 4
                raw_items = current_display.data.get("items", [])
                for i in range(4):
                    if i < len(raw_items):
                        items.append(raw_items[i])
                    else:
                        items.append(("", False))
            else:
                # Default blank list
                items = [("", False) for _ in range(4)]

            # Load and render the template dynamically
            context = {
                "profiles": profiles,
                "current_profile": current_profile,
                "displays": displays,
                "current_display": current_display,
                "current_screen": current_screen,
                "current_type": disp_type.name,
                "checklist_items": items,
            }
            tpl = loader.load("pages/main.html")
            html = tpl.render(context)
            self.send_html(html)
            return

        # Handle static files (CSS/JS)
        elif self.path.endswith('.css'):
            file_path = ASSETS_DIR / 'css' / Path(self.path).name
            self.send_file(file_path, "text/css")
        elif self.path.endswith('.js'):
            file_path = ASSETS_DIR / 'js' / Path(self.path).name
            self.send_file(file_path, "application/javascript")

        # No correct files/paths OR unknown route
        else:
            self.send_error(404, "File not found")

    # -----------------------------------------------------------
    # HTTP POST
    # -----------------------------------------------------------
    def do_POST(self):
        if self.form_data:
            print(self.form_data)
            self.process_form_data()
        # Re-render the main page after POST
        self.do_GET()

    # -----------------------------------------------------------
    # Response helpers
    # -----------------------------------------------------------
    def send_html(self, html: str):
        """Send HTML string to the browser."""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def send_file(self, path: Path, content_type: str):
        """Send static files like CSS/JS."""
        if path.is_file():
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            with open(path.as_posix(), "rb") as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, f"File not found: {path}")

    def get_response(self):
        """Debug helper: return request info as JSON."""
        return json.dumps(
            {
                "path": self.url.path,
                "query_data": self.query_data,
                "post_data": self.post_data.decode("utf-8"),
                "form_data": self.form_data,
                "cookies": {
                    name: cookie.value
                    for name, cookie in self.cookies.items()
                },
            }
        )

    def get_current_profile(self):
        # Get active profile
        profile_id = WebRequestHandler.active_profile_id

        # If no active profile, use default
        if profile_id is None:
            print("No active profile")
            WebRequestHandler.active_profile_id = self.default_profile.id
            return self.default_profile

        # Get from db
        profile = Profile("temp")
        profile.id = profile_id
        profile = self.profile_dao.get_profile(profile)

        # If deleted, reset to default
        if profile is None:
            print(f"No profile by id {profile_id}")
            WebRequestHandler.active_profile_id = self.default_profile.id
            return self.default_profile

        return profile

    def get_current_screen(self):
        # Get active display
        screen_id = WebRequestHandler.active_screen_id

        # If no active, use first
        if screen_id is None:
            print("No active screen")
            first_screen = self.screen_dao.get_all()[0]
            WebRequestHandler.active_screen_id = first_screen.id
            return first_screen

        # Get from db
        screen = Screen("temp")
        screen.id = screen_id
        screen = self.screen_dao.get_screen(screen)

        return screen

    # -----------------------------------------------------------
    # Application Logic
    # -----------------------------------------------------------
    def process_form_data(self):
        post_type = self.form_data.get('type')
        profile_action = self.form_data.get('profile_action')
        screen_action = self.form_data.get('screen_action')

        # Profile Actions
        if profile_action is not None:
            self.handle_profile_form()
            return

        # Screen actions
        if screen_action is not None:
            self.handle_screen_form()
            return

        # OLED actions
        if post_type == "Timer":
            self.handle_timer_form()
            return
        elif post_type == "Text":
            self.handle_text_form()
            return
        elif post_type == "Checklist":
            self.handle_checklist_form()
            return

    def handle_profile_form(self):
        profile_action = self.form_data.get('profile_action')
        if profile_action == "switch":
            try:
                WebRequestHandler.active_profile_id = int(self.form_data.get("profile"))
                self.update_all()
            except (TypeError, ValueError):
                pass
            return
        elif profile_action == "new":
            # Add profile
            profile_name = self.form_data.get('profile_name')
            new_profile = Profile(profile_name)
            try:
                new_profile = self.profile_dao.add_profile(new_profile)
            except DatabaseExceptions.UniqueConstraintFailedException:
                # Do nothing if profile already exists
                print("Profile already exists")
                return

            # Add linked displays
            display_type = self.type_dao.get_type_by_value(DispTypeList.TEXT.name)
            screens = self.screen_dao.get_all()

            for screen in screens:
                display = Display(new_profile.id, screen.id, display_type.id, "")
                # If display isn't added, add it
                display_get = self.display_dao.get_display_by_value(
                    display.profile_id, display.screen_id)
                if display_get is None:
                    self.display_dao.add_display(display)

            # Set active profile
            WebRequestHandler.active_profile_id = new_profile.id
            self.update_all()
            return
        elif profile_action == "rename":
            profile_name = self.form_data.get('profile_name')
            profile_id = self.form_data.get('profile_id')
            temp_profile = Profile(profile_name)
            temp_profile.id = profile_id
            self.profile_dao.update_profile(temp_profile)
            return
        elif profile_action == "delete":
            # Prevent deleting only profile
            profiles = self.profile_dao.get_all()
            if len(profiles) > 1:
                profile_id = self.form_data.get('profile_id')
                temp_profile = Profile("temp")
                temp_profile.id = profile_id
                # Remove displays
                for display in self.display_dao.get_all_by_profile_id(temp_profile):
                    self.display_dao.remove_display(display)
                # Remove profile
                self.profile_dao.remove_profile(temp_profile)
                # Set active profile as first profile
                WebRequestHandler.active_profile_id = self.profile_dao.get_all()[0].id
                self.update_all()
            else:
                # Can't delete last profile, do nothing
                pass
            return

    def handle_screen_form(self):
        screen_action = self.form_data.get('screen_action')
        if screen_action == "switch":
            try:
                WebRequestHandler.active_screen_id = int(self.form_data.get("screen"))
            except (TypeError, ValueError):
                pass
            return

    def handle_text_form(self):
        # Variables
        text = self.form_data.get('text_input')
        screen_id = int(self.form_data.get('screen_id', 0))
        console = False
        if self.form_data.get('display_console'):
            console = True
        profile_id = self.get_current_profile().id
        type_id = self.type_dao.get_type_by_value(DispTypeList.TEXT.name).id

        # Update Database
        content = {
            "text": text,
            "console": console
        }
        display = Display(profile_id, screen_id, type_id, content)
        existing = self.display_dao.get_display_by_value(profile_id, screen_id)
        if existing is not None:
            self.display_dao.update_display(display)
        else:
            self.display_dao.add_display(display)

        # Update OLEDs
        self.update_single(display)

    def handle_timer_form(self):
        screen_id = int(self.form_data.get('screen_id'))
        profile_id = self.get_current_profile().id
        type_id = self.type_dao.get_type_by_value(DispTypeList.TIMER.name).id
        timer_action = self.form_data.get('timer_val')
        speed = float(self.form_data.get('timer_update_speed') or 1)
        name = self.form_data.get('timer_name') or 'Timer'

        # Create display object
        content = {
            "name": name,
            "state": timer_action,
            "delay": speed,
            "value": 0,
            "paused": True
        }
        display = Display(profile_id, screen_id, type_id, content)

        # Update OLEDS and timer state
        if timer_action == "start":
            display.data["paused"] = False
            self.update_single(display)
            print("Start timer")
        elif timer_action == "pause":
            oled = OLEDthread.get_oled(screen_id)
            if type(oled) is OLEDtimer:
                oled.pause()
                OLEDthread.set_dynamic(screen_id, not oled.paused)
                display.data["value"] = oled.value
                display.data["paused"] = oled.paused
                self.update_single(display)
            print("Pause timer")
        elif timer_action == "reset":
            oled = OLEDthread.get_oled(screen_id)
            if type(oled) is OLEDtimer:
                oled.reset()
                OLEDthread.set_dynamic(screen_id, not oled.paused)
                display.data["value"] = 0
                display.data["paused"] = oled.paused
                self.update_single(display)
            print("Restart timer")
        else:
            print("Value not found")

        # Update database
        display.data["text"] = (f"{name}<br>"
                                f"{timer_action} - {speed}s<br>"
                                f"{OLEDtimer.format_time(display.data['value'])}")
        existing = self.display_dao.get_display_by_value(profile_id, screen_id)
        if existing is not None:
            self.display_dao.update_display(display)
        else:
            self.display_dao.add_display(display)

    def handle_checklist_form(self):
        screen_id = int(self.form_data.get('screen_id', 0))
        profile_id = self.get_current_profile().id
        type_id = self.type_dao.get_type_by_value(DispTypeList.CHECKLIST.name).id
        items = []

        # Get items from form
        for i in range(4):
            text = self.form_data.get(f"item_text_{i}", "").strip()
            checked = self.form_data.get(f"item_check_{i}") is not None
            items.append((text, checked))

        # Update database
        content = {
            "items": items,
            "text": "<br>".join(
                    f"{'[x]' if checked else '[ ]'} {text}"
                    for text, checked in items
                ),
        }
        print(content)
        display = Display(profile_id, screen_id, type_id, content)
        existing = self.display_dao.get_display_by_value(profile_id, screen_id)
        if existing is not None:
            self.display_dao.update_display(display)
        else:
            self.display_dao.add_display(display)

        # Update OLEDs
        self.update_single(display)

    # -----------------------------------------------------------
    # OLED functions
    # -----------------------------------------------------------
    def update_all(self):
        displays = self.display_dao.get_all_by_profile_id(self.get_current_profile())
        for display in displays:
            self.update_single(display)

    def update_single(self, display: Display):
        # Get OLED type
        disp_type = DispType("temp")
        disp_type.id = display.type_id
        disp_type = self.type_dao.get_type(disp_type)
        oled_class = OLEDtext
        if disp_type.name == DispTypeList.TIMER.name:
            oled_class = OLEDtimer
        elif disp_type.name == DispTypeList.IMAGE.name:
            oled_class = None
        elif disp_type.name == DispTypeList.SELECTION.name:
            oled_class = None
        elif disp_type.name == DispTypeList.CHECKLIST.name:
            oled_class = OLEDchecklist

        # Update screens
        OLEDthread.change_type(display.screen_id, oled_class, display.data)
        OLEDthread.get_thread(display.screen_id).trigger_update()