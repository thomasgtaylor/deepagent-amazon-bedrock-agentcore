import json

import boto3


def main(
    session_id: str, user_id: str, input: str, agent_runtime_arn: str, region: str
):
    body = {"input": input, "user_id": user_id}
    client = boto3.client("bedrock-agentcore", region_name=region)
    response = client.invoke_agent_runtime(
        agentRuntimeArn=agent_runtime_arn,
        runtimeSessionId=session_id,
        payload=json.dumps(body),
    )

    response_body = b"".join(response["response"]).decode("utf-8")
    response_data = json.loads(response_body)
    print(json.dumps(response_data, indent=2))
