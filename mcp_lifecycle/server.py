from mcp.server.fastmcp import FastMCP
# by default stateless_http = False , json_response = False
mcp = FastMCP("weather",stateless_http = False)

@mcp.tool()
async def get_forecast(city : str) -> str:
    """
    Get the forecast for a city
    """
    return f"the forecast for {city} is sunny"

mcp_app = mcp.streamable_http_app()