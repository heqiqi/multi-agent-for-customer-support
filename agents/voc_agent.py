from strands import Agent, tool
from strands.models import BedrockModel
from agents.prompt_templates import faq_agent_system_prompt
from strands_tools.agent_core_memory import AgentCoreMemoryToolProvider
from config.bedrock_config import (
    BEDROCK_GLOBAL_CLAUDE_4,
    BEDROCK_AGENTCORE_MEMORY_ID,
    AWS_REGION,
)
from bedrock_agentcore.memory import MemoryClient
from typing import Dict, Any, Optional
from tools.logger_config import get_logger

logger = get_logger(__name__)

bedrock_model = BedrockModel(
    # model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    model_id=BEDROCK_GLOBAL_CLAUDE_4,
    temperature=0.3,
    top_p=0.3,
)


def init_agent(agent_name: str, user_id: str, session_id: str) -> Agent:
    provider = AgentCoreMemoryToolProvider(
        memory_id=BEDROCK_AGENTCORE_MEMORY_ID,
        actor_id=f"user_{user_id}",
        session_id=f"session_user_{user_id}",
        namespace=f"/users/user_{user_id}",
        region=AWS_REGION,
    )
    return Agent(
        name=agent_name,
        # system_prompt="You are a helpful assistant with memory capabilities.",
        model=bedrock_model,
        tools=provider.tools,
    )


@tool
def process_customer_info(user_id: str, session_id: str, query: str) -> str:
    """
    Process and respond to the use of product related queries using a specialized return agent.

    Args:
        user_id: customer provided user id
        session_id: current chat session id, in the context model
        query: A return related question or problem from the user

    Returns:
        customer history or save the new event in custoemr memroy store
    """
    # Format the query for the contact agent with clear instructions
    formatted_query = f"{query}"

    try:
        logger.info(
            f"Routed to memory Agent: user_id:{user_id}, session_id:{session_id}, query:{query}"
        )
        agent = init_agent("customer info agent", user_id, session_id)
        agent_response = agent(formatted_query)
        text_response = str(agent_response)
        logger.info(f"customer info agent: {text_response}")
        if len(text_response) > 0:
            return text_response

        return "没有关于这个用户的任何信息。"
    except Exception as e:
        # Return specific error message for shipping processing
        return f"Error processing your return related query: {str(e)}"
