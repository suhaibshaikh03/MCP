import asyncio
import os
from dotenv import load_dotenv, find_dotenv

from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams, create_static_tool_filter


_: bool = load_dotenv(find_dotenv())

# URL of our standalone MCP server (from shared_mcp_server)
MCP_SERVER_URL = "http://localhost:8000/mcp/" # Ensure this matches your running server

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")



async def main():
    static_filter = create_static_tool_filter(allowed_tool_names=["special_greeting"],blocked_tool_names=["get_my_mood"])
    # 1. Configure parameters for the MCPServerStreamableHttp client
    # These parameters tell the SDK how to reach the MCP server.
    mcp_params = MCPServerStreamableHttpParams(url=MCP_SERVER_URL)
    # print(f"MCPServerStreamableHttpParams configured for URL: {mcp_params.get('url')}")

    # 2. Create an instance of the MCPServerStreamableHttp client.
    # This object represents our connection to the specific MCP server.
    # It's an async context manager, so we use `async with` for proper setup and teardown.
    # The `name` parameter is optional but useful for identifying the server in logs or multi-server setups.
    async with MCPServerStreamableHttp(params=mcp_params,
                                       name="MySharedMCPServerClient",
                                       client_session_timeout_seconds=10,
                                       cache_tools_list=True,
                                       tool_filter=static_filter) as mcp_server_client:
        # print(f"MCPServerStreamableHttp client '{mcp_server_client.name}' created and entered context.")
        # print("The SDK will use this client to interact with the MCP server.")

        # 3. Create an agent and pass the MCP server client to it.
        # When an agent is initialized with mcp_servers, the SDK often attempts
        # to list tools from these servers to make the LLM aware of them.
        # You might see a `list_tools` call logged by your shared_mcp_server.
        # await mcp_server_client.invalidate_tools_cache()
        try:
            assistant = Agent(
                name="MyMCPConnectedAssistant",
                mcp_servers=[mcp_server_client],
                model="gpt-5",
            )
            
            # print(f"Agent '{assistant.name}' initialized with MCP server: '{mcp_server_client.name}'.")
            # print("Check the logs of your shared_mcp_server for a 'tools/list' request.")

            # # 4. Explicitly list tools to confirm connection and tool discovery.
            # print(f"Attempting to explicitly list tools from '{mcp_server_client.name}'...")
            # tools = await mcp_server_client.list_tools()
            # print(f"Tools: {tools}")

            # print("\n\nRunning a simple agent interaction...")
            result = await Runner.run(assistant, "What is Sir Zia mood?")
            print(f"\n\n[AGENT RESPONSE]: {result.final_output}")
            result2 = await Runner.run(assistant, "greet Suhaib")
            print(f"\n\n[AGENT RESPONSE]: {result2.final_output}")

        except Exception as e:
            print(f"An error occurred during agent setup or tool listing: {e}")

    # print(f"MCPServerStreamableHttp client '{mcp_server_client.name}' context exited.")
    # print(f"--- Agent Connection Test End ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An unhandled error occurred in the agent script: {e}")