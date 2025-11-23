def parse_url(url: str) -> dict[str, str | int]:
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

# Tests
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
