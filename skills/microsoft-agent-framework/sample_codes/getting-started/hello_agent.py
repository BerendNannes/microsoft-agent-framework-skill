"""
Hello Agent — minimal working example for Microsoft Agent Framework (Python).

Prerequisites:
    pip install agent-framework --pre
    pip install python-dotenv azure-identity

Environment variables (.env or shell):
    AZURE_AI_PROJECT_ENDPOINT=https://<your-project>.services.ai.azure.com/api/projects/<project-id>
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o-mini  (optional, default used if not set)
"""

import asyncio
from dotenv import load_dotenv
from azure.identity.aio import AzureCliCredential
from agent_framework.azure import AzureOpenAIChatClient

load_dotenv()


async def main() -> None:
    async with (
        AzureCliCredential() as credential,
        AzureOpenAIChatClient(credential=credential) as client,
        client.as_agent(
            name="HelloAgent",
            instructions="You are a friendly assistant. Keep your answers brief.",
        ) as agent,
    ):
        # --- Non-streaming ---
        result = await agent.run("What is the capital of France?")
        print(f"Non-streaming: {result.text}")

        # --- Streaming ---
        print("Streaming: ", end="", flush=True)
        async for chunk in agent.run("Tell me a one-sentence fun fact.", stream=True):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print()


if __name__ == "__main__":
    asyncio.run(main())
