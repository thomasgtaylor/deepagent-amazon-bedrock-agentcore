from aws_cdk import App

from .stack import ServerlessDeepAgentStack

app = App()
ServerlessDeepAgentStack(app, "ServerlessDeepAgentStack")

app.synth()
