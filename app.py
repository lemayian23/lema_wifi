import os
from flask import Flask, request, jsonify, render_template
import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime
from dotenv import load_dotenv # <--- NEW: Load environment variables

# Load variables from the .env file
load_dotenv()

app = Flask(__name__)

# ==========================================
# SECURE CONFIGURATION (Loaded from .env)
# ==========================================
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
PASSKEY = os.getenv("PASSKEY")
BUSINESS_SHORTCODE = os.getenv("BUSINESS_SHORTCODE", "174379") 
CALLBACK_URL = os.getenv("CALLBACK_URL", "https://yourdomain.com/mpesa_callback")
BASE_URL = os.getenv("BASE_URL", "https://sandbox.safaricom.co.ke")

# Temporary memory to store MAC addresses while waiting for payment
pending_payments = {}

def get_access_token():
    api_url = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    
    try:
        response = requests.get(
            api_url, 
            auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET),
            timeout=30 
        )
        
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            print(f"❌ Safaricom Error: Status {response.status_code}")
            print(f"❌ Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Network Error: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pay', methods=['POST'])
def pay():
    data = request.json
    raw_phone = data.get('phone')
    amount = data.get('amount')
    mac_address = data.get('mac')
    
    clean_phone = raw_phone.replace(" ", "").replace("+", "")
    if clean_phone.startswith("0"):
        phone = "254" + clean_phone[1:]
    else:
        phone = clean_phone

    token = get_access_token()
    if not token:
        return jsonify({"ResponseCode": "1", "errorMessage": "Failed to get token from Safaricom. Check terminal."})

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = f"{BUSINESS_SHORTCODE}{PASSKEY}{timestamp}"
    password = base64.b64encode(data_to_encode.encode()).decode()

    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline", 
        "Amount": amount, 
        "PartyA": phone,
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "Lema WiFi",
        "TransactionDesc": "WiFi Access"
    }

    response = requests.post(f"{BASE_URL}/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)
    res_data = response.json()
    
    if res_data.get('ResponseCode') == '0':
        checkout_id = res_data.get('CheckoutRequestID')
        pending_payments[checkout_id] = {
            "mac": mac_address,
            "amount": amount
        }
        print(f"✅ STK Push sent to {phone}")
    else:
        print(f"❌ STK Push failed: {res_data}")
    
    return jsonify(res_data)

@app.route('/mpesa_callback', methods=['POST'])
def mpesa_callback():
    data = request.json
    print("\n--- CALLBACK RECEIVED ---")
    try:
        stk_callback = data['Body']['stkCallback']
        checkout_id = stk_callback['CheckoutRequestID']
        
        if stk_callback['ResultCode'] == 0:
            payment_info = pending_payments.get(checkout_id)
            if payment_info:
                mac = payment_info['mac']
                amt = payment_info['amount']
                print(f"✅ PAID KSh {amt}. Ready to whitelist MAC: {mac}")
                # NOTE: Call to mikrotik_router goes here
            else:
                print("Payment succeeded, but MAC address was lost.")
        else:
            print(f"❌ Payment failed: {stk_callback['ResultDesc']}")
    except Exception as e:
        print(f"Error: {e}")

    return jsonify({"ResultCode": 0, "ResultDesc": "Success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)