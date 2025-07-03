from http.server import BaseHTTPRequestHandler, HTTPServer
from controllers.user_controller import *
from controllers.permission_controller import *
from controllers.user_permission_controller import *

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/users":
            # Get all users
            response = handle_user_request()
        elif self.path.startswith("/users/"):
            # Extract username or ID from path (e.g., /users/john)
            name = self.path.split("/")[-1]
            response = handle_user_get_by_name(name)
        elif self.path == "/permissions":
            #response = handle_permission_request("GET")
            response = handle_permission_request()
        elif self.path.startswith("/permissions/"):
            # Extract permission name or ID from path (e.g., /permissions/read)
            name = self.path.split("/")[-1]
            response = handle_permission_get_by_name(name)
        elif self.path == "/user_permissions" :
            response = handle_user_permission_get_all()
        elif self.path.startswith("/user_permissions/") :
            user_id = int(self.path.split("/")[-1])
            response = handle_user_permission_get_by_user(user_id)
        else:
            response = '{"error": "Route not found"}'
        self._send_response(response)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        if self.path == "/user":
            # Add new user
            print(body)
            response = handle_user_add(body)
        elif self.path == "/permission":
            response = handle_permission_add(body)
        elif self.path == "/user_permissions":
            response = handle_user_permission_add(body)
        else:
            response = '{"error": "Route not found"}'
        self._send_response(response)

    def _send_response(self, response_body):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response_body.encode("utf-8"))

def run_server():
    server = HTTPServer(("localhost", 443), MyHandler)
    print("Server started at http://localhost:443")
    server.serve_forever()



