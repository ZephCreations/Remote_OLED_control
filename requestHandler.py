import json
from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse

from OLEDthread import OLEDthread
from OLEDtext import OLEDtext
from OLEDtimer import OLEDtimer


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

    def do_GET(self):
        if self.path == '/':
            self.path = '/pages/main.html'
        try:
            file = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file = "File not found"
            self.send_response(404)

        # self.send_response(200)
        # self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(file, 'utf-8'))
        # self.wfile.write(self.get_response().encode("utf-8"))

    def do_POST(self):
        if self.form_data:
            print(self.form_data)
            self.process_form_data()
        # self.send_response(200)
        # self.send_header("Content-Type", "application/json")
        # self.end_headers()
        # self.wfile.write(self.get_response().encode("utf-8"))
        self.do_GET()

    def get_response(self):
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

    def process_form_data(self):
        name = self.form_data.get('type')
        print(name)
        if name == "Timer":
            value = self.form_data.get('timer_val')
            screen = int(self.form_data.get("screen"))
            if value == "start":
                OLEDthread.change_screen(screen, OLEDtimer)
                speed = int(self.form_data.get("timer_update_speed"))
                if speed is not None:
                    OLEDthread.update_delay(screen, speed)
                print("Start timer")
            elif value == "pause":
                oled = OLEDthread.get_oled(screen)
                if type(oled) is OLEDtimer:
                    oled.pause()
                print("Pause timer")
            elif value == "reset":
                oled = OLEDthread.get_oled(screen)
                if type(oled) is OLEDtimer:
                    oled.reset()
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
            OLEDthread.change_screen(screen, OLEDtext, text, console)
            print(text)

