"""
This script is designed to manage and retrieve secrets for a bot application, specifically handling
the secure storage and access of sensitive data like API tokens and credentials. It uses AWS Secrets
Manager to store and retrieve these secrets. The script defines a BotSecrets enum for easy reference
to specific secrets and a function to retrieve these secrets as needed.
"""

import enum
import json
import typing

import boto3
from botocore.exceptions import ClientError


# Global variable to store the retrieved secrets
SECRET: typing.Union[typing.Dict, None] = None


class BotSecrets(enum.Enum):
    # Enumerations for different secret keys
    SLACK_BOT_TOKEN = enum.auto()
    SLACK_SIGNING_SECRET = enum.auto()
    SLACK_SLASH_COMMAND = enum.auto()

    JIRA_API_TOKEN = enum.auto()
    JIRA_URL = enum.auto()
    JIRA_USER = enum.auto()
    JIRA_PROJECT_KEY = enum.auto()

    @staticmethod
    def get(secret) -> str:
        """
        Retrieves a specific secret value by its key.

        Args:
            secret (BotSecrets): The enum member representing the secret key.

        Returns:
            str: The secret value.

        Raises:
            Exception: If the secret key is not found.
        """
        # Get the secret string from the global secrets dictionary
        secret_str = get_secrets().get(secret.name)

        # Raise an exception if the secret is not found
        if not secret_str:
            raise Exception(f"Fail to find secret key '{secret.name}'")

        return secret_str

def get_secrets() -> typing.Dict:
    """
    Retrieves all secrets from AWS Secrets Manager.

    Returns:
        dict: A dictionary of all secrets.

    Raises:
        Exception: If there is a failure in retrieving secrets.
    """
    global SECRET

    # Check if the secrets have already been retrieved and stored globally
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
            # Fetch the secret value from AWS Secrets Manager
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError:
            raise Exception(f"Fail to get secrets")

        # Parse and store the secret values in the global variable
        SECRET = json.loads(get_secret_value_response['SecretString'])

        # Raise an exception if the retrieved secret is empty
        if not SECRET:
            raise Exception(f"Secret is empty")

    return SECRET
