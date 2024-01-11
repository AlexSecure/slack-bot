"""
This script is part of a Slack application built using the slack_bolt framework.
It is responsible for initializing and configuring a Slack App instance with
relevant bot tokens, signing secrets, and event handlers. The script defines
a global variable `SLACK_APP` to hold the Slack app instance and uses a
function `get_slack_app` to initialize this instance if it's not already done.
The initialization includes setting up a bot token, a signing secret, and
registering handlers for Slack events like slash commands and modal submissions.
"""

import typing

import slack_bolt

from common import parser, secrets
from slack_app.modal import handlers


# Global variable for the Slack app, initialized as None and set when `get_slack_app` is called
SLACK_APP: typing.Union[slack_bolt.App, None] = None


def get_slack_app():
    """
    Retrieves or initializes the Slack app.

    This function checks if the global `SLACK_APP` variable has been set.
    If not, it initializes the `slack_bolt.App` with necessary tokens and secrets,
    and registers event handlers for commands and modal submissions.

    Returns:
        An instance of `slack_bolt.App` representing the Slack app.
    """

    global SLACK_APP

    # Initialize the Slack app if it hasn't been already
    if SLACK_APP is None:
        # Creating the Slack App instance with required tokens and secrets
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
