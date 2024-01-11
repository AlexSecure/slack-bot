import enum
import json
import typing

import boto3
from botocore.exceptions import ClientError


SECRET: typing.Union[typing.Dict, None] = None


class BotSecrets(enum.Enum):

    SLACK_BOT_TOKEN = enum.auto()
    SLACK_SIGNING_SECRET = enum.auto()
    SLACK_SLASH_COMMAND = enum.auto()

    JIRA_API_TOKEN = enum.auto()
    JIRA_URL = enum.auto()
    JIRA_USER = enum.auto()
    JIRA_PROJECT_KEY = enum.auto()

    @staticmethod
    def get(secret) -> str:
        secret_str = get_secrets().get(secret.name)

        if not secret_str:
            raise Exception(f"Fail to find secret key '{secret.name}'")

        return secret_str


def get_secrets() -> BotSecrets:
    global SECRET

    if SECRET is None:
        secret_name = "dev/slack/bot"
        region_name = "eu-west-2"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError:
            raise Exception(f"Fail to get secrets")

        SECRET = json.loads(get_secret_value_response['SecretString'])

        if not SECRET:
            raise Exception(f"Secret is empty")

    return SECRET
