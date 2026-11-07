import requests
from colorama import init, Fore, Style

init(autoreset=True)

def get_public_ip():
    try:
        r = requests.get("https://api.ipify.org?format=json", timeout=10)
        r.raise_for_status()
        return r.json().get("ip", "")
    except requests.RequestException as e:
        print(Fore.RED + f"Ошибка при получении IP: {e}")
        return ""

def geolocate_ip(ip):
    try:
        r = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10)
        r.raise_for_status()
        j = r.json()
        return {
            "city": j.get("city") or "",
            "region": j.get("region") or "",
            "country": j.get("country") or "",
            "lat": j.get("latitude"),
            "lon": j.get("longitude")  
        }
    except requests.RequestException as e:
        print(Fore.RED + f"Ошибка при геолокации IP: {e}")
        return {"city": "", "region": "", "country": "", "lat": None, "lon": None}

def fetch_weather(lat, lon, units="metric"):  
    if lat is None or lon is None:
        return "Не удалось получить координаты для прогноза погоды."
    try:
        url = f"https://wttr.in/{lat},{lon}?{units}"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        return Fore.RED + f"Ошибка при получении погоды: {e}"

def main():
    ip = get_public_ip()
    if not ip:
        print(Fore.RED + "Не удалось получить публичный IP-адрес.")
        return
    print(Fore.YELLOW + f"Public IP: {ip}")
    loc = geolocate_ip(ip)
    print(Fore.GREEN + f"Location: {loc['city']}, {loc['region']}, {loc['country']}")
    weather = fetch_weather(loc['lat'], loc['lon'])
    print(weather)

if __name__ == "__main__":  
    main()
