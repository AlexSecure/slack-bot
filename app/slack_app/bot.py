import typing

import slack_bolt

from common import parser, secrets
from slack_app.modal import handlers

SLACK_APP: typing.Union[slack_bolt.App, None] = None  # Global variable for the Slack app


def get_slack_app():

    global SLACK_APP

    # Initialize the Slack app if it hasn't been already
    if SLACK_APP is None:
        SLACK_APP = slack_bolt.App(
            token=secrets.BotSecrets.get(secrets.BotSecrets.SLACK_BOT_TOKEN),
            signing_secret=secrets.BotSecrets.get(secrets.BotSecrets.SLACK_SIGNING_SECRET),
            process_before_response=True
        )

        # Register the slash command handler
        SLACK_APP.command(secrets.BotSecrets.get(secrets.BotSecrets.SLACK_SLASH_COMMAND))(handlers.handle_open_modal)
        # Register the modal submission handler
        SLACK_APP.view(parser.SLACK_MODAL_WINDOW_ID)(handlers.handle_modal_submission)

    return SLACK_APP
