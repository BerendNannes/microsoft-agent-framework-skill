"""
Function Tools — attach plain Python functions to an agent.

The framework reads the function's type annotations and docstring to generate
the JSON schema the LLM uses when deciding to call the tool.
"""

import asyncio
from dotenv import load_dotenv
from azure.identity.aio import AzureCliCredential
from agent_framework.azure import AzureOpenAIChatClient

load_dotenv()


# --- Define tools as ordinary Python functions ---

def get_weather(city: str) -> str:
    """Returns the current weather for the given city."""
    # Replace with a real API call in production
    return f"Sunny, 22°C in {city}"


def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Converts an amount between two currencies. Returns the converted value as a string."""
    # Placeholder conversion; replace with a real FX API
    rates = {"USD": 1.0, "EUR": 0.92, "GBP": 0.79}
    base = amount / rates.get(from_currency, 1.0)
    converted = base * rates.get(to_currency, 1.0)
    return f"{amount} {from_currency} = {converted:.2f} {to_currency}"


async def main() -> None:
    async with (
        AzureCliCredential() as credential,
        AzureOpenAIChatClient(credential=credential) as client,
        client.as_agent(
            name="ToolAgent",
            instructions=(
                "You are a helpful assistant. Use the tools provided to answer questions "
                "about weather and currency conversion."
            ),
            tools=[get_weather, convert_currency],  # pass a list of callables
        ) as agent,
    ):
        result = await agent.run("What's the weather in Tokyo, and what is 100 USD in EUR?")
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
