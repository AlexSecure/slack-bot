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

    # Creating a new issue
    issue_dict = {
        'project': {'key': project_key},
        'summary': summary,
        'description': description,
        'issuetype': {'name': issue_type},
    }

    new_issue = client.get_jira().create_issue(fields=issue_dict, prefetch=False)

    return f"<{new_issue.self}|{new_issue.key}>"


def save_answers(result: str, user: typing.Dict) -> str:
    name = parser.get_slack_username(user)
    email = parser.get_slack_user_email(user)

    summary = f"New user answered Questionnaire - {name}"

    description = \
        f"""
        {result}
        *User Email:* {email}
        """

    project_key = secrets.BotSecrets.get(secrets.BotSecrets.JIRA_PROJECT_KEY)

    return create(summary, description, project_key)
