import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re

# Initialize session
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (XML Scanner)"
})

# Common XML-related paths
COMMON_XML_PATHS = [
    "/rss", "/feed", "/feeds", "/atom", "/sitemap.xml",
    "/api", "/api.xml", "/wsdl", "/service?wsdl", "/xml",
    "/config.xml", "/web.xml", "/export.xml"
]

def is_xml(content, content_type):
    if "application/xml" in content_type or "text/xml" in content_type:
        return True
    return content.strip().startswith("<?xml")

def scan_known_paths(base_url):
    print("[*] Scanning common XML paths...\n")
    found = []

    for path in COMMON_XML_PATHS:
        url = urljoin(base_url, path)
        try:
            response = session.get(url, timeout=5)
            if response.status_code == 200 and is_xml(response.text, response.headers.get("Content-Type", "")):
                print(f"[XML FOUND] {url} (Type: {response.headers.get('Content-Type')})")
                found.append(url)
        except Exception as e:
            print(f"[ERROR] {url} -> {e}")
    return found

def crawl_and_find_xml(base_url, max_pages=20):
    print("\n[*] Crawling and scanning linked URLs...\n")
    visited = set()
    to_visit = [base_url]
    found_xml = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)
        try:
            resp = session.get(url, timeout=5)
            if resp.status_code != 200:
                continue

            content_type = resp.headers.get("Content-Type", "")
            if is_xml(resp.text, content_type):
                print(f"[XML FOUND] {url} (Type: {content_type})")
                found_xml.append(url)
                continue  # don't parse XML pages for links

            soup = BeautifulSoup(resp.text, "html.parser")
            for link in soup.find_all("a", href=True):
                href = link['href']
                parsed = urljoin(url, href)
                if urlparse(parsed).netloc == urlparse(base_url).netloc:
                    to_visit.append(parsed)
        except Exception as e:
            print(f"[ERROR] {url} -> {e}")

    return found_xml

if __name__ == "__main__":
    target = input("Enter target URL (e.g., https://example.com): ").strip()
    if not target.startswith("http"):
        target = "https://" + target

    print(f"\n[+] Starting XML scan on: {target}\n")
    known_xml = scan_known_paths(target)
    crawled_xml = crawl_and_find_xml(target)

    all_found = list(set(known_xml + crawled_xml))
    print("\n[+] Summary: XML Resources Found")
    if all_found:
        for url in all_found:
            print(f" - {url}")
    else:
        print("[-] No XML content found.")
