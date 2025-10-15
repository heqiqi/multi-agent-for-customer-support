from typing import Dict, Any, List
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import retrieve, think
from agents.prompt_templates import faq_agent_system_prompt
from config.bedrock_config import (
    BEDROCK_GLOBAL_CLAUDE_4,
    DEFAULT_KNOWLEDGE_BASE_ID,
    MAX_RAG_RESULTS,
    MIN_RELEVANCE_SCORE,
    AWS_REGION,
)
import uuid
from tools.logger_config import get_logger
from agents.order_status import check_order_status

logger = get_logger(__name__)

# Set environment variables for bedrock knowledge base
# os.environ["KNOWLEDGE_BASE_ID"] = DEFAULT_KNOWLEDGE_BASE_ID
# os.environ["MIN_SCORE"] = str(MIN_RELEVANCE_SCORE)
# os.environ["AWS_REGION"] = AWS_REGION

bedrock_model = BedrockModel(
    # model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    model_id=BEDROCK_GLOBAL_CLAUDE_4,
    temperature=0.3,
    top_p=0.3,
)


@tool
def retrieve_from_kb(query: str) -> Dict[str, Any]:
    """
    Retrieve information from a knowledge base based on a query.

    Args:
        query: The search query

    Returns:
        Dictionary containing retrieval results
    """

    try:
        # Call the retrieve tool directly
        retrieve_response = retrieve.retrieve(
            {
                "toolUseId": str(uuid.uuid4()),
                "input": {
                    "text": query,
                    "score": MIN_RELEVANCE_SCORE,
                    "numberOfResults": MAX_RAG_RESULTS,
                    "knowledgeBaseId": DEFAULT_KNOWLEDGE_BASE_ID,
                    "region": AWS_REGION,
                    # "retrieveFilter": {
                    #     "andAll": [
                    #         {"equals": {"key": "category", "value": "security"}},
                    #         {"greaterThan": {"key": "year", "value": "2022"}},
                    #     ]
                    # },
                },
            }
        )
        logger.info(f"retrieve_response: {retrieve_response}")
        return retrieve_response
    except Exception as e:
        logger.error(f"Error details: {str(e)}")
        raise
        return {
            "status": "error",
            "message": f"Error retrieving from knowledge base: {str(e)}",
        }


def init_agent(agent_name: str) -> Agent:
    return Agent(
        name=agent_name,
        system_prompt=faq_agent_system_prompt,
        model=bedrock_model,
        tools=[retrieve_from_kb, check_order_status],
    )


@tool
def get_product_usage(query: str, user_id: str) -> str:
    """
    Process and respond to the use of product related queries using a specialized return agent.

    Args:
        query: A return related question or problem from the user
        user_id: current user_id

    Returns:
        A clear return solutions
    """
    # Format the query for the contact agent with clear instructions
    # knowledge_results = retrieve_from_kb(query)
    formatted_query = (
        f"请结合已有的产品资料，相关的问题 : {query}. \n资料：{knowledge_results}"
    )

    try:
        logger.info("Routed to Faq Agent")
        agent = init_agent("faq agent")
        agent_response = agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response

        return (
            "很抱歉，我无法解决这个问题。请检查您的问题是否表述清楚，或尝试重新措辞。"
        )
    except Exception as e:
        # Return specific error message for shipping processing
        return f"Error processing your return related query: {str(e)}"
