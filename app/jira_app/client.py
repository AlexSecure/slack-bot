"""
This script provides a function to create and manage a global JIRA client instance. It uses configuration
settings defined in the secrets module to set up the JIRA client with the server URL, username, and API token.
This setup ensures that a single instance of the JIRA client is used throughout the application, promoting
efficient resource usage and consistent JIRA interactions.
"""

import typing

from jira import JIRA
from common import secrets

# Global variable to store the JIRA client instance
JIRA_GLOBAL: typing.Union[JIRA, None] = None


def get_jira():
    """
    Retrieves or initializes the global JIRA client instance.

    Returns:
        JIRA: A JIRA client instance connected to the specified JIRA server.
    """
    global JIRA_GLOBAL

    # Initialize the JIRA client if it hasn't been already
    if JIRA_GLOBAL is None:
        # Configuration options for the JIRA client, including the server URL
        options = {"server": secrets.BotSecrets.get(secrets.BotSecrets.JIRA_URL)}

        # Creating the JIRA client instance with the specified options and authentication details
        JIRA_GLOBAL = JIRA(
            options=options,
            basic_auth=(
                secrets.BotSecrets.get(secrets.BotSecrets.JIRA_USER),
                secrets.BotSecrets.get(secrets.BotSecrets.JIRA_API_TOKEN)
            )
        )

    # Return the initialized JIRA client
    return JIRA_GLOBAL
