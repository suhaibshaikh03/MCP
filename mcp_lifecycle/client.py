import requests
url = "http://localhost:8000/mcp/"

headers = {
    "Content-Type":"application/json",
    "Accept":"application/json, text/event-stream"
}
# Bad request 400 , no valid session id provided if called first time
# body = {
#     "jsonrpc":"2.0",
#     "method":"tools/list",
#     "id":1,
#     "params":{}
    
# }

# MCP initialize request

body = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {
            "roots": {
                "listChanged": True
            },
            "sampling": {},
            "elicitation": {}
        },
        "clientInfo": {
            "name": "postman-test-client",
            "title": "Postman Test Client",
            "version": "1.0.0"
        }
    }
}

# Send Initialized Notification
header1 = {
    "Content-Type":"application/json",
    "Accept":"application/json, text/event-stream",
    "mcp-session-id":"b8a670cb861c4fad84e1d85102b42e25"
}

body1 = {
    "jsonrpc": "2.0",
    "method": "notifications/initialized"
}
# now it will work because now 3 way handshake is completed
body = {
    "jsonrpc":"2.0",
    "method":"tools/list",
    "id":1,
    "params":{}
    
}
response = requests.post(url, headers=header1,json=body)
print(response.text)