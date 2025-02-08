from flask import Flask, request, jsonify, render_template
import requests
import random
import string
import urllib3

app = Flask(__name__)

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def generate_jsessionid():
    base_id = "87D5D75A90D864E7B85D97D3B8B1B"
    random_suffix = ''.join(random.choices(string.digits, k=3))
    return base_id + random_suffix

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_mobile():
    data = request.json
    mobile_no = data.get("mobileNo")
    if not mobile_no:
        return jsonify({"error": "Mobile number is required"}), 400

    jsessionid = generate_jsessionid()
    url = "https://fms.bsnl.in/saveMobileIptvRegistration"
    headers = {
        "Host": "fms.bsnl.in",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0",
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://fms.bsnl.in",
        "Referer": "https://fms.bsnl.in/iptvreg",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0",
        "Te": "trailers",
        "Connection": "close"
    }
    cookies = {"JSESSIONID": jsessionid}
    payload = {
        "mobileNo": mobile_no,
        "vendorCode": "IPTV_MBITV",
        "circleCode": "BR",
        "zone": "EZ"
    }

    response = requests.post(url, headers=headers, cookies=cookies, data=payload, verify=False, timeout=10)
    return jsonify({"status_code": response.status_code, "response": response.text})

if __name__ == "__main__":
    app.run(debug=True)

