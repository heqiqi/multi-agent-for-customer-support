"""
Post-Sales Customer Service Agent - Using Strands SDK with Bedrock Knowledge Base
Handles post-purchase support, returns, warranties, and product issues
"""

from strands import Agent, tool
from strands.models import BedrockModel
from strands.tools import tool
from strands_tools import file_read
from typing import Dict, Any, List
import boto3
import json
from models.context import CustomerServiceAgentContext
from agents.prompt_templates import order_status_system_prompt
from tools.logger_config import get_logger

logger = get_logger(__name__)

bedrock_model = BedrockModel(
    model_id="global.anthropic.claude-sonnet-4-20250514-v1:0",
    temperature=0.1,
    top_p=0.1,
)


@tool
def check_order_status(query: str, user_id: str) -> str:
    """
    Process and respond to order status related queries using a specialized return agent.

    Args:
        query: 用户的问询语句，
        user_id: 用户id。 根据此id，查询客户的订单号和订单状态。

    Returns:
        订单id，订单状态，订单描述，订单的发货时间，收货时间。
    """
    # Format the query for the contact agent with clear instructions
    formatted_query = f"{query}, 请返回订单id，订单状态，订单描述，订单的发货时间，收货时间，还有订单描述等信息。"

    try:
        logger.info("Routed to Order status Agent")
        agent = Agent(
            name="order status agent",
            system_prompt=order_status_system_prompt,
            model=bedrock_model,
            tools=[file_read],
        )
        agent_response = agent(formatted_query)
        text_response = str(agent_response)
        logger.info(f"Order agent text response: {text_response}")
        if len(text_response) > 0:
            return text_response

        return (
            "很抱歉，我无法解决这个问题。请检查您的问题是否表述清楚，或尝试重新措辞。"
        )
    except Exception as e:
        # Return specific error message for shipping processing
        return f"Error processing your return related query: {str(e)}"
