import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json

class MockBattleNetHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == "/oauth/token":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"access_token": "mock_access_token", "token_type": "bearer", "expires_in": 3600}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path.startswith("/profile/wow/character/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"character": "dummy_character", "realm": "dummy_realm", "level": 60}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def start_mock_server(server_class=HTTPServer, handler_class=MockBattleNetHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    return httpd

# Start mock server before running tests
mock_server = start_mock_server()

class TestAll(unittest.TestCase):
    def test_all(self):
        # Test the BattleNetAPI class
        from battlenet import BattleNetAPI


        # Initialize the API with dummy credentials
        client_id = "dummy_client_id"
        client_secret = "dummy_client_secret"
        api = BattleNetAPI(client_id, client_secret)

        # Test getting an access token
        token = api.get_access_token()
        self.assertIsInstance(token, str)
        self.assertNotEqual(token, "")

        # Test getting WoW profile
        realm = "dummy_realm"
        character_name = "dummy_character"
        profile = api.get_wow_profile(realm, character_name)
        self.assertIsInstance(profile, dict)

if __name__ == '__main__':
    mock_server = start_mock_server()

    unittest.main()
