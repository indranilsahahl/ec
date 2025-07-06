import requests
from urllib.parse import urljoin

# Common WSDL paths
COMMON_WSDL_PATHS = [
    "/?wsdl", "/service?wsdl", "/webservice?wsdl", "/api?wsdl",
    "/soap?wsdl", "/ws?wsdl", "/wsdl", "/services.wsdl", "/service.wsdl"
]

def is_wsdl(content):
    """Quick check for WSDL-like XML content"""
    return (
        "<definitions" in content or
        "<wsdl:definitions" in content or
        "http://schemas.xmlsoap.org/wsdl/" in content
    )

def scan_wsdl(base_url, timeout=5):
    print(f"[+] Scanning {base_url} for WSDL endpoints...\n")
    headers = {
        "User-Agent": "Mozilla/5.0 (WSDL Scanner)"
    }

    found = []

    for path in COMMON_WSDL_PATHS:
        url = urljoin(base_url, path)
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            content = response.text
            code = response.status_code
            if code == 200 and is_wsdl(content):
                ctype = response.headers.get("Content-Type", "")
                print(f"[FOUND] {url} (Status: 200, Type: {ctype})")
                found.append(url)
            elif code in [301, 302]:
                print(f"[REDIRECT] {url} (Status: {code})")
            elif code == 403:
                print(f"[FORBIDDEN] {url} (Status: {code})")
            elif code == 401:
                print(f"[UNAUTHORIZED] {url} (Status: {code})")
        except requests.RequestException as e:
            print(f"[ERROR] {url} -> {e}")

    if not found:
        print("\n[-] No public WSDL endpoints found.")
    else:
        print("\n[+] WSDL Endpoints Found:")
        for url in found:
            print(f"  -> {url}")

if __name__ == "__main__":
    target = input("Enter base URL (e.g., https://examp
