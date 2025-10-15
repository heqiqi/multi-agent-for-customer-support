"""
Bedrock Configuration for Post-Sales Agent
Configure your AWS Bedrock Knowledge Base settings here
"""

# AWS Configuration
AWS_REGION = "us-east-1"  # Change to your region

# Bedrock Knowledge Base Configuration
# Replace with your actual Knowledge Base ID after creating it in AWS Console
DEFAULT_KNOWLEDGE_BASE_ID = "CPKMJER6U3"

# RAG Configuration
MAX_RAG_RESULTS = 3  # Number of documents to retrieve from knowledge base
MIN_RELEVANCE_SCORE = 0.3  # Minimum relevance score for results

# Bedrock Model Configuration
BEDROCK_REGION_CLAUDE_4 = "us.anthropic.claude-sonnet-4-20250514-v1:0"
BEDROCK_GLOBAL_CLAUDE_4 = "global.anthropic.claude-sonnet-4-20250514-v1:0"
MODEL_TEMPERATURE = 0.3
MODEL_TOP_P = 0.3

# Bedrock Agent Core Memory Configuration
# BEDROCK_AGENTCORE_MEMORY_ID = "memory_strands_test1-1VqKHU3EKq"
BEDROCK_AGENTCORE_MEMORY_ID = "MyAgentMemory-5pw6W33cFP"
