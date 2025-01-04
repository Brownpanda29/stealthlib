import requests

class Communication:
    def __init__(self, server_host=None, server_port=None):
        self.base_url = f"https://{server_host}:{server_port}" if server_host and server_port else None

    def send_request(self, endpoint, data):
        """
        Sends a POST request to the server.
        """
        response = requests.post(f"{self.base_url}{endpoint}", json=data, verify=False)
        response.raise_for_status()
        return response.json()
