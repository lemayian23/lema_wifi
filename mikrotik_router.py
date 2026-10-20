from datetime import datetime

# Set this to True when you buy the router and plug it in
ROUTER_CONNECTED = False 

def whitelist_mac(mac_address, amount_paid):
    """Grants internet access to the MAC address."""
    
    # Determine the time limit based on your pricing tiers
    if amount_paid == 10:
        uptime = '1h'
    elif amount_paid == 15:
        uptime = '2h'
    elif amount_paid == 25:
        uptime = '4h'
    elif amount_paid == 30:
        uptime = '12h'
    elif amount_paid == 40:
        uptime = '24h'
    else:
        uptime = '1h'

    if not ROUTER_CONNECTED:
        # This runs while you wait for the router
        print(f"🛠️ SIMULATION: Router command sent! Granting {mac_address} access for {uptime}.")
        return True

    # --- REAL ROUTER CODE (Uncomment when router arrives) ---
    # import librouteros
    # try:
    #     api = librouteros.connect(host="192.168.88.1", username="admin", password="your_pass")
    #     api('/ip/hotspot/ip-binding/add', **{'mac-address': mac_address, 'type': 'bypassed'})
    #     api('/ip/hotspot/user/add', **{'name': mac_address, 'password': mac_address, 'limit-uptime': uptime})
    #     api.close()
    #     print(f"✅ Real Router: Whitelisted {mac_address} for {uptime}")
    #     return True
    # except Exception as e:
    #     print(f"❌ Router Error: {e}")
    #     return False