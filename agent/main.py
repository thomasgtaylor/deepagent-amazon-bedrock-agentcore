from logging import INFO, basicConfig, getLogger
from uuid import uuid4

from bedrock_agentcore import BedrockAgentCoreApp
from deepagents import create_deep_agent
from langgraph.config import RunnableConfig
from langgraph_checkpoint_aws import AgentCoreMemorySaver

from .settings import Settings

basicConfig(level=INFO)

logger = getLogger(__name__)
settings = Settings()
app = BedrockAgentCoreApp()
agent = create_deep_agent(
    model=settings.model,
    checkpointer=AgentCoreMemorySaver(
        memory_id=settings.memory_id, region_name=settings.aws_region
    ),
)


@app.entrypoint
async def invoke(payload, context):
    user_id = payload.get("user_id", str(uuid4()))
    session_id = (
        context.session_id
        if context and context.session_id
        else payload.get("session_id", "DEFAULT")
    )
    config: RunnableConfig = {
        "configurable": {
            "thread_id": session_id,
            "actor_id": user_id,
            "user_id": user_id,
        }
    }
    user_message = payload.get("input")
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": user_message}]}, config=config
    )
    latest_message = response["messages"][-1].content_blocks
    for m in response["messages"]:
        logger.info(m.pretty_repr())

    return {
        "content": latest_message,
        "session_id": session_id,
    }


if __name__ == "__main__":
    app.run()
