"""
Multi-Turn Session — maintain conversation history across agent.run() calls.

AgentSession is the conversation state container. Pass the same session object
to multiple run() calls to give the agent memory of prior turns.
"""

import asyncio
from dotenv import load_dotenv
from azure.identity.aio import AzureCliCredential
from agent_framework import AgentSession
from agent_framework.azure import AzureOpenAIChatClient

load_dotenv()


async def main() -> None:
    async with (
        AzureCliCredential() as credential,
        AzureOpenAIChatClient(credential=credential) as client,
        client.as_agent(
            name="ConversationAgent",
            instructions="You are a helpful assistant that remembers context.",
        ) as agent,
    ):
        # Create a session to hold conversation state
        session = agent.create_session()

        # Turn 1
        response1 = await agent.run("My name is Alice and I live in Amsterdam.", session=session)
        print(f"Agent: {response1.text}")

        # Turn 2 — the agent remembers the previous context
        response2 = await agent.run("What is my name and where do I live?", session=session)
        print(f"Agent: {response2.text}")

        # --- Session serialization (for long-running / server-side scenarios) ---
        serialized = session.to_dict()
        # ... store serialized to a database ...

        # Resume later by deserializing
        resumed_session = AgentSession.from_dict(serialized)
        response3 = await agent.run("Summarize what you know about me.", session=resumed_session)
        print(f"Agent (resumed): {response3.text}")


if __name__ == "__main__":
    asyncio.run(main())
