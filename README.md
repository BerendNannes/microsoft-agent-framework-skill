# Microsoft Agent Framework Skill

A VS Code agent skill for building AI agents and multi-agent workflows with the Microsoft Agent Framework Python package.

## Overview

This skill provides specialized knowledge and best practices for:

- **Single agents**: Create and configure agents with tools, streaming, and MCP server exposure
- **Sessions and history**: Multi-turn conversations with in-memory and custom history providers
- **Context providers**: Inject instructions, messages, and tools before each invocation
- **Multi-agent patterns**: Agent-as-tool hierarchical setups and workflow builders
- **Orchestration patterns**: Sequential, Concurrent, Handoff, Group Chat, and Magentic patterns
- **Provider integrations**: Azure OpenAI, OpenAI, Anthropic, Ollama, and Azure AI Foundry

## Requirements

These skills require the **Microsoft Learn MCP Server** to access official Microsoft documentation and code samples dynamically.

### Install Microsoft Learn MCP Server in VS Code

Click the link below to install the Microsoft Learn MCP server in VS Code:

[Install Microsoft Learn MCP Server](https://vscode.dev/redirect/mcp/install?name=microsoft-learn&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D)

Or manually add to your VS Code MCP configuration:

```json
{
  "mcpServers": {
    "microsoft-learn": {
      "type": "http",
      "url": "https://learn.microsoft.com/api/mcp"
    }
  }
}
```

## Setup

### 1. Copy Skill to Your Workspace

Copy the skill to your VS Code agent workspace:

```bash
# From this repository
cp -r skills/microsoft-agent-framework /path/to/your/vscode/agent/workspace/skills/
```

### 2. Verify Installation

After copying, the skill should appear in your agent's available skills. It will be automatically invoked when working on Microsoft Agent Framework tasks.

## Features

This skill includes:

- Single agent creation and configuration
- Sessions and conversation history management
- Context providers and custom context injection
- Multi-agent patterns (agent-as-tool, hierarchical)
- Workflow builders with graph-based routing (conditional, switch, fan-out, fan-in, multi-selection)
- Orchestration patterns (Sequential, Concurrent, Handoff, Group Chat, Magentic)
- Integration with Azure OpenAI, OpenAI, Anthropic, Ollama, and Azure AI Foundry

## Requirements

- VS Code with agent support
- Microsoft Learn MCP Server installed
- Python 3.12+ (for agent-framework related tasks)