from flask import Flask, jsonify
import threading
import unittest
import battlenet as battlenet

# Flask app to mock BattleNet API
app = Flask(__name__)

@app.route('/token', methods=['POST'])
def oauth_token():
    return jsonify({
        "access_token": "mock_access_token",
        "token_type": "bearer",
        "expires_in": 3600
    })

@app.route('/data/wow/connected-realm/index', methods=['GET'])
def connected_realm_index():
    return jsonify({
        "connected_realms": [
            {
                "id": 1,
                "name": "Mock Realm",
                "slug": "mock-realm",
                "type": "pvp",
                "population": "high"
            }
        ]
    })

def run_flask_app():
    app.run(port=8000, use_reloader=False)

class TestAll(unittest.TestCase):
    def test_01_test_auth(self):
        # Test the auth function
        session = battlenet.auth(
            client_id="mock_client_id",
            client_secret="mock_client_secret",
            region=battlenet.REGION.US,
            auth_domain="localhost",
            api_domain="localhost",
            port=8000,
            https=False
        )
        self.assertIsInstance(session, battlenet.Session)
        self.assertEqual(session.region, battlenet.REGION.US)
        self.assertEqual(session.full_api_domain, "localhost")
        self.assertEqual(session.port, 8000)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    # Give the Flask app a moment to start
    import time
    time.sleep(1)

    unittest.main()
