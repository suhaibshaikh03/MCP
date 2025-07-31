import sys
import asyncio
from typing import Optional, Any
from contextlib import AsyncExitStack
from mcp import ClientSession, types
from mcp.client.streamable_http import streamablehttp_client
from pydantic import AnyUrl
import json


class MCPClient:
    def __init__(
        self,
        server_url: str,
    ):
        self._server_url = server_url
        self._session: Optional[ClientSession] = None
        self._exit_stack: AsyncExitStack = AsyncExitStack()

    async def connect(self):
        streamable_transport = await self._exit_stack.enter_async_context(
            streamablehttp_client(self._server_url)
        )
        _read, _write, _get_session_id = streamable_transport
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(_read, _write)
        )
        await self._session.initialize()

    def session(self) -> ClientSession:
        if self._session is None:
            raise ConnectionError(
                "Client session not initialized or cache not populated. Call connect_to_server first."
            )
        return self._session

    async def list_tools(self) -> list[types.Tool]:
        # Core function: Retrieve the list of tools from the MCP server.
        # This follows the MCP client lifecycle (see MCP Lifecycle Specification: https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle)
        result : types.ListToolsResult = await self.session().list_tools()
        return result.tools

    async def call_tool(
        self, tool_name: str, tool_input: dict
    ) -> types.CallToolResult | None:
        # Core function: Execute a specific tool on the MCP server using its name and input parameters.
        # This call is part of the MCP lifecycle's Operation phase.
        return await self.session().call_tool(tool_name, tool_input)

    async def list_prompts(self) -> list[types.Prompt]:
        # TODO: Return a list of prompts defined by the MCP server
        return []

    async def get_prompt(self, prompt_name, args: dict[str, str]):
        # TODO: Get a particular prompt defined by the MCP server
        return []

    async def read_resource(self, uri: str):
        assert self._session , "Session not available"
        url = AnyUrl(uri)
        resource : types.ReadResourceResult = await self.session().read_resource(url)
        # print(resource.__dict__)
        result = resource.contents[0]
        if isinstance(result,types.TextResourceContents):
            if result.mimeType == "application/json":
                try:
                    return json.loads(result.text)
                except json.JSONDecodeError as e:
                    print(f"Error decoding json: {e}")
                    return result.text
        return result.text
        # return resource

    async def list_resource_template(self) -> list[types.ResourceTemplate]:
        result : types.ListResourceTemplatesResult = await self.session().list_resource_templates()
        # print(result.__dict__)
        return result.resourceTemplates

    async def list_resources(self) -> list[types.Resource]:
        resources : types.ListResourcesResult = await self.session().list_resources()
        return resources.resources

    async def cleanup(self):
        await self._exit_stack.aclose()
        self._session = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()

# ----------------------------------------------------------------------
# MCP Lifecycle Overview:
# This MCPClient class adheres to the MCP lifecycle for robust connection management.
# - Initialization: The connect() method sets up the client session.
# - Operation: Core functions like list_tools() and call_tool() enable tool invocations.
# - Shutdown: The cleanup() method ensures the connection is gracefully closed.
#
# To test your implementation, run main.py to start the chat agent and see your tools in action.
# ----------------------------------------------------------------------

# For testing


async def main():
    async with MCPClient(
        server_url="http://localhost:8000/mcp/",
    ) as _client:
        # Example usage:
        # Retrieve and print available tools to verify the client implementation.
        # tools = await _client.list_tools()
        # for tool in tools:
        #     print(f"Tool Name: {tool.name}, Tool Description: {tool.description}")

            
        # # Call a tool to read a document
        # read_result = await _client.call_tool(
        #     tool_name="read_doc", tool_input={"doc_id": "deposition.md"}
        # )
        # if read_result:
        #     print(f"Document Content: {read_result.content}")   

        # # Call a tool to edit a document
        # edit_result = await _client.call_tool(
        #     tool_name="edit_doc", tool_input={"doc_id": "deposition.md", "content": "Hi this is Suhaib"}
        # )
        # if edit_result:
        #     print(f"Edit Result: {edit_result.content}")   

        # List resources
        # resources = await _client.list_resources()
        # print("resources",resources) # list
        # for res in resources:
        #     print(res)

        # read_resource = await _client.read_resource("docs://documents")
        # print("------read resource-----",read_resource)


        # List resource template
        template = await _client.list_resource_template()
        # for t in template:
        #     print(t)
        
        uri = template[0].uriTemplate.replace("{doc_id}","deposition.md")

        read_doc = await _client.read_resource(uri)
        print("------read doc-----",read_doc)
        

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())