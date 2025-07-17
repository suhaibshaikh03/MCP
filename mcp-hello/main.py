from mcp.server.fastmcp import FastMCP
mcp = FastMCP(name="hello-mcp",stateless_http=True)
mcp_app = mcp.streamable_http_app()

#sample method in python
