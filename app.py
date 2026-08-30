import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# UMANG IOCL API configuration
API_URL = "https://apigw.umangapp.in/ioclApi/ws1/consumervalidate"

HEADERS = {
    "subsid": "0",
    "deptid": "186",
    "tenantid": "",
    "formtrkr": "0",
    "x-api-key": "VKE9PnbY5k1ZYapR5PyYQ33I26sXTX569Ed7eqyg",
    "srvid": "1123",
    "subsid2": "0",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Linux; Android 14; I2202 Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/150.0.7871.13 Mobile Safari/537.36 AgentWeb/5.0.0  UCBrowser/11.6.4.950",
    "origin": "https://web.umang.gov.in",
    "referer": "https://web.umang.gov.in/"
}

PAYLOAD_TEMPLATE = {
    "tkn": "vb841eca56-085f-4a6f-85b1-ae987c06f694/1",
    "trkr": "213132",
    "lang": "en",
    "lat": "21",
    "lon": "90",
    "lac": "90",
    "usag": "90",
    "apitrkr": "123234",
    "usrid": "09",
    "mode": "app",
    "pltfrm": "android",
    "did": "123234",
    "deptid": "186",
    "formtrkr": "0",
    "srvid": "1123",
    "subsid": "0",
    "subsid2": "0",
    "trackingId": "",
    "source": "UMANG",
    "consumerId": "",
    "partnerCode": "",
    "consumerNumber": ""
}

def fetch_lpg_details(mobile):
    payload = PAYLOAD_TEMPLATE.copy()
    payload["mobile"] = mobile
    try:
        resp = requests.post(API_URL, json=payload, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            return resp.json(), None
        else:
            return None, f"UMANG API returned status {resp.status_code}"
    except Exception as e:
        return None, str(e)

@app.route('/lpg', methods=['GET'])
def lpg_info():
    mobile = request.args.get('mobile', '').strip()
    mobile = ''.join(filter(str.isdigit, mobile))[-10:]

    if not mobile or len(mobile) != 10:
        return jsonify({
            "credit_top": "@HYPERMX7",
            "status": "error",
            "error": "10-digit mobile number required",
            "credit_bottom": "@HYPERMX7"
        }), 400

    data, err = fetch_lpg_details(mobile)
    if err:
        return jsonify({
            "credit_top": "@HYPERMX7",
            "status": "error",
            "error": err,
            "credit_bottom": "@HYPERMX7"
        }), 502

    return jsonify({
        "credit_top": "@HYPERMX7",
        "status": "success",
        "mobile": mobile,
        "data": data,
        "credit_bottom": "@HYPERMX7"
    })

@app.route('/')
def home():
    return jsonify({
        "credit_top": "@HYPERMX7",
        "app": "LPG Consumer Info API (via UMANG IOCL)",
        "usage": "/lpg?mobile=9876543210",   # 👈 mock number
        "note": "Use a registered LPG mobile to get real data.",
        "credit_bottom": "@HYPERMX7"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)