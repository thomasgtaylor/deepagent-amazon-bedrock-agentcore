from pathlib import Path

from aws_cdk import CfnOutput, Stack
from aws_cdk import aws_iam as iam
from aws_cdk.aws_bedrock_agentcore_alpha import AgentRuntimeArtifact, Memory, Runtime
from constructs import Construct


class ServerlessDeepAgentStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        deepagent_runtime_artifact = AgentRuntimeArtifact.from_asset(
            str(Path(__file__).parent.parent.resolve())
        )

        memory = Memory(self, "Memory", memory_name="memory")
        runtime = Runtime(
            self,
            "DeepAgent",
            runtime_name="deep_agent",
            agent_runtime_artifact=deepagent_runtime_artifact,
            environment_variables={
                "AWS_REGION": self.region,
                "MEMORY_ID": memory.memory_id,
                "MODEL": "bedrock:global.anthropic.claude-sonnet-4-5-20250929-v1:0",
            },
        )

        runtime.add_to_role_policy(
            iam.PolicyStatement(
                actions=["bedrock:InvokeModel*"],
                resources=[
                    "arn:aws:bedrock:*::foundation-model/*",
                    "arn:aws:bedrock:*:*:inference-profile/*",
                ],
            )
        )
        runtime.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "logs:DescribeLogStreams",
                    "logs:CreateLogGroup",
                    "logs:DescribeLogGroups",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                ],
                resources=["*"],
            )
        )
        memory.grant_read_long_term_memory(runtime)
        memory.grant_read_short_term_memory(runtime)
        memory.grant_write(runtime)

        CfnOutput(self, "RuntimeName", value=runtime.agent_runtime_id)
        CfnOutput(self, "MemoryId", value=memory.memory_id)
