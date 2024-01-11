"""
This script contains functions to create and manage tasks in JIRA. It allows for the creation of new tasks
in a JIRA project and includes a function specifically designed to save user responses from a Slack application
as tasks in JIRA. The script uses a JIRA client from the jira_app module and integrates with the common parser
and secrets modules for handling user data and configuration settings.
"""

import typing

from jira_app import client
from common import parser, secrets


def create(summary, description, project_key, issue_type="Task"):
    """
    Creates a task in JIRA.

    Args:
        summary (str): Summary of the task.
        description (str): Description of the task.
        project_key (str): Key of the JIRA project.
        issue_type (str): Type of the issue. Defaults to 'Task'.

    Returns:
        str: The issue key of the created task.
    """

    # Define the issue dictionary with project key, summary, description, and issue type
    issue_dict = {
        'project': {'key': project_key},
        'summary': summary,
        'description': description,
        'issuetype': {'name': issue_type},
    }

    # Create a new issue in JIRA using the JIRA client and the defined issue dictionary
    new_issue = client.get_jira().create_issue(fields=issue_dict, prefetch=False)

    # Return the link and key of the newly created issue
    return f"<{new_issue.self}|{new_issue.key}>"


def save_answers(result: str, user: typing.Dict) -> str:
    """
    Saves the answers from a user as a task in JIRA.

    Args:
        result (str): The formatted result string to be saved in JIRA.
        user (dict): A dictionary containing user information.

    Returns:
        str: The issue key of the task created in JIRA.
    """

    # Extract the username and email from the user dictionary
    name = parser.get_slack_username(user)
    email = parser.get_slack_user_email(user)

    # Define the summary of the JIRA issue
    summary = f"New user answered Questionnaire - {name}"

    # Format the description with the result and user email
    description = \
        f"""
        {result}
        *User Email:* {email}
        """

    # Retrieve the project key from bot secrets
    project_key = secrets.BotSecrets.get(secrets.BotSecrets.JIRA_PROJECT_KEY)

    # Create the task in JIRA and return the issue key
    return create(summary, description, project_key)
