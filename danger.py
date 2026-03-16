import os
import json
import time
import requests
from flask import Flask, request, jsonify
from danger_ffjwt import guest_to_jwt  # આ ફાઈલ હોવી જરૂરી છે

app = Flask(__name__)

# ---------- Version fetching ----------
_versions_cache = {
    "ob_version": "OB52",
    "client_version": "1.120.1",
    "last_fetch": 0
}

def get_versions():
    global _versions_cache
    now = time.time()
    if now - _versions_cache["last_fetch"] > 3600:
        try:
            resp = requests.get("https://raw.githubusercontent.com/dangerapix/danger-ffjwt/main/versions.json", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                _versions_cache["ob_version"] = data.get("ob_version", "OB52")
                _versions_cache["client_version"] = data.get("client_version", "1.120.1")
                _versions_cache["last_fetch"] = now
        except Exception:
            pass
    return _versions_cache["ob_version"], _versions_cache["client_version"]

# ---------- Routes ----------
@app.route('/token', methods=['GET'])
def token_converter():
    ob_ver, client_ver = get_versions()
    args = request.args

    uid = args.get('uid', '').strip()
    pwd = args.get('password', '').strip()

    if not uid or not pwd:
        return jsonify({"error": "UID and password required"}), 400

    try:
        result = guest_to_jwt(uid, pwd, ob_version=ob_ver, client_version=client_ver)

        # જો result ડિક્શનરી હોય તો તેમાંથી ટોકન કાઢો
        if isinstance(result, dict):
            token = result.get("token", "Error getting token")
        else:
            token = result

        # માત્ર UID અને TOKEN જ મોકલો
        return jsonify({
            "uid": uid,
            "token": token
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)