import httpx

with httpx.Client() as client:
        response = client.get("http://nginx:80/api/comments/")
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"Body: {response.text}")