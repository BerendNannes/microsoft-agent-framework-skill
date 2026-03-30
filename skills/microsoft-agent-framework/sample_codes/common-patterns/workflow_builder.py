"""
Workflow Builder — compose multiple agents into an explicit graph-based workflow.

Workflows provide deterministic execution order and are ideal when:
- Multiple agents must coordinate in a defined sequence
- You need checkpointing or human-in-the-loop steps
- The task is too structured for a single LLM to route autonomously

This example builds a simple Researcher → Writer pipeline.
"""

import asyncio
from dotenv import load_dotenv
from azure.identity.aio import AzureCliCredential
from agent_framework import WorkflowBuilder
from agent_framework.azure import AzureOpenAIChatClient

load_dotenv()


async def main() -> None:
    async with (
        AzureCliCredential() as credential,
        AzureOpenAIChatClient(credential=credential) as client,
    ):
        # Create individual agents
        researcher = client.as_agent(
            name="Researcher",
            description="Researches a topic and produces bullet-point findings.",
            instructions=(
                "You are a research assistant. Given a topic, produce concise bullet-point "
                "findings. Do not write prose — only bullets."
            ),
        )

        writer = client.as_agent(
            name="Writer",
            description="Turns research bullets into a short article.",
            instructions=(
                "You are a technical writer. Take the research bullets you receive and turn them "
                "into a short, readable article of 2-3 paragraphs."
            ),
        )

        # Compose into a workflow: Researcher → Writer
        workflow = (
            WorkflowBuilder()
            .add_agent(researcher, name="Researcher")
            .add_agent(writer, name="Writer", output_response=True)
            .add_edge("Researcher", "Writer")
            .set_start_executor("Researcher")
            .build()
        )

        result = await workflow.run("AI in healthcare")
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
