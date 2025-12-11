# Serverless Deep Agent

A serverless AI agent built with Amazon Bedrock AgentCore + DeepAgents. This project deploys an AI agent runtime on AWS that can maintain conversation state.

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- Docker
- AWS Account with appropriate permissions
- AWS CLI configured with credentials

## Quick Start

1. Install dependencies:
```bash
uv sync
```

2. Set up environment variables:
```bash
cp .env.template .env
```

Edit `.env` and fill in required values:
- `AWS_REGION`: Your AWS region (e.g., `us-east-1`)
- `MEMORY_ID`: DynamoDB table name for agent memory
- `MODEL`: Bedrock model to use (default: `bedrock:global.anthropic.claude-sonnet-4-5-20250929-v1:0`)

## Directory Structure

```
.
├── agent
│   ├── __init__.py
│   ├── main.py        # Main agent entrypoint with BedrockAgentCore integration
│   └── settings.py    # Configuration settings using Pydantic
├── cdk.json
├── docker-compose.yml # Local development with Docker
├── Dockerfile         # Agent container definition
├── iac                # Infrastructure as Code (AWS CDK)
│   ├── __init__.py
│   ├── app.py         # CDK app entry point
│   └── stack.py       # CDK stack definition
├── pyproject.toml     # Python project configuration
├── README.md
├── scripts            # Utility scripts
│   ├── __init__.py
│   └── invoke.py      # Script to invoke deployed agent
└── uv.lock
```

## Available Commands

This project uses [Poethepoet](https://github.com/nat-n/poethepoet) for task automation. Run commands using `uv run poe <command>`.

### Code Quality

| Command | Description |
|---------|-------------|
| `uv run poe lint` | Run Ruff linter to check code quality |
| `uv run poe format` | Format code using Ruff |

### Docker Development

| Command | Description |
|---------|-------------|
| `uv run poe build` | Build Docker image |
| `uv run poe start` | Start agent in Docker container (detached) |
| `uv run poe restart` | Rebuild and restart agent container |
| `uv run poe down` | Stop and remove containers |
| `uv run poe logs` | Follow container logs |
| `uv run poe dev` | Start Docker Compose in watch mode (auto-reload on changes) |

### Deployment

| Command | Description |
|---------|-------------|
| `uv run poe deploy` | Deploy infrastructure to AWS using CDK |

### Invoke Deployed Agent

```bash
uv run poe invoke \
  --session-id "my-session-123" \
  --user-id "user-456" \
  --input "Hello, how can you help me?" \
  --agent-runtime-arn "arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/xyz"
```

Parameters:
- `--session-id`: Unique session identifier for conversation continuity
- `--user-id`: User identifier
- `--input`: Message to send to the agent
- `--agent-runtime-arn`: ARN of the deployed agent runtime
- `--region`: (Optional) AWS region (defaults to `AWS_REGION` from .env)

## Development Workflow

### Local Development with Docker

1. Build and start the agent:
```bash
uv run poe start
```

2. The agent will be available at `http://localhost:8080`

3. For active development with auto-reload:
```bash
uv run poe dev
```

This watches the `agent/` directory and syncs changes automatically. If `pyproject.toml` changes, it rebuilds the container.

4. View logs:
```bash
uv run poe logs
```

### Code Quality

Before committing, ensure code quality:

```bash
uv run poe lint
uv run poe format
```

### Deploy to AWS

1. Ensure AWS credentials are configured

2. Deploy the stack:
```bash
uv run poe deploy
```

3. After deployment, note the `agentRuntimeArn` from the CDK output

4. Test the deployed agent:
```bash
uv run poe invoke \
  --session-id "test-session" \
  --user-id "test-user" \
  --input "What can you do?" \
  --agent-runtime-arn "<your-agent-runtime-arn>"
```

## Architecture

- **Agent**: Built using [DeepAgents](https://github.com/anthropics/deepagents) framework with Claude Sonnet 4.5
- **Runtime**: AWS Bedrock AgentCore for serverless execution
- **Memory**: LangGraph checkpointing with AWS AgentCore Memory Saver
- **Infrastructure**: AWS CDK for infrastructure management
- **Containerization**: Docker for local development and deployment

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AWS_REGION` | AWS region for deployment | Yes |
| `MEMORY_ID` | DynamoDB table name for agent memory | Yes |
| `MODEL` | Bedrock model identifier | Yes |
| `AWS_ACCESS_KEY_ID` | AWS access key (for local Docker) | No* |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key (for local Docker) | No* |
| `AWS_SESSION_TOKEN` | AWS session token (for local Docker) | No* |

*Note: For local Docker development, AWS credentials are mounted from `~/.aws` by default. Environment variables can be used as an alternative.

## Technologies

- **[uv](https://github.com/astral-sh/uv)**: Fast Python package manager
- **[Poethepoet](https://github.com/nat-n/poethepoet)**: Task runner for Python projects
- **[DeepAgents](https://github.com/anthropics/deepagents)**: Framework for building AI agents
- **[AWS Bedrock AgentCore](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)**: Serverless agent runtime
- **[LangGraph](https://github.com/langchain-ai/langgraph)**: Graph-based agent orchestration
- **[AWS CDK](https://aws.amazon.com/cdk/)**: Infrastructure as Code for AWS
