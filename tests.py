from flask import Flask, jsonify, request
import threading
import unittest
import battlenet as battlenet

# Flask app to mock BattleNet API
app = Flask(__name__)

last_client_id = None
last_client_secret = None


@app.route('/token', methods=['POST'])
def oauth_token():
    global last_client_id, last_client_secret
    data = request.form
    last_client_id = data.get('client_id')
    last_client_secret = data.get('client_secret')

    return jsonify({
        "access_token": "mock_access_token",
        "token_type": "bearer",
        "expires_in": 3600
    })

@app.route('/data/wow/connected-realm/index', methods=['GET'])
def connected_realm_index():
    return jsonify({
  "_links": {
    "self": {
      "href": "https://us.api.blizzard.com/data/wow/realm/?namespace=dynamic-us"
    }
  },
  "realms": [
    {
      "key": {
        "href": "https://us.api.blizzard.com/data/wow/realm/129?namespace=dynamic-us"
      },
      "name": "Gurubashi",
      "id": 129,
      "slug": "gurubashi"
    },]})

def run_flask_app():
    app.run(port=8000, use_reloader=False)

class TestAll(unittest.TestCase):
    def test_01_auth(self):
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
        self.assertEqual(session.token, "mock_access_token")
        self.assertEqual(last_client_id, "mock_client_id")
        self.assertEqual(last_client_secret, "mock_client_secret")
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
