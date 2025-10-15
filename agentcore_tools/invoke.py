import boto3
import json
import sys

# Get specific argument
if len(sys.argv) > 1:
    print(f"argv:${sys.argv[1]}")
else:
    print(f"argv:None")
    exit()

client = boto3.client("bedrock-agentcore", region_name="us-east-1")
payload = json.dumps({"input": {"prompt": sys.argv[1]}})

response = client.invoke_agent_runtime(
    agentRuntimeArn="arn:aws:bedrock-agentcore:us-east-1:123321123213:runtime/xxxxxx", # update agentcore runtime ARN
    runtimeSessionId="123eoagmreaklgmrkleafremoigrmtesogmtrskhmtkrlshmt",  # Must be 33+ chars
    payload=payload,
    qualifier="DEFAULT",  # Optional
)
response_body = response["response"].read()
response_data = json.loads(response_body)
print("Agent Response:", response_data)
