from mcp.server.fastmcp import FastMCP
mcp = FastMCP(name="hello-mcp",stateless_http=True)

@mcp.tool(name="online researcher",description="online search" )
def search_online(query:str):
    """Searches online for a query"""
    return f"search online for {query}"

@mcp.tool()
async def get_weather(city:str):
    """Gets weather for a city"""
    return f"Weather in {city} is sunny"
@mcp.tool()
async def addition(num1:int,num2:int):
    """Add two numbers"""
    return num1+num2

mcp_app = mcp.streamable_http_app()

