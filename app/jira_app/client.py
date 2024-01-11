import typing

from jira import JIRA

from common import secrets

JIRA_GLOBAL: typing.Union[JIRA, None] = None


def get_jira():
    global JIRA_GLOBAL

    if JIRA_GLOBAL is None:
        options = {"server": secrets.BotSecrets.get(secrets.BotSecrets.JIRA_URL)}
        JIRA_GLOBAL = JIRA(
            options=options,
            basic_auth=(
                secrets.BotSecrets.get(secrets.BotSecrets.JIRA_USER),
                secrets.BotSecrets.get(secrets.BotSecrets.JIRA_API_TOKEN)
            )
        )

    return JIRA_GLOBAL
