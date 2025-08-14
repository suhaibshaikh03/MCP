import requests
url = "http://localhost:8000/mcp/"

headers = {
    "Content-Type":"application/json",
    "Accept":"application/json, text/event-stream"
}
# method to get all tools list (tools/list)
body = {
    "jsonrpc":"2.0",
    "method":"tools/list",
    "id":1,
    "params":{}
    
}
# method to call any tool list (tools/call)
body1 = {
    "jsonrpc":"2.0",
    "method":"tools/call",
    "id":1,
    "params":{
        "name":"get_weather",
        "arguments":{
            "city":"New York"
        }
    }
}

# response = requests.post(url, headers=headers,json=body)
# print(response.text)

# call_tool = requests.post(url,headers=headers, json=body1)
# print(call_tool.text)
# print(dir(call_tool))

#addition tool
body2 = {
    "jsonrpc":"2.0",
    "method":"tools/call",
    "id":1,
    "params":{
         "name":"addition",
        "arguments":{
            "num1":1,
            "num2":2
    }
    
}
}
response = requests.post(url, headers=headers,json=body1)
print(response.text)
