import json
from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse
from pathlib import Path

from utils import get_project_root
# from OLED import OLEDthread, OLEDtext, OLEDtimer
from template import TemplateLoader

loader = TemplateLoader()
ASSETS_DIR = get_project_root() / 'assets'

class WebRequestHandler(BaseHTTPRequestHandler):
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
            # Load and render the template dynamically
            tpl = loader.load("pages/main.html")
            html = tpl.render({
                "screens": ["Alpha", "Theta", "Zeta"]
            })
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

    # -----------------------------------------------------------
    # Application Logic
    # -----------------------------------------------------------
    def process_form_data(self):
        name = self.form_data.get('type')
        print(name)
        if name == "Timer":
            value = self.form_data.get('timer_val')
            screen = int(self.form_data.get("screen"))
            if value == "start":
                # OLEDthread.change_screen(screen, OLEDtimer)
                speed = int(self.form_data.get("timer_update_speed"))
                # if speed is not None:
                    # OLEDthread.update_delay(screen, speed)
                print("Start timer")
            elif value == "pause":
                # oled = OLEDthread.get_oled(screen)
                # if type(oled) is OLEDtimer:
                #     oled.pause()
                print("Pause timer")
            elif value == "reset":
                # oled = OLEDthread.get_oled(screen)
                # if type(oled) is OLEDtimer:
                #     oled.reset()
                print("Restart timer")
            else:
                print("Value not found")
        elif name == "Text":
            text = self.form_data.get("text_input")
            if text is None:
                text = ""
            screen = int(self.form_data.get("screen"))
            console = False
            if self.form_data.get("display_console"):
                console = True
            # OLEDthread.change_screen(screen, OLEDtext, text, console)
            print(text)

