# Lema WiFi: Open-Source M-Pesa Hotspot Billing

> **"We provide the internet. We build the toll booth. The ISP is just the pipe."**

Lema WiFi is a lightweight, self-hosted WiFi billing system designed for Kenyan entrepreneurs, cybercafés, and local WISPs. It allows you to sell internet access by the hour, day, or week using **M-Pesa STK Push**, completely bypassing the need for expensive third-party billing providers or calling your ISP for permission.

## 🛑 The Problem We Are Solving
For too long, ISPs and network providers have acted as gatekeepers. If you want to share your internet connection and charge for it, they force you into expensive business plans, complex hardware contracts, or proprietary billing systems. 

**Lema WiFi changes the game.** 
If you have a router and a power source, you can become a micro-ISP. You own the hardware, you own the data, and you keep the revenue. We believe the person who pays for the pipe should have the right to sell the water.

## ✨ Features
- **M-Pesa STK Push Integration:** Seamlessly integrated with Safaricom Daraja API.
- **MikroTik Integration:** Automatically whitelists MAC addresses and enforces time limits (e.g., 1 hour, 4 hours, 24 hours) using the MikroTik API.
- **Captive Portal:** A clean, responsive HTML frontend that works on any smartphone.
- **Self-Hosted:** Run this on a Raspberry Pi, an old laptop, or a local server. No cloud subscriptions required.

## 🏗️ Architecture
1. User connects to WiFi.
2. MikroTik redirects them to the Lema WiFi Captive Portal.
3. User selects a plan (e.g., 10 KES for 1 hour) and enters their phone number.
4. Python backend triggers the M-Pesa STK Push.
5. User enters their PIN.
6. Safaricom sends a callback to the backend.
7. The backend talks to the MikroTik API to whitelist the user's MAC address for the purchased duration.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- A MikroTik Router (with Hotspot and API enabled)
- A Safaricom Daraja Developer Account (for API keys)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lema-wifi.git
   cd lema-wifi