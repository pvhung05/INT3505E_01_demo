import requests

BASE = "http:127.0.0.1:5001/api"

def main():
    r = requests.get("{BASE}/info")
    print("GET /info ->", r.status_code, r.json())

    r2 = requests.post(f"{BASE}/echo", json={"hello:" "world"})
    print("POST /echo ->", r2.status_code, r2.json())

if __name__ == "__main__":
    main()
