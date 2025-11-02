from Website.requestHandler import WebRequestHandler
from http.server import ThreadingHTTPServer


Address = ("0.0.0.0", 8000)

if __name__ == "__main__":
    server = ThreadingHTTPServer(Address, WebRequestHandler)
    print(f"Server running on address {Address}")
    server.serve_forever()
