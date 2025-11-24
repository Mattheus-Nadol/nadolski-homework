"""
Moduł do parsowania adresów URL.

Zawiera funkcję parse_url(), która zwraca słownik z protokołem,
domeną, portem i ścieżką na podstawie podanego adresu URL.
"""

from typing import Union

def parse_url(url: str) -> dict[str, Union[str,int]]:
    """
    Funkcja, która przyjmuje jako argument adres URL w formie stringa
    (np. https://api.example.com:8080/users/search?active=true )
    Zwraca słownik zawierający jego części: 
    protocol ,  domain ,  port  i  path 
    """
    protocol = url.split("://")[0]
    host_path = url.split("://")[1].split("/", 1)
    host = host_path[0]
    path = "/" + host_path[1] if len(host_path) > 1 else ""
    if ":" in host:
        domain, port_str = host.split(":")
        port = int(port_str)
    else:
        domain = host
        port = 80 if protocol == "http" else 443
    result = {
        "protocol": protocol,
        "domain": domain,
        "port": port,
        "path": path
    }
    print(result)
    return result #type: ignore

website = "https://api.example.com:8080/users/search?active=true"
parse_url(website)

# Tests PRINT
print("TESTS:")
urls_test = [
    "http://example.com/test",
    "https://secure.example.org",
    "https://example.com/search?q=python#section",
    "http://example.com:1234/path/to/resource",
    "http://example.com",
    "https://api.v1.example.co.uk:8080/data",
]

for test_url in urls_test:
    parse_url(test_url)


# TESTY z użyciem assert w pętli
print("Assert TESTS:")
urls_test_assert = [
    ("http://example.com/test", {
        "protocol": "http",
        "domain": "example.com",
        "port": 80,
        "path": "/test"
    }),
    ("https://secure.example.org", {
        "protocol": "https",
        "domain": "secure.example.org",
        "port": 443,
        "path": ""
    }),
    ("https://example.com/search?q=python#section", {
        "protocol": "https",
        "domain": "example.com",
        "port": 443,
        "path": "/search?q=python#section"
    }),
    ("http://example.com:1234/path/to/resource", {
        "protocol": "http",
        "domain": "example.com",
        "port": 1234,
        "path": "/path/to/resource"
    }),
    ("http://example.com", {
        "protocol": "http",
        "domain": "example.com",
        "port": 80,
        "path": ""
    }),
    ("https://api.v1.example.co.uk:8080/data", {
        "protocol": "https",
        "domain": "api.v1.example.co.uk",
        "port": 8080,
        "path": "/data"
    }),
]

for url, expected in urls_test_assert:
    result = parse_url(url)
    assert result == expected, f"Test failed for {url}. Got {result}, expected {expected}"

print("Wszystkie testy zakończone sukcesem!")
