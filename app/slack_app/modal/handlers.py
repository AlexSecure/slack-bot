from slack_sdk import errors

from common import parser
from jira_app import task
from slack_app.questions import results, view as modal_view


def open_modal(client, trigger_id):
    """
    Opens a modal in Slack using the provided trigger ID.

    Args:
        client: Slack WebClient instance to communicate with Slack API.
        trigger_id: Trigger ID received from the Slack event to open a modal.
    """

    try:
        # Attempt to open a modal using the provided view definition
        client.views_open(
            trigger_id=trigger_id,
            view=modal_view.get_view(),
        )

    except errors.SlackApiError as e:
        # Print error if the modal fails to open
        print(f"Error opening modal: {e}")


def handle_open_modal(ack, body, client):
    """
    Handles the slash command to open a modal in Slack.

    Args:
        ack: Function to acknowledge the incoming request from Slack.
        body: The body of the request from Slack containing details of the command.
        client: Slack WebClient instance to communicate with Slack API.
    """

    # Acknowledge the incoming request from Slack
    ack()

    # Call function to open modal passing the trigger_id from the request
    open_modal(client, body["trigger_id"])


def handle_modal_submission(ack, body, view, client):
    """
    Processes the submitted modal form from Slack and sends a response message.

    Args:
        ack: Function to acknowledge the modal submission event.
        body: The body of the request from Slack containing user and form details.
        view: Contains state values of the submitted modal.
        client: Slack WebClient instance to communicate with Slack API.
    """

    # Acknowledge the incoming request from Slack
    ack()

    # Extract the user ID who submitted the modal
    user_id = body["user"]["id"]

    user_result = client.users_info(user=user_id)
    user = user_result.get("user", {})

    # Extract the selected options from the modal submission
    try:
        selected_options = view["state"]["values"]["section-identifier"]["checkboxes-action"]["selected_options"]
        selected_answers = modal_view.get_selected_answers(selected_options)
    except Exception:
        raise Exception(f"Failed to get 'selected_options' data.")

    task_link = task.save_answers(
        result=results.generate_response_jira(selected_answers, user),
        user=user
    )

    message = results.generate_response_slack(selected_answers, user, task_link)

    # Send a message to the user with the calculated score and description
    client.chat_postMessage(channel=user_id, text=message.text,  blocks=message.blocks)
