from mcp.server.fastmcp import FastMCP
mcp = FastMCP(name="hello-mcp",stateless_http=True)

@mcp.tool()
def search_online(query:str):
    return f"search online for {query}"

@mcp.tool()
async def get_weather(city:str):
    """Gets weather for a city"""
    return f"Weather in {city} is sunny"

mcp_app = mcp.streamable_http_app()

