from Website.requestHandler import WebRequestHandler
from http.server import ThreadingHTTPServer


Address = ("", 8000)

if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()
