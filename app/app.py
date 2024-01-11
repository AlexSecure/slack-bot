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
