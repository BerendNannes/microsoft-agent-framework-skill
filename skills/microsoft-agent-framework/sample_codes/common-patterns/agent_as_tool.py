"""
Agent-as-Tool (Hierarchical Agents) — use one agent as a callable tool for another.

agent.as_tool() converts an agent into a function tool. The coordinator agent
can then call the inner agent the same way it calls any other function tool.
This pattern enables hierarchical or specialist agent architectures without
requiring a full Workflow graph.
"""

import asyncio
from dotenv import load_dotenv
from azure.identity.aio import AzureCliCredential
from agent_framework.azure import AzureOpenAIChatClient

load_dotenv()


def get_weather(city: str) -> str:
    """Returns the current weather conditions for the given city."""
    return f"Sunny, 22°C in {city}"


def check_order_status(order_id: str) -> str:
    """Returns the shipping status of the given order ID."""
    return f"Order {order_id} is out for delivery, estimated arrival tomorrow."


async def main() -> None:
    async with (
        AzureCliCredential() as credential,
        AzureOpenAIChatClient(credential=credential) as client,
    ):
        # Specialist agents
        weather_agent = client.as_agent(
            name="WeatherAgent",
            description="Answers questions about weather in any city.",
            instructions="You answer weather questions. Use the get_weather tool.",
            tools=[get_weather],
        )

        order_agent = client.as_agent(
            name="OrderAgent",
            description="Handles order tracking and shipping inquiries.",
            instructions="You look up order statuses using the check_order_status tool.",
            tools=[check_order_status],
        )

        # Coordinator delegates to specialist agents as tools
        coordinator = client.as_agent(
            name="Coordinator",
            instructions=(
                "You are a helpful customer service coordinator. Delegate weather questions to "
                "WeatherAgent and order questions to OrderAgent using the tools provided."
            ),
            tools=[
                weather_agent.as_tool(),
                order_agent.as_tool(),
            ],
        )

        result = await coordinator.run(
            "What's the weather in Berlin, and what is the status of order #12345?"
        )
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
