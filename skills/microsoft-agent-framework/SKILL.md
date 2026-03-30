---
name: microsoft-agent-framework
description: Build AI agents and multi-agent workflows with the Microsoft Agent Framework Python package (`pip install agent-framework`). Use when agents need to create LLM-backed agents with tools, sessions, middleware, or orchestrate them in graph-based workflows. Supports Azure OpenAI, OpenAI, Anthropic, Ollama, Azure AI Foundry, and more. The successor to both Semantic Kernel and AutoGen.
---

# Microsoft Agent Framework (Python)

> All imports use `agent_framework.*` regardless of sub-package installed.
> Successor to Semantic Kernel and AutoGen.

## Setup

```bash
pip install agent-framework          # everything (dev/exploration)
pip install agent-framework-core     # core agent framework (production)
pip install agent-framework-azure-ai # Azure only (production)
```

```python
from agent_framework import Agent, AgentSession, InMemoryHistoryProvider, ContextProvider, Context
from agent_framework.azure import AzureOpenAIChatClient, AzureAIAgentClient
from agent_framework.openai import OpenAIChatClient
from agent_framework.anthropic import AnthropicClient
from agent_framework.mcp import MCPStdioTool
from agent_framework.orchestrations import SequentialBuilder, ConcurrentBuilder, HandoffBuilder, GroupChatBuilder, MagenticBuilder
```

> Always call `load_dotenv()` explicitly — Agent Framework does not auto-load `.env` files.

For code samples: `microsoft_code_sample_search(query="agent-framework python", language="python")`

## Single Agent

Create an agent via `client.as_agent(name, instructions, tools=[...])` and run it with `await agent.run(prompt)`. The result's `.text` property contains the response.

- **Tools**: Pass Python functions to `tools=[...]`. Docstrings and type annotations become the tool schema automatically. Async functions are also supported.
- **Local MCP tools**: Pass `MCPStdioTool(command=..., args=[...])` from `agent_framework.mcp` to `tools`
- **Streaming**: `async for chunk in agent.run(..., stream=True)` — check `chunk.text`
- **Expose as MCP server**: `agent.as_mcp_server()`

`microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/agents/providers/")`

## Context and History

| Feature | API | Notes |
|---------|-----|-------|
| Multi-turn sessions | `session = agent.create_session()`, pass `session=session` to each `run()` | History tracked per session object |
| In-memory history | Add `InMemoryHistoryProvider("key", load_messages=True)` to `context_providers` | Use when provider is stateless (Chat Completion, Ollama). Only one `load_messages=True` per agent |
| Custom context | Subclass `ContextProvider`, implement `async def invoking(...) -> Context` | Inject instructions, messages, or tools before each invocation |
| Session serialization | `session.to_dict()` / `AgentSession.from_dict(d)` | For persisting sessions across processes |

`microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/agents/conversations/context-providers")`

## Multi-Agent Setups

### Agent-as-tool (hierarchical)

Call `inner_agent.as_tool()` and pass it to the outer agent's `tools=[...]`. The inner agent becomes a callable tool the outer LLM can invoke.

### Workflow Builder (graph-based)

`WorkflowBuilder` builds a directed graph of agents and executors. Chain `.add_agent()`, `.add_edge()`, and `.build()`. Use `start_executor` to set the entry point. Use this when the `orchestrations` builders are too rigid.

**Edge types:**

| Pattern | API | Use case |
|---------|-----|----------|
| Direct | `.add_edge(a, b)` | Fixed linear step |
| Conditional | `.add_edge(a, b, condition=fn)` | Binary if/else routing |
| Switch-case | `.add_switch(a, lambda s: s.add_case(fn, b).with_default(c))` | Multi-branch routing |
| Fan-out | `.add_fan_out_edge(a, targets=[b, c], target_selector=fn)` | One → many (parallel, dynamic) |
| Fan-in | `.add_fan_in_barrier_edge(sources=[b, c], target=d)` | Many → one (aggregation) |
| **Multi-selection** | `.add_multi_selection_edge_group(a, [b, c, d], selection_func=fn)` | **Dynamically pick which subset of targets run in parallel** |

### Multi-Selection Edge Group

Activates a runtime-determined subset of branches in parallel. Ideal for orchestrator patterns where a structured routing output (e.g. Pydantic model) controls which specialist agents run.

`selection_func(output: YourType, target_ids: list[str]) -> list[str]` — receives the source node's output and the ordered list of candidate IDs; returns the non-empty subset to activate.

> Selected branches run **in parallel**. Downstream shared nodes are invoked **once per active branch**.

### Custom Executors

Use `@executor(id="...")` on async functions to add typed message-passing steps between agent nodes.

For full edge docs: `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/workflows/edges")`

## Orchestration Patterns (High-Level Builders)

All builders live in `agent_framework.orchestrations`. Call `.build()` → `workflow.run(prompt)`.

| Pattern | Builder | Use when |
|---------|---------|----------|
| Sequential | `SequentialBuilder(agents=[...])` | Fixed steps, each building on the last |
| Concurrent | `ConcurrentBuilder(agents=[...])` | Diverse/independent perspectives on same input |
| Handoff | `HandoffBuilder(participants=[...])` | Dynamic routing by domain expertise |
| Group Chat | `GroupChatBuilder(participants, termination_condition, selection_func)` | Iterative refinement between collaborating agents |
| Magentic | `MagenticBuilder(participants, manager_agent, max_round_count)` | Complex autonomous multi-step planning |

`microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/workflows/orchestrations/")`

## Other Features (Reference)

- **Providers**: Azure OpenAI (Chat/Responses/Assistants), OpenAI, Azure AI Foundry (`AzureAIAgentClient`), Anthropic, Ollama, Copilot Studio — `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/agents/providers/")`
- **Hosted MCP tools** (Responses API / Foundry only — web search, file search, code interpreter) — `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/agents/tools/hosted-mcp-tools")`
- **Tool approval** (human-in-the-loop, Responses API and Foundry) — `microsoft_docs_search(query="agent-framework tool approval human in the loop python")`
- **Agent Skills** (`SkillsProvider`): load `SKILL.md` bundles as context providers with progressive disclosure — `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/agents/skills")`
- **Compaction** (`CompactionProvider`, `SlidingWindowStrategy`, `TruncationStrategy`): trim in-memory history — `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/agents/conversations/compaction")`
- **Middleware**: logging, security, caching hooks on request/response cycle — `microsoft_docs_search(query="agent-framework middleware python")`
- **A2A protocol**: inter-agent communication across services — `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/integrations/a2a")`
- **Declarative YAML workflows**: `WorkflowFactory().create_workflow_from_yaml_path(path)` — `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/workflows/declarative")`
- **Mem0 / Redis / Azure AI Search / Purview**: additional memory/storage integrations — `microsoft_docs_search(query="agent-framework memory provider python")`
- **Session serialization**: `session.to_dict()` / `AgentSession.from_dict(d)` for long-running scenarios
- **MCP server exposure**: `agent.as_mcp_server()` exposes an agent as a local MCP server

## Learn More

| Topic | How to Find |
|-------|-------------|
| Azure OpenAI provider setup | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/agents/providers/azure-openai")` |
| Anthropic / Ollama providers | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/agents/providers/")` |
| Hosted MCP tools (Foundry) | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/agents/tools/hosted-mcp-tools")` |
| Local MCP servers | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/agents/tools/local-mcp-tools")` |
| Tool approval (human-in-the-loop) | `microsoft_docs_search(query="agent-framework tool approval human in the loop python")` |
| Session management | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/agents/conversations/session")` |
| Context providers (full reference) | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/agents/conversations/context-providers")` |
| History storage modes | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/agents/conversations/storage")` |
| Compaction strategies | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/agents/conversations/compaction")` |
| Agent Skills (full guide) | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/agents/skills")` |
| Skills: code-defined skills | `microsoft_docs_search(query="agent-framework code-defined skills Skill SkillsProvider python")` |
| Middleware patterns | `microsoft_docs_search(query="agent-framework middleware python logging security")` |
| Orchestration overview | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/workflows/orchestrations/")` |
| Sequential orchestration | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/workflows/orchestrations/sequential")` |
| Concurrent orchestration | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/workflows/orchestrations/concurrent")` |
| Handoff orchestration | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/workflows/orchestrations/handoff")` |
| Group Chat orchestration | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/workflows/orchestrations/group-chat")` |
| Magentic orchestration | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/workflows/orchestrations/magentic")` |
| Workflows: edges, executors | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/workflows/")` |
| Declarative YAML workflows | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/workflows/declarative")` |
| A2A protocol integration | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/integrations/a2a")` |
| Migration from Semantic Kernel | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/migration-guide/from-semantic-kernel/")` |
| Migration from AutoGen | `microsoft_docs_fetch(url="https://learn.microsoft.com/agent-framework/migration-guide/from-autogen/")` |
| Python API reference | `microsoft_docs_fetch(url="https://learn.microsoft.com/python/api/agent-framework-core/agent_framework?view=agent-framework-python-latest")` |
| Code examples | `microsoft_code_sample_search(query="agent-framework python", language="python")` |

## CLI Alternative

If the Learn MCP server is not available, use the `mslearn` CLI instead:

| MCP Tool | CLI Command |
|----------|-------------|
| `microsoft_docs_search(query: "...")` | `mslearn search "..."` |
| `microsoft_code_sample_search(query: "...", language: "...")` | `mslearn code-search "..." --language ...` |
| `microsoft_docs_fetch(url: "...")` | `mslearn fetch "..."` |

Run directly with `npx @microsoft/learn-cli <command>` or install globally with `npm install -g @microsoft/learn-cli`.
