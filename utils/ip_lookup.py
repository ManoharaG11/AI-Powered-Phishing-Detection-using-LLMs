# utils/ip_lookup.py
import os
import requests

IP_API = os.getenv("IP_LOOKUP_API", "")  # optional API key if using paid service

def lookup_ip_info(ip: str) -> dict:
    """
    Uses ip-api.com free endpoint to fetch basic geolocation information.
    """
    if not ip:
        return {}
    try:
        url = f"http://ip-api.com/json/{ip}"
        resp = requests.get(url, timeout=6)
        if resp.status_code == 200:
            data = resp.json()
            # keep only a few useful fields
            return {
                "ip": ip,
                "country": data.get("country"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "isp": data.get("isp"),
                "lat": data.get("lat"),
                "lon": data.get("lon"),
                "query": data.get("query"),
                "status": data.get("status")
            }
        else:
            return {"error": f"Status code {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}
