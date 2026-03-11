import os
import json
import time
import requests
from flask import Flask, request, jsonify
from danger_ffjwt import guest_to_jwt  

app = Flask(__name__)

# --- અહીં તમારી પોતાની API KEY સેટ કરો ---
MY_API_KEY = "TUFAN95" 

DEV_CREDIT = "@danger_ff_like"
DEV_TELEGRAM = "t.me/danger_ff_like"

# (બાકીનું વર્ઝન ફેચિંગ લોજિક જેવું છે તેવું જ રહેશે...)

@app.route('/token', methods=['GET'])
def token_converter():
    ob_ver, client_ver = get_versions()
    args = request.args

    # --- API KEY ચેક કરવાનું લોજિક ---
    user_key = args.get('key')
    if user_key != MY_API_KEY:
        return jsonify({
            "success": False, 
            "error": "Invalid API Key. Access Denied.",
            "credit": DEV_TELEGRAM
        }), 401

    # UID અને Password પેરામીટર્સ ચેક કરો
    if 'uid' not in args or 'password' not in args:
        return jsonify({
            "success": False,
            "error": "Missing parameters. Use ?uid=UID&password=PASSWORD&key=YOUR_KEY",
            "credit": DEV_TELEGRAM
        }), 400

    uid = args.get('uid').strip()
    pwd = args.get('password').strip()

    try:
        result = guest_to_jwt(uid, pwd, ob_version=ob_ver, client_version=client_ver)
        if isinstance(result, dict):
            result["credit"] = DEV_TELEGRAM
        else:
            result = {"success": True, "token": result, "credit": DEV_TELEGRAM}
        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e), "credit": DEV_TELEGRAM}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)