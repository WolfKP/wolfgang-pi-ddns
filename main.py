from dotenv import load_dotenv
import os
import requests
import sys

load_dotenv()

def get_public_ip():
    response = requests.get("https://api.ipify.org")

    return response.text.strip()

def get_dns_record():
    url = f"https://api.cloudflare.com/client/v4/zones/{os.getenv('ZONE_ID')}/dns_records"
    headers = {"Authorization": f"Bearer {os.getenv('CF_API_TOKEN')}"}
    params = {"type": "A", "name": os.getenv("RECORD_NAME")}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if not data["result"]:
        print(f"ERROR: No A record found for {os.getenv('RECORD_NAME')}")
        sys.exit()

    record = data["result"][0]

    return record["id"], record["content"]

def update_dns_record(record_id, new_ip):
    url = f"https://api.cloudflare.com/client/v4/zones/{os.getenv('ZONE_ID')}/dns_records/{record_id}"
    headers = {"Authorization": f"Bearer {os.getenv('CF_API_TOKEN')}"}
    payload = {
        "type": "A",
        "name": os.getenv("RECORD_NAME"),
        "content": new_ip,
        "ttl": 1,
        "proxied": False
    }

    response = requests.put(url, headers=headers, json=payload)

    return response.json()["success"]

def main():
    current_ip = get_public_ip()
    record_id, dns_ip = get_dns_record()

    if current_ip == dns_ip:
        print(f"IP unchanged ({current_ip}) - no update needed")

        return

    print(f"IP changed: {dns_ip} → {current_ip} - updating...")
    success = update_dns_record(record_id, current_ip)

    if success:
        print(f"SUCCESS: {os.getenv('RECORD_NAME')} updated to {current_ip}")
    else:
        print("ERROR: Update failed")
        sys.exit()

main()
