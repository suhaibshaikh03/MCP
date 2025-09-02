from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="SharedStandAloneMCPServer",
    stateless_http=True,
    json_response=True, # Generally easier for HTTP clients if they don't need full SSE parsing
)

# --- 2. Define a simple tool ---
@mcp.tool(
    name="special_greeting",
    description="Returns a personalized greeting from the shared MCP server."
)
def greet(name: str = "World") -> str:
    """A simple greeting tool."""
    print(f"Tool 'greet_from_shared_server' called with name: {name}")
    response_message = f"Hello, {name}, from the SharedStandAloneMCPServer!"
    return response_message

@mcp.tool(
    name="get_my_mood",
    description="Returns the mood of a given person"
)
def mood(name: str = "World") -> str:
    """A simple greeting tool."""
    print(f"Tool 'moo' called with name: {name}")
    return "I am happy"



mcp_app = mcp.streamable_http_app()


