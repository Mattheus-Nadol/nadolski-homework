from typing import Optional

class HttpRequest:
    def __init__(self, method: str, target: str, headers: Optional[dict[str, str]] = None, body: Optional[str] = None):
        self.method = method
        self.target = target
        self.headers = headers
        self.body = body
    
    def display(self):
        print("--- HTTP Request ---")
        print(f"Method: {self.method}")
        print(f"Target: {self.target}")
        print("Headers:")
        # print(f"  Host: {self.headers['Host']}")
        # print(f"  User-Agent: {self.headers['User-Agent']}")
        if self.headers:
            for key, value in self.headers.items():
                print(f"  {key}: {value}")
        else:
            print(f"  {self.headers}")     
        print("Body:")
        print(f"  {self.body}")
        print("--------------------")

request1 = HttpRequest("GET", "/index.html", {"Host": "example.com", "User-Agent": "PythonClient/1.0"}, "(empty)")
request1.display()

request2 = HttpRequest("POST", "/api/index.html", {"Host": "bobubo.com", "User-Agent": "MyClient/1.0"}, "{'imie': 'Mateusz', 'wiek': '34'}")
request2.display()

request3 = HttpRequest("GET", "/index.html")
request3.display()