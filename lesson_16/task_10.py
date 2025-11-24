"""
Module: HTTP Header Validator
Provides a function to validate required HTTP headers in a request dictionary.
Raises ValueError if any required header is missing.
"""
def validate_request(request_dict: dict):
    """
    Validate that the request contains required HTTP headers.
    Args:
        request_dict (dict): Dictionary with a 'headers' key containing header names.
    Raises:
        ValueError: If 'Host' or 'User-Agent' is missing.
    """
    required_headers = ["Host", "User-Agent"]
    request_headers = request_dict["headers"]
    for header in required_headers:
        if header not in request_headers:
            raise ValueError(f"Missing required header: '{header}'")

http_ok_request = {
    "headers": {
        "Host": "my-blog.com",
        "User-Agent": "Chrome/1.0",
        "Accept": "application/json"
    }
}
http_wrong_request = {
    "headers": {
        "Host": "my-blog.com"
    }
}

test_requests = [http_ok_request, http_wrong_request]
for test in test_requests:
    print(f"Testing request: {test}")
    try:
        validate_request(test)
        print("Request correct!")
    except ValueError as e:
        print(f"Request Error: {e}")
