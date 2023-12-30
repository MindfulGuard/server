from fastapi import Request

def get_client_ip(request: Request) -> str:
    # Let's try to get the IP from the X-Real-IP header
    client_ip = request.headers.get("x-real-ip")
    
    if client_ip is not None:
        return client_ip
    
    # If the header is not set, we use remote_addr directly
    return request.client.host