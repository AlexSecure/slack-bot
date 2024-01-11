"""
This script sets up an AWS Lambda function to handle Slack events.
It uses the `slack_bolt` library's AWS Lambda adapter to interface with Slack API.
The main functionality is provided by a Slack app defined in `slack_app` module,
which is expected to contain the necessary logic and handlers for processing
Slack events. The lambda_handler function is the entry point for AWS Lambda
to process incoming Slack events, and it delegates the event processing
to the SlackRequestHandler from the `slack_bolt` library.
"""

from slack_bolt.adapter import aws_lambda

from slack_app import bot


def lambda_handler(event, context):
    """
    AWS Lambda handler function for Slack events.

    Args:
        event: AWS Lambda event object.
        context: AWS Lambda context object.

    Returns:
        The response from the SlackRequestHandler.
    """

    app = bot.get_slack_app()

    # Create a request handler for AWS Lambda
    request_handler = aws_lambda.SlackRequestHandler(app=app)
    # Handle the incoming event and return the response
    return request_handler.handle(event, context)
