"""
Post-Sales Customer Service Agent - Using Strands SDK with Bedrock Knowledge Base
Handles post-purchase support, returns, warranties, and product issues
"""

from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools.memory import memory
from typing import Dict, Any, List
import boto3
import json
from models.context import CustomerServiceAgentContext
from agents.prompt_templates import return_process_agent_system_prompt
from tools.logger_config import get_logger

logger = get_logger(__name__)

bedrock_model = BedrockModel(
    model_id="global.anthropic.claude-sonnet-4-20250514-v1:0",
    temperature=0.1,
    top_p=0.1,
)


@tool
def start_return_process(query: str) -> str:
    """
    Process and respond to return related queries using a specialized return agent.

    Args:
        query: A return related question or problem from the user

    Returns:
        A clear retur policy and alternate solutions
    """
    # Format the query for the contact agent with clear instructions
    formatted_query = f"请回答相关的问题，如果没有合适答案，可以使用tools查找 : {query}"

    try:
        logger.info("Routed to Return Agent")
        agent = Agent(
            name="return service agent",
            system_prompt=return_process_agent_system_prompt,
            model=bedrock_model,
        )
        agent_response = agent(formatted_query)
        text_response = str(agent_response)
        logger.info(f"return agent text response: {text_response}")
        if len(text_response) > 0:
            return text_response

        return (
            "很抱歉，我无法解决这个问题。请检查您的问题是否表述清楚，或尝试重新措辞。"
        )
    except Exception as e:
        # Return specific error message for shipping processing
        return f"Error processing your return related query: {str(e)}"


agent = Agent(
    tools=[memory],
    system_prompt=return_process_agent_system_prompt,
    model=bedrock_model,
)

# Retrieve content using semantic search
agent.tool.memory(
    action="retrieve",
    query="meeting information",
    min_score=0.7,
    STRANDS_KNOWLEDGE_BASE_ID="my1234kb",
)

# # List all documents
# agent.tool.memory(
#     action="list",
#     max_results=50,
#     STRANDS_KNOWLEDGE_BASE_ID="my1234kb"
# )

# # Store content in Knowledge Base
# agent.tool.memory(
#     action="store",
#     content="Important information to remember",
#     title="Meeting Notes",
#     STRANDS_KNOWLEDGE_BASE_ID="my1234kb"
# )
